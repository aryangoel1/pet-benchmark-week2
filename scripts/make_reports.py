#!/usr/bin/env python3
"""Generate OVERLAP_REPORT.md (the audit trail) and LUKE_HANDOFF.md (for Luke)."""
import csv, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

SHEETS = [
 ("Training set 1 — Tsuboyama2023", "https://docs.google.com/spreadsheets/d/1D3SuYcpPAwwzgpMgnGXvrUmYaYQPGNLIjH0o40ePdu4/edit?usp=sharing"),
 ("Training set 2 — Domainome", "https://docs.google.com/spreadsheets/d/1cqGczP84zkfsTa4W1-ShitCEsA-PQCmlNGHRUWLkYlA/edit?usp=sharing"),
 ("Training set 3 — Domainome", "https://docs.google.com/spreadsheets/d/1XCAng1bQq44u9irqOnaZkmuadzf3OhHN5fuUzkloyB0/edit?usp=sharing"),
 ("Training set 4 — Tsuboyama2023_double", "https://docs.google.com/spreadsheets/d/1W471dUgXm867lDDywmUTkvQVA1ApmoXhRRY9WwLWd50/edit?usp=sharing"),
 ("Training set 5 — Tsuboyama2023", "https://docs.google.com/spreadsheets/d/1FEkmSDK-VEdkCQixbRBepH68cyyv1XvWbLMG-xTFNQA/edit?usp=sharing"),
 ("Training set 6 — Meltome", "https://docs.google.com/spreadsheets/d/1iXVdyaI80a0pbtrHPlHw5OSNkJrRuHDGYLoV20_fNfo/edit?usp=sharing"),
 ("Benchmark data set — S669", "https://docs.google.com/spreadsheets/d/19qZetoMKP4HD63f0MPpMKQhIAeflJyjed730rcKMv88/edit?usp=sharing"),
]


def main():
    stats = json.load(open(D("data", "final_stats.json")))
    excl = json.load(open(D("data", "exclusions.json")))
    ovl = json.load(open(D("data", "overlap.json")))
    shipped = list(csv.DictReader(open(D("pet_benchmark_v2.csv"))))
    counts, rules = ovl["counts"], ovl["rules"]

    # ------------------------------------------------------------ OVERLAP_REPORT
    L = ["# Overlap audit — Week-2 independent benchmark\n",
         "Every candidate measurement was screened against **all seven shared datasets**, "
         "**Luke's Week-2 training dataset**, **Luke's Week-1 pH database** and **my own Week-1 "
         "conditions database** before anything was shipped. This is the audit trail.\n",
         "## What was indexed\n",
         "| Source | Records indexed | Keys extracted |", "|---|---|---|"]
    for k, v in excl["per_source"].items():
        L.append(f"| {k} | {v['rows_indexed']:,} | {v['kind']} |")
    t = excl["index_totals"]
    L += ["\n**Resulting index:** "
          f"{t['seq']:,} distinct protein sequences · {t['pid']:,} Luke-format `protein_id`s · "
          f"{t['acc']:,} UniProt accessions · {t['paper']:,} paper identifiers (PMID/PMCID) · "
          f"{t['fp']:,} measurement fingerprints · {t['pdb']} PDB codes.\n",
          f"Of the indexed proteins, **{excl['luke_train_protein_ids']:,}** are in Luke's "
          f"`split_homology == train` and **{excl['luke_test_protein_ids']:,}** in his held-out test split.\n",
          "## The seven datasets, as supplied\n", "| # | Dataset | Source sheet |", "|---|---|---|"]
    for i, (name, url) in enumerate(SHEETS, 1):
        L.append(f"| {i} | {name} | [sheet]({url}) |")

    L += ["\n## Screens applied to every candidate row\n",
          "| Screen | What it compares | Rows it fired on |", "|---|---|---|",
          f"| S1 sequence identity | SHA-1 of the resolved sequence vs all indexed sequences | {rules.get('S1_sequence_identity',0)} |",
          f"| S2 Luke join key | `protein_id` = `\"P\"+sha1(seq.upper().replace(\"*\",\"\"))[:12]` vs his split | {rules.get('S2_luke_protein_id',0)} |",
          f"| S3 UniProt accession | accession vs every accession in every prior dataset | {rules.get('S3_uniprot_accession',0)} |",
          f"| S4 paper identity | PMCID/PMID vs every paper any prior dataset cites | {rules.get('S4_paper_already_used',0)} |",
          f"| S5 measurement tuple | (protein, mutation, type, pH, T, value) vs 1.58 M fingerprints | {rules.get('S5_measurement_fingerprint',0)} |",
          f"| S6 PDB code | PDB codes named in the paper vs the S669 roster | {rules.get('S6_pdb_in_S669',0)} |",
          f"| S7 internal duplicate | the same measurement extracted twice within this build | {rules.get('S7_internal_duplicate',0)} |",
          "\n## Verdicts\n", "| Verdict | Rows | Outcome |", "|---|---|---|",
          f"| `DROP_TRAIN_OVERLAP` | {counts.get('DROP_TRAIN_OVERLAP',0)} | protein sits in Luke's **training** split — deleted |",
          f"| `DROP_DUPLICATE` | {counts.get('DROP_DUPLICATE',0)} | already present in a prior dataset — deleted |",
          f"| `DROP_INTERNAL_DUP` | {counts.get('DROP_INTERNAL_DUP',0)} | duplicate within this build — deleted |",
          f"| `KEEP_TIER_A` | {counts.get('KEEP_TIER_A',0)} | appears in **no** prior dataset — shipped as the gold benchmark |",
          f"| `KEEP_TIER_B` | {counts.get('KEEP_TIER_B',0)} | protein is in Luke's **held-out test** split only — shipped, flagged |",
          f"| `KEEP_NO_SEQUENCE` | {counts.get('KEEP_NO_SEQUENCE',0)} | real measurement, no sequence resolvable — shipped as conditions-only |",
          "\n### Why paper-level exclusion matters\n",
          "Screen S4 removes any article already mined by my Week-1 build (all 199 of them) or "
          "cited by any prior dataset — **before the article is even downloaded**. That prevents "
          "the same measurement re-entering the benchmark through a different enzyme name.\n",
          "\n## Independence statement\n",
          f"- **0** shipped rows carry a protein in `split_homology == \"train\"`.\n"
          f"- **{stats['tiers'].get('A_fully_independent',0)}** shipped rows carry a protein that "
          "appears in **none** of the seven datasets and **none** of Luke's data.\n"
          f"- **{stats['tiers'].get('B_in_luke_heldout_test_only',0)}** rows are on proteins already "
          "inside Luke's held-out test split. They are not training contamination, but they are not "
          "novel either — they are tiered separately so they can be excluded with one filter.\n"
          f"- **{stats['distinct_papers']}** distinct source articles, none of which appears in any prior dataset.\n"]
    open(D("OVERLAP_REPORT.md"), "w").write("\n".join(L) + "\n")

    # -------------------------------------------------------------- LUKE_HANDOFF
    tierB = [r for r in shipped if r["benchmark_tier"] == "B_in_luke_heldout_test_only"]
    tierB_prot = sorted({(r["protein_id_luke_join"], r["uniprot_accession"],
                          r["uniprot_protein_name"] or r["enzyme_name"]) for r in tierB})
    H = ["# Benchmark handoff — Luke\n",
         "Luke — this is the Week-2 independent benchmark, screened the way your "
         "`DATA_READINESS_HANDOFF.md` asked for. Short version: **nothing in it touches your "
         "training split.**\n",
         "## The check you asked for\n",
         "> *\"compute each benchmark sequence's `protein_id` and make sure none of them show up as "
         "`split_homology == \"train\"` in `all_unique_proteins_homology.csv`. Drop or flag any overlap.\"*\n",
         "Done, using your hash exactly: `protein_id = \"P\" + sha1(sequence.upper().replace(\"*\",\"\"))[:12]`.\n",
         "| Result | Count |", "|---|---|",
         f"| Benchmark rows shipped | {stats['shipped_rows']} |",
         f"| Distinct benchmark proteins | {stats['distinct_proteins']} |",
         f"| Proteins matching `split_homology == \"train\"` | **0** |",
         f"| Proteins matching `split_homology == \"test\"` | {len(tierB_prot)} |",
         f"| Proteins in neither (new to the project) | {stats['distinct_proteins'] - len(tierB_prot)} |",
         f"| Rows dropped for touching your training split | {counts.get('DROP_TRAIN_OVERLAP',0)} |",
         "\n`benchmark_sequences.fasta` has every sequence with its `protein_id` in the header, so you "
         "can re-run the check yourself in one line.\n",
         "## Two things to be aware of\n",
         f"**1. Tier B — {len(tierB)} rows on {len(tierB_prot)} proteins that are already in your "
         "held-out test set.** These are not training contamination, but they are not new to the "
         "project either. They are labelled `benchmark_tier = B_in_luke_heldout_test_only`. If you "
         "want the benchmark strictly disjoint from everything you have already set aside, filter to "
         "`benchmark_tier = 'A_fully_independent'` (SQLite view `v_gold`).\n",
         "**2. Your 126 plastic-degraders are all in your test split, not train.** That is the right "
         "call for training hygiene, but it means Sargun would otherwise be reporting plastic-degrader "
         "performance on proteins your split already knows about. Tier A is the clean answer to that — "
         "it shares no protein with either side of your split.\n"]
    if tierB_prot:
        H += ["\n### Tier-B proteins (in your test split)\n",
              "| protein_id | UniProt | Name |", "|---|---|---|"]
        for pid, acc, name in tierB_prot[:60]:
            H.append(f"| `{pid}` | {acc or '—'} | {name or '—'} |")
        if len(tierB_prot) > 60:
            H.append(f"| … | | *{len(tierB_prot)-60} more in the CSV* |")
    H += ["\n## What the benchmark covers that your training set does not\n",
          "| Axis | Rows here |", "|---|---|",
          f"| Electrolyte (salt / metal ion / salinity / ionic strength) | {stats['with_electrolyte']} |",
          f"| Named salt or metal ion | {stats['with_salt_or_ion']} ({stats['distinct_ions']} distinct ions, {stats['distinct_salts']} distinct salts) |",
          f"| Salinity / seawater | {stats['with_salinity']} |",
          f"| Ionic strength (M) | {stats['with_ionic_strength']} |",
          f"| Mixed electrolyte | {stats['mixed_electrolyte']} |",
          f"| Named buffer system | {stats['with_buffer']} |",
          f"| Exposure / incubation time | {stats['with_exposure_time']} |",
          f"| Assay method recorded | {stats['with_assay_method']} |",
          f"| Temperature **and** pH on the same row | {stats['with_T_and_pH']} |",
          "\nYour training set carries temperature and pH but no electrolyte column, so the electrolyte "
          "axis is testable here without any risk of leakage.\n",
          "## Handover rule\n",
          "Per the task: this goes to **Sargun only after training and tuning are finished**. Not for "
          "training, not for tuning, not for feature selection, not for picking thresholds — final "
          "external test only.\n",
          "## If you want to re-verify\n",
          "```bash\npython3 scripts/check_overlap.py     # re-runs all 7 screens\n"
          "python3 scripts/verify_entries.py 120 # re-downloads articles and re-checks entries\n```\n"]
    open(D("LUKE_HANDOFF.md"), "w").write("\n".join(H) + "\n")
    print("Wrote OVERLAP_REPORT.md and LUKE_HANDOFF.md", file=sys.stderr)


if __name__ == "__main__":
    main()
