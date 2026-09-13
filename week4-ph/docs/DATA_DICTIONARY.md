# Data dictionary — pH benchmark

Covers `data/ph_benchmark_v1.csv` (native schema, 52 columns) and the two
Luke-format exports. Empty means *the source did not state it*; no field is ever filled
with a plausible default.

---

## 1. `ph_benchmark_v1.csv` — native schema

### Identity and provenance

| Column | Type | Notes |
|---|---|---|
| `ph_measurement_id` | `PH` + 8 hex | stable; derived from `source_measurement_id`, so it survives rebuilds |
| `source_measurement_id` | `BM…` | the row's id in the Week-2 benchmark — the join back to the parent dataset |
| `benchmark_tier` | enum | `A_fully_independent` (9 rows) / `C_conditions_only_no_sequence` (59). `B_in_luke_heldout_test_only` is a valid value but no longer occurs: the only tier-B protein was a misattributed sequence, withdrawn on deep re-read |
| `pmcid`, `pubmed_id`, `doi` | string | article identifiers; `pmcid` and `doi` are on every row |
| `paper_title`, `journal`, `year` | string | `journal` is frequently empty upstream |
| `section` | enum | where in the article the sentence came from |
| `evidence_quote` | string | **the verbatim sentence the value was read from**; every row has one |
| `source_verification` | enum | `source_verified` on all rows — the Week-2 pipeline located this quote in a freshly downloaded copy of the article |
| `overlap_rules_checked` | string | which of the seven Week-2 overlap screens fired |

### Role and scoring eligibility

| Column | Type | Notes |
|---|---|---|
| `ph_role` | enum | `outcome` (pH is what was measured) or `covariate` (pH is the stated assay condition for a temperature measurement) |
| `scored_condition_axis` | yes/no | usable to score a prediction on the pH axis: an outcome row, a point value, not internally contradicted |
| `scored_sequence_model` | yes/no | the above **and** a resolved sequence **and** unambiguous single-enzyme attribution |
| `unscored_reason` | string | why a row is not scoreable — empty when it is |

`scored_*` are conveniences, not gates: every row is real and every row is shipped. They
exist so an evaluation script does not have to re-derive the eligibility rules.

### Enzyme identity

| Column | Type | Notes |
|---|---|---|
| `enzyme_name` | string | as the evidence names it |
| `enzyme_name_source` | enum | `as_reported` / `corrected_from_evidence` / `not_named_in_evidence` |
| `enzyme_class` | string | catalytic family the article assigns (lipase, cutinase, PHB depolymerase, …) |
| `polymer_target` | string | **only** where the article names a polymer substrate; empty otherwise |
| `organism`, `ec_number` | string | as reported |
| `uniprot_accession` | string | UniProt or GenBank accession |
| `protein_id_luke_join` | `P` + 12 hex | `"P" + sha1(sequence.upper().replace("*",""))[:12]` — the project join key |
| `sequence`, `sequence_length` | string / int | empty for tier C |
| `attribution_certainty` | enum | `single_enzyme` or `multiple_enzymes_same_value` (the sentence gives one value for several enzymes) |

### The pH measurement

| Column | Type | Notes |
|---|---|---|
| `measurement_type` | enum | see §2 |
| `pH` | float 0–14 | the point value |
| `pH_low`, `pH_high` | float 0–14 | interval bounds; also set on point rows where the article states the surrounding active range |
| `pH_is_range` | yes/no | `yes` means this row *is* an interval statement, not a point |
| `ph_range_group` | string | links the endpoint rows of one interval (`R-<pmcid-stem>-<letter>`) |
| `relative_activity_pct` | float 0–200 | **the outcome at that pH** — % of maximal or initial activity |
| `relative_activity_pct_high` | float | upper end when the article gives a band ("89–97%") |
| `relative_activity_qualifier` | enum | `exact` / `approx` / `gte` / `lte` / `range` — preserves "about", "over", "less than" |
| `direction` | enum | `optimum` / `stabilising` / `destabilising` — mandatory on stability rows |
| `value_std`, `value_unit_std` | float / string | the canonical value: the pH for pH-typed rows, the temperature for covariate rows |
| `internal_conflict` | yes/no | the article contradicts this row elsewhere; excluded from scoring |

### Assay context

| Column | Type | Notes |
|---|---|---|
| `temperature_c` | float | assay temperature where stated |
| `buffer_name`, `buffer_conc_mM` | string / float | buffers not named in the evidence have been cleared |
| `exposure_time_min` | float | incubation time for stability measurements |
| `substrate` | string | where the article names one |
| `assay_method` | string | where the article names one |
| `confidence` | enum | `High` / `Medium-High` / `Medium` / `Low`, inherited from the parent pipeline |

### Audit trail

| Column | Type | Notes |
|---|---|---|
| `audit_verdict` | `KEEP` | shipped rows only; excluded rows are in `ph_excluded_v1.csv` |
| `audit_rules` | `;`-joined | correction codes `PH-C1…PH-C7`, derived from the field edits actually applied |
| `audit_rule_names` | `;`-joined | human-readable form of the above |
| `audit_note` | string | why this call was made, in prose |
| `corrections_applied` | `;`-joined | the field names that were changed |

---

## 2. Measurement-type vocabulary

| Type | pH is the… | `value_std` | Rows |
|---|---|---|---:|
| `pH optimum` | outcome | the optimum pH | 25 |
| `pH stability` | outcome | the pH tested | 17 |
| `pH stability range` | outcome | the endpoint pH | 9 |
| `pH activity` | outcome | the pH tested | 4 |
| `pH activity range` | outcome | the endpoint pH | 3 |
| `temperature optimum` | covariate | the optimum temperature (°C) | 9 |
| `thermostability` | covariate | the temperature (°C) | 1 |

`pH stability` = activity remaining after incubation at that pH.
`pH activity` = activity measured at that pH, a point on the activity-vs-pH profile.
The distinction matters: an enzyme can be *active* at a pH it is not *stable* at, and
three articles in this corpus report both profiles separately.

---

## 3. Unit handling

pH is dimensionless, so the work here is representational rather than arithmetic.

| Quantity | Canonical unit | Converted from | Rule |
|---|---|---|---|
| pH | dimensionless | — | one decimal place; ranges split into `pH_low`/`pH_high`, **never** averaged to a midpoint |
| Relative / residual activity | % of maximal or initial | fractions, "x-fold" | qualifier retained separately; never rounded into the value |
| Temperature | °C | K, °F | inherited from the parent pipeline |
| Exposure time | minutes | s, h, d, weeks | `1 h → 60`, `15 h → 900`, `30 min → 30` |
| Buffer concentration | mM | M, µM, %(w/v), mg/mL, g/L | via formula weight, inherited |

**Two invariants, both enforced by `validate_ph.py`:**

1. **No synthesised midpoints.** "optimal between pH 4.0 and 6.0" is stored as the
   interval, never as 5.0.
2. **No dropped qualifiers.** "less than 50%" is `50` + `lte`. Storing a bare `50` would
   let a model read a bound as an observation.

---

## 4. Luke-format exports

`ph_benchmark_luke_format.csv` is byte-compatible with the 24-column header of
`temp_pH_dataset_ML_homology.csv` (verified by comparing headers directly).
`ph_benchmark_luke_format_extended.csv` adds 28 `ext_*` columns carrying everything the
24-column schema cannot hold.

| Native field | Luke field | Note |
|---|---|---|
| `pH` | `pH` **and** `measured_value` | his convention: for a pH-type row the measured value *is* the pH |
| `value_std` | `measured_value` | for temperature-type rows |
| `enzyme_name` | `protein_name` | |
| `confidence` | `condition_quality` | adds `Low` to his High/Medium-High/Medium scale |
| `pubmed_id` | `source_id` | matches his `pH_enzyme_db` rows |
| `assay_method` | `method` | falls back to `not specified in sentence` / `not specified in table` |
| `protein_id_luke_join` | `protein_id` | |
| — | `cluster_id` | **empty** — needs MMseqs2 over his full protein set |
| — | `split_homology` | **`test_external`** — a new value; see below |
| — | `source_datasets` | `pet_ph_benchmark_v1` |
| `relative_activity_pct` | *(no slot)* | → `ext_relative_activity_pct` |
| `direction` | *(no slot)* | → `ext_direction` |
| `pH_low` / `pH_high` | *(no slot)* | → `ext_pH_low` / `ext_pH_high` |
| `evidence_quote` | *(no slot)* | → `ext_evidence_quote` |

### Type mapping

| Native | Luke | |
|---|---|---|
| `pH optimum` | `pH optimum` | exact |
| `pH stability`, `pH stability range` | `pH stability` | his one-row-per-endpoint convention |
| `pH activity range` | `pH activity range` | exact |
| `pH activity` | `pH property` | **compromise** — no point-activity type exists in his vocabulary |
| `temperature optimum` | `temperature optimum` | exact |
| `thermostability` | `thermostability` | exact |

### Why `split_homology = "test_external"`

Reusing `"test"` would silently merge this benchmark into Luke's held-out split, which is
a different thing with a different purpose. `"train"` would be false. `test_external`
says what it is: an external, test-only benchmark. Any filter written as
`split_homology != "train"` continues to behave correctly.

---

## 5. Other files

| File | What it is |
|---|---|
| `ph_excluded_v1.csv` | all 37 removed candidates, each with its rule, reason and evidence |
| `ph_audit_log.csv` | all 105 candidates, verdict + rules + note, machine-readable |
| `ph_benchmark_v1.sqlite` | the shipped rows, indexed, with views `v_ph_scored`, `v_ph_scored_seq`, `v_ph_optimum`, `v_ph_stability`, `v_ph_ranges`, `v_ph_covariate`, `v_tier_a`, `v_with_sequence` |
| `ph_benchmark.fasta` | one record per distinct protein, header carries `protein_id` |
| `ph_stats.json` | every number quoted in the documentation |
| `ph_validation.json` | the result of each validation check |
| `ph_overlap_luke.json` | the train-overlap check, per protein |
| `ph_luke_format_mapping.json` | the format conversion, field by field |
