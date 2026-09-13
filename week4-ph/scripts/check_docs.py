"""
Check that the numbers written in the prose still match the shipped data.

    python3 scripts/check_docs.py

The generated documents (AUDIT_REPORT, DATASET_SUMMARY) cannot drift, because they are
rebuilt from the data. The hand-written ones (README, METHODS, LIMITATIONS,
SCREENER_PH_REPRESENTATION, FIGURE_PLAN, REVIEW_REQUEST, the abstracts) can. This script
asserts the specific claims those documents make, so a data change that invalidates a
sentence fails loudly instead of silently shipping.

Exits non-zero if any assertion fails.
"""
import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ph_curation import SEQUENCE_REJECTIONS  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

failures = []


def assert_eq(label, got, want):
    ok = got == want
    if not ok:
        failures.append(f"{label}: docs say {want}, data says {got}")
    print(f"  [{'ok ' if ok else 'FAIL'}] {label:<52} {got}")


def main():
    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    with open(os.path.join(DATA, "ph_excluded_v1.csv"),
              encoding="utf-8", newline="") as fh:
        excl = list(csv.DictReader(fh))
    stats = json.load(open(os.path.join(DATA, "ph_stats.json"), encoding="utf-8"))
    overlap = json.load(open(os.path.join(DATA, "ph_overlap_luke.json"),
                             encoding="utf-8"))
    valid = json.load(open(os.path.join(DATA, "ph_validation.json"), encoding="utf-8"))
    deep = json.load(open(os.path.join(DATA, "ph_deep_verification.json"),
                         encoding="utf-8"))

    print("claims made in the hand-written documents:\n")

    # README / METHODS / abstracts headline figures
    assert_eq("67 measurements shipped", len(rows), 67)
    assert_eq("30 source articles", stats["distinct_papers_shipped"], 30)
    assert_eq("105 candidates audited", stats["candidates"], 105)
    assert_eq("38 rows removed", len(excl), 38)
    assert_eq("36% removal rate", round(stats["exclusion_rate_pct"]), 36)
    assert_eq("44 candidate articles", stats["distinct_papers_candidates"], 44)
    assert_eq("14 articles lost every row", stats["distinct_papers_dropped_entirely"], 14)
    assert_eq("pH range floor 3.0", stats["ph_min"], 3.0)
    assert_eq("pH range ceiling 12.0", stats["ph_max"], 12.0)
    assert_eq("median pH 8.0", stats["ph_median"], 8.0)
    assert_eq("19 enzyme classes", stats["enzyme_classes"], 19)
    assert_eq("57 pH-outcome rows", stats["ph_outcome_rows"], 57)
    assert_eq("10 pH-covariate rows", stats["ph_covariate_rows"], 10)
    assert_eq("45 scoreable on the pH axis", stats["scored_condition_axis"], 45)
    assert_eq("7 scoreable by a sequence model", stats["scored_sequence_model"], 7)
    assert_eq("29 rows carry an outcome at the pH", stats["rows_with_outcome_pct"], 29)
    assert_eq("52 rows carry a direction", stats["rows_with_direction"], 52)
    assert_eq("3 distinct proteins", stats["distinct_proteins"], 3)
    assert_eq("9 rows with a sequence", stats["rows_with_sequence"], 9)
    assert_eq("22 rows with pH and temperature", stats["rows_with_temperature"], 22)

    # exclusion-rule counts quoted in METHODS, the figure caption and the abstracts
    ex = stats["exclusion_rule_counts"]
    assert_eq("PH-X1 protocol sentences = 13", ex.get("PH-X1"), 13)
    assert_eq("PH-X6 off-target enzymes = 8", ex.get("PH-X6"), 8)
    assert_eq("PH-X7 secondhand/review = 7", ex.get("PH-X7"), 7)
    assert_eq("PH-X3 wrong enzyme = 6", ex.get("PH-X3"), 6)
    assert_eq("PH-X9 unsupported type = 6", ex.get("PH-X9"), 6)
    assert_eq("PH-X5 predicted value = 1", ex.get("PH-X5"), 1)
    assert_eq("12 exclusion rules fired", len(ex), 12)

    # correction counts quoted in METHODS
    co = stats["correction_rule_counts"]
    assert_eq("PH-C1 five corrected optima", co.get("PH-C1"), 5)
    assert_eq("PH-C5 52 enzyme names set", co.get("PH-C5"), 52)
    assert_eq("PH-C3 reconciles with outcome rows",
              co.get("PH-C3"), stats["rows_with_outcome_pct"])
    assert_eq("PH-C7 reconciles with direction rows",
              co.get("PH-C7"), stats["rows_with_direction"])

    # independence claims
    assert_eq("0 proteins in Luke's training split",
              overlap["proteins_in_luke_train"], 0)
    assert_eq("0 proteins in Luke's held-out test split",
              overlap["proteins_in_luke_test"], 0)
    assert_eq("3 proteins new to the project",
              overlap["proteins_new_to_the_project"], 3)

    # validation claims quoted in README and METHODS
    kinds = Counter(r["kind"] for r in valid["results"])
    status = Counter(r["status"] for r in valid["results"])
    assert_eq("22 validation checks", len(valid["results"]), 22)
    assert_eq("19 hard checks", kinds["HARD"], 19)
    assert_eq("3 advisory checks", kinds["WARN"], 3)
    assert_eq("0 hard failures", status["FAIL"], 0)
    assert_eq("1 advisory warning raised", status["WARN"], 1)
    assert_eq("9 scored rows without an enzyme identity",
              sum(1 for r in rows if r["scored_condition_axis"] == "yes"
                  and not (r["enzyme_name"] or r["uniprot_accession"])), 9)

    # LIMITATIONS claims
    assert_eq("14 feruloyl + acetyl xylan esterase rows",
              sum(1 for r in rows
                  if r["enzyme_class"] in ("feruloyl esterase",
                                           "acetyl xylan esterase")), 14)
    assert_eq("53 rows if those were dropped",
              len(rows) - sum(1 for r in rows
                              if r["enzyme_class"] in ("feruloyl esterase",
                                                       "acetyl xylan esterase")), 53)
    assert_eq("7 multiple-enzyme rows", stats["multi_enzyme_attribution"], 7)
    assert_eq("56 rows graded Low upstream",
              sum(1 for r in rows if r["confidence"] == "Low"), 56)
    assert_eq("1 row names its buffer", stats["rows_with_buffer"], 1)
    assert_eq("21 rows record an assay method",
              sum(1 for r in rows if r["assay_method"]), 21)
    assert_eq("1 internally contradicted row", stats["internal_conflict_rows"], 1)
    assert_eq("10 articles contribute exactly one row",
              sum(1 for _, n in Counter(r["pmcid"] for r in rows).items() if n == 1), 10)
    # deep re-read of the full articles
    assert_eq("3 sequence attributions rejected on deep re-read",
              len(SEQUENCE_REJECTIONS), 3)
    assert_eq("30/30 shipped articles are research-articles",
              deep["article_types"].get("research-article"), 30)
    assert_eq("67/67 quotes relocated in fresh full text",
              deep["quotes_relocated"], 67)
    assert_eq("0 open deep-verification findings", len(deep["findings"]), 0)
    assert_eq("no tier-B rows remain",
              stats["tiers"].get("B_in_luke_heldout_test_only", 0), 0)
    assert_eq("9 tier-A rows", stats["tiers"]["A_fully_independent"], 9)
    assert_eq("58 tier-C rows", stats["tiers"]["C_conditions_only_no_sequence"], 58)
    assert_eq("busiest protein contributes 7 rows",
              max(Counter(r["protein_id_luke_join"] for r in rows
                          if r["sequence"]).values()), 7)

    # FIGURE_PLAN panel sizes
    assert_eq("panel A: 24 pH optima",
              sum(1 for r in rows if r["measurement_type"] == "pH optimum"), 24)
    assert_eq("panel B: 29 rows with an outcome",
              sum(1 for r in rows if r["relative_activity_pct"]), 29)
    assert_eq("panel C: 22 rows with both axes",
              sum(1 for r in rows if r["pH"] and r["temperature_c"]), 22)
    assert_eq("12 interval rows", stats["range_rows"], 12)
    assert_eq("10 range groups", stats["range_groups"], 10)

    print()
    if failures:
        print(f"{len(failures)} claim(s) no longer match the data:")
        for f in failures:
            print("   -", f)
        return 1
    print("all documented claims match the shipped data")
    return 0


if __name__ == "__main__":
    sys.exit(main())
