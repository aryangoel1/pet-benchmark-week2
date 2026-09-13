# How pH is represented in the unified screener

A specification, not a description. This is the contract the pH axis should follow inside
the screener; where it departs from what the current data files can express, that is
called out and a migration is proposed.

---

## 1. The problem this solves

pH plays **three different roles** in this project, and the current schema collapses them
into one column.

| Role | Example | What the model does with it |
|---|---|---|
| **Condition input** | "activity was assayed at pH 7.0" | a feature, alongside temperature |
| **Prediction target** | "the optimum pH is 8.0" | a regression target |
| **Outcome context** | "82% of activity retained at pH 8" | the *label* is 82%, and pH is the input |

In `temp_pH_dataset_ML_homology.csv` all three end up in the same place. For every
pH-typed row, `measured_value` **is** the pH:

```
measurement_type = "pH optimum",  pH = 4.5,  measured_value = 4.5
measurement_type = "pH stability", pH = 12.0, measured_value = 12.0
```

That is coherent for role 2 and lossy for roles 1 and 3. Two consequences:

- **A stability row cannot say which way the effect went.** `pH stability = 12.0` is read
  identically whether the enzyme was rock-solid at pH 12 or destroyed by it. Both occur
  in the literature; in our own candidate pool both occurred *in the same article*.
- **The outcome at a pH has nowhere to live.** "retains over 90% activity at pH 10" and
  "less than 15% residual at pH 9" carry the actual signal, and the schema keeps only the
  10 and the 9.

The pH benchmark recovers that information for 29 of 68 rows and records direction on 53.
The representation below is what lets the screener use it.

---

## 2. The representation

### 2.1 Three fields, three roles

| Field | Role | Type | Present when |
|---|---|---|---|
| `pH` | condition input | float, 0–14 | the assay pH is stated |
| `ph_target` | prediction target | float, 0–14 | `measurement_type` is a pH-optimum type |
| `activity_at_pH` | outcome | float, % of maximal/initial | an outcome is reported at that pH |

A row populates `pH` and at most one of the other two. This is the whole of the change:
splitting one overloaded column into the three questions it was being asked to answer.

### 2.2 Four measurement types, and what each means

| Type | `ph_target` | `activity_at_pH` | Screener task |
|---|---|---|---|
| `pH optimum` | the optimum | — | regress pH optimum from sequence |
| `pH activity` | — | % of maximal activity | regress activity given (sequence, pH) |
| `pH stability` | — | % of initial activity after incubation | regress retention given (sequence, pH, time) |
| `pH activity range` / `pH stability range` | — | bound on % over an interval | evaluation only; never a training target |

### 2.3 Direction is mandatory on stability rows

`direction ∈ {optimum, stabilising, destabilising}`. A `pH stability` row without a
direction is malformed and the validation suite rejects it. Where the article gives a
number, `activity_at_pH` makes direction redundant; where it does not
(*"almost lost all of its activity at pH 3.0"*), direction carries the whole signal.

### 2.4 Qualifiers are preserved, never rounded away

`relative_activity_qualifier ∈ {exact, approx, gte, lte, range}`. *"over 90%"* is stored
as `90 / gte`, not as `90`. A model trained on bare numbers treats "at least 80%" as
"exactly 80%", which biases every bound in the dataset toward its own threshold.

### 2.5 Intervals are never collapsed to midpoints

An interval is stored as two endpoint rows sharing a `ph_range_group`, with
`pH_is_range = yes` and both bounds on each row. No midpoint is synthesised — "optimal
between pH 4.0 and 6.0" must never become 5.0, because 5.0 is a number no one measured.
Interval rows are excluded from point-value scoring and are available for interval
metrics (does the predicted optimum fall inside the reported active range?).

---

## 3. Using pH as a model input

**Encoding.** Feed pH as a raw float. It is already a log-scale quantity; transforming it
again is double-counting. Do not standardise it against the training distribution — the
benchmark deliberately covers pH 3.0–12.0 while training data clusters at 7.0–7.5, and
z-scoring against the training mean makes the tails look like outliers rather than the
test cases they are.

**Missingness.** 32,955 rows in the training table have a temperature but no pH. Use an
explicit `has_pH` flag plus a sentinel, not mean imputation: imputing pH 7.4 into a row
that never reported one manufactures a condition, which is exactly what the parent
benchmark's integrity statement forbids upstream.

**Interaction with temperature.** pH and temperature are not separable for
polyester hydrolases — alkaline pH accelerates the background chemical hydrolysis of PET
while simultaneously destabilising many cutinases, so the joint optimum is not the
product of the marginal optima. If the screener uses a linear head, add an explicit
`pH × temperature` term. The 22 benchmark rows carrying both axes exist to test this.

---

## 4. Defining the class label for pH

Luke's handoff deliberately leaves the classification threshold to the modeller. For the
pH axis, the natural definition — and the one this benchmark is built to score — is:

> **A protein is `pH-robust` at pH *p* if it retains ≥ 50% of its maximal or initial
> activity at pH *p*.**

Why 50%: it is the threshold the source literature already uses. Papers in this corpus
report "more than 50% relative activity between pH 7.5 and 8.5" and "retained more than
50% of their activity over a pH range from 7.0 to 9.0" as their own summary statistic, so
scoring at 50% compares like with like instead of imposing an external cutoff.

Applying it to the benchmark gives 29 directly labelled rows, plus 27 more labelled by
`direction` where the article is qualitative. Rows with qualifier `gte`/`lte` label
cleanly when the bound falls on one side of 50 and are **excluded when the bound sits
exactly on it** — `lte 50` and `gte 50` are both uninformative about "≥ 50%". Three rows
are dropped by that rule, leaving **53 labelled rows**.

Whatever threshold is finally chosen, it must match the one the existing temperature-only
screener uses, or the before/after comparison is not apples to apples.

---

## 5. Migration from the current schema

The benchmark ships in both shapes, so nothing has to change at once.

| File | Shape | Use |
|---|---|---|
| `data/ph_benchmark_luke_format.csv` | exactly the current 24 columns | drops into the existing pipeline today |
| `data/ph_benchmark_luke_format_extended.csv` | those 24 + `ext_*` | same rows, with the recovered fields alongside |
| `data/ph_benchmark_v1.csv` | native schema | the representation above, in full |

**Proposed change to the shared schema** — four columns, all nullable, none breaking:

```
activity_at_pH              float    % of maximal or initial activity at `pH`
activity_qualifier          enum     exact | approx | gte | lte | range
direction                   enum     optimum | stabilising | destabilising
ph_range_group              string   links the endpoint rows of one interval
```

Existing rows take `NULL` in all four and behave exactly as they do now. The 173
`pH activity range` rows and 165 `pH stability` rows already in the training table would
benefit from the same backfill, but that is a separate piece of work and is not assumed
here.

### Known mapping compromises

Converting into the current 24 columns loses information by definition. Three places
where the mapping had to make a choice, all recorded in
`data/ph_luke_format_mapping.json`:

1. `pH activity` rows map to `measurement_type = "pH property"`, the nearest existing
   term. There is no point-activity type in the vocabulary. **Flagged for Luke to
   overrule** — adding `pH activity` would be cleaner than overloading `pH property`.
2. `split_homology = "test_external"`, a new value. Reusing `"test"` would silently merge
   this benchmark into the held-out split; `"train"` would be false. Filters written as
   `!= "train"` keep working.
3. `condition_quality = "Low"` extends the existing High / Medium-High / Medium scale
   rather than promoting weakly evidenced rows to `Medium`.

---

## 6. The handover rule stands

This benchmark is for the **final external test only** — not training, not tuning, not
feature selection, not threshold selection. That is the rule in Luke's
`DATA_READINESS_HANDOFF.md` and it applies unchanged to the pH subset. Zero benchmark
proteins are in the training split, and after the deep re-read removed a misattributed
sequence, none sits in his held-out test split either.
