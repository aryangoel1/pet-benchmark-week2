#!/usr/bin/env python3
"""Fetch sequences for the accessions found by rescan_accessions.py.

Acceptance rule for both sources: the record's OWN description must be a
hydrolase-class protein. That single rule discards every false positive the
accession regexes produce (strain designations, catalogue numbers, standards)
without any hand-maintained blacklist.

Output: data/sequences_rescan.json {"uniprot": {...}, "genbank": {...}}
"""
import json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
UA = {"User-Agent": "pet-labs-week2-benchmark/1.0 (research)"}
FIELDS = "accession,id,protein_name,organism_name,ec,sequence,length,reviewed"
HYDRO = re.compile(r"hydrolase|esterase|cutinase|lipase|depolymerase|carboxylesterase|PETase|"
                   r"MHETase|polyesterase|amidase|lactonase|acylase|tannase|feruloyl|"
                   r"arylesterase|serine hydrolase|alpha/beta", re.I)


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


def uniprot(acc):
    txt = get(f"https://rest.uniprot.org/uniprotkb/{acc}.json?fields={FIELDS}")
    if not txt:
        return None
    try:
        d = json.loads(txt)
    except Exception:
        return None
    seq = (d.get("sequence") or {}).get("value", "")
    pn = (((d.get("proteinDescription") or {}).get("recommendedName") or {})
          .get("fullName") or {}).get("value", "")
    ec = ";".join(e.get("value", "") for e in
                  (((d.get("proteinDescription") or {}).get("recommendedName") or {})
                   .get("ecNumbers") or []))
    if not seq or not (HYDRO.search(pn or "") or ec.startswith("3.")):
        return None
    return {"accession": d.get("primaryAccession", acc), "entry_name": d.get("uniProtkbId", ""),
            "protein_name": pn, "organism": (d.get("organism") or {}).get("scientificName", ""),
            "ec": ec, "sequence": re.sub(r"[^A-Z]", "", seq.upper()),
            "length": (d.get("sequence") or {}).get("length", len(seq)),
            "reviewed": "Swiss-Prot" if d.get("entryType", "").endswith("(Swiss-Prot)") else "TrEMBL"}


def genbank(acc):
    txt = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id="
              + urllib.parse.quote(acc) + "&rettype=fasta&retmode=text", timeout=30)
    if not txt or not txt.startswith(">"):
        return None
    lines = txt.splitlines()
    header = lines[0]
    seq = re.sub(r"[^A-Z]", "", "".join(lines[1:]).upper())
    if len(seq) < 80 or not HYDRO.search(header):
        return None
    m = re.match(r">(\S+)\s+(.*?)\s*\[(.*?)\]", header)
    return {"accession": (m.group(1) if m else acc), "entry_name": "",
            "protein_name": (m.group(2) if m else "").strip(),
            "organism": (m.group(3) if m else "").strip(), "ec": "",
            "sequence": seq, "length": len(seq), "reviewed": "GenBank"}


def main():
    scan = json.load(open(D("data", "accessions_rescan.json")))
    us = sorted({a for v in scan.values() for a in v["uniprot"]})
    gs = sorted({a for v in scan.values() for a in v["genbank"]})
    print(f"{len(us)} UniProt-format and {len(gs)} GenBank-format accessions to fetch", file=sys.stderr)

    U, G = {}, {}
    for i, a in enumerate(us, 1):
        r = uniprot(a)
        if r:
            U[a] = r
        if i % 25 == 0:
            print(f"  uniprot {i}/{len(us)} -> {len(U)} hydrolases", file=sys.stderr)
        time.sleep(0.1)
    print(f"UniProt: {len(U)} hydrolase records", file=sys.stderr)

    for i, a in enumerate(gs, 1):
        r = genbank(a)
        if r:
            G[a] = r
        if i % 50 == 0:
            print(f"  genbank {i}/{len(gs)} -> {len(G)} hydrolases", file=sys.stderr)
        time.sleep(0.36)
    print(f"GenBank: {len(G)} hydrolase records", file=sys.stderr)

    json.dump({"uniprot": U, "genbank": G, "per_paper": scan},
              open(D("data", "sequences_rescan.json"), "w"))
    print("Wrote data/sequences_rescan.json", file=sys.stderr)


if __name__ == "__main__":
    main()
