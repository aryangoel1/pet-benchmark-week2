# Week-2 independent benchmark — plastic-degrading enzyme performance

An **independent test-only benchmark** of experimentally measured plastic-degrading enzyme
performance across **temperature, pH and electrolyte conditions**, built so it can be used as the
final external test of the screener model — and **only** after Sargun has finished training and
tuning.

> **Integrity statement.** Every value here was measured in a laboratory and reported in a
> peer-reviewed open-access article. Nothing is synthetic, predicted, interpolated, imputed or
> model-generated. Every row carries the verbatim source text in `evidence_quote` plus its PMCID
> and DOI. Fields the source did not state are left **empty**, never defaulted. The one derived
> quantity — ionic strength — is labelled `computed from …` in `ionic_strength_source` and is
> never presented as a reported value.

## Headline numbers

| Metric | Count |
|---|---|
| **Measurements shipped** | **528** |
| **Distinct source articles** | **79** |
| Candidate rows removed by the overlap gate | 196 |
| Tier A — appears in **no** prior dataset | 105 |
| Tier B — protein in Luke's held-out **test** split only | 21 |
| Tier C — conditions only, no sequence resolved | 402 |
| Rows overlapping Luke's **training** split | **0** |
| Entries re-verified against the original articles | 528 |
| Distinct proteins with a sequence | 13 |
| Distinct UniProt accessions | 15 |

### Condition coverage

| Axis | Rows |
|---|---|
| Temperature recorded | 199 |
| pH recorded | 88 |
| Temperature **and** pH on the same row | 34 |
| **Electrolyte (any)** | **115** |
| — named salt or metal ion | 115 |
| — salinity / seawater | 0 |
| — ionic strength (M) | 21 |
| — mixed electrolyte | 2 |
| Named buffer system | 37 |
| Exposure / incubation time | 81 |
| Assay method recorded | 12 |
| Measurements on engineered variants | 16 |
| Distinct ionic species | 15 |
| Distinct salts | 16 |

**Ions covered:** Na(+) (27), Ca(2+) (21), Mg(2+) (14), Zn(2+) (10), Cu(2+) (10), K(+) (7), Co(2+) (6), Mn(2+) (6), Fe(3+) (5), Fe(2+) (2), Ba(2+) (2), NH4(+) (2), Li(+) (1), Hg(2+) (1), Ni(2+) (1)

**Salts covered:** NaCl (22), CaCl2 (9), MgCl2 (5), KCl (3), ZnCl2 (2), CoCl2 (2), FeCl3 (2), CuSO4 (2), ZnSO4 (2), CuCl2 (2), MnSO4 (1), MgSO4 (1), BaCl2 (1), HgCl2 (1), MnCl2 (1), NiCl2 (1)

### Measurement types

| Type | Rows |
|---|---|
| thermostability | 137 |
| relative activity | 122 |
| salt effect | 92 |
| temperature optimum | 44 |
| pH stability | 39 |
| inhibition | 37 |
| pH optimum | 31 |
| kinetic constant | 14 |
| specific activity | 11 |
| ionic strength effect | 1 |

## Files

| File | What it is |
|---|---|
| `pet_benchmark_v2.csv` | **Main deliverable** — 528 rows × 70 columns |
| `pet_benchmark_v2.sqlite` | Same data, indexed, with the views `v_gold`, `v_sequence`, `v_temperature`, `v_ph`, `v_electrolyte`, `v_verified` |
| `benchmark_sequences.fasta` | Every benchmark protein, header carries Luke's `protein_id` join key |
| `OVERLAP_REPORT.md` | The audit trail — what was screened against what, and every verdict |
| `LUKE_HANDOFF.md` | **The document to send Luke** — the train-overlap check he asked for |
| `VERIFICATION_REPORT.md` | Every entry re-checked against a freshly downloaded article |
| `MANUAL_VERIFICATION.md` | **Read this before trusting any number** — what manual review found, what was fixed, and the measured residual error rate |
| `MANUAL_REVIEW_PACKET.md` | Entries printed next to the original article text for human review |
| `scripts/*.py` | The reproducible pipeline, standard library only except `pypdf` |
| `data/` | Intermediates: exclusion index, mined rows, resolved sequences, verdicts |

## The three tiers

The benchmark is tiered by how independent each row is. Use the tier that matches how strict you
need to be:

| Tier | Meaning | Use it for |
|---|---|---|
| `A_fully_independent` | The protein appears in **none** of the seven shared datasets and **nowhere** in Luke's data | The headline external test. SQLite: `SELECT * FROM v_gold` |
| `B_in_luke_heldout_test_only` | The protein is in Luke's **held-out test** split — no training contamination, but not novel to the project | Include for coverage; exclude if you want strict novelty |
| `C_conditions_only_no_sequence` | A real measurement whose enzyme could not be resolved to a sequence | Condition-axis analysis; **not** usable by a sequence model |

Nothing in any tier touches Luke's training split — that check is the gate, not a label.

## How overlap was excluded

Every candidate row was screened against an index built from **all seven shared datasets**, Luke's
Week-2 training dataset, Luke's Week-1 pH database, and my own Week-1 conditions database:

- 970,289 distinct protein sequences (SHA-1)
- 970,289 `protein_id`s in Luke's exact hash format
- 16,297 UniProt accessions
- 6,941 paper identifiers (PMID/PMCID)
- 1,579,354 measurement fingerprints
- 89 PDB codes from S669

Seven screens fire per row (S1 sequence identity → S7 internal duplicate). The full breakdown,
including which rule fired on which row, is in `OVERLAP_REPORT.md` and in the `overlap_rules_checked`
column of the CSV.

**Papers already mined are excluded before download.** All 418 articles here
were checked against every PMID/PMCID in every prior dataset — including all 199 articles my Week-1
build mined — *before* their full text was fetched. The same measurement therefore cannot re-enter
under a different enzyme name.

## Verification

550 entries were re-checked against a **freshly downloaded copy** of
their article. The harvest-time cache is never read during verification, so a corrupted cache cannot
verify itself. An entry passes only when its recorded evidence is located in the fresh copy — verbatim
for prose, cell-by-cell for tables — **and** the recorded standardized value is present in that text.
3 entries failed and were removed before shipping. See
`VERIFICATION_REPORT.md`.

`MANUAL_REVIEW_PACKET.md` goes further: it prints entries beside the surrounding text of the original
article so a human can confirm the value is *attributed* correctly — right enzyme, right condition,
right direction — which an automated string match cannot establish.

## Unit standardization

| Quantity | Canonical unit | Converted from |
|---|---|---|
| Temperature | °C | K, °F |
| pH | dimensionless | ranges split into `pH_low` / `pH_high` |
| Concentration | mM | M, µM, nM, %(w/v), mg/mL, g/L via formula weight |
| Salinity | g/L and PSU | %, ppt, PSU, g/kg, NaCl molarity |
| Ionic strength | M | reported, or computed as I = ½Σcᵢzᵢ² and labelled as computed |
| Time | minutes | s, h, d, weeks |
| KM | mM | µM, M |
| kcat | s⁻¹ | min⁻¹, h⁻¹ |

`python3 scripts/standardize_units.py` runs the conversion self-tests on their own.

## Sources

418 open-access articles mined; 79 contributed a shipped row.
Publication years: 2026 (140), 2025 (49), 2024 (69), 2023 (120), 2022 (116), 2021 (6), 2020 (2), 2018 (1).
Leading journals: .

## Handover rule

**Give this to Sargun only after training and tuning are complete.** Not for training, not for
tuning, not for feature selection, not for threshold picking. Final external test only. This is
also the rule Luke states in his `DATA_READINESS_HANDOFF.md`.

## Reproducing

```bash
python3 scripts/build_exclusions.py      # index the 7 datasets + Luke + week 1
python3 scripts/harvest_benchmark.py     # mine NEW open-access articles
python3 scripts/resolve_sequences.py     # attach UniProt sequences
python3 scripts/build_benchmark.py       # standardize units
python3 scripts/check_overlap.py         # the overlap gate
python3 scripts/verify_entries.py        # re-verify against the originals
python3 scripts/finalize.py              # write CSV / SQLite / FASTA
python3 scripts/make_reports.py          # OVERLAP_REPORT + LUKE_HANDOFF
python3 scripts/manual_review_packet.py  # human review packet
```

## Known limitations

- **13 distinct proteins carry sequences.** Sequence resolution only accepts an accession
  when the article names exactly one hydrolase record, because accepting ambiguous ones is
  how a benchmark acquires silently wrong labels. That precision costs coverage: most rows
  ship as tier C (real conditions, no sequence) and cannot be scored by a sequence model.
  Tier A is small but clean — treat it as the scored set.
- **Residual defect rate ~5-8%, concentrated in tier C.** Measured by manual review, not
  assumed. See `MANUAL_VERIFICATION.md`.

- Coverage is bounded by what is **open access in Europe PMC**. Paywalled characterisation papers
  are not represented.
- Rows in tier C carry real conditions and a real value but no sequence, so a sequence-based model
  cannot consume them. They are shipped because the condition axes are still useful, and flagged so
  they are never counted as sequence-model test cases.
- Extraction is pattern-based over article text and tables. That is why every row keeps its evidence
  quote, why 550 entries were re-verified against fresh downloads, and
  why the manual review packet exists.
- `mixed_electrolyte` is detected from salts co-named in the same sentence or table row; a paper that
  describes a buffer's composition elsewhere in the methods will not always be captured.
