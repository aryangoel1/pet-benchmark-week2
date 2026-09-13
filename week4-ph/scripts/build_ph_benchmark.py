"""
Build the Week-4 pH benchmark from the Week-2 conditions benchmark + the curation table.

    python3 scripts/build_ph_benchmark.py

Inputs
    ../pet_benchmark_v2.csv     the Week-2 benchmark (606 rows x 74 cols)
    scripts/ph_curation.py      one explicit verdict per candidate pH row

Outputs (all under week4-ph/)
    data/ph_benchmark_v1.csv    the finalised pH benchmark
    data/ph_excluded_v1.csv     every excluded candidate with its rule and reason
    data/ph_audit_log.csv       all 105 candidates, verdict + rules + note, in one table
    data/ph_benchmark_v1.sqlite indexed, with the scoring views
    data/ph_benchmark.fasta     one record per distinct benchmark protein
    data/ph_stats.json          every number quoted in the documentation

Nothing here invents a value. Corrections only ever move a field to something the
article's own sentence states; the sentence itself travels with the row in
`evidence_quote` so any reader can check the call.
"""
import csv
import hashlib
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ph_curation import CURATION, EXCLUSION_RULES, CORRECTION_RULES  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "..", "pet_benchmark_v2.csv")
DATA = os.path.join(HERE, "data")

# Paper-level annotation. enzyme_class is the catalytic family the article assigns;
# polymer_target is filled in ONLY where the article names a polymer substrate, and is
# left empty otherwise rather than guessed.
PAPER_ANNOT = {
    "PMC11651597": ("lipase", ""),
    "PMC9709933":  ("esterase", ""),
    "PMC10146132": ("feruloyl esterase", ""),
    "PMC12896513": ("GDSL esterase", ""),
    "PMC10385968": ("esterase (HSL family IV)", ""),
    "PMC10003648": ("PHA depolymerase", "PHA"),
    "PMC7936011":  ("esterase", ""),
    "PMC10495362": ("feruloyl esterase", "PET"),
    "PMC12734981": ("lipase", ""),
    "PMC4624153":  ("PHB depolymerase", "PHB"),
    "PMC9104356":  ("acetyl xylan esterase", ""),
    "PMC12428281": ("phthalate hydrolase", "DEHP (plasticiser)"),
    "PMC9606172":  ("acetyl xylan esterase", ""),
    "PMC10707221": ("lipase", ""),
    "PMC11611003": ("PETase", "PET"),
    "PMC11782994": ("polyester hydrolase", "aliphatic + aromatic polyester"),
    "PMC10607177": ("PVC depolymerase", "PVC"),
    "PMC12898461": ("esterase", ""),
    "PMC12188634": ("protease (subtilisin)", "PLA"),
    "PMC13323979": ("lipase", "polyester"),
    "PMC12960341": ("feruloyl esterase", ""),
    "PMC10418727": ("carboxylesterase", "BHET (PET monomer)"),
    "PMC9452428":  ("esterase", ""),
    "PMC8767016":  ("promiscuous esterase", "PET"),
    "PMC12767561": ("nylon hydrolase", "nylon (polyamide)"),
    "PMC9805092":  ("MHET hydrolase", "MHET (PET monomer)"),
    "PMC13035632": ("lipase", ""),
    "PMC12741466": ("PCL depolymerase", "PCL"),
    "PMC8971842":  ("PCL depolymerase", "PCL"),
    "PMC11055803": ("cutinase", "cutin / polyester"),
}

OUT_COLS = [
    "ph_measurement_id", "source_measurement_id", "benchmark_tier",
    "ph_role", "scored_condition_axis", "scored_sequence_model", "unscored_reason",
    "enzyme_name", "enzyme_name_source", "enzyme_class", "polymer_target",
    "organism", "ec_number", "uniprot_accession", "protein_id_luke_join",
    "sequence_length", "sequence", "attribution_certainty",
    "measurement_type", "pH", "pH_low", "pH_high", "pH_is_range", "ph_range_group",
    "relative_activity_pct", "relative_activity_pct_high",
    "relative_activity_qualifier", "direction",
    "temperature_c", "buffer_name", "buffer_conc_mM", "exposure_time_min", "substrate",
    "value_std", "value_unit_std", "assay_method", "section",
    "pmcid", "pubmed_id", "doi", "paper_title", "journal", "year",
    "evidence_quote", "confidence", "internal_conflict",
    "audit_verdict", "audit_rules", "audit_rule_names", "audit_note",
    "corrections_applied", "source_verification", "overlap_rules_checked",
]

POINT_TYPES = {"pH optimum", "pH stability", "pH activity"}
RANGE_TYPES = {"pH activity range", "pH stability range"}


def nz(row, key):
    return (row.get(key) or "").strip()


def luke_protein_id(seq):
    """Luke's join key, verbatim from his DATA_READINESS_HANDOFF.md."""
    if not seq:
        return ""
    return "P" + hashlib.sha1(seq.upper().replace("*", "").encode()).hexdigest()[:12]


def ph_id(source_id):
    """Stable pH-benchmark id derived from the Week-2 id, so it never re-shuffles."""
    return "PH" + hashlib.sha1(source_id.encode()).hexdigest()[:8].upper()


# Which correction rule each curated field edit corresponds to. Deriving the rule codes
# from the edits themselves keeps the audit counts honest: a correction cannot be applied
# to the data without also being counted in the report.
FIELD_TO_RULE = {
    "pH": "PH-C1", "value_std": "PH-C1",
    "measurement_type": "PH-C2",
    "rel_pct": "PH-C3", "rel_pct_high": "PH-C3", "rel_qual": "PH-C3",
    "buffer_name": "PH-C4",
    "enzyme_name": "PH-C5",
    "pH_low": "PH-C6", "pH_high": "PH-C6", "pH_is_range": "PH-C6",
    "ph_range_group": "PH-C6",
    "direction": "PH-C7",
}


def derive_rules(cur, src):
    """Curated rule codes, plus any implied by a field edit the curator did not list."""
    rules = list(cur["rules"])
    if cur["verdict"] != "KEEP":
        return rules
    for field in cur["set"]:
        code = FIELD_TO_RULE.get(field)
        if not code or code in rules:
            continue
        # Only count it as a correction if the value actually differs from Week 2.
        new = "" if cur["set"][field] is None else str(cur["set"][field])
        if new != nz(src, field):
            rules.append(code)
    return sorted(rules)


def main():
    with open(SRC, encoding="utf-8", newline="") as fh:
        all_rows = list(csv.DictReader(fh))

    candidates = [r for r in all_rows
                  if nz(r, "pH") or nz(r, "pH_low") or nz(r, "pH_high")]
    cand_ids = {r["measurement_id"] for r in candidates}

    # The curation table must cover the candidate set exactly, or the audit has drifted.
    missing = cand_ids - set(CURATION)
    extra = set(CURATION) - cand_ids
    if missing or extra:
        raise SystemExit(
            f"curation/candidate mismatch\n  missing verdicts: {sorted(missing)}\n"
            f"  verdicts for unknown rows: {sorted(extra)}")
    print(f"candidates          : {len(candidates)}")

    kept, excluded, audit = [], [], []

    for src in sorted(candidates, key=lambda r: r["measurement_id"]):
        mid = src["measurement_id"]
        cur = CURATION[mid]
        setf = cur["set"]
        rules = derive_rules(cur, src)
        pmcid = nz(src, "pmcid")
        enzyme_class, polymer = PAPER_ANNOT.get(pmcid, ("", ""))

        audit.append({
            "source_measurement_id": mid,
            "pmcid": pmcid,
            "original_measurement_type": nz(src, "measurement_type"),
            "original_pH": nz(src, "pH"),
            "original_value_std": nz(src, "value_std"),
            "verdict": cur["verdict"],
            "rules": ";".join(rules),
            "rule_names": ";".join(
                EXCLUSION_RULES.get(r) or CORRECTION_RULES.get(r, "") for r in rules),
            "note": cur["note"],
            "evidence_quote": nz(src, "evidence_quote"),
        })

        if cur["verdict"] == "EXCLUDE":
            excluded.append({
                "source_measurement_id": mid,
                "pmcid": pmcid,
                "paper_title": nz(src, "paper_title"),
                "year": nz(src, "year"),
                "measurement_type": nz(src, "measurement_type"),
                "pH": nz(src, "pH"),
                "value_std": nz(src, "value_std"),
                "value_unit_std": nz(src, "value_unit_std"),
                "enzyme_name": nz(src, "enzyme_name"),
                "uniprot_accession": nz(src, "uniprot_accession"),
                "exclusion_rules": ";".join(rules),
                "exclusion_rule_names": ";".join(
                    EXCLUSION_RULES.get(r, "") for r in rules),
                "reason": cur["note"],
                "evidence_quote": nz(src, "evidence_quote"),
            })
            continue

        # ---- apply the curated corrections ------------------------------------
        def g(field, default=""):
            """Curated value if the curation sets it, else the Week-2 value."""
            if field in setf:
                v = setf[field]
                return "" if v is None else str(v)
            return nz(src, default or field)

        mtype = g("measurement_type")
        seq = nz(src, "sequence")
        role = "outcome" if mtype.startswith("pH") else "covariate"
        conflict = setf.get("internal_conflict", "no")
        attribution = setf.get("attribution_certainty", "single_enzyme")
        enzyme_name = g("enzyme_name")
        if "PH-C5" in rules:
            name_source = "corrected_from_evidence"
        elif enzyme_name:
            name_source = "as_reported"
        else:
            name_source = "not_named_in_evidence"

        # ---- scoring eligibility ----------------------------------------------
        reasons = []
        if role != "outcome":
            reasons.append("covariate row (pH is the assay condition, not the outcome)")
        if mtype in RANGE_TYPES:
            reasons.append("interval statement, not a point value")
        if conflict == "yes":
            reasons.append("contradicted elsewhere in the same article")
        scored_axis = "yes" if not reasons else "no"

        seq_reasons = list(reasons)
        if not seq:
            seq_reasons.append("no sequence resolved")
        if attribution == "multiple_enzymes_same_value":
            seq_reasons.append("value shared by >1 enzyme in the sentence")
        scored_seq = "yes" if not seq_reasons else "no"

        kept.append({
            "ph_measurement_id": ph_id(mid),
            "source_measurement_id": mid,
            "benchmark_tier": nz(src, "benchmark_tier"),
            "ph_role": role,
            "scored_condition_axis": scored_axis,
            "scored_sequence_model": scored_seq,
            "unscored_reason": "; ".join(seq_reasons),
            "enzyme_name": enzyme_name,
            "enzyme_name_source": name_source,
            "enzyme_class": enzyme_class,
            "polymer_target": polymer,
            "organism": nz(src, "organism"),
            "ec_number": nz(src, "ec_number"),
            "uniprot_accession": nz(src, "uniprot_accession"),
            "protein_id_luke_join": luke_protein_id(seq),
            "sequence_length": str(len(seq)) if seq else "",
            "sequence": seq,
            "attribution_certainty": attribution,
            "measurement_type": mtype,
            "pH": g("pH"),
            "pH_low": g("pH_low"),
            "pH_high": g("pH_high"),
            "pH_is_range": setf.get("pH_is_range", "no"),
            "ph_range_group": setf.get("ph_range_group", ""),
            "relative_activity_pct": str(setf.get("rel_pct", "")),
            "relative_activity_pct_high": str(setf.get("rel_pct_high", "")),
            "relative_activity_qualifier": setf.get("rel_qual", ""),
            "direction": g("direction"),
            "temperature_c": g("temperature_c"),
            "buffer_name": g("buffer_name"),
            "buffer_conc_mM": nz(src, "buffer_conc_mM"),
            "exposure_time_min": g("exposure_time_min"),
            "substrate": g("substrate"),
            "value_std": g("value_std"),
            "value_unit_std": nz(src, "value_unit_std"),
            "assay_method": nz(src, "assay_method"),
            "section": nz(src, "section"),
            "pmcid": pmcid,
            "pubmed_id": nz(src, "pubmed_id"),
            "doi": nz(src, "doi"),
            "paper_title": nz(src, "paper_title"),
            "journal": nz(src, "journal"),
            "year": nz(src, "year"),
            "evidence_quote": nz(src, "evidence_quote"),
            "confidence": nz(src, "confidence"),
            "internal_conflict": conflict,
            "audit_verdict": "KEEP",
            "audit_rules": ";".join(rules),
            "audit_rule_names": ";".join(CORRECTION_RULES.get(r, "") for r in rules),
            "audit_note": cur["note"],
            "corrections_applied": ";".join(sorted(setf)) if setf else "",
            "source_verification": nz(src, "verification"),
            "overlap_rules_checked": nz(src, "overlap_rules_checked"),
        })

    os.makedirs(DATA, exist_ok=True)

    def write_csv(path, rows, cols):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

    write_csv(os.path.join(DATA, "ph_benchmark_v1.csv"), kept, OUT_COLS)
    write_csv(os.path.join(DATA, "ph_excluded_v1.csv"), excluded,
              list(excluded[0].keys()))
    write_csv(os.path.join(DATA, "ph_audit_log.csv"), audit, list(audit[0].keys()))

    # ---- FASTA -------------------------------------------------------------
    seen, fasta = set(), []
    for r in kept:
        if r["sequence"] and r["protein_id_luke_join"] not in seen:
            seen.add(r["protein_id_luke_join"])
            hdr = (f">{r['protein_id_luke_join']} "
                   f"accession={r['uniprot_accession'] or 'NA'} "
                   f"enzyme={r['enzyme_name'] or 'NA'} "
                   f"organism={r['organism'] or 'NA'} tier={r['benchmark_tier']}")
            fasta.append(hdr + "\n" + r["sequence"])
    with open(os.path.join(DATA, "ph_benchmark.fasta"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(fasta) + "\n")

    # ---- SQLite ------------------------------------------------------------
    db_path = os.path.join(DATA, "ph_benchmark_v1.sqlite")
    if os.path.exists(db_path):
        os.remove(db_path)
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE ph_benchmark (%s)" %
                ",".join(f'"{c}" TEXT' for c in OUT_COLS))
    con.executemany(
        "INSERT INTO ph_benchmark VALUES (%s)" % ",".join("?" * len(OUT_COLS)),
        [[r[c] for c in OUT_COLS] for r in kept])
    for name, where in [
        ("v_ph_scored", "scored_condition_axis='yes'"),
        ("v_ph_scored_seq", "scored_sequence_model='yes'"),
        ("v_ph_optimum", "measurement_type='pH optimum'"),
        ("v_ph_stability", "measurement_type LIKE 'pH stability%'"),
        ("v_ph_ranges", "pH_is_range='yes'"),
        ("v_ph_covariate", "ph_role='covariate'"),
        ("v_tier_a", "benchmark_tier='A_fully_independent'"),
        ("v_with_sequence", "sequence<>''"),
    ]:
        con.execute(f"CREATE VIEW {name} AS SELECT * FROM ph_benchmark WHERE {where}")
    for col in ("pmcid", "measurement_type", "benchmark_tier",
                "protein_id_luke_join", "ph_range_group"):
        con.execute(f"CREATE INDEX idx_{col} ON ph_benchmark({col})")
    con.commit()
    con.close()

    # ---- stats -------------------------------------------------------------
    def count(pred):
        return sum(1 for r in kept if pred(r))

    types = {}
    for r in kept:
        types[r["measurement_type"]] = types.get(r["measurement_type"], 0) + 1
    tiers = {}
    for r in kept:
        tiers[r["benchmark_tier"]] = tiers.get(r["benchmark_tier"], 0) + 1
    years = {}
    for r in kept:
        years[r["year"]] = years.get(r["year"], 0) + 1
    excl_rules = {}
    for r in excluded:
        for code in r["exclusion_rules"].split(";"):
            if code:
                excl_rules[code] = excl_rules.get(code, 0) + 1
    corr_rules = {}
    for r in kept:
        for code in r["audit_rules"].split(";"):
            if code:
                corr_rules[code] = corr_rules.get(code, 0) + 1

    ph_vals = sorted(float(r["pH"]) for r in kept if r["pH"])
    stats = {
        "candidates": len(candidates),
        "shipped": len(kept),
        "excluded": len(excluded),
        "exclusion_rate_pct": round(100 * len(excluded) / len(candidates), 1),
        "distinct_papers_candidates": len({nz(r, "pmcid") for r in candidates}),
        "distinct_papers_shipped": len({r["pmcid"] for r in kept}),
        "distinct_papers_dropped_entirely":
            len({nz(r, "pmcid") for r in candidates}) - len({r["pmcid"] for r in kept}),
        "distinct_proteins": len(seen),
        "distinct_accessions": len({r["uniprot_accession"] for r in kept
                                    if r["uniprot_accession"]}),
        "rows_with_sequence": count(lambda r: r["sequence"]),
        "ph_outcome_rows": count(lambda r: r["ph_role"] == "outcome"),
        "ph_covariate_rows": count(lambda r: r["ph_role"] == "covariate"),
        "scored_condition_axis": count(lambda r: r["scored_condition_axis"] == "yes"),
        "scored_sequence_model": count(lambda r: r["scored_sequence_model"] == "yes"),
        "rows_with_outcome_pct": count(lambda r: r["relative_activity_pct"]),
        "rows_with_direction": count(lambda r: r["direction"]),
        "rows_with_temperature": count(lambda r: r["temperature_c"]),
        "rows_with_buffer": count(lambda r: r["buffer_name"]),
        "rows_with_exposure_time": count(lambda r: r["exposure_time_min"]),
        "range_rows": count(lambda r: r["pH_is_range"] == "yes"),
        "range_groups": len({r["ph_range_group"] for r in kept if r["ph_range_group"]}),
        "internal_conflict_rows": count(lambda r: r["internal_conflict"] == "yes"),
        "enzyme_named": count(lambda r: r["enzyme_name"]),
        "enzyme_name_corrected":
            count(lambda r: r["enzyme_name_source"] == "corrected_from_evidence"),
        "multi_enzyme_attribution":
            count(lambda r: r["attribution_certainty"] == "multiple_enzymes_same_value"),
        "measurement_types": dict(sorted(types.items(), key=lambda kv: -kv[1])),
        "tiers": dict(sorted(tiers.items())),
        "years": dict(sorted(years.items())),
        "exclusion_rule_counts": dict(sorted(excl_rules.items())),
        "correction_rule_counts": dict(sorted(corr_rules.items())),
        "ph_min": ph_vals[0] if ph_vals else None,
        "ph_max": ph_vals[-1] if ph_vals else None,
        "ph_median": ph_vals[len(ph_vals) // 2] if ph_vals else None,
        "enzyme_classes": len({r["enzyme_class"] for r in kept if r["enzyme_class"]}),
        "polymer_named": count(lambda r: r["polymer_target"]),
    }
    with open(os.path.join(DATA, "ph_stats.json"), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=1)

    print(f"shipped             : {len(kept)}")
    print(f"excluded            : {len(excluded)}")
    print(f"papers shipped      : {stats['distinct_papers_shipped']}"
          f" (of {stats['distinct_papers_candidates']})")
    print(f"pH outcome rows     : {stats['ph_outcome_rows']}")
    print(f"pH covariate rows   : {stats['ph_covariate_rows']}")
    print(f"scored (condition)  : {stats['scored_condition_axis']}")
    print(f"scored (sequence)   : {stats['scored_sequence_model']}")
    print(f"with outcome %      : {stats['rows_with_outcome_pct']}")
    print(f"distinct proteins   : {stats['distinct_proteins']}")
    print("wrote data/ph_benchmark_v1.csv, ph_excluded_v1.csv, ph_audit_log.csv,")
    print("      ph_benchmark_v1.sqlite, ph_benchmark.fasta, ph_stats.json")


if __name__ == "__main__":
    main()
