# Manual review packet

45 shipped entries, spread across measurement types and across electrolyte / non-electrolyte rows. For each one: what the benchmark records, and the surrounding text of the original article so the extraction can be judged in context.

The automated verifier confirms a value **is present** in the source. This packet is for confirming the value is **attributed correctly** — right enzyme, right condition, right direction.

---

### 1. `BM000022` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = glycerol |
| Assay | — |
| **Value** | **97.9 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12741466 · 10.1016/j.isci.2025.114173 ·  2025 |

**Recorded evidence:** Table in PMC12741466 — Table 2 :: Organic solvent=Glycerola | Residual activity (%)=97.9 ± 2.2

**In the article:** *(context not located — check manually)*

---

### 2. `BM000516` — ionic strength effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AAB51445.1 (genbank_deposit_section_unique) |
| Organism | Streptomyces sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = NaCl @ 250.0 mM; ion = Na(+); I = 0.25 M (computed from 250.0 mM NaCl) |
| Assay | — |
| **Value** | **60.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC10707221 · 10.3390/ijms242317071 ·  2023 |

**Recorded evidence:** Likewise, SeLipC was sensitive to high ionic strength (I) as the enzyme lost 60% of its activity at 250 mM NaCl, while it was almost deactivated at salt concentrations higher than 500 mM (Figure 4C).

**In the article:** *(context not located — check manually)*

---

### 3. `BM000153` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | MYD18970.1 (genbank_unique_in_article) |
| Organism | Rhodothermaceae bacterium |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **0.246 mM** |
| Tier | A_fully_independent |
| Source | PMC12720421 · 10.1002/pro.70402 ·  2026 |

**Recorded evidence:** Table in PMC12720421 — TABLE 3 :: =Rp_EST | k cat (s−1)=12.0 ± 1.3 | K M (μM)=246 ± 72 | k cat/K M (s−1 M−1)=4.9 × 104

**In the article:** *(context not located — check manually)*

---

### 4. `BM000699` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 5.0 |
| Assay | — |
| **Value** | **5.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC11651597 · 10.1371/journal.pone.0314556 ·  2024 |

**Recorded evidence:** The recombinant lipase exhibited activity across a wide pH spectrum, ranging from pH 5 to pH 9, with optimal activity observed at pH 7 (Fig 5A).

**In the article:** …spite this, MLipA exhibits moderate thermolabile behavior, notably retaining activity at 35°C. Effect of pH on MLipA activity and stability The recombinant lipase exhibited activity across a wide pH spectrum, ranging from pH 5 to pH 9, with optimal activity observed at pH 7 ( Fig 5A ). It maintained high activity levels, retaining 93% of its activity at pH 6 and 82% at pH 8. However, its relative activities decreased significantly at pH 4 (11%) and pH 5 (45%). Beyond pH 9, a sharp decline in activity was observed, with relative activities of 46%, 22%, and 8% at pH 9, pH 10, and pH 11, respectively. 10.1371/journal.pone.0314556.g005 Fig 5 pH p…

---

### 5. `BM000603` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | amorphous PET |
| Conditions | pH = 6.0; buffer = sodium acetate (100.0 mM); salt = NaCl @ 100.0 mM; ion = Na(+); I = 0.1 M (computed from 100.0 mM NaCl) |
| Assay | — |
| **Value** | **6.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9772341 · 10.1038/s41467-022-35237-x ·  2022 |

**Recorded evidence:** For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5).

**In the article:** …s were filtered through 0.2 µm nylon filters for monomer quantitation. All PET hydrolysis screening reactions were performed in triplicate. For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5). The reactions were again stopped at 96 h by the additional of an equal volume of 100% methanol and worked up in the same manner as described directly above. Aromatic product release data are reported throughout relative to bac…

---

### 6. `BM000680` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PHB |
| Conditions | pH = 6.5; additive = Tween-80 |
| Assay | — |
| **Value** | **6.5 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC13220297 · 10.1021/acs.jafc.6c02898 ·  2026 |

**Recorded evidence:** The enzyme immobilized on PHB demonstrated greater stability at pH values between 5.0 and 6.0, whereas at pH 4.5 and pH 6.5, it retained approximately 50% of its activity.

**In the article:** …ty results regarding the incubation of the invertase immobilized on PHB and SG functionalized with glutaraldehyde are presented in Figure . The enzyme immobilized on PHB demonstrated greater stability at pH values between 5.0 and 6.0, whereas at pH 4.5 and pH 6.5, it retained approximately 50% of its activity. On the other hand, the enzyme immobilized on SG presented its highest stability at pH 5.0 and an activity reduction of approximately 75% at pH 5.5 and pH 6.5, indicating a smaller pH stability range. 4 Stability of the invertase from B. tequilensis (PP6) immobilized on functionalized SG (■) and PHB (gray triangle) after 24 h of incubation at 4 °C at different pH values, with the maximum enzymati…

---

### 7. `BM001342` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **100.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 2 :: Effector=Control* | Residual activity (%) at=100.00

**In the article:** *(context not located — check manually)*

---

### 8. `BM000087` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Mg(2+) |
| Assay | — |
| **Value** | **102.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 2 :: Metal Ion=Mg2+ | Concentration=10 mM | Residual Activity, %=102 ± 3

**In the article:** *(context not located — check manually)*

---

### 9. `BM000854` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | PHAZ |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = MgCl2; ion = Mg(2+) |
| Assay | — |
| **Value** | **89.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC4624153 · 10.1007/s13205-015-0287-4 ·  2015 |

**Recorded evidence:** Table in PMC4624153 — Table 2 :: Reagent=MgCl2 | Relative activity (%)=89

**In the article:** *(context not located — check manually)*

---

### 10. `BM000105` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl myristate (C14) |
| Conditions | — |
| Assay | — |
| **Value** | **51.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl myristate (C14) | Abbreviation=pNPM | Specific Activity, U/mg=51 ± 1

**In the article:** *(context not located — check manually)*

---

### 11. `BM000567` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 40.0 °C; pH = 8.0 |
| Assay | — |
| **Value** | **40.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9104356 · 10.3390/molecules27092999 ·  2022 |

**Recorded evidence:** BaAXE showed optimal activity at pH 8 and 40 °C.

**In the article:** …of the mean (SEM). 2.3. Biochemical Properties The biochemical properties of BaAXE were investigated in assays with 4-NPA as the substrate. BaAXE showed optimal activity at pH 8 and 40 °C. The km, kcat, and kcat/km (catalytic efficiency) values were calculated as 0.43 mM, 122.4 s -1 , and 282 mM -1 s -1 , respectively. A thermostability assay showed that the BaAXE retained around 40% activity after incubating the enzyme for 2 h at 40-100 °C but showed no clear activity at acidic pHs. At pH 7 and 9, BaAXE retained over 80% activity after incubating the enzyme for 4 h ( Figure 5 ). Figure 5 Biochemical …

---

### 12. `BM000520` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AAB51445.1 (genbank_deposit_section_unique) |
| Organism | Streptomyces sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 70.0 °C |
| Assay | — |
| **Value** | **70.0 degrees Celsius** |
| Tier | A_fully_independent |
| Source | PMC10707221 · 10.3390/ijms242317071 ·  2023 |

**Recorded evidence:** However, its thermostability was clearly enhanced when protein concentration was increased approximately 25-fold (19 µg/mL), allowing the enzyme to maintain 60% residual activity after incubation at temperatures above 70 °C.

**In the article:** …y poor thermal stability at low protein concentrations (0.72 µg/mL) since residual enzyme activity was strongly decreased from 35 to 60 °C. However, its thermostability was clearly enhanced when protein concentration was increased approximately 25-fold (19 µg/mL), allowing the enzyme to maintain 60% residual activity after incubation at temperatures above 70 °C. Figure 5 Thermal stability of Se LipC. ( A ) Effect of temperature on Se LipC stability using different enzyme concentrations and activity assays. ( B ) Thermal inactivation kinetics of Se LipC at 45 °C using different enzyme concentrations and activity assays; inset: the decrease in enzyme activity followed exponential regression (first-order…

---

### 13. `BM000160` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | Cut190 |
| UniProt | BAO42836.1 (genbank_deposit_section_unique) |
| Organism | Saccharomonospora viridis |
| Mutation | S184P/R186S |
| Substrate | PLA |
| Conditions | T = 60.0 °C; ion = Ca(2+); exposure = 3.1 min |
| Assay | — |
| **Value** | **60.0 degrees Celsius** |
| Tier | B_in_luke_heldout_test_only |
| Source | PMC9321771 · 10.1002/cssc.202102750 ·  2022 |

**Recorded evidence:** The combination of Ca2+ and sucrose played an important stabilizing role in Cut190 S184P/R186S, helping the enzyme keep 25 % of residual activity after 96 h at 60 °C as observed in Figure 6, without interfering with the coupled assay (Figure S5).

**In the article:** *(context not located — check manually)*

---

### 14. `BM000716` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = ethanol |
| Assay | — |
| **Value** | **-0.24 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC11651597 · 10.1371/journal.pone.0314556 ·  2024 |

**Recorded evidence:** Table in PMC11651597 — Table 2 :: =Ethanol | Relative Activity (%)=-0.24

**In the article:** *(context not located — check manually)*

---

### 15. `BM000147` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | MYD18970.1 (genbank_unique_in_article) |
| Organism | Rhodothermaceae bacterium |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **0.194 mM** |
| Tier | A_fully_independent |
| Source | PMC12720421 · 10.1002/pro.70402 ·  2026 |

**Recorded evidence:** Table in PMC12720421 — TABLE 3 :: =AlinE4 | k cat (s−1)=15.0 ± 1.4 | K M (μM)=194 ± 55 | k cat/K M (s−1 M−1)=7.7 × 104

**In the article:** *(context not located — check manually)*

---

### 16. `BM000004` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PCL |
| Conditions | pH = 7.0; additive = Tween-80 |
| Assay | — |
| **Value** | **7.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12741466 · 10.1016/j.isci.2025.114173 ·  2025 |

**Recorded evidence:** The optimal pH for PCLase0801 activity was determined to be 8.0, with relatively high enzyme activity maintained between pH 7.0 and 9.0 (Figure 3C).

**In the article:** …ntained stability at temperatures up to 50°C for 4 h; however, stability declined sharply when the temperature exceeded 60°C ( Figure 3 B). The optimal pH for PCLase0801 activity was determined to be 8.0, with relatively high enzyme activity maintained between pH 7.0 and 9.0 ( Figure 3 C). PCLase0801 retained over 80% of its enzymatic activity across pH conditions ranging from 6.0 to 9.0 after 24 h of incubation. However, it became unstable when the pH dropped below 5.0 or exceeded 10.0 ( Figure 3 D). Several PCL-degrading enzymes, as reported by B. Ruiz and M. Amin et al., also exhibited both stability and notable activity within the pH rang…

---

### 17. `BM000071` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 40.0 °C; pH = 7.0; buffer = sodium phosphate (50.0 mM) |
| Assay | — |
| **Value** | **7.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0).

**In the article:** …lyse the thermal stability, the enzyme extract was pre-incubated for 5 h at 40, 50, 60 or 70 °C in 50 mM Tris-HCl buffer solution (pH 7.0). The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0). The results were expressed as a percentage of the activity of the extract not subjected to thermal incubation. All experiments were performed in triplicate. 2.9. Effect of Metal Ions and Detergents on Esterase Activity The effect of metal ions on esterase activity was determined using the following ions: Ca 2+ , Mg 2+ , Mn 2+ , Cu 2+ , Zn 2+ , and Fe 2+ . The effect of the metal ions, the reducing agents β-mercaptoe…

---

### 18. `BM000849` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | PHAZ |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **100.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC4624153 · 10.1007/s13205-015-0287-4 ·  2015 |

**Recorded evidence:** Table in PMC4624153 — Table 2 :: Reagent=Control | Relative activity (%)=100

**In the article:** *(context not located — check manually)*

---

### 19. `BM000203` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = NaCl; ion = Na(+) |
| Assay | — |
| **Value** | **100.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Table in PMC12898461 — Table 5 :: [NaCl] (M)=0 | Relative Activity (%)=100 ± 0

**In the article:** *(context not located — check manually)*

---

### 20. `BM001491` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Co(2+) |
| Assay | — |
| **Value** | **78.17 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10146132 · 10.3390/microorganisms11040989 ·  2023 |

**Recorded evidence:** Table in PMC10146132 — Table 3 :: Metal Ions and Organic Compounds=Co2+ | Relative Activity/(%)=78.17 ± 4.48

**In the article:** *(context not located — check manually)*

---

### 21. `BM000106` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl palmitate (C16) |
| Conditions | — |
| Assay | — |
| **Value** | **45.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl palmitate (C16) | Abbreviation=pNPP | Specific Activity, U/mg=45 ± 4

**In the article:** *(context not located — check manually)*

---

### 22. `BM000338` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | BHET |
| Conditions | T = 50.0 °C; buffer = MES |
| Assay | — |
| **Value** | **50.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9764356 · 10.1021/acscatal.2c03772 ·  2022 |

**Recorded evidence:** Thus, 50 °C appeared to be the optimal temperature for BHET hydrolysis by both enzymes.

**In the article:** …55 °C, the considerably lower total substrate conversion levels with both enzymes exclude this temperature as the ideal reaction condition. Thus, 50 °C appeared to be the optimal temperature for BHET hydrolysis by both enzymes. Next, we performed the enzymatic hydrolysis of MHET at 50 °C. At the same substrate concentration of 2 mM, more than twofold TPA was released from MHET compared to BHET with both enzymes. TfCa WA yielded 3.3-fold and 2.6-fold more TPA from the hydrolysis of BHET and MHET than TfCa wt, respectively. Finally, we compared the rates of TPA release as a result of the enzymatic hydrolysis of MHET at various concentrations…

---

### 23. `BM000683` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PHB |
| Conditions | T = 4.0 °C; exposure = 1440.0 min |
| Assay | — |
| **Value** | **4.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC13220297 · 10.1021/acs.jafc.6c02898 ·  2026 |

**Recorded evidence:** Stability of the invertase from B. tequilensis (PP6) immobilized on functionalized SG (■) and PHB (gray triangle) after 24 h of incubation at 4 °C at different pH values, with the maximum enzymatic activity of 2.30 U/g.

**In the article:** …highest stability at pH 5.0 and an activity reduction of approximately 75% at pH 5.5 and pH 6.5, indicating a smaller pH stability range. 4 Stability of the invertase from B. tequilensis (PP6) immobilized on functionalized SG (■) and PHB (gray triangle) after 24 h of incubation at 4 °C at different pH values, with the maximum enzymatic activity of 2.30 U/g. Immobilization tends to protect the structure of the enzyme from the effects of pH; thus, higher pH stability favors storage and industrial applications. As observed for thermal stability, the samples immobilized on functionalized PHB presented a similar stability to that of the soluble enzyme; therefore, this support may be offering a favorable en…

---

### 24. `BM000866` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | PHAZ |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = EDTA |
| Assay | — |
| **Value** | **59.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC4624153 · 10.1007/s13205-015-0287-4 ·  2015 |

**Recorded evidence:** Table in PMC4624153 — Table 2 :: Reagent=EDTA | Relative activity (%)=59

**In the article:** *(context not located — check manually)*

---

### 25. `BM000152` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | MYD18970.1 (genbank_unique_in_article) |
| Organism | Rhodothermaceae bacterium |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **0.419 mM** |
| Tier | A_fully_independent |
| Source | PMC12720421 · 10.1002/pro.70402 ·  2026 |

**Recorded evidence:** Table in PMC12720421 — TABLE 3 :: =shMt_EST | k cat (s−1)=53.2 ± 4.4 | K M (μM)=419 ± 78 | k cat/K M (s−1 M−1)=1.3 × 105

**In the article:** *(context not located — check manually)*

---

### 26. `BM001504` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 8.0 |
| Assay | — |
| **Value** | **8.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10385968 · 10.3390/molecules28145410 ·  2023 |

**Recorded evidence:** The optimal pH for EstD04 activity was pH 8.

**In the article:** …ity of EstD04, measured by the tolerance of the enzyme to different temperatures, dropped drastically between 50 °C to 70 °C ( Figure 6 B). The optimal pH for EstD04 activity was pH 8. Finally, we also demonstrated the pH stability (or tolerance) of EstD04 esterase by measuring its enzymatic activity after pre-incubation with buffers of various pH values ( Figure 6 C). EstD04 exhibited favorable pH stability between pH 8 to pH 11, in which the enzyme retained at least 80% activity. The maximal stability was maintained at pH 10 ( Figure 6 C), suggesting that this enzyme could be an alkaline lipolyt…

---

### 27. `BM001489` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 6.0 |
| Assay | — |
| **Value** | **6.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10146132 · 10.3390/microorganisms11040989 ·  2023 |

**Recorded evidence:** A pH of 6.0~10.0 had good stability, the retained enzyme activity was more than 60%, and pH 8.0, the best stability of enzyme activity, could retain about 80% of enzyme activity.

**In the article:** …ss stable when pH was 3.0 to 5.0, the enzyme activity was lost when pH was 3.0, and the stability was less than 50% when pH was 4.0 to 5.0. A pH of 6.0~10.0 had good stability, the retained enzyme activity was more than 60%, and pH 8.0, the best stability of enzyme activity, could retain about 80% of enzyme activity. Shu et al. screened the FAE activity gene estF27 from the soil metagenic library, which also showed good activity at pH 8, and its stability could preserve 80% of the enzyme activity at pH 8 [ 24 ]. Zhang et al. studied Bi76, a protein with FAE activity from B. intestinalis . It has good activity and stability at pH 5.5, but the FAE enzyme activity is less than 10% at pH 8.0 [ 25 ]. This …

---

### 28. `BM000094` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = beta-mercaptoethanol |
| Assay | — |
| **Value** | **37.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 2 :: Metal Ion=β-Mercaptoethanol | Concentration=10 mM | Residual Activity, %=37 ± 1

**In the article:** *(context not located — check manually)*

---

### 29. `BM000086` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ca(2+) |
| Assay | — |
| **Value** | **52.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 2 :: Metal Ion=Ca2+ | Concentration=10 mM | Residual Activity, %=52 ± 6

**In the article:** *(context not located — check manually)*

---

### 30. `BM001498` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Mn(2+) |
| Assay | — |
| **Value** | **60.33 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10146132 · 10.3390/microorganisms11040989 ·  2023 |

**Recorded evidence:** Table in PMC10146132 — Table 3 :: Metal Ions and Organic Compounds=Mn2+ | Relative Activity/(%)=60.33 ± 6.73

**In the article:** *(context not located — check manually)*

---

### 31. `BM000102` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl octanoate (C8) |
| Conditions | — |
| Assay | — |
| **Value** | **44.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl octanoate (C8) | Abbreviation=pNPO | Specific Activity, U/mg=44 ± 2

**In the article:** *(context not located — check manually)*

---

### 32. `BM001123` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 10.0 °C |
| Assay | — |
| **Value** | **10.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12428281 · 10.3390/ijms26178141 ·  2025 |

**Recorded evidence:** The activity of DehpH increased in the temperature range of 10 °C to 30 °C and showed maximum activity at 30 °C (Figure 4C).

**In the article:** …hpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 ( Figure 4 B). The activity of DehpH increased in the temperature range of 10 °C to 30 °C and showed maximum activity at 30 °C ( Figure 4 C). Subsequently, the activity of DehpH decreased in the temperature range from 30 °C to 80 °C, and DehpH almost lost its activity under 80 °C. The thermostability experiment showed that the activity of DehpH decreased with the increasing of the incubation time, and the higher the temperature, the greater the loss of activity ( Figure 4 D). After 5 h incubation, approximately 64.0% of…

---

### 33. `BM001396` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | DuraPETase |
| UniProt | GAP38373.1 (genbank_deposit_section_unique) |
| Organism | Pseudideonella sakaiensis |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 50.0 °C |
| Assay | — |
| **Value** | **50.0 degrees Celsius** |
| Tier | B_in_luke_heldout_test_only |
| Source | PMC11033240 · 10.1007/s00253-024-13144-z ·  2024 |

**Recorded evidence:** Overall, the changes in activity at 50 °C and 52 °C reflect the observed changes in thermostability.

**In the article:** …d 52 °C to see how the enzymes performed at the optimum temperature of the original DuraPETase (50 °C) and slightly above this temperature. Overall, the changes in activity at 50 °C and 52 °C reflect the observed changes in thermostability. DuraPETase S223Y —which showed the strongest increase in T m —showed practically identical PET degradation rates at 50 °C compared to the original DuraPETase but was approx. ten percent more active at 52 °C. Similarly, a better performance at 52 °C was also recorded for one of the other two more thermostable variants, DuraPETase S42M . For the third stable variant, DuraPETase S61M , the same tendency was observed at…

---

### 34. `BM000821` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = Tween-80 |
| Assay | — |
| **Value** | **86.8 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC8971842 · 10.3389/fbioe.2022.835847 ·  2022 |

**Recorded evidence:** Table in PMC8971842 — TABLE 3 :: Organic solvent=Tween-80 | Residual activity (%)=86.80 ± 0.20

**In the article:** *(context not located — check manually)*

---

### 35. `BM001367` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **0.031 mM** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 4 :: p-NP esters=p-NP-C2 | Specific activity (U/mg)=0.470 ± 0.0002 | Relative activity (%)=100.00 | Km (mM)=0.031 | Kcat (sec−1)=20.39 | Kcat/Km (sec−1 mM−1)=657.7

**In the article:** *(context not located — check manually)*

---

### 36. `BM001332` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 8.0 |
| Assay | — |
| **Value** | **8.0 pH** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** The optimum pH for enzyme activity was realized at pH 8.0 (Fig.

**In the article:** …H (s) from 5.0 to 12.0. Significant differences ( P < 0.05) were evidenced among values of enzyme activity over the tested range of pH (s). The optimum pH for enzyme activity was realized at pH 8.0 (Fig. 7 A). Pertaining to pH stability, the purified EstRag exhibited 100, 100, and 93.41% stability for 24 h at pH (s) 8.0, 9.0, and 10.0, respectively (Fig. 7 B). EstRag stability decreased significantly ( P < 0.05) at pH(s) less than 8.0 and greater than 10.0. Regarding the enzyme-temperature profile, an appreciable enzyme activity with significant differences at P < 0.05 was remarked over a wide range of temperatures …

---

### 37. `BM000846` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | PHAZ |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 55.0 °C; pH = 4.0; exposure = 60.0 min |
| Assay | — |
| **Value** | **4.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC4624153 · 10.1007/s13205-015-0287-4 ·  2015 |

**Recorded evidence:** The enzyme was stable at pH 4.0, 5.0 and 6.0 and 55 °C for 1 h with a residual activity of almost 70–80 %.Fig.

**In the article:** …ctivity for P. expansum PHB depolymerase was detected between pH 4.0 and 6.0, the highest being at pH 5.0 (Fig. 2 ) and at 50 °C (Fig. 3 ). The enzyme was stable at pH 4.0, 5.0 and 6.0 and 55 °C for 1 h with a residual activity of almost 70-80 %. Fig. 2 pH optima of P. expansum PHB depolymerase activity Fig. 3 Temperature optima of P. expansum PHB depolymerase activity Furthermore, the kinetic parameters of PhaZ Pen for PHB hydrolysis were also determined. The apparent K m and V max values were 1.04 μg/mL and 4.5 μg/min, respectively (Fig. 4 ). The kinetic parameters of recombinant PHAZ sa of Streptomyces ascomycinicus for PHB hydrolysis dete…

---

### 38. `BM001200` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **100.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10725956 · 10.3389/fmicb.2023.1304233 ·  2023 |

**Recorded evidence:** Table in PMC10725956 — Table 1 :: Cations=Control | Relative activity (%) a=100

**In the article:** *(context not located — check manually)*

---

### 39. `BM000089` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Cu(2+) |
| Assay | — |
| **Value** | **0.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 2 :: Metal Ion=Cu2+ | Concentration=10 mM | Residual Activity, %=0

**In the article:** *(context not located — check manually)*

---

### 40. `BM001500` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ca(2+) |
| Assay | — |
| **Value** | **55.56 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10146132 · 10.3390/microorganisms11040989 ·  2023 |

**Recorded evidence:** Table in PMC10146132 — Table 3 :: Metal Ions and Organic Compounds=Ca2+ | Relative Activity/(%)=55.56 ± 5.21

**In the article:** *(context not located — check manually)*

---

### 41. `BM000107` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl stearate (C18) |
| Conditions | — |
| Assay | — |
| **Value** | **31.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl stearate (C18) | Abbreviation=pNPS | Specific Activity, U/mg=31 ± 16

**In the article:** *(context not located — check manually)*

---

### 42. `BM000006` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PCL |
| Conditions | T = 45.0 °C; exposure = 480.0 min |
| Assay | — |
| **Value** | **45.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12741466 · 10.1016/j.isci.2025.114173 ·  2025 |

**Recorded evidence:** The optimal reaction system for ε-caprolactone ring-opening polymerization catalyzed by PCLase0801 consisted of 25 mg of enzyme powder, a temperature set at 45°C, a duration of 8 h, hexane as the solvent, and a water activity of 0.11 (details are provided in the Supplementary Materials, Figure S2–S6 and Tables S1 and S2).

**In the article:** …increase the conversion of monomers in the catalytic synthesis of PCL, we optimized key parameters in the enzymatic polymerization process. The optimal reaction system for ε-caprolactone ring-opening polymerization catalyzed by PCLase0801 consisted of 25 mg of enzyme powder, a temperature set at 45°C, a duration of 8 h, hexane as the solvent, and a water activity of 0.11 (details are provided in the Supplementary Materials, Figure S2-S6 and Tables S1 and S2 ). The reaction system for ε-caprolactone ring-opening polymerization reported by Li and Ma et al. was at 80°C-90°C and the reaction time was 72 h, 34 , 35 other lipases even require more than 10 days. 20 Compared with other reported enzyme catalys…

---

### 43. `BM001102` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 60.0 °C |
| Assay | — |
| **Value** | **60.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC13118911 · 10.3390/microorganisms14040856 ·  2026 |

**Recorded evidence:** Enzyme activity measurements across 40–90 °C showed that wild-type B10 laccase began to lose activity substantially at 60 °C, retained only minimal residual activity at 80 °C, and was completely inactivated at 90 °C (Figure 2c).

**In the article:** … and successfully expressed and purified in E. coli BL21(DE3), with SDS-PAGE showing a single band at approximately 35 kDa ( Figure 2 a,b). Enzyme activity measurements across 40-90 °C showed that wild-type B10 laccase began to lose activity substantially at 60 °C, retained only minimal residual activity at 80 °C, and was completely inactivated at 90 °C ( Figure 2 c). By contrast, all seven single-site variants showed enhanced thermostability at elevated temperatures. Among these variants, the R196C mutant showed the best overall performance, displaying the highest absolute activity between 50 and 60 °C and retaining more than 96% of its relative activity after a 10 min heat treatment at 80 °C. In sub…

---

### 44. `BM000713` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = DMSO |
| Assay | — |
| **Value** | **-1.22 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC11651597 · 10.1371/journal.pone.0314556 ·  2024 |

**Recorded evidence:** Table in PMC11651597 — Table 2 :: =DMSO | Relative Activity (%)=-1.22

**In the article:** *(context not located — check manually)*

---

### 45. `BM000174` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | Ces1-ET |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **0.25 mM** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Table in PMC12898461 — Table 3 :: Enzyme=Ces1-ET | Vmax(µmoles p-Nitrophenol/10 min)=15 ± 4 | Km (mM)=0.25 ±0.05

**In the article:** *(context not located — check manually)*

---

