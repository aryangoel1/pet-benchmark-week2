#!/usr/bin/env python3
"""The overlap gate. Every benchmark row is screened against every prior dataset.

Screens applied, in the order they fire (first hit wins, all hits recorded):

  S1  sequence identity   SHA-1 of the resolved sequence vs 970k indexed sequences
                          (the 7 shared datasets + Luke week-1 + Luke week-2)
  S2  Luke join key       protein_id = "P"+sha1(seq.upper().strip("*"))[:12]
                          checked against split_homology == "train"  <- fatal
  S3  UniProt accession   vs every accession in every prior dataset
  S4  paper identity      PMCID/PMID vs every paper any prior dataset cites,
                          including all 199 papers Aryan's week-1 run mined
  S5  measurement tuple   (protein, mutation, type, pH, T, value) vs 1.58M
                          indexed fingerprints
  S6  PDB code            vs the S669 benchmark's PDB roster
  S7  internal duplicate  same measurement extracted twice inside this build

Verdicts:
  DROP_TRAIN_OVERLAP  sequence is in Luke's TRAINING split -> removed, never shipped
  DROP_DUPLICATE      measurement/paper already used anywhere -> removed
  DROP_INTERNAL_DUP   duplicate of another row in this build -> removed
  KEEP_TIER_A         appears in NO prior dataset at all -> fully independent
  KEEP_TIER_B         protein is in Luke's HELD-OUT TEST split only (no training
                      contamination) but is not novel -> shipped, flagged separately
  KEEP_NO_SEQUENCE    real measurement, no sequence resolved -> shipped in the
                      conditions table, excluded from the sequence-model core

Output: data/overlap.json  (per-row verdict + the rule and the matched id)
"""
import hashlib, json, os, re, sqlite3, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCL = os.path.join(ROOT, "data", "exclusions.sqlite")
IN_ROWS = os.path.join(ROOT, "data", "bench_std.json")
OUT = os.path.join(ROOT, "data", "overlap.json")


def clean_seq(s):
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()


def protein_id(seq):
    return "P" + hashlib.sha1(seq.upper().replace("*", "").encode()).hexdigest()[:12]


def norm_acc(a):
    a = (a or "").strip().upper().split("-")[0].split(".")[0]
    return a if re.fullmatch(r"[A-Z0-9]{6,10}", a) else ""


def fp_key(*parts):
    return "|".join(str(p).strip().lower() for p in parts)


def main():
    db = sqlite3.connect(EXCL)
    cur = db.cursor()
    rows = json.load(open(IN_ROWS))
    print(f"Screening {len(rows)} standardized rows against the exclusion index", file=sys.stderr)

    def hit(table, col, val):
        if not val:
            return None
        r = cur.execute(f"SELECT * FROM {table} WHERE {col}=?", (val,)).fetchone()
        return r

    verdicts, counts, seen_internal = [], collections.Counter(), {}

    for r in rows:
        rules, matched = [], []
        seq = clean_seq(r.get("sequence"))
        acc = norm_acc(r.get("uniprot_accession"))
        verdict = None

        # ---- S1/S2 sequence identity and Luke's split -------------------------
        if seq:
            pid = protein_id(seq)
            h = cur.execute("SELECT sha1,protein_id,source,split FROM seq WHERE sha1=?",
                            (sha1(seq),)).fetchone()
            p = cur.execute("SELECT protein_id,source,split FROM pid WHERE protein_id=?",
                            (pid,)).fetchone()
            src_split = None
            if h:
                rules.append("S1_sequence_identity"); matched.append(f"{h[2]}:{h[1]}")
                src_split = (h[2], h[3])
            if p:
                rules.append("S2_luke_protein_id"); matched.append(f"{p[1]}:{p[0]}")
                src_split = src_split or (p[1], p[2])
            if src_split:
                source, split = src_split
                if split == "train":
                    verdict = "DROP_TRAIN_OVERLAP"
                elif split == "test":
                    verdict = "KEEP_TIER_B"
                else:
                    verdict = "DROP_DUPLICATE"     # in one of the 7 datasets

        # ---- S3 accession ------------------------------------------------------
        if acc:
            a = cur.execute("SELECT uniprot,source,split FROM acc WHERE uniprot=?", (acc,)).fetchone()
            if a:
                rules.append("S3_uniprot_accession"); matched.append(f"{a[1]}:{a[0]}")
                if verdict is None:
                    verdict = ("DROP_TRAIN_OVERLAP" if a[2] == "train"
                               else "KEEP_TIER_B" if a[2] == "test" else "DROP_DUPLICATE")

        # ---- S4 paper ----------------------------------------------------------
        for ident in ((r.get("pmcid") or "").upper(), (r.get("pubmed_id") or "").upper()):
            pp = hit("paper", "ident", ident)
            if pp:
                rules.append("S4_paper_already_used"); matched.append(f"{pp[2]}:{pp[0]}")
                verdict = verdict or "DROP_DUPLICATE"

        # ---- S5 measurement fingerprint ---------------------------------------
        # symmetric to the indexing rule: a fingerprint with no protein identity is
        # not evidence of duplication, so it is not screened on
        ident = acc or (protein_id(seq) if seq else "")
        fp_queries = ([fp_key(ident, r.get("mutation"), r.get("measurement_type"), r.get("pH"),
                              r.get("temperature_c"), r.get("value_std")),
                       fp_key(ident, r.get("mutation"), r.get("measurement_type"), r.get("pH"),
                              "", r.get("value_std"))] if ident else [])
        for key in fp_queries:
            f = hit("fp", "fingerprint", key)
            if f:
                rules.append("S5_measurement_fingerprint"); matched.append(f"{f[1]}")
                verdict = verdict or "DROP_DUPLICATE"
                break

        # ---- S6 PDB ------------------------------------------------------------
        for pdbid in (r.get("pdb_in_text") or "").split(";"):
            if pdbid:
                q = hit("pdb", "pdb_id", pdbid.upper())
                if q:
                    rules.append("S6_pdb_in_S669"); matched.append(f"{q[1]}:{q[0]}")
                    break

        # ---- S7 internal duplicate --------------------------------------------
        # Scoped to the article. Two papers independently reporting "topt 37 C" are two
        # measurements, not one — collapsing them across papers would delete real data,
        # and for rows with no resolved protein it would collapse unrelated enzymes.
        # Within one article, the same value restated in four sentences IS one measurement.
        ikey = fp_key(r.get("pmcid") or "",
                      acc or seq[:24] or (r.get("enzyme_name") or "")[:24],
                      r.get("mutation"), r.get("measurement_type"), r.get("pH"),
                      r.get("temperature_c"), r.get("ion_species"), r.get("additive"),
                      r.get("value_std"), r.get("value_unit_std"))
        if ikey in seen_internal:
            rules.append("S7_internal_duplicate"); matched.append(seen_internal[ikey])
            verdict = "DROP_INTERNAL_DUP"
        else:
            seen_internal[ikey] = r["measurement_id"]

        if verdict is None:
            verdict = "KEEP_TIER_A" if seq else "KEEP_NO_SEQUENCE"

        counts[verdict] += 1
        verdicts.append({"measurement_id": r["measurement_id"], "verdict": verdict,
                         "rules_fired": rules, "matched": matched[:4]})

    for k, v in counts.most_common():
        print(f"  {v:>6}  {k}", file=sys.stderr)
    rule_counts = collections.Counter(x for v in verdicts for x in v["rules_fired"])
    print("\n  rules fired:", file=sys.stderr)
    for k, v in rule_counts.most_common():
        print(f"  {v:>6}  {k}", file=sys.stderr)

    json.dump({"verdicts": verdicts, "counts": dict(counts), "rules": dict(rule_counts)},
              open(OUT, "w"))
    print(f"\nWrote {OUT}", file=sys.stderr)
    db.close()


if __name__ == "__main__":
    main()
