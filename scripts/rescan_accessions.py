#!/usr/bin/env python3
"""Re-scan the cached full text for sequence accessions, near their deposit context.

The harvest's accession regex only caught UniProt-format IDs. Papers that describe a
NEWLY characterised enzyme — exactly the papers this benchmark wants — almost always
deposit in GenBank/RefSeq instead, in formats the first pass missed (WP_, NP_, XP_,
two-letter+six-digit, versioned .1 suffixes).

This runs entirely offline against data/fulltext_xml/ — no article is re-downloaded.

An accession is only accepted when it appears within ~200 characters of deposit
language ("accession", "deposited", "GenBank", "UniProt", "sequence data"), which
keeps strain designations and catalogue numbers out.

Output: data/accessions_rescan.json  {pmcid: {"uniprot": [...], "genbank": [...]}}
"""
import json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML = os.path.join(ROOT, "data", "fulltext_xml")
OUT = os.path.join(ROOT, "data", "accessions_rescan.json")

UNIPROT_RE = re.compile(r"\b([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})\b")
GENBANK_RE = re.compile(r"\b((?:[A-Z]{3}\d{5}|[A-Z]{2}\d{6}|[A-Z]{4}\d{8}|"
                        r"(?:WP|NP|XP|YP|AP|ZP)_\d{6,9})(?:\.\d+)?)\b")
DEPOSIT = re.compile(r"accession|deposit|genbank|uniprot|ncbi|embl|ddbj|refseq|"
                     r"sequence data|nucleotide sequence|protein sequence|databank|"
                     r"data availability", re.I)
WINDOW = 240

# never accept these — they are database prefixes for things that are not proteins
BAD = re.compile(r"^(PMC|DOI|ISO|ASTM|DSM\d|ATCC|KCTC|CGMCC|JCM|NBRC)", re.I)


def main():
    files = sorted(f for f in os.listdir(XML) if f.endswith(".xml"))
    print(f"Re-scanning {len(files)} cached articles (offline)", file=sys.stderr)
    out, tot_u, tot_g = {}, 0, 0
    for fn in files:
        pmcid = fn[:-4]
        try:
            raw = open(os.path.join(XML, fn)).read()
        except Exception:
            continue
        text = " ".join(re.sub(r"<[^>]+>", " ", raw).split())
        # positions where deposit language occurs
        spans = [(max(0, m.start() - WINDOW), m.end() + WINDOW) for m in DEPOSIT.finditer(text)]
        if not spans:
            continue
        merged = []
        for a, b in sorted(spans):
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        ctx = " ".join(text[a:b] for a, b in merged)

        up, gb = [], []
        for m in UNIPROT_RE.finditer(ctx):
            a = m.group(1).upper()
            if a not in up and not BAD.match(a):
                up.append(a)
        for m in GENBANK_RE.finditer(ctx):
            a = m.group(1).upper()
            if a not in gb and not BAD.match(a):
                gb.append(a)
        if up or gb:
            out[pmcid] = {"uniprot": up[:12], "genbank": gb[:12]}
            tot_u += len(up[:12]); tot_g += len(gb[:12])

    print(f"{len(out)} articles carry accessions in deposit context: "
          f"{tot_u} UniProt-format, {tot_g} GenBank-format", file=sys.stderr)
    allg = {a for v in out.values() for a in v["genbank"]}
    allu = {a for v in out.values() for a in v["uniprot"]}
    print(f"distinct: {len(allu)} UniProt, {len(allg)} GenBank", file=sys.stderr)
    json.dump(out, open(OUT, "w"), indent=0)
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
