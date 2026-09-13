# Joint pH abstract — master version and adaptation plan

One piece of work, three audiences. This file holds the canonical abstract and explains
what changes for each venue; the three submission-ready versions are alongside it.

> **Author line — needs confirming before any submission.**
> `A. Goel, L. ——, A. ——, S. —— · Predictive Enzyme Technology Laboratory (PET Lab)`
> Surnames and the final order are not recorded anywhere in this repository. Given the
> work split — benchmark construction and curation here, the training dataset and
> homology-aware split by Luke — a joint first-author note may be appropriate. That is a
> conversation, not a default.

---

## The canonical abstract (≈300 words)

**A curated pH benchmark for plastic-degrading enzymes, and what auditing it revealed
about literature-extracted data**

Machine-learning screeners for plastic-degrading enzymes are increasingly asked to
predict performance under specified reaction conditions, but the external benchmarks
needed to test them are scarce, and the literature-mined datasets that fill the gap are
rarely audited beyond confirming that a reported number appears somewhere in the source
article.

We present an independent, test-only pH benchmark of 67 experimentally measured values
from 30 open-access articles, spanning pH 3.0–12.0 and 19 enzyme classes, and screened to
contain no protein present in the screener's training split. Every candidate row was read
against the source sentence it was extracted from. Of 105 candidates, 38 (36%) were
removed under twelve explicit, published rules, each recorded per row with its reason.

The removed rows were not random noise. They were systematic and directional. Thirteen
took their value from a methods or protocol sentence rather than a result — an assay
buffer read as a pH optimum, an incubation temperature read as thermostability, in one
case a substrate loading parsed as relative activity. Five reported the low endpoint of
an activity interval as the optimum while the same sentence gave the true optimum,
errors of 0.5–2.0 pH units in exactly the quantity a screener predicts. Seven restated
another study's result, six attached the wrong enzyme to a real measurement, and one
recorded a response-surface prediction in a dataset whose stated policy excludes
predicted values. Every one of these defects is a correct quotation placed in the wrong
field, and every one survives an automated check that asks only whether the number is
present in the article.

A second pass re-read every shipped row against the freshly downloaded full article, and
found a defect class the sentence-level audit could not see: three of six sequence
attributions were accessions the articles *cite* rather than *deposit* — a structural
modelling template, a phylogenetic-tree neighbour, and a comparison enzyme standing in for
the article's own. A wrong sequence on a correct measurement passes every automated check
and fails silently only at evaluation.

Curation also recovered a quantity the standard schema discards: the activity retained
**at** each pH, present for 29 rows, plus the direction of the effect for 52. Without it,
a stability record at pH 10 cannot distinguish an enzyme that tolerates alkali from one
destroyed by it.

We argue that "value located in source" and "value correctly attributed" should be
reported as two separate quality metrics for any extracted dataset.

---

## What changes per venue

| | Computational biology | Enzyme engineering | Environmental biotechnology |
|---|---|---|---|
| **File** | `abstract_comp_bio.md` | `abstract_enzyme_engineering.md` | `abstract_env_biotech.md` |
| **Target length** | 250 words | 200 words | 350 words |
| **Lead with** | the benchmark-quality problem and evaluation methodology | the enzymology: what the pH data actually says | plastic waste and real-world process conditions |
| **Emphasise** | covariate shift vs training data; audit as a reproducible protocol; the two-metric proposal | pH optima and stability profiles; the optimum-vs-range error and why it matters for engineering targets; retained-activity data | coverage across polymer classes (PET, PHA, PHB, PCL, PVC, PLA, nylon, plasticisers); the alkaline-and-hot gap vs industrial depolymerisation |
| **De-emphasise** | enzymology detail | schema and ML evaluation mechanics | per-rule audit breakdown |
| **Keep verbatim** | the 36% figure and the systematic-not-random finding — it is the paper's central claim and should read identically everywhere |
| **Sequence finding** | keep (it *is* the two-metric argument) | keep, framed as scaffold-identity risk | drop if space is tight |

---

## Candidate venues

| Track | Venues worth checking |
|---|---|
| Computational biology | ISMB/ECCB (posters), RECOMB, Machine Learning for Structural Biology workshop, PSB |
| Enzyme engineering | Enzyme Engineering Conference (ECI), BioTrans, Biocatalysis Gordon Research Conference |
| Environmental biotechnology | ISEB, EFB European Biotechnology Congress, Plastics Biodegradation / Bio-based Materials meetings, SETAC |

Deadlines and exact word limits were not verified — check each call for papers before
submitting, and re-cut to the stated limit rather than trusting the numbers above.

---

## Before submitting

1. Confirm the author list and order.
2. Confirm word limits against the actual call for papers.
3. Decide whether the benchmark is released publicly at submission; if so, add the
   repository URL and a DOI.
4. Have Luke check the claims about the shared schema — the abstract asserts that it
   cannot represent activity-at-pH, which is true of the current file but is his call to
   confirm.
5. If the screener's pH results are ready in time, add one sentence of model performance.
   The abstracts are written so that sentence can be dropped in without restructuring.
6. The three venue cuts predate the deep re-read and carry the headline numbers but not
   the sequence-attribution finding. Decide per venue whether to spend the words on it.
