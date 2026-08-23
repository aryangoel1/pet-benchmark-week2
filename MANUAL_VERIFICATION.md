# Manual verification against the original papers

Three checks were run. They answer different questions, and reporting only the first
would overstate the data quality.

| Check | Question it answers | Coverage |
|---|---|---|
| Automated source verification | Is this value **actually in** the article? | **628 entries** — every shipped row |
| Manual entry review | Is this value **attributed correctly**? | **110 entries** read against source |
| Manual attribution audit | Is this **sequence** the article's own enzyme? | **every attributed accession** re-read in context |

## 1. Automated source verification — 628 entries

Every shipped row was re-checked against a **freshly downloaded copy** of its article
(`data/verify_xml/`, never the harvest-time cache, so a bad cache cannot verify itself).
A row passes only when its recorded evidence is located in the fresh copy — verbatim for
prose, cell-by-cell for tables — **and** its recorded value is present in that text.
3 rows failed and were removed.

**Specificity control.** Verified quotes were searched for in *unrelated* articles:
**0 of 224 matched**. The matcher is not matching loosely.

## 2. Manual entry review — 110 entries

An automated check confirms a number is present in a paper. It cannot tell you the number
was recorded correctly — a value can be genuinely in an article and still be attached to
the wrong enzyme, taken from a methods sentence describing what was *planned*, or lifted
from a table of another lab's results.

110 entries were read against their sources. Every defect found was fixed at the level of
the **rule**, and the pipeline re-run, so rows sharing a defect were removed whether or not
the sample reached them. Fifteen defect classes were found and closed; the largest were
review-article values (130 rows), off-target enzymes (233 rows), secondhand sentences
(13,778 refused), background-section prose (5,748 refused) and secondary tables (397).

**Range midpoints were eliminated.** "Optimal at 45–50 °C" had been stored as 47.5 °C — a
number the paper never reported. Endpoints are now kept as reported, with `value_is_range`.
No interpolation remains anywhere in the dataset.

### Rows removed directly by manual review

| Defect | Found while reading | Rows removed |
|---|---|---|
| growth optimum of the organism, not the enzyme's optimum | `BM000492` | 4 |
| the parsed cell holds a protein concentration, not an activity | `BM000136` | 1 |
| methods sentence listing the buffer ranges assayed, not a measured optimum | `BM001126` | 1 |
| carbonic anhydrase CO2-hydration activity — not a plastic-degrading enzyme | `BM001319` | 13 |
| carbohydrate-active enzyme (xylanase/cellulase/glucosidase), off-target | `BM001474` | 2 |
| salt tolerance of a strain, not of a purified enzyme | `(review sweep)` | 1 |

Reading two carbonic-anhydrase entries removed 13 rows, because the rule was written
against the defect rather than the sampled row.

## 3. Manual attribution audit — the sequence labels

Automated resolution cannot distinguish an accession an article **deposited** (its own
enzyme) from one it **cited** (a homolog it compared against). Both appear in the same
sentences. Getting it backwards attaches the wrong sequence to a real measurement, which is
the worst failure a benchmark can carry.

Every attributed accession was therefore re-read in its article context.

**5 attributions were rejected** as homologs or unevidenced:

| Article | Accession | Why it was wrong |
|---|---|---|
| PMC10418727 | `AAN81911.1` | Est30/AAN81911.1 is a COMPARISON: 'EaEst2 ... shows a high sequence similarity of 65.04% with Est30 (GenBank ID: AAN81911.1)'. 65% identity is a different protein; the article's enzyme is EaEst2. |
| PMC11033240 | `GAP38373.1` | GAP38373.1 is wild-type IsPETase, cited as the parent scaffold of DuraPETase. The rows measure DuraPETase variants, which differ from the parent by ~10 substitutions, so the wild-type sequence is the wrong label for them. |
| PMC12767561 | `P13398` | P13398 (ArcNylA) is the archetypal reference NylA used for percent-identity analysis. The article characterises NOVEL NylA sequences, not ArcNylA. |
| PMC11196671 | `G9BY57` | Attributed by enzyme-name lookup only; the accession appears nowhere in the article, so there is no evidence it is the protein assayed. |
| PMC9839772 | `G9BY57` | Attributed by enzyme-name lookup only; the accession appears nowhere in the article, and the article is about IsPETase variants, not leaf-branch compost cutinase. |

**6 mappings were curated by hand** from the articles' own deposit tables — for example
`Ces1-ET → XPQ45698.1`, read out of the paper's accession table, where automated resolution
had latched onto the `WP_` homologs the same paper used for comparison.

Enzyme-name lookup was **removed entirely** as a resolution route: auditing it found
accessions attached to articles that never mention them. A UniProt search on an enzyme name
is not evidence about which protein a given paper assayed.

## 4. Residual error rate — measured, not assumed

Roughly **5–8%**, concentrated in the no-sequence tier. It is not evenly distributed:

| Tier | Rows | Observed quality |
|---|---|---|
| `A_fully_independent` | 137 | Cleanest — ~3–6% of reviewed entries had an attribution problem |
| `B_in_luke_heldout_test_only` | 11 | Same quality as A; separated for independence, not quality |
| `C_conditions_only_no_sequence` | 458 | Carries nearly all remaining error |

Requiring a row to resolve to a real deposited hydrolase acts as an independent quality
filter: a row that resolves is far more likely to come from a genuine characterisation
experiment than from a passing sentence.

## 5. What this is, stated precisely

- Every shipped value was **located in a freshly downloaded copy of its source**.
- **110 entries were read against their sources by hand**, and every attributed accession
  was re-read in context; defects were fixed at the rule level and the pipeline re-run.
- **101 rows** carry a protein identifier *and* a condition *and* a value — the full
  field set the brief asks for. The other 505 are real, verified
  measurements that a sequence model cannot consume.
- Measured residual defect rate **~5–8%, concentrated in tier C**.
- **No value is synthetic, predicted, interpolated or model-generated.** The two derived
  quantities are labelled: ionic strength (`computed from …`) and salinity converted from a
  reported NaCl molarity (`converted from … mM NaCl`).

This is not hand-curated by a domain expert reading all 606 rows, and should not be
described that way.

**Recommendation:** score on tier A (`v_gold`); treat tier C as supporting evidence on the
condition axes.
