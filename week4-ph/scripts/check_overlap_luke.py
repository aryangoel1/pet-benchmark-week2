"""
Re-run Luke's train-overlap check against the Week-4 pH benchmark specifically.

    python3 scripts/check_overlap_luke.py [path_to_luke_folder]

Luke's DATA_READINESS_HANDOFF.md asks for exactly this:

    "compute each benchmark sequence's protein_id and make sure none of them show up as
     split_homology == 'train' in all_unique_proteins_homology.csv. Drop or flag any
     overlap."

The Week-2 build ran this over all 606 rows. It is re-run here over the pH subset alone
so the pH deliverable carries its own standalone proof, rather than inheriting one.

Writes data/ph_overlap_luke.json.
"""
import csv
import hashlib
import json
import os
import sys

csv.field_size_limit(10 ** 9)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
DEFAULT_LUKE = (r"C:\Users\worki\Downloads"
                r"\Week 2_ temperature_ph_dataset_v2-20260913T050402Z-1-001"
                r"\Week 2_ temperature_ph_dataset_v2")


def luke_protein_id(seq):
    return "P" + hashlib.sha1(seq.upper().replace("*", "").encode()).hexdigest()[:12]


def main():
    luke_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LUKE
    proteins_csv = os.path.join(luke_dir, "all_unique_proteins_homology.csv")
    if not os.path.exists(proteins_csv):
        raise SystemExit(f"cannot find {proteins_csv}\n"
                         f"pass Luke's folder as the first argument")

    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Recompute the join key from the sequence rather than trusting the column.
    bench = {}
    for r in rows:
        if r["sequence"]:
            pid = luke_protein_id(r["sequence"])
            assert pid == r["protein_id_luke_join"], r["ph_measurement_id"]
            bench.setdefault(pid, {
                "accessions": set(), "enzymes": set(), "rows": 0,
                "tier": r["benchmark_tier"], "organism": r["organism"]})
            bench[pid]["rows"] += 1
            if r["uniprot_accession"]:
                bench[pid]["accessions"].add(r["uniprot_accession"])
            if r["enzyme_name"]:
                bench[pid]["enzymes"].add(r["enzyme_name"])

    split = {}
    with open(proteins_csv, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            split[r["protein_id"]] = r["split_homology"]

    verdicts = {}
    for pid, info in bench.items():
        verdicts[pid] = split.get(pid, "not_in_lukes_data")

    in_train = [p for p, v in verdicts.items() if v == "train"]
    in_test = [p for p, v in verdicts.items() if v == "test"]
    novel = [p for p, v in verdicts.items() if v == "not_in_lukes_data"]

    rows_no_seq = sum(1 for r in rows if not r["sequence"])

    out = {
        "luke_folder": luke_dir,
        "luke_proteins_indexed": len(split),
        "benchmark_rows": len(rows),
        "benchmark_rows_with_sequence": len(rows) - rows_no_seq,
        "benchmark_rows_without_sequence": rows_no_seq,
        "benchmark_distinct_proteins": len(bench),
        "proteins_in_luke_train": len(in_train),
        "proteins_in_luke_test": len(in_test),
        "proteins_new_to_the_project": len(novel),
        "verdict": ("CLEAN - no benchmark protein appears in Luke's training split"
                    if not in_train else "TRAINING OVERLAP FOUND - drop these rows"),
        "per_protein": [
            {"protein_id": p,
             "split_homology": verdicts[p],
             "rows": bench[p]["rows"],
             "tier": bench[p]["tier"],
             "organism": bench[p]["organism"],
             "accessions": sorted(bench[p]["accessions"]),
             "enzymes": sorted(bench[p]["enzymes"])}
            for p in sorted(bench, key=lambda x: -bench[x]["rows"])],
    }

    with open(os.path.join(DATA, "ph_overlap_luke.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)

    print(f"Luke proteins indexed        : {out['luke_proteins_indexed']:,}")
    print(f"pH benchmark rows            : {out['benchmark_rows']}")
    print(f"  with a resolved sequence   : {out['benchmark_rows_with_sequence']}")
    print(f"  distinct proteins          : {out['benchmark_distinct_proteins']}")
    print(f"in Luke's TRAIN split        : {out['proteins_in_luke_train']}")
    print(f"in Luke's held-out TEST split: {out['proteins_in_luke_test']}")
    print(f"new to the project           : {out['proteins_new_to_the_project']}")
    print(f"\n{out['verdict']}\n")
    for p in out["per_protein"]:
        print(f"  {p['protein_id']}  {p['split_homology']:<18} rows={p['rows']:<3}"
              f" {','.join(p['accessions']) or '-':<22} {p['organism'][:34]}")
    return 0 if not in_train else 1


if __name__ == "__main__":
    sys.exit(main())
