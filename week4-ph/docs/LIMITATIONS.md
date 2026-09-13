# Limitations

Stated plainly, so nobody has to discover them downstream. Ordered roughly by how much
they should change what you do with the dataset.

---

## 1. It is small, and the sequence-scoreable part is very small

68 measurements. **Seven** of them can be scored by a sequence model — 3 distinct
proteins, one of which contributes 7 of the 9 sequence-carrying rows.

This got smaller, not larger, after the deep re-read: three of the six accessions the
dataset originally carried turned out to be citations rather than deposits (§2), and
their rows now ship without a sequence.

**What this means in practice:** this is not a dataset for measuring a model's pH
accuracy to two decimal places. It is a dataset for catching a model that is badly wrong,
and for testing behaviour at pH values the training data barely covers. Report it as a
sanity check with confidence intervals, not as a leaderboard number. A single
misprediction moves a 10-row metric by 10 points.

The parent benchmark's sequence-resolution rule is the reason: an accession is accepted
only when an article names exactly one hydrolase record, because accepting ambiguous ones
is how a benchmark silently acquires wrong labels. That precision costs coverage, and the
cost lands here.

## 2. What the two verification passes do and do not cover

**Pass 1 — evidence-sentence audit.** All 105 candidates were read against the sentence
the parent pipeline stored with them. That produced the 37 exclusions and the corrections.

**Pass 2 — deep re-read against full text.** All 31 shipped articles were re-downloaded
from Europe PMC and every shipped row re-checked in the surrounding article context
(`scripts/deep_verify_ph.py`). This found what pass 1 structurally could not:

- **Three of six sequence attributions were wrong** — accessions the articles *cite*
  rather than *deposit*. `P26495` was an AlphaFold modelling template, `AAB51445.1` a
  phylogenetic-tree neighbour from a different strain, `WP_054022242.1` the IsPETase
  comparison enzyme rather than the article's own SbPETase. Each was invisible from the
  evidence sentence, which does not mention the accession at all. All three are recorded
  in `SEQUENCE_REJECTIONS` with the quoted proof.
- **One enzyme name was wrong** — rows from PMC11651597 had been named for the *strain*
  (IBRL-CHS2) rather than the enzyme. The article calls it MLipA.
- **One measurement type was wrong** — a PanLipΔN value read as post-incubation stability
  is a point on the activity-vs-pH profile, which only the full paragraph shows.
- **One publication year was wrong** (PMC12767561: 2026 → 2025).

What pass 2 still does not do is read the figures. Several rows rest on prose that
summarises a figure (*"Fig 5A illustrates that..."*), and if the prose misdescribes its
own figure, nothing here would catch it. Nor does it check for post-publication
corrections or retractions beyond the JATS `article-type`, which is `research-article`
for all 30.

Accurate phrasing for the manuscript: every shipped row was checked against its source
article in context. It was not an independent domain expert re-deriving each value from
the underlying figures.

**Pass 3 — deep re-read of the exclusions.** Every removed candidate was re-checked
against full text as well (`scripts/deep_verify_exclusions.py`), using the articles' own
JATS section structure. Outcome:

- **One removal was wrong and has been reversed.** `BM85EC0EEFF2` was dropped because the
  sentence *"The optimal activity was at pH 7.5"* names no enzyme. The full paragraph
  names one throughout — *"Since PD3 possesses the best long-term stability, further
  characterization of PD3's esterase activity was performed…"* — so the row is back, as
  PD3, pH optimum 7.5.
- **Ten of the thirteen `PH-X1` removals sit objectively inside a Materials and Methods
  section**, confirmed from the article's own markup.
- **The three articles removed as reviews are `article-type="review-article"`** in their
  own metadata.
- Every other removal held.

One wording consequence: `PH-X1` is about what a sentence *is*, not where it sits. Three
of its rows are in Results sections — a figure caption defining a normalisation baseline,
and a parenthetical *"(assayed at pH 5.0)"* — and are protocol statements regardless.

## 3. Curation is one person's judgement, unreviewed

The 105 verdicts in `scripts/ph_curation.py`, and the three sequence rejections added by
the deep re-read, were made by a single reviewer and have not yet been independently
reviewed. Several are genuine judgement calls, not mechanical
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

57 of 68 rows carry `confidence = Low`, inherited from the parent pipeline. That grade
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
- **One sequence is the precursor, not the assayed form.** `AOT80658.1` is the
  full-length LipA (204 aa); the article characterises **MLipA**, the mature enzyme after
  removal of a 30-residue signal peptide (cleavage between Ala-30 and Ala-31). Seven of
  the nine sequence-carrying rows are affected. For a sequence model this is a real
  discrepancy, and it is flagged rather than silently corrected because trimming the
  sequence ourselves would fabricate a record no database holds.
- **Buffers are almost entirely missing.** After clearing four unsupported buffer
  attributions, one row names its buffer. Buffer identity affects measured optima, and
  this dataset cannot control for it.
- **Assay methods are recorded on 21 of 68 rows.** Optima measured on different substrates
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
a re-extraction. All 30 articles are now cached locally under `data/fulltext_xml/`, so
re-extraction is a tractable next step rather than a new download exercise.

## 8. `cluster_id` is empty in the Luke-format export

Homology-aware cluster assignment needs MMseqs2 run over the full protein set, which is
Luke's pipeline. `data/ph_benchmark.fasta` is ready for it. Until that is run, these rows
cannot be placed in his cluster-disjoint split — though the train-overlap check that
matters has been run and is clean.

## 9. What is *not* a limitation

Worth stating, because these are the questions that get asked:

- **Training contamination.** Zero benchmark proteins appear in `split_homology == "train"`.
  After the deep re-read removed the misattributed IsPETase sequence, zero appear in the
  held-out **test** split either. Re-run `scripts/check_overlap_luke.py` to confirm.
- **Review articles.** None. All 31 shipped articles carry JATS
  `article-type="research-article"`, checked against freshly downloaded full text.
- **Wrong sequences.** The three that were present have been removed. The three that
  remain (`AOT80658.1`, `QIT07223.1`, `RLI42440.1`) were each confirmed against an
  explicit deposit statement in the article's own text.
- **Synthetic or predicted values.** None. One candidate carrying a response-surface
  prediction was found and removed, and the validation suite now scans every shipped
  evidence sentence for prediction language.
- **Interpolated values.** None. No midpoint of a reported range is ever stored.
- **Provenance gaps.** Every row carries its PMCID, DOI and the verbatim sentence.
