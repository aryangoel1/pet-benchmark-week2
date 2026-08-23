#!/usr/bin/env python3
"""Records defects found by READING entries against their source, and removes every
row that shares each defect's signature — not merely the rows that were sampled.

Each rule below was found by manual review of a specific entry. The rule is written
against the defect's signature so it also removes the rows the sample did not reach.
Anything removed here is listed with its reason in MANUAL_VERIFICATION.md.

Output: data/manual_exclusions.json {measurement_id: reason}
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

# (found_in_entry, reason, predicate on the row)
RULES = [
    ("BM000492", "growth optimum of the organism, not the enzyme's optimum",
     lambda r: re.search(r"optim\w*\s+(?:conditions?\s+)?for\s+\w+\s+growth|growth\s+(?:were|was|temperature)",
                         r["evidence_quote"], re.I) and r["measurement_type"] in
               ("temperature optimum", "pH optimum")),

    ("BM000136", "the parsed cell holds a protein concentration, not an activity",
     lambda r: re.search(r"=\s*[^|]*\b(?:purified\s+)?protein\s*\(?\s*\d[^|]*(?:µM|μM|uM|mg/mL|nM)",
                         r["evidence_quote"], re.I)),

    ("BM001126", "methods sentence listing the buffer ranges assayed, not a measured optimum",
     lambda r: re.search(r"(?:was|were)\s+determined\s+in\s+different\s+buffers|"
                         r"buffers?\s*:\s*pH\s*[\d.]+\s*[-–]", r["evidence_quote"], re.I)),

    ("BM001319", "carbonic anhydrase CO2-hydration activity — not a plastic-degrading enzyme",
     lambda r: re.search(r"CO2\s*hydration|carbonic\s+anhydrase|\brCAH3\b",
                         r["evidence_quote"], re.I)),

    ("BM001474", "carbohydrate-active enzyme (xylanase/cellulase/glucosidase), off-target",
     lambda r: re.search(r"\b(?:xylanase|cellulase|glucosidase|glucanase|amylase|chitosanase|"
                         r"chitinase|pectinase|mannanase)\b", r["evidence_quote"], re.I)),

    ("BM001208", "a target temperature the authors aimed at, not a measured value",
     lambda r: re.search(r"\bwith the aim to|\bin order to (?:improve|prevent)|"
                         r"\bto prevent\b[^.]{0,60}\bat temperatures?\s*[><]",
                         r["evidence_quote"], re.I)),

    ("(review sweep)", "drug-delivery / prodrug release, not enzyme performance",
     lambda r: re.search(r"drug release|prodrug|lapachone|tumou?r|micelle|payload",
                         r["evidence_quote"], re.I)),

    ("(review sweep)", "salt tolerance of a strain, not of a purified enzyme",
     lambda r: re.search(r"salt tolerance range|the strain to withstand|halotolerance of the strain",
                         r["evidence_quote"], re.I)),
]


def main():
    rows = list(csv.DictReader(open(D("pet_benchmark_v2.csv"))))
    out = {}
    per_rule = {}
    for found, reason, pred in RULES:
        n = 0
        for r in rows:
            if r["measurement_id"] in out:
                continue
            try:
                if pred(r):
                    out[r["measurement_id"]] = reason
                    n += 1
            except Exception:
                pass
        per_rule[reason] = {"found_reviewing": found, "rows_removed": n}
        print(f"  {n:>4}  {reason}   (found while reviewing {found})", file=sys.stderr)

    json.dump({"exclusions": out, "rules": per_rule}, open(D("data", "manual_exclusions.json"), "w"),
              indent=1)
    print(f"\n{len(out)} rows flagged by manual review", file=sys.stderr)


if __name__ == "__main__":
    main()
