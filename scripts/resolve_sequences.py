#!/usr/bin/env python3
"""Attach a real protein sequence to every benchmark row that can carry one.

The screener Sargun is training takes a SEQUENCE plus conditions, so a benchmark
row without a sequence cannot test it. This resolves each measured enzyme to a
UniProt entry and records HOW it was resolved, so a reviewer can audit it:

  accession_in_paper  the article itself printed the accession -> strongest
  name_lookup         UniProt search on the enzyme name, restricted to
                      hydrolase/esterase/cutinase/lipase/depolymerase entries,
                      accepted only on an unambiguous single best hit
  unresolved          no sequence -> the row is kept but excluded from the
                      sequence-model benchmark core, never guessed at

Nothing here invents a sequence. Every sequence is fetched live from UniProt and
its accession is stored next to it.

Output: data/sequences.json
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_ROWS = os.path.join(ROOT, "data", "bench_rows.json")
OUT = os.path.join(ROOT, "data", "sequences.json")
UA = {"User-Agent": "pet-labs-week2-benchmark/1.0 (research)"}
UNIPROT = "https://rest.uniprot.org/uniprotkb"

ENZYME_WORDS = re.compile(
    r"hydrolase|esterase|cutinase|lipase|depolymerase|peptidase|protease|carboxylesterase|"
    r"PETase|MHETase|polyesterase|amidase|lactonase|acyltransferase|serine hydrolase", re.I)

# names that are not an enzyme identity and must never drive a lookup
JUNK_NAME = re.compile(r"^\s*(?:none|control|blank|nd|n\.?a\.?|-+|wild[- ]?type|wt|total|mean|"
                       r"average|buffer|substrate|enzyme|protein|sample|\d+(?:\.\d+)?)\s*$", re.I)


def get(url, timeout=45, retries=3):
    last = None
    for a in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:
            last = ex
            if getattr(ex, "code", None) in (400, 404):
                return ""
            time.sleep(1.2 * (a + 1))
    return ""


FIELDS = "accession,id,protein_name,organism_name,ec,sequence,length,reviewed,cc_catalytic_activity"


def fetch_accession(acc):
    txt = get(f"{UNIPROT}/{acc}.json?fields={FIELDS}")
    if not txt:
        return None
    try:
        d = json.loads(txt)
    except Exception:
        return None
    seq = (d.get("sequence") or {}).get("value", "")
    if not seq:
        return None
    return {
        "accession": d.get("primaryAccession", acc),
        "entry_name": d.get("uniProtkbId", ""),
        "protein_name": (((d.get("proteinDescription") or {}).get("recommendedName") or {})
                         .get("fullName") or {}).get("value", ""),
        "organism": (d.get("organism") or {}).get("scientificName", ""),
        "ec": ";".join(e.get("value", "") for e in
                       (((d.get("proteinDescription") or {}).get("recommendedName") or {})
                        .get("ecNumbers") or [])),
        "sequence": re.sub(r"[^A-Z]", "", seq.upper()),
        "length": (d.get("sequence") or {}).get("length", len(seq)),
        "reviewed": "Swiss-Prot" if d.get("entryType", "").endswith("(Swiss-Prot)") else "TrEMBL",
    }


def search_name(name):
    """Single unambiguous hydrolase hit, or nothing."""
    q = f'(protein_name:"{name}" OR gene:"{name}") AND (ec:3.1.* OR ec:3.5.*)'
    txt = get(f"{UNIPROT}/search?format=json&size=5&fields={FIELDS}&query=" + urllib.parse.quote(q))
    if not txt:
        return None
    try:
        res = json.loads(txt).get("results", [])
    except Exception:
        return None
    cands = []
    for d in res:
        seq = (d.get("sequence") or {}).get("value", "")
        pn = (((d.get("proteinDescription") or {}).get("recommendedName") or {})
              .get("fullName") or {}).get("value", "")
        if not seq or not ENZYME_WORDS.search(pn or ""):
            continue
        cands.append({
            "accession": d.get("primaryAccession", ""), "entry_name": d.get("uniProtkbId", ""),
            "protein_name": pn, "organism": (d.get("organism") or {}).get("scientificName", ""),
            "ec": ";".join(e.get("value", "") for e in
                           (((d.get("proteinDescription") or {}).get("recommendedName") or {})
                            .get("ecNumbers") or [])),
            "sequence": re.sub(r"[^A-Z]", "", seq.upper()),
            "length": (d.get("sequence") or {}).get("length", len(seq)),
            "reviewed": "Swiss-Prot" if d.get("entryType", "").endswith("(Swiss-Prot)") else "TrEMBL",
        })
    if len(cands) != 1:
        # accept a clear Swiss-Prot winner, otherwise refuse to guess
        sp = [c for c in cands if c["reviewed"] == "Swiss-Prot"]
        if len(sp) == 1:
            return sp[0]
        return None
    return cands[0]


def main():
    rows = json.load(open(IN_ROWS))
    print(f"{len(rows)} rows to resolve", file=sys.stderr)

    # 1. every accession any paper printed
    acc_needed = set()
    for r in rows:
        for a in (r.get("uniprot_in_text") or "").split(";"):
            if a:
                acc_needed.add(a)
    print(f"{len(acc_needed)} distinct accessions printed in the mined papers", file=sys.stderr)

    acc_cache = {}
    for i, a in enumerate(sorted(acc_needed), 1):
        rec = fetch_accession(a)
        if rec:
            acc_cache[a] = rec
        if i % 25 == 0:
            print(f"  ...{i}/{len(acc_needed)} accessions, {len(acc_cache)} live", file=sys.stderr)
        time.sleep(0.12)
    print(f"{len(acc_cache)} accessions resolved to sequences", file=sys.stderr)

    # keep only accessions that look like the enzyme class we are benchmarking
    hydro = {a: r for a, r in acc_cache.items()
             if ENZYME_WORDS.search(r["protein_name"] or "") or r["ec"].startswith("3.")}
    print(f"{len(hydro)} of those are hydrolase-class entries", file=sys.stderr)

    # 2. name lookups for enzyme names with no accession in their paper
    names = {}
    for r in rows:
        n = (r.get("enzyme_name") or "").strip()
        if not n or JUNK_NAME.match(n) or len(n) < 2 or len(n) > 60:
            continue
        names.setdefault(n, 0)
        names[n] += 1
    print(f"{len(names)} distinct enzyme names to look up", file=sys.stderr)

    name_cache = {}
    for i, (n, cnt) in enumerate(sorted(names.items(), key=lambda x: -x[1]), 1):
        rec = search_name(n)
        if rec:
            name_cache[n] = rec
        if i % 25 == 0:
            print(f"  ...{i}/{len(names)} names, {len(name_cache)} resolved", file=sys.stderr)
        time.sleep(0.12)
    print(f"{len(name_cache)} enzyme names resolved", file=sys.stderr)

    json.dump({"by_accession": hydro, "all_accessions": acc_cache, "by_name": name_cache},
              open(OUT, "w"))
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
