"""
Convert the Week-4 pH benchmark into Luke's standardized spreadsheet format.

    python3 scripts/to_luke_format.py

Target schema -- the 24 columns of `temp_pH_dataset_ML_homology.csv`, in his order:

    record_id, source_datasets, protein_id, uniprot_id, pdb_id, organism, ec_number,
    protein_name, mutation, position, wt_aa, mut_aa, temperature_c, pH, method,
    measurement_type, measured_value, has_temp, has_pH, has_both, condition_quality,
    source_id, cluster_id, split_homology

Two files are written:

    data/ph_benchmark_luke_format.csv           exactly those 24 columns -- drop-in
    data/ph_benchmark_luke_format_extended.csv  the same 24 + ext_* columns carrying
                                                everything his schema has no slot for
    data/ph_luke_format_mapping.json            the transformation, field by field

Three deliberate departures from his file, each flagged rather than hidden:

  1. `split_homology = "test_external"`, a value his data does not use. Reusing "test"
     would silently merge this benchmark into his held-out split; "train" would be a lie.
     Anything filtering `!= "train"` still picks these rows up.
  2. `condition_quality = "Low"` appears. His pH_enzyme_db rows use High / Medium-High /
     Medium; "Low" extends that ordinal scale downwards rather than re-labelling weak
     rows as something stronger.
  3. `cluster_id` is empty. Cluster assignment needs MMseqs2 over his full protein set,
     which is his pipeline, not ours -- `data/ph_benchmark.fasta` is ready for it.

His schema stores the pH itself as `measured_value` for every pH-type row and has no
field for the outcome AT that pH. The recovered residual/relative activity therefore
lives in `ext_relative_activity_pct`; see docs/SCREENER_PH_REPRESENTATION.md.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

LUKE_COLS = [
    "record_id", "source_datasets", "protein_id", "uniprot_id", "pdb_id", "organism",
    "ec_number", "protein_name", "mutation", "position", "wt_aa", "mut_aa",
    "temperature_c", "pH", "method", "measurement_type", "measured_value",
    "has_temp", "has_pH", "has_both", "condition_quality", "source_id",
    "cluster_id", "split_homology",
]

EXT_COLS = [
    "ext_ph_measurement_id", "ext_source_measurement_id", "ext_benchmark_tier",
    "ext_ph_role", "ext_scored_condition_axis", "ext_scored_sequence_model",
    "ext_measurement_type_native", "ext_pH_low", "ext_pH_high", "ext_pH_is_range",
    "ext_ph_range_group", "ext_relative_activity_pct", "ext_relative_activity_pct_high",
    "ext_relative_activity_qualifier", "ext_direction", "ext_exposure_time_min",
    "ext_buffer_name", "ext_substrate", "ext_enzyme_class", "ext_polymer_target",
    "ext_attribution_certainty", "ext_internal_conflict", "ext_enzyme_name_source",
    "ext_pmcid", "ext_doi", "ext_year", "ext_evidence_quote", "ext_audit_rules",
]

# native measurement_type -> Luke's controlled vocabulary
TYPE_MAP = {
    "pH optimum":          "pH optimum",
    "pH stability":        "pH stability",
    "pH stability range":  "pH stability",       # his convention: one row per endpoint
    "pH activity range":   "pH activity range",
    "pH activity":         "pH property",        # his catch-all; no point-activity type
    "temperature optimum": "temperature optimum",
    "thermostability":     "thermostability",
}

SOURCE_TAG = "pet_ph_benchmark_v1"
SPLIT_VALUE = "test_external"


def main():
    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Deterministic ordering so record_ids are stable across rebuilds.
    rows.sort(key=lambda r: (r["pmcid"], r["measurement_type"], r["pH"],
                             r["source_measurement_id"]))

    out, ext_out = [], []
    for i, r in enumerate(rows, 1):
        native = r["measurement_type"]
        mapped = TYPE_MAP[native]

        # Luke's rule: for a pH-type row the measured value IS the pH; for a
        # temperature-type row it is the temperature.
        if mapped in ("pH optimum", "pH stability", "pH activity range", "pH property"):
            measured = r["pH"]
        else:
            measured = r["value_std"]

        if r["assay_method"]:
            method = r["assay_method"]
        else:
            method = ("not specified in table" if r["section"] == "table"
                      else "not specified in sentence")

        has_t = "1" if r["temperature_c"] else "0"
        has_p = "1" if r["pH"] else "0"

        rec = {
            "record_id": f"PHB{i:04d}",
            "source_datasets": SOURCE_TAG,
            "protein_id": r["protein_id_luke_join"],
            "uniprot_id": r["uniprot_accession"],
            "pdb_id": "",
            "organism": r["organism"],
            "ec_number": r["ec_number"],
            "protein_name": r["enzyme_name"],
            "mutation": "",          # every pH row is wild-type / unspecified
            "position": "",
            "wt_aa": "",
            "mut_aa": "",
            "temperature_c": r["temperature_c"],
            "pH": r["pH"],
            "method": method,
            "measurement_type": mapped,
            "measured_value": measured,
            "has_temp": has_t,
            "has_pH": has_p,
            "has_both": "1" if has_t == "1" and has_p == "1" else "0",
            "condition_quality": r["confidence"],
            "source_id": r["pubmed_id"],
            "cluster_id": "",
            "split_homology": SPLIT_VALUE,
        }
        out.append(rec)

        ext = dict(rec)
        ext.update({
            "ext_ph_measurement_id": r["ph_measurement_id"],
            "ext_source_measurement_id": r["source_measurement_id"],
            "ext_benchmark_tier": r["benchmark_tier"],
            "ext_ph_role": r["ph_role"],
            "ext_scored_condition_axis": r["scored_condition_axis"],
            "ext_scored_sequence_model": r["scored_sequence_model"],
            "ext_measurement_type_native": native,
            "ext_pH_low": r["pH_low"],
            "ext_pH_high": r["pH_high"],
            "ext_pH_is_range": r["pH_is_range"],
            "ext_ph_range_group": r["ph_range_group"],
            "ext_relative_activity_pct": r["relative_activity_pct"],
            "ext_relative_activity_pct_high": r["relative_activity_pct_high"],
            "ext_relative_activity_qualifier": r["relative_activity_qualifier"],
            "ext_direction": r["direction"],
            "ext_exposure_time_min": r["exposure_time_min"],
            "ext_buffer_name": r["buffer_name"],
            "ext_substrate": r["substrate"],
            "ext_enzyme_class": r["enzyme_class"],
            "ext_polymer_target": r["polymer_target"],
            "ext_attribution_certainty": r["attribution_certainty"],
            "ext_internal_conflict": r["internal_conflict"],
            "ext_enzyme_name_source": r["enzyme_name_source"],
            "ext_pmcid": r["pmcid"],
            "ext_doi": r["doi"],
            "ext_year": r["year"],
            "ext_evidence_quote": r["evidence_quote"],
            "ext_audit_rules": r["audit_rules"],
        })
        ext_out.append(ext)

    def write(path, rows_, cols):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows_)

    write(os.path.join(DATA, "ph_benchmark_luke_format.csv"), out, LUKE_COLS)
    write(os.path.join(DATA, "ph_benchmark_luke_format_extended.csv"),
          ext_out, LUKE_COLS + EXT_COLS)

    type_counts = {}
    for r in out:
        type_counts[r["measurement_type"]] = type_counts.get(r["measurement_type"], 0) + 1

    mapping = {
        "target_schema": "temp_pH_dataset_ML_homology.csv (24 columns)",
        "rows": len(out),
        "source_datasets_tag": SOURCE_TAG,
        "split_homology_value": SPLIT_VALUE,
        "measurement_type_map": TYPE_MAP,
        "measurement_type_counts_after_mapping": type_counts,
        "field_rules": {
            "record_id": "PHB####, assigned in (pmcid, type, pH, source id) order",
            "protein_id": "P + sha1(sequence.upper().replace('*',''))[:12] -- Luke's hash",
            "measured_value": "the pH for pH-type rows, the temperature for T-type rows "
                              "-- follows his pH_enzyme_db convention",
            "method": "assay_method when the article states one, else "
                      "'not specified in sentence' / 'not specified in table'",
            "condition_quality": "carried across from the benchmark's confidence field",
            "source_id": "PubMed ID, as in his pH_enzyme_db rows",
            "cluster_id": "left empty -- needs MMseqs2 over his full protein set",
            "mutation/position/wt_aa/mut_aa/pdb_id": "empty; all pH rows are wild-type",
        },
        "departures_from_his_file": [
            "split_homology = 'test_external' (new value; avoids merging into his test "
            "split while keeping '!= train' filters correct)",
            "condition_quality = 'Low' (extends his High/Medium-High/Medium scale)",
            "cluster_id empty (his clustering step, not ours)",
            "measurement_type 'pH property' used for point activity-vs-pH values, which "
            "his vocabulary has no exact term for",
        ],
        "not_representable_in_his_schema": [
            "outcome at the pH (residual/relative activity %) -> ext_relative_activity_pct",
            "direction of the effect -> ext_direction",
            "pH interval bounds -> ext_pH_low / ext_pH_high / ext_ph_range_group",
            "exposure time of a stability assay -> ext_exposure_time_min",
            "buffer identity -> ext_buffer_name",
            "evidence sentence and audit trail -> ext_evidence_quote / ext_audit_rules",
        ],
    }
    with open(os.path.join(DATA, "ph_luke_format_mapping.json"),
              "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, indent=1)

    print(f"rows converted : {len(out)}")
    print("measurement_type after mapping:")
    for k, v in sorted(type_counts.items(), key=lambda kv: -kv[1]):
        print(f"    {k:<22} {v}")
    print("\nwrote data/ph_benchmark_luke_format.csv (24 cols)")
    print("      data/ph_benchmark_luke_format_extended.csv "
          f"({len(LUKE_COLS) + len(EXT_COLS)} cols)")
    print("      data/ph_luke_format_mapping.json")


if __name__ == "__main__":
    main()
