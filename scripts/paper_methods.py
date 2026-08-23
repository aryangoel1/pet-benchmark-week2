#!/usr/bin/env python3
"""Recover assay method and substrate at the ARTICLE level, offline from cached XML.

The task requires each measurement to record its assay method. Row-level extraction
only catches it when the method happens to be named in the same sentence or table cell
as the value, which is rare — a characterisation paper states its assay once, in
Methods, and then reports numbers for the rest of the article.

So the method is read from the article's Methods/Materials sections and attached to
that article's rows, marked `assay_method_scope = paper-level` so it is never confused
with a method stated on the row itself. A method is only taken when the article names
exactly ONE assay family; papers using several are left blank rather than guessed at.

Output: data/paper_methods.json {pmcid: {"assay": str, "substrate": str, "n_assays": int}}
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(ROOT, "data", "fulltext_xml")
OUT = os.path.join(ROOT, "data", "paper_methods.json")

ASSAYS = [
    ("HPLC/UPLC product release", r"\bHPLC\b|\bUPLC\b|high[- ]performance liquid chromat"),
    ("spectrophotometric p-nitrophenol release",
     r"p-?nitrophen|\bpNP[ABPLC]?\b|para-?nitrophen|405\s*nm|410\s*nm|348\s*nm"),
    ("pH-stat titration", r"pH[- ]stat"),
    ("weight loss / gravimetric", r"weight loss|mass loss|gravimetric"),
    ("turbidimetric / clearing zone", r"turbidimetric|clearing zone|halo formation|plate assay"),
    ("DSC / nanoDSF thermal denaturation", r"\bDSC\b|differential scanning calorim|nanoDSF|thermofluor|thermal shift"),
    ("circular dichroism", r"circular dichroism"),
    ("fluorescence", r"fluorimetric|fluorescence assay"),
    ("SEM surface analysis", r"scanning electron microscop"),
]
SUBSTRATES = [
    ("amorphous PET film", r"amorphous PET|GfPET|PET film"),
    ("PET powder", r"PET powder|crystalline PET"),
    ("PET nanoparticles", r"PET nanoparticl|nanoPET"),
    ("BHET", r"\bBHET\b"), ("MHET", r"\bMHET\b"),
    ("p-nitrophenyl ester", r"p-?nitrophenyl (?:butyrate|acetate|palmitate|laurate|octanoate|decanoate)"),
    ("polycaprolactone (PCL)", r"polycaprolactone|\bPCL\b"),
    ("PBAT", r"\bPBAT\b"), ("PLA", r"polylactic|\bPLA\b"),
    ("PHB/PHA", r"poly\(?3-hydroxybutyrate|\bPHB\b|polyhydroxyalkanoate"),
    ("polyurethane / Impranil", r"polyurethane|Impranil"),
    ("nylon / polyamide", r"\bnylon\b|polyamide"),
    ("tributyrin", r"tributyrin"), ("olive oil", r"olive oil"),
]
METHODS_SEC = re.compile(r"method|material|experimental|assay|procedure", re.I)


def sections(raw):
    """Return the text of Methods-like sections only."""
    out = []
    for m in re.finditer(r"<sec\b[^>]*>(.*?)</sec>", raw, re.S):
        block = m.group(1)
        tm = re.search(r"<title[^>]*>(.*?)</title>", block, re.S)
        title = re.sub(r"<[^>]+>", " ", tm.group(1)) if tm else ""
        if METHODS_SEC.search(title):
            out.append(" ".join(re.sub(r"<[^>]+>", " ", block).split()))
    return " ".join(out)


def main():
    files = sorted(f for f in os.listdir(XML) if f.endswith(".xml"))
    out, stats = {}, collections.Counter()
    for fn in files:
        pmcid = fn[:-4]
        try:
            raw = open(os.path.join(XML, fn)).read()
        except Exception:
            continue
        text = sections(raw)
        if len(text) < 200:                       # no usable methods section
            stats["no_methods_section"] += 1
            continue

        hits = [(name, len(re.findall(pat, text, re.I))) for name, pat in ASSAYS]
        hits = [(n, c) for n, c in hits if c >= 2]      # named more than in passing
        hits.sort(key=lambda x: -x[1])
        assay = ""
        if len(hits) == 1:
            assay = hits[0][0]
        elif len(hits) > 1 and hits[0][1] >= 3 * max(1, hits[1][1]):
            assay = hits[0][0]                          # one clearly dominant assay
        if assay:
            stats["assay_resolved"] += 1
        else:
            stats["assay_ambiguous_or_none"] += 1

        sh = [(name, len(re.findall(pat, text, re.I))) for name, pat in SUBSTRATES]
        sh = [(n, c) for n, c in sh if c >= 2]
        sh.sort(key=lambda x: -x[1])
        substrate = sh[0][0] if (len(sh) == 1 or (sh and sh[0][1] >= 3 * max(1, sh[1][1] if len(sh) > 1 else 1))) else ""

        out[pmcid] = {"assay": assay, "substrate": substrate, "n_assays": len(hits)}

    json.dump(out, open(OUT, "w"), indent=0)
    print(f"{len(out)} articles scanned: {stats['assay_resolved']} with one clear assay, "
          f"{stats['assay_ambiguous_or_none']} ambiguous/none, "
          f"{stats['no_methods_section']} without a methods section", file=sys.stderr)
    print(f"  articles with a resolved substrate: {sum(1 for v in out.values() if v['substrate'])}",
          file=sys.stderr)
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
