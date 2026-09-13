# Computational biology version

**Target venues:** ISMB/ECCB (poster track), RECOMB, PSB, ML for Structural Biology
**Target length:** 250 words · **Actual: 250**
**Emphasis:** benchmark quality as an evaluation problem; covariate shift; the audit as a
reproducible protocol

---

**Two quality metrics, not one: auditing a literature-extracted pH benchmark for
plastic-degrading enzyme screeners**

A. Goel, L. ——, A. ——, S. —— · Predictive Enzyme Technology Laboratory

---

Screeners for plastic-degrading enzymes are trained on literature-mined condition data
and evaluated on held-out splits of the same corpora. Both inherit one unexamined
assumption: that a value verified to appear in its source article is correctly recorded.

We tested that assumption while finalising an independent, test-only pH benchmark of 67
measurements from 30 open-access articles, spanning pH 3.0–12.0 and sharing no protein
with the training split. All 105 candidates had already passed automated source
verification — each located verbatim in a freshly downloaded copy of its article.
Re-reading each against that sentence removed 38 (36%) under twelve explicit rules,
recorded per row.

The failures were systematic, not stochastic. Thirteen rows took their value from a
methods sentence rather than a result; five reported an activity-interval endpoint as the
optimum while the same sentence stated the true optimum, giving errors of 0.5–2.0 pH
units in the prediction target; six attached the wrong enzyme to a real measurement; one
carried a response-surface prediction. Each is a correct quotation in the wrong field,
invisible to string-level verification.

Curation also recovered activity retained at each pH (29 rows) and the direction of the
effect (52) — quantities the standard schema cannot represent, without which a stability
record is sign-ambiguous. Benchmark pH differs sharply from training data (median 8.0
versus a training mode of 7.0–7.5), so pH should not be standardised against training
statistics.

We propose reporting extraction datasets under two metrics: value located, and
value correctly attributed. Data, audit trail and code are released.
