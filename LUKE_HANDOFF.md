# Benchmark handoff — Luke

Luke — this is the Week-2 independent benchmark, screened the way your `DATA_READINESS_HANDOFF.md` asked for. Short version: **nothing in it touches your training split.**

## The check you asked for

> *"compute each benchmark sequence's `protein_id` and make sure none of them show up as `split_homology == "train"` in `all_unique_proteins_homology.csv`. Drop or flag any overlap."*

Done, using your hash exactly: `protein_id = "P" + sha1(sequence.upper().replace("*",""))[:12]`.

| Result | Count |
|---|---|
| Benchmark rows shipped | 528 |
| Distinct benchmark proteins | 13 |
| Proteins matching `split_homology == "train"` | **0** |
| Proteins matching `split_homology == "test"` | 6 |
| Proteins in neither (new to the project) | 7 |
| Rows dropped for touching your training split | 89 |

`benchmark_sequences.fasta` has every sequence with its `protein_id` in the header, so you can re-run the check yourself in one line.

## Two things to be aware of

**1. Tier B — 21 rows on 6 proteins that are already in your held-out test set.** These are not training contamination, but they are not new to the project either. They are labelled `benchmark_tier = B_in_luke_heldout_test_only`. If you want the benchmark strictly disjoint from everything you have already set aside, filter to `benchmark_tier = 'A_fully_independent'` (SQLite view `v_gold`).

**2. Your 126 plastic-degraders are all in your test split, not train.** That is the right call for training hygiene, but it means Sargun would otherwise be reporting plastic-degrader performance on proteins your split already knows about. Tier A is the clean answer to that — it shares no protein with either side of your split.


### Tier-B proteins (in your test split)

| protein_id | UniProt | Name |
|---|---|---|
| `P04159d914ead` | BAO42836.1 | cutinase |
| `P58458fbad1df` | A0A0K8P6T7 | Poly(ethylene terephthalate) hydrolase |
| `P58458fbad1df` | GAP38373.1 | lipase |
| `P58458fbad1df` | WP_054022242.1 | poly(ethylene terephthalate) hydrolase |
| `Pbe30a4ab193d` | G9BY57 | Leaf-branch compost cutinase |
| `Pfdc10a904ab5` | P13398 | 6-aminohexanoate-cyclic-dimer hydrolase |

## What the benchmark covers that your training set does not

| Axis | Rows here |
|---|---|
| Electrolyte (salt / metal ion / salinity / ionic strength) | 115 |
| Named salt or metal ion | 115 (15 distinct ions, 16 distinct salts) |
| Salinity / seawater | 0 |
| Ionic strength (M) | 21 |
| Mixed electrolyte | 2 |
| Named buffer system | 37 |
| Exposure / incubation time | 81 |
| Assay method recorded | 12 |
| Temperature **and** pH on the same row | 34 |

Your training set carries temperature and pH but no electrolyte column, so the electrolyte axis is testable here without any risk of leakage.

## Handover rule

Per the task: this goes to **Sargun only after training and tuning are finished**. Not for training, not for tuning, not for feature selection, not for picking thresholds — final external test only.

## If you want to re-verify

```bash
python3 scripts/check_overlap.py     # re-runs all 7 screens
python3 scripts/verify_entries.py 120 # re-downloads articles and re-checks entries
```

