#!/usr/bin/env python3
"""Hand-curated enzyme -> accession mappings, and hand-rejected mis-attributions.

Every entry below was decided by reading the article. The quote that justifies each
decision is stored with it, so a reviewer can check the call without re-reading the paper.

Why this file exists: automated resolution cannot tell the difference between an
accession an article DEPOSITED (its own enzyme) and one it CITED (a homolog it compared
against). Both appear in the same sentences. Getting that backwards attaches the wrong
sequence to a real measurement, which is the worst failure mode a benchmark has.

Output: data/curated_sequences.json
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "curated_sequences.json")
UA = {"User-Agent": "pet-labs-week2-benchmark/1.0 (research)"}

# --------------------------------------------------------------- ACCEPTED
# (pmcid, enzyme-name pattern, accession, source, justification quote)
CURATED = [
    ("PMC12898461", r"^Ces1-?ET$", "XPQ45698.1", "genbank",
     "Table A1: 'Ces1-ET  PV146438  XPQ45698.1' — the article's own deposit. The WP_ "
     "accessions in this paper are homology comparisons, not its enzymes."),
    ("PMC12898461", r"^Est1-?ET$", "XPQ45697.1", "genbank",
     "Table A1: 'Est1-ET  PV146437  XPQ45697.1' — the article's own deposit."),
    ("PMC12898461", r"^Plp1-?ET$", "XPQ45699.1", "genbank",
     "Table A1: 'Plp1-ET  PV146439  XPQ45699.1' — the article's own deposit."),
    ("PMC11651597", r"^(?:LipA|lipase)?$", "AOT80658", "genbank",
     "'The lipase gene was cloned into the pGEM-T Easy vector, and its sequences were "
     "registered in GenBank (KU984433 and AOT80658).' AOT80658 is the protein deposit; "
     "CAB95850/ACB38749 in the same paper are homologs at 65-66% identity."),
    ("PMC8971842", r"PCLase\s*I\b(?!I)", "WP_004373894.1", "genbank",
     "'The peptide fingerprints showed that PCLase I had 100% similarity to a "
     "hypothetical protein (WP_004373894.1) from Pseudomonas mendocina ymp.' 100% "
     "fingerprint identity means this is the sequence assayed."),
    ("PMC8971842", r"PCLase\s*II\b", "WP_003239806.1", "genbank",
     "'...PCLase II had 100% similarity to a lactonizing lipase (WP_003239806.1) from "
     "the same strain.'"),
]

# --------------------------------------------------------------- REJECTED
# (pmcid, accession, why the automated attribution is wrong)
REJECTED = [
    ("PMC10418727", "AAN81911.1",
     "Est30/AAN81911.1 is a COMPARISON: 'EaEst2 ... shows a high sequence similarity of "
     "65.04% with Est30 (GenBank ID: AAN81911.1)'. 65% identity is a different protein; "
     "the article's enzyme is EaEst2."),
    ("PMC11033240", "GAP38373.1",
     "GAP38373.1 is wild-type IsPETase, cited as the parent scaffold of DuraPETase. The "
     "rows measure DuraPETase variants, which differ from the parent by ~10 substitutions, "
     "so the wild-type sequence is the wrong label for them."),
    ("PMC12767561", "P13398",
     "P13398 (ArcNylA) is the archetypal reference NylA used for percent-identity analysis. "
     "The article characterises NOVEL NylA sequences, not ArcNylA."),
    ("PMC11196671", "G9BY57",
     "Attributed by enzyme-name lookup only; the accession appears nowhere in the article, "
     "so there is no evidence it is the protein assayed."),
    ("PMC9839772", "G9BY57",
     "Attributed by enzyme-name lookup only; the accession appears nowhere in the article, "
     "and the article is about IsPETase variants, not leaf-branch compost cutinase."),
]

HYDRO = re.compile(r"hydrolase|esterase|cutinase|lipase|depolymerase|carboxylesterase|PETase|"
                   r"phospholipase|acetylesterase|patatin|alpha/beta", re.I)


def get(url, timeout=40, retries=3):
    for a in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:
            if getattr(ex, "code", None) in (400, 404):
                return ""
            time.sleep(1.0 * (a + 1))
    return ""


def fetch_genbank(acc):
    txt = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id="
              + urllib.parse.quote(acc) + "&rettype=fasta&retmode=text", timeout=30)
    if not txt.startswith(">"):
        return None
    lines = txt.splitlines()
    header, seq = lines[0], re.sub(r"[^A-Z]", "", "".join(lines[1:]).upper())
    if len(seq) < 80:
        return None
    m = re.match(r">(\S+)\s+(.*?)\s*\[(.*?)\]", header)
    return {"accession": (m.group(1) if m else acc), "entry_name": "",
            "protein_name": (m.group(2) if m else "").strip(),
            "organism": (m.group(3) if m else "").strip(), "ec": "",
            "sequence": seq, "length": len(seq), "reviewed": "GenBank"}


def main():
    accepted, failed = {}, []
    for pmcid, pat, acc, src, why in CURATED:
        rec = fetch_genbank(acc)
        time.sleep(0.36)
        if not rec:
            failed.append((pmcid, acc, "could not fetch"))
            print(f"  !! {pmcid} {acc}: fetch failed", file=sys.stderr)
            continue
        # The hydrolase name-check is a guard against AUTOMATED errors. These entries were
        # decided by reading the article, so a terse deposit name ("Ces1, partial") is not
        # evidence against them — it is just how the depositor labelled the record. The
        # check is kept as a visible warning rather than a veto.
        if not HYDRO.search(rec["protein_name"]):
            print(f"  note {pmcid} {acc}: deposit name '{rec['protein_name']}' is not "
                  f"self-describing; accepted on the article's own mapping table",
                  file=sys.stderr)
        # GenBank marks incomplete CDS translations "partial". The sequence is real but
        # truncated, which matters to a sequence model, so it is flagged not hidden.
        rec["partial"] = bool(re.search(r"\bpartial\b", rec["protein_name"], re.I))
        accepted.setdefault(pmcid, []).append(
            {"enzyme_pattern": pat, "record": rec, "justification": why})
        print(f"  ok {pmcid:<14} {acc:<16} {rec['protein_name'][:44]:<46} "
              f"{rec['length']} aa", file=sys.stderr)

    rejected = {}
    for pmcid, acc, why in REJECTED:
        rejected.setdefault(pmcid, {})[acc] = why
        print(f"  reject {pmcid:<14} {acc:<16} {why[:60]}", file=sys.stderr)

    json.dump({"accepted": accepted, "rejected": rejected, "failed": failed},
              open(OUT, "w"), indent=1)
    print(f"\n{sum(len(v) for v in accepted.values())} curated mappings, "
          f"{sum(len(v) for v in rejected.values())} rejections, {len(failed)} failed",
          file=sys.stderr)


if __name__ == "__main__":
    main()
