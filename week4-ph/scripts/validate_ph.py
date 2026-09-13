"""
Validation suite for the Week-4 pH benchmark.

    python3 scripts/validate_ph.py

Every check is either a HARD check (must pass; a failure means the dataset is not
shippable) or a WARN check (records something a reader needs to know about, but does not
block). The script exits non-zero if any hard check fails, so it can gate a rebuild.

Results are written to data/ph_validation.json and printed.
"""
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
BENCH = os.path.join(DATA, "ph_benchmark_v1.csv")

# Useful buffering ranges (approximately pKa +/- 1), used to catch buffers that were
# attached to a row from elsewhere in the article and cannot hold the recorded pH.
BUFFER_RANGES = {
    "citrate": (3.0, 6.2),
    "sodium citrate": (3.0, 6.2),
    "acetate": (3.6, 5.6),
    "sodium acetate": (3.6, 5.6),
    "MES": (5.5, 6.7),
    "phosphate buffer": (5.8, 8.0),
    "sodium phosphate": (5.8, 8.0),
    "potassium phosphate": (5.8, 8.0),
    "KPO": (5.8, 8.0),
    "KH2PO4": (5.8, 8.0),
    "HEPES": (6.8, 8.2),
    "Tris-HCl": (7.0, 9.0),
    "Tris": (7.0, 9.0),
    "borate": (8.5, 10.2),
    "glycine-NaOH": (8.6, 10.6),
    "carbonate": (9.2, 10.8),
    "bicarbonate": (9.2, 10.8),
}

VALID_TYPES = {
    "pH optimum", "pH stability", "pH activity",
    "pH activity range", "pH stability range",
    "temperature optimum", "thermostability",
}
VALID_DIRECTION = {"", "optimum", "stabilising", "destabilising", "none"}
VALID_QUALIFIER = {"", "exact", "approx", "gte", "lte", "range"}
VALID_TIERS = {"A_fully_independent", "B_in_luke_heldout_test_only",
               "C_conditions_only_no_sequence"}
AA = set("ACDEFGHIKLMNPQRSTVWYXBZUO")

PREDICTION_LANGUAGE = re.compile(
    r"\b(model predicted|predicted by|in silico|simulation predicted|"
    r"docking predicted|rsm predicted|predicted optimum)\b", re.I)

results = []


def check(name, kind, ok, detail=""):
    results.append({"check": name, "kind": kind,
                    "status": "PASS" if ok else ("FAIL" if kind == "HARD" else "WARN"),
                    "detail": detail})
    return ok


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def quote_contains_ph(quote, value):
    """Is this pH value actually present in the evidence sentence?"""
    if value is None:
        return True
    q = quote.replace("–", "-").replace("−", "-")
    cands = {f"{value:g}"}
    if value == int(value):
        cands.add(str(int(value)))
        cands.add(f"{int(value)}.0")
    else:
        cands.add(f"{value:.1f}")
        cands.add(f"{value:.2f}")
    return any(re.search(r"(?<![0-9.])" + re.escape(c) + r"(?![0-9])", q)
               for c in cands)


def main():
    with open(BENCH, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(f"validating {len(rows)} rows\n")

    # 1 -- identifiers unique
    ids = [r["ph_measurement_id"] for r in rows]
    check("unique_ph_measurement_id", "HARD", len(ids) == len(set(ids)),
          f"{len(ids)} ids, {len(set(ids))} distinct")
    src = [r["source_measurement_id"] for r in rows]
    check("unique_source_measurement_id", "HARD", len(src) == len(set(src)))

    # 2 -- pH physically possible
    bad = [r["ph_measurement_id"] for r in rows
           if (v := num(r["pH"])) is not None and not (0.0 <= v <= 14.0)]
    check("pH_within_0_14", "HARD", not bad, f"offenders: {bad}")

    # 3 -- pH bounds ordered and consistent
    bad = []
    for r in rows:
        lo, hi, v = num(r["pH_low"]), num(r["pH_high"]), num(r["pH"])
        if lo is not None and hi is not None and lo > hi:
            bad.append((r["ph_measurement_id"], "low>high"))
        if v is not None and lo is not None and hi is not None and not (lo <= v <= hi):
            bad.append((r["ph_measurement_id"], "pH outside [low,high]"))
    check("pH_bounds_ordered", "HARD", not bad, f"offenders: {bad}")

    # 4 -- for pH-outcome point rows the standardised value must equal the pH
    bad = []
    for r in rows:
        if r["measurement_type"] in ("pH optimum", "pH stability", "pH activity"):
            v, p = num(r["value_std"]), num(r["pH"])
            if v is None or p is None or abs(v - p) > 1e-9:
                bad.append((r["ph_measurement_id"], r["value_std"], r["pH"]))
    check("value_std_equals_pH_for_pH_types", "HARD", not bad, f"offenders: {bad}")

    # 5 -- the recorded pH is present in the evidence sentence
    bad = [r["ph_measurement_id"] for r in rows
           if not quote_contains_ph(r["evidence_quote"], num(r["pH"]))]
    check("pH_present_in_evidence_quote", "HARD", not bad, f"offenders: {bad}")

    # 6 -- relative activity sane
    bad = []
    for r in rows:
        lo, hi = num(r["relative_activity_pct"]), num(r["relative_activity_pct_high"])
        if lo is not None and not (0.0 <= lo <= 200.0):
            bad.append((r["ph_measurement_id"], "out of range", lo))
        if lo is not None and hi is not None and lo > hi:
            bad.append((r["ph_measurement_id"], "low>high", lo, hi))
    check("relative_activity_sane", "HARD", not bad, f"offenders: {bad}")

    # 7 -- controlled vocabularies
    bad = sorted({r["measurement_type"] for r in rows} - VALID_TYPES)
    check("measurement_type_vocabulary", "HARD", not bad, f"unexpected: {bad}")
    bad = sorted({r["direction"] for r in rows} - VALID_DIRECTION)
    check("direction_vocabulary", "HARD", not bad, f"unexpected: {bad}")
    bad = sorted({r["relative_activity_qualifier"] for r in rows} - VALID_QUALIFIER)
    check("qualifier_vocabulary", "HARD", not bad, f"unexpected: {bad}")
    bad = sorted({r["benchmark_tier"] for r in rows} - VALID_TIERS)
    check("tier_vocabulary", "HARD", not bad, f"unexpected: {bad}")

    # 8 -- provenance complete on every row
    bad = [r["ph_measurement_id"] for r in rows
           if not (r["pmcid"] and r["doi"] and r["evidence_quote"])]
    check("provenance_complete", "HARD", not bad, f"offenders: {bad}")

    # 9 -- Luke's join key recomputes from the sequence
    bad = []
    for r in rows:
        if r["sequence"]:
            want = "P" + hashlib.sha1(
                r["sequence"].upper().replace("*", "").encode()).hexdigest()[:12]
            if want != r["protein_id_luke_join"]:
                bad.append(r["ph_measurement_id"])
            if str(len(r["sequence"])) != r["sequence_length"]:
                bad.append((r["ph_measurement_id"], "length"))
    check("luke_protein_id_recomputes", "HARD", not bad, f"offenders: {bad}")

    # 10 -- sequences are protein sequences
    bad = [r["ph_measurement_id"] for r in rows
           if r["sequence"] and set(r["sequence"].upper()) - AA]
    check("sequences_are_amino_acids", "HARD", not bad, f"offenders: {bad}")

    # 11 -- no predicted / modelled values survived
    bad = [r["ph_measurement_id"] for r in rows
           if PREDICTION_LANGUAGE.search(r["evidence_quote"])]
    check("no_model_predicted_values", "HARD", not bad, f"offenders: {bad}")

    # 12 -- no duplicate scored measurement
    seen, dup = {}, []
    for r in rows:
        if r["scored_condition_axis"] != "yes":
            continue
        key = (r["pmcid"], r["enzyme_name"].lower(), r["measurement_type"], r["pH"])
        if key in seen:
            dup.append((seen[key], r["ph_measurement_id"], key))
        seen[key] = r["ph_measurement_id"]
    check("no_duplicate_scored_measurements", "HARD", not dup, f"duplicates: {dup}")

    # 13 -- range groups are internally consistent
    groups = {}
    for r in rows:
        if r["ph_range_group"]:
            groups.setdefault(r["ph_range_group"], []).append(r)
    bad = [g for g, rs in groups.items()
           if len({(x["pH_low"], x["pH_high"], x["measurement_type"]) for x in rs}) != 1]
    check("range_groups_consistent", "HARD", not bad, f"inconsistent: {bad}")

    # 14 -- every range row carries both bounds
    bad = [r["ph_measurement_id"] for r in rows
           if r["pH_is_range"] == "yes" and not (r["pH_low"] and r["pH_high"])]
    check("range_rows_have_bounds", "HARD", not bad, f"offenders: {bad}")

    # 15 -- buffer can actually hold the recorded pH  (WARN: articles do misreport)
    bad = []
    for r in rows:
        b, v = r["buffer_name"].strip(), num(r["pH"])
        if b and v is not None and b in BUFFER_RANGES:
            lo, hi = BUFFER_RANGES[b]
            if not (lo - 0.5 <= v <= hi + 0.5):
                bad.append((r["ph_measurement_id"], b, v, f"{lo}-{hi}"))
    check("buffer_compatible_with_pH", "WARN", not bad, f"incompatible: {bad}")

    # 16 -- stability rows should say which way the effect went
    bad = [r["ph_measurement_id"] for r in rows
           if r["measurement_type"].startswith("pH stability") and not r["direction"]]
    check("stability_rows_have_direction", "WARN", not bad, f"offenders: {bad}")

    # 17 -- scored rows should carry an enzyme identity of some kind
    bad = [r["ph_measurement_id"] for r in rows
           if r["scored_condition_axis"] == "yes"
           and not (r["enzyme_name"] or r["uniprot_accession"])]
    check("scored_rows_identify_an_enzyme", "WARN", not bad, f"offenders: {bad}")

    # 18 -- every row was source-verified by the Week-2 pipeline
    bad = [r["ph_measurement_id"] for r in rows
           if r["source_verification"] != "source_verified"]
    check("all_rows_source_verified_upstream", "HARD", not bad, f"offenders: {bad}")

    # ---- report ------------------------------------------------------------
    hard_fail = [r for r in results if r["status"] == "FAIL"]
    warns = [r for r in results if r["status"] == "WARN"]
    width = max(len(r["check"]) for r in results)
    for r in results:
        mark = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN"}[r["status"]]
        print(f"  [{mark}] {r['check']:<{width}}  {r['detail'][:110]}")
    print(f"\n{len(results)} checks: "
          f"{sum(1 for r in results if r['status'] == 'PASS')} pass, "
          f"{len(hard_fail)} hard failures, {len(warns)} warnings")

    with open(os.path.join(DATA, "ph_validation.json"), "w", encoding="utf-8") as fh:
        json.dump({"rows": len(rows), "results": results}, fh, indent=1)

    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
