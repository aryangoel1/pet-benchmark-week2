# Week 4 — the pH benchmark

The finalised pH axis of the plastic-degrading enzyme benchmark: **68 curated
measurements from 31 open-access articles**, spanning **pH 3.0–12.0** across **19 enzyme
classes**, with every value read against the sentence it came from, every shipped row
re-checked against the freshly downloaded full article, and a recorded verdict for all
105 candidates considered.

> **Integrity statement.** Every value was measured in a laboratory and reported in a
> peer-reviewed open-access article. Nothing is synthetic, predicted, interpolated or
> model-generated — one candidate that carried a response-surface prediction was found
> and removed, and the validation suite now scans every shipped sentence for prediction
> language. No midpoint of a reported range is ever stored. Fields the source did not
> state are left empty.

> **Handover rule.** Final external test only. Not for training, tuning, feature
> selection or threshold selection. Zero benchmark proteins appear in the training split.

---

## Headline numbers

| | |
|---|---:|
| Measurements shipped | **68** |
| Source articles | **31** |
| Candidates audited | 105 |
| Removed by the audit | 37 (35%) |
| pH as the measured outcome / as an assay covariate | 58 / 10 |
| Scoreable on the pH axis / by a sequence model | 46 / 7 |
| Rows carrying the outcome **at** that pH | 29 |
| Rows carrying the direction of the effect | 53 |
| Distinct proteins | 3 |
| Rows in Luke's training split | **0** |
| Sequence attributions rejected on deep re-read | 3 of 6 |

Full breakdowns: [`docs/DATASET_SUMMARY.md`](docs/DATASET_SUMMARY.md).

---

## Read in this order

| # | Document | What it answers |
|---|---|---|
| 1 | [`docs/DATASET_SUMMARY.md`](docs/DATASET_SUMMARY.md) | What is in the dataset — Table 1 and every breakdown |
| 2 | [`docs/AUDIT_REPORT.md`](docs/AUDIT_REPORT.md) | What the audit removed and why, row by row |
| 3 | [`docs/METHODS.md`](docs/METHODS.md) | Publication-ready Methods: sources, inclusion criteria, cleaning, deduplication, units, validation |
| 4 | [`docs/SCREENER_PH_REPRESENTATION.md`](docs/SCREENER_PH_REPRESENTATION.md) | **How pH should be represented in the unified screener** |
| 5 | [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) | Every column, and the format conversion |
| 6 | [`docs/FIGURE_PLAN.md`](docs/FIGURE_PLAN.md) | The planned figure, its rationale and draft caption |
| 7 | [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) | **Read before quoting any number from this** |
| 8 | [`docs/REVIEW_REQUEST.md`](docs/REVIEW_REQUEST.md) | What Luke and Ayush are being asked to check |

---

## Files

### Data

| File | What it is |
|---|---|
| `data/ph_benchmark_v1.csv` | **the benchmark** — 68 rows × 52 columns, native schema |
| `data/ph_benchmark_luke_format.csv` | the same rows in the project's standardized 24-column format, header-identical to `temp_pH_dataset_ML_homology.csv` |
| `data/ph_benchmark_luke_format_extended.csv` | those 24 columns plus 28 `ext_*` columns for what the schema cannot hold |
| `data/ph_benchmark_v1.sqlite` | indexed, with views `v_ph_scored`, `v_ph_scored_seq`, `v_ph_optimum`, `v_ph_stability`, `v_ph_ranges`, `v_ph_covariate`, `v_tier_a`, `v_with_sequence` |
| `data/ph_benchmark.fasta` | one record per protein, header carries the `protein_id` join key |
| `data/ph_excluded_v1.csv` | all 37 removed candidates, each with rule, reason and evidence |
| `data/ph_audit_log.csv` | all 105 candidates, verdict + rules + note |
| `data/ph_stats.json` · `ph_validation.json` · `ph_overlap_luke.json` · `ph_luke_format_mapping.json` | every number quoted in the docs, the validation results, the overlap proof, the format mapping |

### Figure

`figures/figure_ph.svg` — four panels, generated from the shipped data.

### Abstracts

`abstracts/ABSTRACT_master.md` holds the canonical joint abstract and the adaptation
plan; `abstract_comp_bio.md` (250 w), `abstract_enzyme_engineering.md` (177 w) and
`abstract_env_biotech.md` (311 w) are the venue-specific cuts.

---

## Reproducing

Python 3.12, standard library only — no third-party packages.

```bash
python3 scripts/build_ph_benchmark.py    # apply the curation, write data/
python3 scripts/validate_ph.py           # 22 checks; exits non-zero on a hard failure
python3 scripts/check_overlap_luke.py    # the train-overlap check, on the pH subset
python3 scripts/to_luke_format.py        # convert to the standardized schema
python3 scripts/make_reports.py          # regenerate AUDIT_REPORT + DATASET_SUMMARY
python3 scripts/make_figure.py           # regenerate the figure
python3 scripts/deep_verify_ph.py        # re-download articles, verify shipped rows in context
python3 scripts/deep_verify_exclusions.py # re-check every removal against full text
python3 scripts/check_docs.py            # assert the prose still matches the data
```

`check_docs.py` is the guard on the hand-written documents: it asserts every number the
README, Methods, Limitations, figure plan and abstracts quote, so a data change that
invalidates a sentence fails loudly instead of shipping quietly.

`scripts/check_overlap_luke.py` takes the path to Luke's `Week 2_ temperature_ph_dataset_v2`
folder as an optional first argument.

### Where the curation lives

[`scripts/ph_curation.py`](scripts/ph_curation.py) is the audit's source of truth: one
explicit verdict per candidate row, with its rule codes and the reasoning in prose. The
build applies it mechanically and `AUDIT_REPORT.md` is generated from it, so the data and
the documentation cannot disagree. **Disagreeing with a call means editing one entry and
re-running the build.**

---

## How this relates to Week 2

The Week-2 deliverable (`../pet_benchmark_v2.csv`) is a 606-row benchmark across
temperature, pH and electrolyte conditions. 105 of those rows recorded a pH; this is what
happened when those 105 were finalised.

The headline result is worth stating plainly: **all 105 had already passed automated
source verification**, each located verbatim in a freshly downloaded copy of its article.
Reading each against that sentence still removed 36% of them. Automated verification
answers "is this number in the article?"; it cannot answer "is this number recorded
correctly?", and in this corpus the two answers differ for more than a third of rows.

---

## Validation status

```
validate_ph.py      22 checks: 21 pass, 0 hard failures, 1 warning
deep_verify_ph.py   31/31 articles re-downloaded, 68/68 quotes relocated, 0 findings
check_docs.py       every number quoted in the prose matches the data
```

The warning is expected and documented: 9 scored rows carry neither an enzyme name nor an
accession, because the article's own sentence names no enzyme. They remain usable for
condition-axis analysis and are excluded from sequence-model scoring by construction.

---

## Status

Data, code, documentation, figure and abstracts are complete and self-consistent. What is
**not** done:

- The 105 curation verdicts, and the 3 sequence rejections from the deep re-read, are one
  reviewer's judgement and have not been independently reviewed — that is the ask in
  `docs/REVIEW_REQUEST.md`.
- Figures were not re-derived; rows resting on prose that summarises a figure are trusted
  to describe their own figure correctly.
- `cluster_id` is empty in the Luke-format export; it needs MMseqs2 over the full protein
  set, which is Luke's pipeline. `data/ph_benchmark.fasta` is ready for it.
- Author list and order on the abstracts are unconfirmed.
- Conference word limits and deadlines have not been verified against the actual calls
  for papers.
