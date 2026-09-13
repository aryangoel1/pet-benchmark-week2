# Limitations

Stated plainly, so nobody has to discover them downstream. Ordered roughly by how much
they should change what you do with the dataset.

---

## 1. It is small, and the sequence-scoreable part is very small

67 measurements. Ten of them can be scored by a sequence model — 6 distinct proteins,
one of which contributes 7 of the 16 sequence-carrying rows.

**What this means in practice:** this is not a dataset for measuring a model's pH
accuracy to two decimal places. It is a dataset for catching a model that is badly wrong,
and for testing behaviour at pH values the training data barely covers. Report it as a
sanity check with confidence intervals, not as a leaderboard number. A single
misprediction moves a 10-row metric by 10 points.

The parent benchmark's sequence-resolution rule is the reason: an accession is accepted
only when an article names exactly one hydrolase record, because accepting ambiguous ones
is how a benchmark silently acquires wrong labels. That precision costs coverage, and the
cost lands here.

## 2. The audit read evidence sentences, not whole articles

Every one of the 105 candidates was read against the sentence the parent pipeline stored
with it, and that sentence had already been located in a freshly downloaded copy of the
article. So the quote is reliable *as text*.

What this pass adds is a judgement about whether the number was the right reading of that
text. What it cannot do is catch a defect that is only visible outside the quoted
sentence — an enzyme renamed three paragraphs earlier, a figure that contradicts the
prose, a correction notice on the article. Claims in this repository are worded as
"read against its recorded evidence", and that is the correct strength. It should not be
described as expert re-reading of 30 papers.

## 3. Curation is one person's judgement, unreviewed

The 105 verdicts in `scripts/ph_curation.py` were made by a single pass and have not yet
been independently reviewed. Several are genuine judgement calls, not mechanical
applications of a rule, and a second reader could reasonably disagree. The ones most
worth arguing about:

- **Feruloyl and acetyl xylan esterases are in scope** (14 rows) on the grounds that they
  are carboxylester hydrolases and that PET46 — in this benchmark — is a feruloyl esterase
  that degrades PET. A stricter reading would exclude them and take the benchmark to 53
  rows.
- **`multiple_enzymes_same_value` rows are kept** (7 rows) where a sentence gives one
  value for two or more enzymes. They are flagged and excluded from sequence-model
  scoring, but a stricter reading would drop them outright.
- **Five pH optima were corrected rather than excluded.** Each correction is supported by
  the same sentence that carried the error, but "correct it" and "drop it" are both
  defensible policies and the choice changes five target values.
- **One row (`PH4AD21534`, KoFAE pH 6.0–10.0) is kept despite being contradicted** by another
  row from the same article. It is flagged `internal_conflict` and unscored.

Every verdict carries its reason, so disagreeing is a matter of editing one line and
re-running the build.

## 4. Confidence is low on most rows

56 of 67 rows carry `confidence = Low`, inherited from the parent pipeline. That grade
reflects how the value was extracted (prose pattern-matching), not whether the audit
found it sound — the audit is the reason to trust these rows, and it is recorded
separately in `audit_rules` and `audit_note`. Do not filter on `confidence` expecting it
to mean "post-audit quality"; it does not.

## 5. Coverage is uneven and thin at the edges

- **Alkaline-skewed.** Median pH optimum 8.0; one measurement below pH 4.
- **Joint coverage is sparse.** Only 22 rows carry both pH and temperature, and none sits
  in the alkaline-and-hot regime where industrial PET depolymerisation runs.
- **Ten articles contribute exactly one row.** The three largest contribute 17 of the 67.
  Per-article effects are not separable from per-enzyme effects at this size.
- **Buffers are almost entirely missing.** After clearing four unsupported buffer
  attributions, one row names its buffer. Buffer identity affects measured optima, and
  this dataset cannot control for it.
- **Assay methods are recorded on 21 of 67 rows.** Optima measured on different substrates
  are not strictly comparable, and mostly we do not know which substrate was used.

## 6. Bounded by open access

Only open-access Europe PMC articles were mined. Paywalled characterisation papers — a
large share of the classical enzymology literature — are not represented, and there is no
reason to think the open-access subset is unbiased with respect to pH optima.

## 7. Known unrecovered data

The audit found values in evidence sentences that are real but not currently extracted as
rows — for example a pH-stability range of 4.5–10.0 with >95% retention for Tan410, and a
second optimum (pH 8.0 on PET film) for SbPETase alongside the pH 7.0 on BHET that is
shipped. These were left out because this was a finalisation pass over existing rows, not
a re-extraction. Adding them is straightforward and would improve coverage; it would also
mean re-opening the articles, which returns to limitation 2.

## 8. `cluster_id` is empty in the Luke-format export

Homology-aware cluster assignment needs MMseqs2 run over the full protein set, which is
Luke's pipeline. `data/ph_benchmark.fasta` is ready for it. Until that is run, these rows
cannot be placed in his cluster-disjoint split — though the train-overlap check that
matters has been run and is clean.

## 9. What is *not* a limitation

Worth stating, because these are the questions that get asked:

- **Training contamination.** Zero benchmark proteins appear in `split_homology == "train"`.
  Re-run `scripts/check_overlap_luke.py` to confirm independently.
- **Synthetic or predicted values.** None. One candidate carrying a response-surface
  prediction was found and removed, and the validation suite now scans every shipped
  evidence sentence for prediction language.
- **Interpolated values.** None. No midpoint of a reported range is ever stored.
- **Provenance gaps.** Every row carries its PMCID, DOI and the verbatim sentence.
