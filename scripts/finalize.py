#!/usr/bin/env python3
"""Assemble the shipped benchmark: apply the overlap gate + verification, write
CSV / SQLite / FASTA, and generate the coordination reports.

Shipped only if:  verdict startswith KEEP  AND  (verified OR not selected for verification)
Rows that failed verification are removed; rows that were never selected keep the
flag `verification=not_selected` so nobody mistakes them for verified.

Outputs:
  pet_benchmark_v2.csv / .sqlite / benchmark_sequences.fasta
  OVERLAP_REPORT.md      - the audit trail against all 7 datasets + Luke
  LUKE_HANDOFF.md        - the document to send Luke
  data/final_stats.json
"""
import csv, hashlib, json, os, re, sqlite3, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)


def protein_id(seq):
    return "P" + hashlib.sha1(seq.upper().replace("*", "").encode()).hexdigest()[:12]


COLUMNS = [
    "measurement_id", "benchmark_tier",
    # identity
    "enzyme_name", "uniprot_accession", "uniprot_protein_name", "organism", "ec_number",
    "protein_id_luke_join", "sequence_length", "sequence_completeness", "sequence_resolution", "reviewed_status_uniprot",
    "mutation", "is_wild_type",
    # substrate
    "substrate", "substrate_scope", "substrate_form",
    # temperature
    "temperature_raw", "temperature_c", "temperature_c_low", "temperature_c_high",
    # pH
    "pH_raw", "pH", "pH_low", "pH_high",
    # buffer + electrolyte
    "buffer_name", "buffer_conc_mM", "salt_species", "salt_conc_raw", "salt_conc_mM",
    "ion_species", "ion_charge", "mixed_electrolyte", "electrolyte_composition",
    "salinity_raw", "salinity_g_per_L", "salinity_psu", "salinity_source", "seawater_type",
    "ionic_strength_M", "ionic_strength_source", "additive", "additive_conc_mM",
    # exposure + assay
    "exposure_time_raw", "exposure_time_min", "assay_method", "assay_method_scope",
    # measurement
    "measurement_type", "value_raw", "value_unit_raw", "value_std", "value_std_high",
    "value_unit_std", "value_is_range",
    "relative_activity_pct", "direction", "kinetic_param",
    # provenance
    "source_db", "source_type", "pmcid", "pubmed_id", "doi", "paper_title", "journal", "year",
    "search_axis", "section", "evidence_quote", "data_origin",
    # quality / audit
    "plastic_relevance", "confidence", "verification", "overlap_rules_checked",
    "sequence",
]


def main():
    rows = {r["measurement_id"]: r for r in json.load(open(D("data", "bench_std.json")))}
    ovl = {v["measurement_id"]: v for v in json.load(open(D("data", "overlap.json")))["verdicts"]}
    # defects found by reading entries against their source, expanded to every row
    # sharing each defect's signature (scripts/manual_exclusions.py)
    mx_path = D("data", "manual_exclusions.json")
    manual_ex = json.load(open(mx_path))["exclusions"] if os.path.exists(mx_path) else {}
    ver = {}
    vp = D("data", "verification.json")
    if os.path.exists(vp):
        ver = {v["measurement_id"]: v for v in json.load(open(vp))["results"]}

    shipped, removed = [], collections.Counter()
    for mid, r in rows.items():
        v = ovl.get(mid, {})
        verdict = v.get("verdict", "KEEP_TIER_A")
        if not verdict.startswith("KEEP"):
            removed[verdict] += 1
            continue
        if mid in manual_ex:
            removed["MANUAL_REVIEW_REJECTED"] += 1
            continue
        vr = ver.get(mid)
        if vr and vr["status"] != "VERIFIED":
            removed[f"VERIFICATION_{vr['status']}"] += 1
            continue
        out = {c: "" for c in COLUMNS}
        for k in r:
            if k in out:
                out[k] = r[k]
        out["measurement_id"] = mid
        out["benchmark_tier"] = {"KEEP_TIER_A": "A_fully_independent",
                                 "KEEP_TIER_B": "B_in_luke_heldout_test_only",
                                 "KEEP_NO_SEQUENCE": "C_conditions_only_no_sequence"}[verdict]
        out["protein_id_luke_join"] = protein_id(r["sequence"]) if r.get("sequence") else ""
        out["verification"] = ("source_verified" if vr and vr["status"] == "VERIFIED"
                               else "not_selected")
        out["overlap_rules_checked"] = ";".join(v.get("rules_fired", [])) or "none_fired"
        shipped.append(out)

    shipped.sort(key=lambda x: (x["benchmark_tier"], x["measurement_id"]))
    print(f"Shipping {len(shipped)} rows; removed {dict(removed)}", file=sys.stderr)

    # ------------------------------------------------------------------- CSV
    with open(D("pet_benchmark_v2.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(shipped)

    # ------------------------------------------------------------------ FASTA
    seen = {}
    for r in shipped:
        if r["sequence"] and r["uniprot_accession"] not in seen:
            seen[r["uniprot_accession"]] = r
    with open(D("benchmark_sequences.fasta"), "w") as f:
        for acc, r in sorted(seen.items()):
            f.write(f">{acc}|{r['protein_id_luke_join']}|{r['organism']}|"
                    f"{r['uniprot_protein_name'] or r['enzyme_name']}\n")
            s = r["sequence"]
            for i in range(0, len(s), 60):
                f.write(s[i:i + 60] + "\n")

    # ----------------------------------------------------------------- SQLite
    dbp = D("pet_benchmark_v2.sqlite")
    if os.path.exists(dbp):
        os.remove(dbp)
    db = sqlite3.connect(dbp)
    db.execute(f"CREATE TABLE benchmark ({', '.join(f'{c} TEXT' for c in COLUMNS)})")
    db.executemany(f"INSERT INTO benchmark VALUES ({','.join('?' * len(COLUMNS))})",
                   [[str(r[c]) for c in COLUMNS] for r in shipped])
    db.executescript("""
        CREATE INDEX ix_acc  ON benchmark(uniprot_accession);
        CREATE INDEX ix_pid  ON benchmark(protein_id_luke_join);
        CREATE INDEX ix_type ON benchmark(measurement_type);
        CREATE INDEX ix_tier ON benchmark(benchmark_tier);
        CREATE VIEW v_gold        AS SELECT * FROM benchmark WHERE benchmark_tier='A_fully_independent';
        CREATE VIEW v_sequence    AS SELECT * FROM benchmark WHERE sequence <> '';
        CREATE VIEW v_temperature AS SELECT * FROM benchmark WHERE temperature_c <> '';
        CREATE VIEW v_ph          AS SELECT * FROM benchmark WHERE pH <> '';
        CREATE VIEW v_electrolyte AS SELECT * FROM benchmark
              WHERE ion_species<>'' OR salt_species<>'' OR salinity_raw<>'' OR ionic_strength_M<>'';
        CREATE VIEW v_verified    AS SELECT * FROM benchmark WHERE verification='source_verified';
    """)
    db.commit(); db.close()

    # ------------------------------------------------------------------ stats
    def c(key):
        return collections.Counter(r[key] for r in shipped)

    papers = {r["pmcid"] for r in shipped if r["pmcid"]}
    prot = {r["protein_id_luke_join"] for r in shipped if r["protein_id_luke_join"]}
    stats = {
        "shipped_rows": len(shipped),
        "removed": dict(removed),
        "distinct_papers": len(papers),
        "distinct_proteins": len(prot),
        "distinct_accessions": len({r["uniprot_accession"] for r in shipped if r["uniprot_accession"]}),
        "tiers": dict(c("benchmark_tier")),
        "measurement_types": dict(c("measurement_type")),
        "with_sequence": sum(1 for r in shipped if r["sequence"]),
        "with_temperature": sum(1 for r in shipped if r["temperature_c"] != ""),
        "with_pH": sum(1 for r in shipped if r["pH"] != ""),
        "with_T_and_pH": sum(1 for r in shipped if r["temperature_c"] != "" and r["pH"] != ""),
        "with_electrolyte": sum(1 for r in shipped if r["ion_species"] or r["salt_species"]
                                or r["salinity_raw"] or r["ionic_strength_M"] != ""),
        "with_salt_or_ion": sum(1 for r in shipped if r["ion_species"] or r["salt_species"]),
        "with_salinity": sum(1 for r in shipped if r["salinity_raw"]),
        "with_ionic_strength": sum(1 for r in shipped if r["ionic_strength_M"] != ""),
        "mixed_electrolyte": sum(1 for r in shipped if r["mixed_electrolyte"] == "yes"),
        "with_buffer": sum(1 for r in shipped if r["buffer_name"]),
        "with_exposure_time": sum(1 for r in shipped if r["exposure_time_min"] != ""),
        "with_assay_method": sum(1 for r in shipped if r["assay_method"]),
        "with_mutation": sum(1 for r in shipped if r["is_wild_type"] == "no"),
        "source_verified": sum(1 for r in shipped if r["verification"] == "source_verified"),
        "distinct_ions": len({r["ion_species"] for r in shipped if r["ion_species"]}),
        "distinct_salts": len({r["salt_species"] for r in shipped if r["salt_species"]}),
        "plastic_relevance": dict(c("plastic_relevance")),
        "confidence": dict(c("confidence")),
        "sequence_resolution": dict(c("sequence_resolution")),
    }
    json.dump(stats, open(D("data", "final_stats.json"), "w"), indent=1)
    print(json.dumps(stats, indent=1)[:2200], file=sys.stderr)
    print(f"\nWrote pet_benchmark_v2.csv / .sqlite / benchmark_sequences.fasta", file=sys.stderr)


if __name__ == "__main__":
    main()
