# Week 2 submission — what to hand over

**Deliverable:** an independent, test-only benchmark of plastic-degrading enzyme performance
across temperature, pH and electrolyte conditions. 528 measurements from 79 open-access
articles, screened against all seven shared datasets and Luke's training data.

## Read in this order

1. `PET_Benchmark_Week2_Final_Brief.docx` — the brief (opens in Google Docs)
2. `README.md` — schema, methods, provenance
3. `MANUAL_VERIFICATION.md` — what manual review found and the measured error rate
4. `OVERLAP_REPORT.md` — the full audit trail

## Data files

| File | Contents |
|---|---|
| `pet_benchmark_v2.csv` | 528 rows × 70 columns |
| `pet_benchmark_v2.sqlite` | Same data, indexed, with `v_gold` and five other views |
| `benchmark_sequences.fasta` | 15 sequences, headers carry Luke's `protein_id` join key |

## Distribution

| Who | What they get | When |
|---|---|---|
| **Luke** | `LUKE_HANDOFF.md` + `benchmark_sequences.fasta` | Now — so he can re-run the train-overlap check himself |
| **Sargun** | The full benchmark | **Only after training and tuning are finished.** Final external test only. |

## Rebuilding from scratch

```bash
python3 -m venv .venv && .venv/bin/pip install python-docx pypdf
python3 scripts/build_exclusions.py      # index the 7 datasets + Luke + week 1
python3 scripts/harvest_benchmark.py     # mine NEW open-access articles
python3 scripts/resolve_sequences.py     # UniProt accessions named in text
python3 scripts/resolve_by_paper.py      # PubMed cross-refs + GenBank
python3 scripts/rescan_accessions.py     # deposit-section accessions (offline)
python3 scripts/resolve_rescan.py        # fetch those sequences
python3 scripts/paper_relevance.py       # article-level plastic relevance (offline)
python3 scripts/build_benchmark.py       # standardize units + quality gates
python3 scripts/check_overlap.py         # the seven overlap screens
python3 scripts/verify_entries.py        # re-verify against fresh downloads
python3 scripts/manual_exclusions.py     # apply manual-review findings
python3 scripts/finalize.py              # CSV / SQLite / FASTA
python3 scripts/make_reports.py          # OVERLAP_REPORT + LUKE_HANDOFF
python3 scripts/make_readme.py
.venv/bin/python scripts/make_final_docx.py
```

Everything is standard library except `pypdf` (reads the S669 PDF) and `python-docx`
(writes the brief).
