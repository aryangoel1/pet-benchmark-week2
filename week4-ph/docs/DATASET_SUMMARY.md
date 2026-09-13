# pH benchmark -- dataset summary

Table 1 as it will appear in the paper, plus the breakdowns that support it. Generated from `data/ph_benchmark_v1.csv`.

## Table 1. Composition of the pH benchmark

| Property | Value |
|---|---|
| Measurements | **67** |
| Source articles | **30** |
| Publication years | 2015–2026 |
| pH as the measured outcome | 57 |
| pH as a recorded assay covariate | 10 |
| Scoreable on the pH axis | 45 |
| Scoreable by a sequence model | 10 |
| Rows with a resolved protein sequence | 16 |
| Distinct proteins | 6 |
| Distinct accessions | 6 |
| Distinct enzyme classes | 19 |
| Rows naming a polymer substrate | 27 |
| pH range covered | 3.0–12.0 (median 8.0) |
| Rows carrying an outcome at the pH (% activity) | 29 |
| Rows carrying the direction of the effect | 54 |
| Rows with temperature recorded as well | 22 |
| Rows with an exposure time | 18 |
| pH interval rows (in 10 range groups) | 12 |
| Rows in Luke's training split | **0** |

## Measurement types

| Type | Rows | pH is the... |
|---|---:|---|
| pH optimum | 24 | outcome |
| pH stability | 18 | outcome |
| pH stability range | 9 | outcome |
| temperature optimum | 9 | covariate |
| pH activity range | 3 | outcome |
| pH activity | 3 | outcome |
| thermostability | 1 | covariate |

## Independence tiers

| Tier | Rows | Meaning |
|---|---:|---|
| `A_fully_independent` | 14 | protein appears in none of the seven shared datasets and nowhere in Luke's data |
| `B_in_luke_heldout_test_only` | 2 | protein sits in Luke's held-out test split -- no training contamination, but not novel to the project |
| `C_conditions_only_no_sequence` | 51 | a real measurement whose enzyme could not be resolved to a sequence |

## Enzyme classes represented

| Class | Rows | Polymer named |
|---|---:|---|
| lipase | 14 | polyester |
| esterase | 9 | -- |
| feruloyl esterase | 8 | PET |
| acetyl xylan esterase | 6 | -- |
| esterase (HSL family IV) | 4 | -- |
| PHB depolymerase | 3 | PHB |
| PHA depolymerase | 3 | PHA |
| polyester hydrolase | 2 | aliphatic + aromatic polyester |
| PVC depolymerase | 2 | PVC |
| protease (subtilisin) | 2 | PLA |
| GDSL esterase | 2 | -- |
| PETase | 2 | PET |
| carboxylesterase | 2 | BHET (PET monomer) |
| PCL depolymerase | 2 | PCL |
| phthalate hydrolase | 2 | DEHP (plasticiser) |
| promiscuous esterase | 1 | PET |
| nylon hydrolase | 1 | nylon (polyamide) |
| MHET hydrolase | 1 | MHET (PET monomer) |
| cutinase | 1 | cutin / polyester |

## Source articles

| PMCID | Year | Rows | Enzyme(s) | Title |
|---|---:|---:|---|---|
| PMC11651597 | 2024 | 7 | lipase IBRL-CHS2 | Characterization of a novel subfamily 1.4 lipase from Bacillus lichenif... |
| PMC10146132 | 2023 | 5 | KoFAE | Characterization of Feruloyl Esterase from <i>Klebsiella oxytoca</i> Z2... |
| PMC9709933 | 2022 | 5 | -- | Heterologous expression, molecular studies and biochemical characteriza... |
| PMC10385968 | 2023 | 4 | EstD04 | Enzymatic Characterization of a Novel HSL Family IV Esterase EstD04 fro... |
| PMC10003648 | 2023 | 3 | PhaZ | Polymer-Degrading Enzymes of <i>Pseudomonas chloroaphis</i> PA23 Displa... |
| PMC4624153 | 2015 | 3 | PHAZ(Pen) | Poly(-β-hydroxybutyrate) (PHB) depolymerase PHAZ <sub>Pen</sub> from Pe... |
| PMC9104356 | 2022 | 3 | BaAXE | Characterisation of a Novel Acetyl Xylan Esterase (BaAXE) Screened from... |
| PMC9606172 | 2022 | 3 | AXE-HAS10 | Recombinant acetylxylan esterase of Halalkalibacterium halodurans NAH-E... |
| PMC10418727 | 2023 | 2 | EaEst2 | Structural and Biochemical Insights into Bis(2-hydroxyethyl) Terephthal... |
| PMC10607177 | 2023 | 2 | -- | Optimizing Eco-Friendly Degradation of Polyvinyl Chloride (PVC) Plastic... |
| PMC10707221 | 2023 | 2 | SeLipC | A Novel Lipase from <i>Streptomyces exfoliatus</i> DSMZ 41693 for Biote... |
| PMC11611003 | 2022 | 2 | SbPETase | Biochemical characterization of a polyethylene terephthalate hydrolase ... |
| PMC11782994 | 2024 | 2 | -- | Activity of an anaerobic <i>Thermoanaerobacterales</i> hydrolase on ali... |
| PMC12188634 | 2025 | 2 | Savinase | Efficient Degradation of Consumer-Grade PLA by Commercial Savinase: Opt... |
| PMC12428281 | 2025 | 2 | DehpH | Identification and Characterization of a Novel Di-(2-ethylhexyl) Phthal... |
| PMC12734981 | 2025 | 2 | PanLipdN | A CALB-like Cold-Active Lipolytic Enzyme from &lt;i&gt;Pseudonocardia a... |
| PMC12896513 | 2026 | 2 | rEST-24 | Cloning and Characterization of GDSL Esterases from &lt;i&gt;Bacillus p... |
| PMC12898461 | 2026 | 2 | Ces1-ET, Plp1-ET | Production of Novel Thermostable Esterases from &lt;i&gt;Thermus thermo... |
| PMC12960341 | 2026 | 2 | CaFaeA | Unveiling a catalytically promiscuous feruloyl esterase from Clostridiu... |
| PMC13323979 | 2026 | 2 | -- | Spontaneous efficient degradation of polyesters in soil by an enzyme@MO... |
| PMC10495362 | 2023 | 1 | PET46 | An archaeal lid-containing feruloyl esterase degrades polyethylene tere... |
| PMC11055803 | 2024 | 1 | ANCUT1 | ANCUT1, a novel thermoalkaline cutinase from Aspergillus nidulans and i... |
| PMC12741466 | 2025 | 1 | PCLase0801 | Degradation and ring-opening polymerization of poly(ε-caprolactone) by ... |
| PMC12767561 | 2026 | 1 | TflNylA | Toward the Bioremediation of Nylon Waste Materials: Genome Mining Leads... |
| PMC13035632 | 2026 | 1 | LipC | Co-expression, purification, and characterization of an acidophilic and... |
| PMC7936011 | 2021 | 1 | Tan410 | A novel esterase from a soil metagenomic library displaying a broad sub... |
| PMC8767016 | 2021 | 1 | PET27 | The Bacteroidetes <i>Aequorivita</i> sp. and <i>Kaistella jeonii</i> Pr... |
| PMC8971842 | 2022 | 1 | PCLase I | Two Extracellular Poly(<i>ε</i>-caprolactone)-Degrading Enzymes From <i... |
| PMC9452428 | 2022 | 1 | EstRag | Molecular study on recombinant cold-adapted, detergent- and alkali stab... |
| PMC9805092 | 2022 | 1 | -- | Development of a yeast whole-cell biocatalyst for MHET conversion into ... |

## Distribution of reported pH optima

| pH | Count |
|---:|---|
| 3.5 | # (1) |
| 5 | # (1) |
| 7 | ####### (7) |
| 7.5 | ## (2) |
| 8 | ########## (10) |
| 8.5 | ### (3) |

Range 3.5–8.5; median 8; n = 24. The alkaline skew is real and expected -- polyester hydrolysis is base-favoured -- but it also means the benchmark tests acid-tolerant enzymes thinly.

## What was removed, by rule

| Rule | Rows |
|---|---:|
| `PH-X1` methods_or_protocol_sentence | 13 |
| `PH-X6` off_target_enzyme_class | 8 |
| `PH-X7` secondhand_or_review | 7 |
| `PH-X3` enzyme_attribution_mismatch | 6 |
| `PH-X9` measurement_type_unsupported | 6 |
| `PH-X10` duplicate_measurement | 3 |
| `PH-X11` garbled_table_extraction | 3 |
| `PH-X4` ambiguous_multi_enzyme | 3 |
| `PH-X12` no_outcome_at_stated_pH | 1 |
| `PH-X2` range_endpoint_as_optimum | 1 |
| `PH-X5` model_predicted_value | 1 |
| `PH-X8` analytical_method_pH | 1 |

Full reasoning per row: `docs/AUDIT_REPORT.md` and `data/ph_excluded_v1.csv`.
