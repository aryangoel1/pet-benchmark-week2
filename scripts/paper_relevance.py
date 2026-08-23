#!/usr/bin/env python3
"""Score each mined article for plastic relevance from its FULL TEXT, offline.

Judging relevance from the title alone is wrong in both directions: a paper titled
"A novel esterase from a soil metagenomic library" may assay PCL and PET films
throughout its results, while a paper that mentions microplastics once in its
introduction may actually be about carbonic anhydrase.

An article counts as plastic-relevant when it names a synthetic polymer substrate
often enough, and in enough distinct places, to be studying one — not merely
gesturing at the field in its opening paragraph.

Output: data/paper_relevance.json {pmcid: {"score": n, "relevant": bool, "hits": {...}}}
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(ROOT, "data", "fulltext_xml")
OUT = os.path.join(ROOT, "data", "paper_relevance.json")

POLYMERS = {
    "PET": r"\bPET\b|poly\(?ethylene terephthalate|polyethylene terephthalate",
    "BHET/MHET": r"\bBHET\b|\bMHET\b|hydroxyethyl\)? terephthalate",
    "polyester": r"polyester|polyesterase",
    "PCL": r"\bPCL\b|polycaprolactone|poly\(?caprolactone",
    "PBAT": r"\bPBAT\b|polybutylene adipate",
    "PBS-polymer": r"polybutylene succinate|\bPBSA?\b",
    "PLA": r"\bPLA\b|polylactic|poly\(?lactic",
    "PHA/PHB": r"\bPHA\b|\bPHB\b|\bPHBV\b|polyhydroxyalkanoate|poly\(?3-hydroxybutyrate",
    "polyurethane": r"polyurethane|\bPUR\b|Impranil",
    "nylon/polyamide": r"\bnylon\b|polyamide|aminohexanoate",
    "PE/PS": r"\bpolyethylene\b(?! terephthalate)|\bpolystyrene\b",
    "cutin": r"\bcutin\b|cutinase",
    "plastic": r"plastic|microplastic",
}
# these alone never establish relevance — they are the generic framing words
WEAK = {"plastic"}


def main():
    files = sorted(f for f in os.listdir(XML) if f.endswith(".xml"))
    out = {}
    for fn in files:
        pmcid = fn[:-4]
        try:
            raw = open(os.path.join(XML, fn)).read()
        except Exception:
            continue
        text = " ".join(re.sub(r"<[^>]+>", " ", raw).split())
        body = text
        m = re.search(r"<body[^>]*>", raw)
        if m:
            body = " ".join(re.sub(r"<[^>]+>", " ", raw[m.end():]).split())

        hits = {}
        for name, pat in POLYMERS.items():
            n = len(re.findall(pat, body, re.I))
            if n:
                hits[name] = n
        strong = {k: v for k, v in hits.items() if k not in WEAK}
        # sustained use of a named polymer, not a single passing mention
        score = sum(strong.values())
        distinct = len(strong)
        relevant = (score >= 8 and distinct >= 1) or (distinct >= 3 and score >= 5)
        out[pmcid] = {"score": score, "distinct": distinct, "relevant": bool(relevant),
                      "hits": hits}

    rel = sum(1 for v in out.values() if v["relevant"])
    print(f"{rel} of {len(out)} articles are plastic-relevant by full text", file=sys.stderr)
    json.dump(out, open(OUT, "w"), indent=0)
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
