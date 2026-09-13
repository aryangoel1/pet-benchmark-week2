# Planned pH figure

The figure is already rendered from the shipped data — `figures/figure_ph.svg`, produced
by `scripts/make_figure.py`. This document is the plan behind it: what each panel is for,
why it is in the paper, and what has to change before submission.

---

## Figure N. The pH benchmark and what curating it removed

**Four panels, one page-width figure.**

```
┌──────────────────────────────┬────────────────────────────┐
│ A  reported pH optima        │ B  activity retained at pH │
│    histogram, by enzyme class│    scatter, direction-coded│
├──────────────────────────────┼────────────────────────────┤
│ C  pH x temperature coverage │ D  audit funnel by rule    │
│    scatter, by enzyme class  │    horizontal bars         │
└──────────────────────────────┴────────────────────────────┘
```

### Panel A — Reported pH optima (n = 25)

Stacked histogram, 0.5-unit bins from pH 3 to 9.5, coloured by enzyme class.

*Why it is in the paper.* It is the distribution the screener is asked to predict, and it
is visibly skewed alkaline (median 8.0). That skew is chemically real — polyester
hydrolysis is base-favoured — but it also means the benchmark tests acid-tolerant enzymes
thinly, and a reviewer should be able to see that rather than read it in a limitation.
The single acidophilic lipase at pH 3.5 is the whole of the low tail, and it should look
as lonely as it is.

### Panel B — Activity retained at pH (n = 29)

Scatter of `relative_activity_pct` against assay pH. Upward triangles where activity was
retained, downward where it was lost, with a dashed line at 50%.

*Why it is in the paper.* **This is the panel that cannot be drawn from the current shared
schema.** `temp_pH_dataset_ML_homology.csv` stores the pH as the measured value for every
pH-typed row and has no field for the outcome at that pH, so a plot of "how much activity
survived" simply has no data to draw. It exists here only because the audit recovered the
outcome from the source sentence for 29 rows. Showing it makes the schema argument in
`SCREENER_PH_REPRESENTATION.md` concrete instead of theoretical, and the 50% line is the
class threshold the paper proposes.

### Panel C — Joint pH × temperature coverage (n = 22)

Scatter of assay temperature against pH, coloured by enzyme class, jittered where points
collide.

*Why it is in the paper.* The screener predicts under both conditions at once, and the
honest statement is that only 22 rows constrain the joint surface. The panel shows the
sparsity plainly and shows where it sits: clustered at pH 7–8.5 and 30–60 °C, with almost
nothing at the alkaline-and-hot corner where industrial PET depolymerisation actually
runs. That gap is a finding, not a flaw to be hidden.

### Panel D — What the audit removed, and why (n = 37 across 12 rules)

Horizontal bars, one per exclusion rule, ordered by count, with the funnel stated above
and below: 105 candidates → 37 removed → 68 shipped, of which 46 are scoreable on the pH
axis and 7 by a sequence model.

*Why it is in the paper.* A curation claim is only worth as much as its auditability. The
panel converts "we cleaned the data" into a per-rule count a reader can check against
`data/ph_excluded_v1.csv`. It also carries the paper's sharpest point: the largest bar is
`PH-X1`, values taken from protocol sentences rather than results — 13 rows that every
automated "is this number in the article?" check would pass.

---

## Design decisions

**Colour.** One palette across panels A and C so an enzyme class reads the same in both.
Green/red reserved exclusively for direction in panel B, and not reused, so the
retained/lost distinction stays unambiguous. Print-safe and distinguishable in greyscale
by position and marker shape rather than hue alone.

**No error bars.** The sources report single values without dispersion. Adding intervals
would imply a precision the literature does not provide.

**Ranges excluded from A.** The 12 interval rows are not plotted as points, because
plotting an interval endpoint as an optimum is the exact defect the audit removed. They
appear in panel B where a bound is meaningful.

**Counts on every panel.** Each panel states its own n, because the four panels draw on
different subsets of the same 67 rows and a reader should never have to guess which.

---

## Before submission

1. **Re-render at final width.** Currently 1180 × 820 px. Set to the journal's column
   width and re-run; the script is resolution-independent SVG.
2. **Confirm the n values against the final dataset.** They are generated, not typed, so
   re-running `make_figure.py` after any data change is sufficient.
3. **Decide whether panel D belongs in the main text or the supplement.** If the paper's
   emphasis is the screener rather than the benchmark, D moves to supplementary and A–C
   become a three-panel figure; the script supports this by dropping the D block.
4. **Convert to PDF/EPS** if the journal rejects SVG (`rsvg-convert` or Inkscape).
5. **Caption** — draft below.

---

## Draft caption

> **Figure N. Composition and curation of the pH benchmark.**
> (**A**) Distribution of reported pH optima across 25 measurements, binned at 0.5 pH
> units and coloured by enzyme class. The distribution is skewed alkaline (median pH 8.0),
> consistent with base-favoured polyester hydrolysis, and acid-tolerant enzymes are
> sparsely represented.
> (**B**) Activity retained as a function of assay pH for the 29 measurements where the
> source reports an outcome at the tested pH. Upward triangles denote retained activity,
> downward triangles loss; the dashed line marks the 50% retention threshold used to
> define the pH-robustness class label. This axis is absent from the project's current
> shared schema and was recovered from source sentences during curation.
> (**C**) Joint pH and temperature coverage for the 22 measurements reporting both.
> Coverage clusters at pH 7–8.5 and 30–60 °C; the alkaline, high-temperature regime
> relevant to industrial PET depolymerisation is not represented.
> (**D**) Curation outcome. Of 105 candidate rows inherited from the parent conditions
> benchmark, 37 (35%) were removed under 12 explicit rules, leaving 68 measurements from
> 31 articles. The largest single class (`PH-X1`, 13 rows) is values extracted from
> methods or protocol sentences rather than from reported results — errors that pass any
> check based on locating the number in the source text; ten of those thirteen sit inside
> a Materials and Methods section in the article's own markup.
> All panels are generated from `data/ph_benchmark_v1.csv` by `scripts/make_figure.py`.

---

## Supplementary figures worth having

| Figure | Content | Why |
|---|---|---|
| S1 | pH stability/activity profiles per enzyme, where ≥3 pH points exist | shows the shape of the curves the screener must reproduce; 3 enzymes qualify (KoFAE, lipase IBRL-CHS2, and the unnamed alkaline esterase of PMC9709933), each with 5 points |
| S2 | Full audit funnel, rule × article | lets a reviewer trace any single removal |
| S3 | Benchmark pH distribution against the training-set pH distribution | makes the covariate shift explicit — training clusters at 7.0–7.5, the benchmark spans 3.0–12.0 |

S3 is the one to prioritise: it is the clearest single argument for why an external pH
benchmark was needed at all.
