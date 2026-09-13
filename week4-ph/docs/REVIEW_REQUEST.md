# Review request — Luke and Ayush

The Week-4 pH benchmark is finished and self-consistent, but the part that most needs a
second pair of eyes is the part a script cannot check: **105 curation verdicts made by
one reviewer.** This is what I'd like each of you to look at, and roughly how long it
should take.

Everything is in `week4-ph/`. Start with `README.md`.

---

## Luke — three specific asks

### 1. Confirm the format conversion is actually usable (15 min)

`data/ph_benchmark_luke_format.csv` has a byte-identical header to
`temp_pH_dataset_ML_homology.csv`, so it should concatenate straight onto your table.
Three deliberate departures, and I'd rather you overrule any of them now than discover
them later:

| Departure | Why | If you disagree |
|---|---|---|
| `split_homology = "test_external"` — a value your data doesn't use | reusing `"test"` would silently merge this benchmark into your held-out split; `"train"` would be false. `!= "train"` filters still work | one line in `scripts/to_luke_format.py` |
| `condition_quality = "Low"` — extends your High / Medium-High / Medium scale | 57 of 68 rows are `Low` upstream; promoting them to `Medium` would overstate them | same file |
| `measurement_type = "pH property"` for point activity-vs-pH values | your vocabulary has no point-activity type, and `pH activity range` would be wrong | **this is the one I'd most like your call on** — adding `pH activity` to the vocabulary seems cleaner than overloading `pH property` |

### 1b. Note: three sequences were withdrawn after a deep re-read (5 min)

Since the first draft, all 31 articles were re-downloaded and every row re-checked in
context. Three of the six accessions turned out to be cited, not deposited — an AlphaFold
modelling template (`P26495`), a phylogenetic-tree neighbour from another strain
(`AAB51445.1`), and the IsPETase comparison enzyme standing in for the article's own
SbPETase (`WP_054022242.1`). Those rows keep their measurements and lose their sequences.

Two consequences for you: the FASTA is now **3 proteins, not 6**, and the benchmark no
longer overlaps your held-out test split at all — the single tier-B protein *was* the
misattributed IsPETase. Proof in `data/ph_deep_verification.json` and `SEQUENCE_REJECTIONS`
in `scripts/ph_curation.py`.

### 2. Run the cluster assignment (10 min, your pipeline)

`cluster_id` is empty because homology clustering needs MMseqs2 over your full protein
set. `data/ph_benchmark.fasta` has all 3 proteins with `protein_id` in the header.

The train-overlap check you asked for in `DATA_READINESS_HANDOFF.md` **has** been run, on
the pH subset specifically rather than inherited from the Week-2 build
(`scripts/check_overlap_luke.py`, result in `data/ph_overlap_luke.json`):

```
in Luke's TRAIN split        : 0
in Luke's held-out TEST split: 0
new to the project           : 3
```

### 3. Sanity-check the schema argument before it goes in a paper (20 min)

`docs/SCREENER_PH_REPRESENTATION.md` argues that the current shared schema cannot
represent the outcome **at** a pH — that for every pH-typed row `measured_value` is the pH
itself, so "82% retained at pH 8" and "8% retained at pH 8" are stored identically. The
abstracts and the Methods both lean on this.

I believe it is true of `temp_pH_dataset_ML_homology.csv` as shipped, but it is your
dataset and your design decision, and if there's a convention I've missed the claim needs
rewording before submission. The proposed fix is four nullable columns
(`activity_at_pH`, `activity_qualifier`, `direction`, `ph_range_group`) that leave every
existing row unchanged.

---

## Ayush — the audit itself

The most valuable review here is **disagreeing with specific calls.**
`docs/AUDIT_REPORT.md` lists all 105 candidates grouped by article, each with its verdict,
rule codes and the reasoning in prose. `scripts/ph_curation.py` is the same content as
editable source.

### Where I'd focus (45–60 min)

**a. The five corrected pH optima.** Each was reported as a range endpoint while the same
sentence gave the true optimum, and I corrected rather than dropped them:

| Row | Was | Now | The sentence says |
|---|---|---|---|
| `BMDFDCB2C50A` | 5.0 | **7.0** | "ranging from pH 5 to pH 9, with optimal activity observed at pH 7" |
| `BM168196487C` | 4.0 | **5.0** | "between pH 4.0 and 6.0, the highest being at pH 5.0" |
| `BM34567040FA` | 7.5 | **8.0** | "between pH 7.5 and 8.5, with its highest activity at pH 8.0" |
| `BMD363C6A8E6` | 7.0 | **8.0** | "determined to be 8.0, with … activity maintained between pH 7.0 and 9.0" |
| `BM6E5147B1F9` | 7.0 | **7.5** | "reaching its optimal activity at approximately pH 7.5" |

"Correct it" and "drop it" are both defensible. If you think dropping is safer, that is a
one-line change each and takes the benchmark to 63 rows.

**b. `BM6E5147B1F9` specifically.** This one also changes the enzyme. It was recorded as
`Est1` with range 7.0–8.5, but 7.0–8.5 belongs to **Ces1-ET** in that sentence; Est1-ET's
own range is 7.0–9.0 with a maximum at pH 9.0. I re-attributed it to Ces1-ET. Worth a
second read of the quote — it's the most intricate call in the set.

**c. Scope: are feruloyl and acetyl xylan esterases in or out?** 14 rows. I kept them
because they are carboxylester hydrolases and because PET46 — in this benchmark — is an
archaeal feruloyl esterase that degrades PET. A stricter reading drops them and the
benchmark becomes 54 rows. This single decision moves the headline number more than any
other.

**d. The seven `multiple_enzymes_same_value` rows**, where a sentence gives one value for
two or more enzymes ("LIP3 and PhaZ … optimal activity at pH 8"). Kept, flagged, excluded
from sequence-model scoring. Drop them instead?

**e. The three withdrawn sequence attributions.** `SEQUENCE_REJECTIONS` in
`scripts/ph_curation.py` quotes the sentence justifying each. If you read any of them as a
genuine deposit rather than a citation, that row's sequence should come back.

**f. Spot-check the exclusions.** `data/ph_excluded_v1.csv` has all 38 with their evidence
quotes. If any look like they should have survived, say which.

---

## Both of you — the one thing I'd most like challenged

The claim the paper rests on is that **the defects were systematic and directional, not
random noise** — protocol sentences read as results (13 rows), range endpoints read as
optima (5), wrong enzyme attached (6), secondhand sentences (7). If that pattern doesn't
hold up under your reading, the Discussion needs rewriting, and I'd rather know now.

On scope of verification, the accurate phrasing is: the audit read the evidence sentence
for **all 105 candidates**, and the deep pass re-checked **all 67 shipped rows** against
the freshly downloaded full article. It is not an independent domain expert re-deriving
each value from the underlying figures, and it did not re-open the 37 exclusions at the
deeper level. If you see that overstated anywhere in the docs, flag it — I would rather
under-claim than have a reviewer find the gap.

---

## What's not blocked on you

The dataset, code, validation, figure and Methods are complete and pass all checks. The
abstracts are drafted at three lengths. The two things genuinely blocked are the author
list (I don't have surnames or a preferred order) and the conference deadlines, which I
haven't verified against the actual calls for papers.

---

## Quick reference

```bash
cd week4-ph
python3 scripts/validate_ph.py        # 22 checks, 0 hard failures
python3 scripts/check_overlap_luke.py # 0 proteins in the training split
python3 scripts/deep_verify_ph.py     # re-download all 31 articles, 0 findings
python3 scripts/check_docs.py         # prose numbers match the data
```

| If you want… | Open |
|---|---|
| the numbers | `docs/DATASET_SUMMARY.md` |
| every verdict | `docs/AUDIT_REPORT.md` |
| the Methods text | `docs/METHODS.md` |
| the schema proposal | `docs/SCREENER_PH_REPRESENTATION.md` |
| what I don't trust | `docs/LIMITATIONS.md` |
