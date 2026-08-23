#!/usr/bin/env python3
"""Second-pass sequence resolution — the routes that actually cover this literature.

Most novel esterases/cutinases characterised in these papers are not named with a
UniProt accession in the running text. Two stronger routes:

  R1  UniProt literature cross-reference:  lit_pubmed:<PMID>
      UniProt curators link entries to the paper that characterised them. When a
      paper links to exactly one hydrolase-class entry, that IS the paper's enzyme.
      This is a curated assertion, not a guess.

  R2  GenBank/NCBI protein accession printed in the article
      Fetched from NCBI and accepted only when the record's own description is a
      hydrolase-class protein — which discards the regex's false positives
      (strain numbers like DSM44342, standards like ISO17088) automatically.

Output: data/sequences_by_paper.json
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
UA = {"User-Agent": "pet-labs-week2-benchmark/1.0 (research)"}
FIELDS = "accession,id,protein_name,organism_name,ec,sequence,length,reviewed"

HYDRO = re.compile(r"hydrolase|esterase|cutinase|lipase|depolymerase|carboxylesterase|PETase|"
                   r"MHETase|polyesterase|amidase|lactonase|acylase|serine hydrolase|"
                   r"tannase|feruloyl|arylesterase", re.I)


def get(url, timeout=45, retries=3):
    for a in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:
            if getattr(ex, "code", None) in (400, 404):
                return ""
            time.sleep(1.2 * (a + 1))
    return ""


def rec_from(d):
    seq = (d.get("sequence") or {}).get("value", "")
    if not seq:
        return None
    pn = (((d.get("proteinDescription") or {}).get("recommendedName") or {})
          .get("fullName") or {}).get("value", "")
    return {"accession": d.get("primaryAccession", ""), "entry_name": d.get("uniProtkbId", ""),
            "protein_name": pn, "organism": (d.get("organism") or {}).get("scientificName", ""),
            "ec": ";".join(e.get("value", "") for e in
                           (((d.get("proteinDescription") or {}).get("recommendedName") or {})
                            .get("ecNumbers") or [])),
            "sequence": re.sub(r"[^A-Z]", "", seq.upper()),
            "length": (d.get("sequence") or {}).get("length", len(seq)),
            "reviewed": "Swiss-Prot" if d.get("entryType", "").endswith("(Swiss-Prot)") else "TrEMBL"}


def by_pubmed(pmid):
    txt = get("https://rest.uniprot.org/uniprotkb/search?format=json&size=25&fields="
              + FIELDS + "&query=" + urllib.parse.quote(f"lit_pubmed:{pmid}"))
    if not txt:
        return None
    try:
        res = json.loads(txt).get("results", [])
    except Exception:
        return None
    cands = [r for r in (rec_from(d) for d in res) if r]
    hyd = [c for c in cands if HYDRO.search(c["protein_name"] or "") or c["ec"].startswith("3.")]
    if len(hyd) == 1:
        return hyd[0]
    # a single reviewed hydrolase among several also identifies the paper's enzyme
    sp = [c for c in hyd if c["reviewed"] == "Swiss-Prot"]
    return sp[0] if len(sp) == 1 else None


def by_genbank(acc):
    txt = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id="
              + urllib.parse.quote(acc) + "&rettype=fasta&retmode=text", timeout=30)
    if not txt or not txt.startswith(">"):
        return None
    lines = txt.splitlines()
    header, seq = lines[0], re.sub(r"[^A-Z]", "", "".join(lines[1:]).upper())
    if len(seq) < 80 or not HYDRO.search(header):
        return None            # discards strain IDs, standards, and non-enzymes
    m = re.match(r">(\S+)\s+(.*?)\s*\[(.*?)\]", header)
    return {"accession": (m.group(1) if m else acc), "entry_name": "",
            "protein_name": (m.group(2) if m else "").strip(),
            "organism": (m.group(3) if m else "").strip(), "ec": "",
            "sequence": seq, "length": len(seq), "reviewed": "GenBank"}


def main():
    rows = json.load(open(D("data", "bench_rows.json")))
    pmid_of = {}
    for r in rows:
        if r.get("pmcid") and r.get("pubmed_id"):
            pmid_of[r["pmcid"]] = r["pubmed_id"]
    gb = set()
    for r in rows:
        for g in (r.get("genbank_in_text") or "").split(";"):
            if g:
                gb.add(g)

    print(f"R1: {len(pmid_of)} papers to look up by PubMed cross-reference", file=sys.stderr)
    by_paper = {}
    for i, (pmcid, pmid) in enumerate(sorted(pmid_of.items()), 1):
        rec = by_pubmed(pmid)
        if rec:
            by_paper[pmcid] = rec
        if i % 20 == 0:
            print(f"  ...{i}/{len(pmid_of)} papers, {len(by_paper)} resolved", file=sys.stderr)
        time.sleep(0.1)
    print(f"R1 resolved {len(by_paper)} papers to a single hydrolase entry", file=sys.stderr)

    print(f"\nR2: {len(gb)} GenBank-style accessions to check", file=sys.stderr)
    by_gb = {}
    for i, a in enumerate(sorted(gb), 1):
        rec = by_genbank(a)
        if rec:
            by_gb[a] = rec
        if i % 40 == 0:
            print(f"  ...{i}/{len(gb)}, {len(by_gb)} are real hydrolase records", file=sys.stderr)
        time.sleep(0.36)                      # NCBI: <=3 requests/second
    print(f"R2 resolved {len(by_gb)} GenBank accessions", file=sys.stderr)

    json.dump({"by_paper": by_paper, "by_genbank": by_gb}, open(D("data", "sequences_by_paper.json"), "w"))
    print(f"\nWrote data/sequences_by_paper.json", file=sys.stderr)


if __name__ == "__main__":
    main()
