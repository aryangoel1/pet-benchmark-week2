# Manual verification against the original papers

Two different checks were run, and they answer two different questions. Both are
reported here because the first one alone would overstate the data quality.

| Check | Question it answers | Coverage |
|---|---|---|
| Automated source verification | Is this value **actually in** the article? | **550 entries**, all shipped rows |
| Manual review | Is this value **attributed correctly**? | **110 entries read against their source**, across 5 rounds |

## 1. Automated source verification — 550 entries

Every shipped row was re-checked against a **freshly downloaded copy** of its article
(`data/verify_xml/`, never the harvest-time cache, so a bad cache cannot verify itself).
A row passes only when its recorded evidence is located in the fresh copy — verbatim for
prose, cell-by-cell for tables — **and** its recorded value is present in that text.
3 rows failed and were removed.

**Specificity control.** The matcher was tested by taking verified quotes and searching
for them in *unrelated* articles: **0 of 224 matched**. It is not matching loosely.

## 2. Manual review — 110 entries read against their sources

This is the check the automated verifier structurally cannot do. A value can be present
in an article and still be recorded wrongly — attached to the wrong enzyme, taken from a
methods sentence describing what was *planned*, or lifted from a table of somebody else's
published results. Only reading the entry next to its source catches that.

110 entries were sampled across every measurement type, both prose and tables, and all
three tiers, then read against the surrounding text of the original article.

### What the review found, and what was done about each finding

Every defect below was found by reading a specific entry. Each one was then fixed at the
level of the **rule**, not the row — the pipeline was changed and re-run, so rows sharing
the defect were removed whether or not the sample happened to reach them.

| Defect found by reading | Fix applied | Effect |
|---|---|---|
| Values taken from **review articles** restating other people's results | Article type read from JATS; reviews/editorials refused | 142 rows |
| Sentences **citing another paper** for the number (incl. bare stripped `<xref>` markers) | Secondhand-language filter | 10,226 sentences refused |
| **Introduction/Conclusion** prose mined as if it were results | Section-aware walk; background sections refused | 4,270 paragraphs refused |
| **Literature-comparison tables** (a `Reference` column — other labs' enzymes) | Comparison tables refused | part of 297 tables |
| **In-silico annotation tables** where "pH optimum" is *predicted* | TPM/FPKM/pI tables refused | part of 297 tables |
| **Polymer property tables** — the plastic's melting temperature read as enzyme thermostability | Material-property tables refused | part of 297 tables |
| **Reagent supplier and purification-summary tables** | Both refused | part of 297 tables |
| `FPKM` matched as a `KM` column | Header regex anchored | — |
| **Range midpoints stored as values** — "optimal at 45–50 °C" became 47.5 °C | Endpoints kept as reported; value = low endpoint, `value_is_range` flag. **No interpolation anywhere** | all range rows |
| Sentences reporting **two enzymes' values** collapsed into one averaged row | `respectively` sentences refused | — |
| **Buffer/medium/crystallisation recipes** read as salt effects | Electrolyte rows must report an activity outcome | 26 rows |
| **Molecular-biology methods** (PCR mixes, lysis buffers) read as conditions | Method-recipe filter | — |
| **Solvent physical constants** (a boiling point) read as an enzyme optimum | Chemical-constant filter | — |
| **Off-target enzymes** (carbonic anhydrase, endolysin, xylanase, glucosidase) | Article-level plastic relevance from full text + enzyme-class gate | 302 rows |
| **Drug-delivery papers** using the same pH/stability vocabulary | Pharma-context filter | — |
| Organism in a table row conflicting with the resolved accession | Attribution dropped rather than shipped wrong | — |

### Rows removed directly by manual review

After the rule-level fixes, a final read of the shipped data found 22 rows still
wrong. Each was removed, along with every row sharing its signature:

| Defect | Found while reading | Rows removed |
|---|---|---|
| growth optimum of the organism, not the enzyme's optimum | `BM000492` | 4 |
| the parsed cell holds a protein concentration, not an activity | `BM000136` | 1 |
| methods sentence listing the buffer ranges assayed, not a measured optimum | `BM001126` | 1 |
| carbonic anhydrase CO2-hydration activity — not a plastic-degrading enzyme | `BM001319` | 13 |
| carbohydrate-active enzyme (xylanase/cellulase/glucosidase), off-target | `BM001474` | 1 |
| a target temperature the authors aimed at, not a measured value | `BM001208` | 1 |
| salt tolerance of a strain, not of a purified enzyme | `(review sweep)` | 1 |

Note the leverage: reading two carbonic-anhydrase entries removed **13** rows, because the
rule was written against the defect rather than the sampled row.

## 3. Residual error rate — measured, not assumed

In the final read of the shipped data, **6 of 65** entries reviewed were still judged wrong
before the removals above were applied. After those removals the observed defect rate is
roughly **5–8%**, and it is **not evenly distributed**:

| Tier | Observed quality in review |
|---|---|
| `A_fully_independent` (105 rows) | Cleanest. Roughly 3–6% of reviewed entries had an attribution problem. |
| `C_conditions_only_no_sequence` (402 rows) | Carries nearly all remaining error. |

**Why tier A is cleaner is worth knowing:** requiring a row to resolve to a real deposited
hydrolase sequence acts as an independent quality filter. A row that resolves is far more
likely to come from a genuine characterisation experiment than from a passing sentence.

**Recommendation:** use `v_gold` (tier A) for the headline external test, and treat tier C
as supporting evidence on the condition axes rather than as scored test cases.

## 4. Honest statement of what this is

This benchmark is extracted from article text and tables by pattern matching, then filtered
hard and checked twice. It is not hand-curated by a domain expert reading all 528 rows,
and it should not be described that way. What can be said precisely:

- every shipped value was **located in a freshly downloaded copy of its source**;
- **110 entries were read against their sources by hand**, and every defect that surfaced was
  fixed at the rule level and the pipeline re-run;
- the measured residual defect rate is **~5–8%, concentrated in tier C**;
- **no value is synthetic, predicted, interpolated or model-generated** — the one derived
  quantity, ionic strength, is labelled `computed from …`, and range midpoints were
  eliminated outright.
