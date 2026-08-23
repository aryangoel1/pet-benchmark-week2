# Manual review packet

45 shipped entries, spread across measurement types and across electrolyte / non-electrolyte rows. For each one: what the benchmark records, and the surrounding text of the original article so the extraction can be judged in context.

The automated verifier confirms a value **is present** in the source. This packet is for confirming the value is **attributed correctly** — right enzyme, right condition, right direction.

---

### 1. `BM87FFE167BE` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = glycerol |
| Assay | — |
| **Value** | **80.93 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 3 :: Organic solvent=Glycerol | Residual activity (%) at=80.93 ± 0.040 | Log Pa=97.73 ± 0.009

**In the article:** *(context not located — check manually)*

---

### 2. `BM15C62C6E18` — ionic strength effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AAB51445.1 (genbank_deposit_section_unique) |
| Organism | Streptomyces sp. |
| Mutation | wild-type/unspecified |
| Substrate | olive oil |
| Conditions | salt = NaCl @ 250.0 mM; ion = Na(+); salinity = 14.61 g/L; I = 0.25 M (computed from 250.0 mM NaCl) |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **60.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC10707221 · 10.3390/ijms242317071 ·  2023 |

**Recorded evidence:** Likewise, SeLipC was sensitive to high ionic strength (I) as the enzyme lost 60% of its activity at 250 mM NaCl, while it was almost deactivated at salt concentrations higher than 500 mM (Figure 4C).

**In the article:** *(context not located — check manually)*

---

### 3. `BM64EF4F1D0E` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | MYD18970.1 (genbank_unique_in_article) |
| Organism | Rhodothermaceae bacterium |
| Mutation | wild-type/unspecified |
| Substrate | PBAT |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **0.242 mM** |
| Tier | A_fully_independent |
| Source | PMC12720421 · 10.1002/pro.70402 ·  2026 |

**Recorded evidence:** Table in PMC12720421 — TABLE 3 :: =PpEST | k cat (s−1)=14.0 ± 1.0 | K M (μM)=242 ± 49 | k cat/K M (s−1 M−1)=5.8 × 104

**In the article:** *(context not located — check manually)*

---

### 4. `BMA443B034DB` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ni(2+) |
| Assay | — |
| **Value** | **6.571 s− 1.mM−1** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9606172 · 10.1186/s13568-022-01476-w ·  2022 |

**Recorded evidence:** Table in PMC9606172 — Table 1 :: Status=Ni2+ affinity chromatography | Vol. (mL)=9.0 | Total units=30.95 | Total mg protein=0.837 | Specific activity (U/mg)=36.99 | Fold=11.450 | Yield (%)=71.84 | Km (mM)=0.096 | kcat (s− 1)=63.06 | kcat/Km (s− 1.mM−1)=6.571 × 102

**In the article:** *(context not located — check manually)*

---

### 5. `BME71810CC95` — pH optimum

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
| Source | PMC12428281 · 10.3390/ijms26178141 ·  2025 |

**Recorded evidence:** The results indicated that the optimal pH was 8.0, and DehpH showed relatively high activity ranging from pH 6.0 to pH 9.0.

**In the article:** …optimal conditions for DehpH were proposed thereafter ( Section 4.8 ). The effects of pH on the activity of DehpH were shown in Figure 4 A. The results indicated that the optimal pH was 8.0, and DehpH showed relatively high activity ranging from pH 6.0 to pH 9.0. After incubation at 4 °C under different pH for 1 h, the activity of DehpH decreased significantly under acid conditions (pH 3.0 to 6.0), and DehpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 ( Figure 4 B). The activity of DehpH increased in the temperature range of 10 °C to 30 °C and showed maximum activity at 30 °C ( Figure 4 C). Subseque…

---

### 6. `BM037C0E4939` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | amorphous PET |
| Conditions | pH = 6.0; buffer = sodium acetate (100.0 mM); salt = NaCl @ 100.0 mM; ion = Na(+); salinity = 5.844 g/L; I = 0.1 M (computed from 100.0 mM NaCl) |
| Assay | — |
| **Value** | **6.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9772341 · 10.1038/s41467-022-35237-x ·  2022 |

**Recorded evidence:** For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5).

**In the article:** …s were filtered through 0.2 µm nylon filters for monomer quantitation. All PET hydrolysis screening reactions were performed in triplicate. For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5). The reactions were again stopped at 96 h by the additional of an equal volume of 100% methanol and worked up in the same manner as described directly above. Aromatic product release data are reported throughout relative to bac…

---

### 7. `BM4E1ACC14B4` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AAB51445.1 (genbank_deposit_section_unique) |
| Organism | Streptomyces sp. |
| Mutation | wild-type/unspecified |
| Substrate | olive oil |
| Conditions | pH = 10.0 |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **10.0 pH** |
| Tier | A_fully_independent |
| Source | PMC10707221 · 10.3390/ijms242317071 ·  2023 |

**Recorded evidence:** Results show that the activity of SeLipC was abruptly decreased after incubation at pH 10.0, whereas it was stable when incubated at pH values ranging from 5.0 to 9.5 (Figure 4A).

**In the article:** *(context not located — check manually)*

---

### 8. `BM766A97521D` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | p-nitrophenyl |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **54.2 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12504323 · 10.1007/s00253-025-13605-z ·  2025 |

**Recorded evidence:** Table in PMC12504323 — Table 2 :: =p-nitrophenyl octanoate | Relative activity (%)=54.2 ± 3.8

**In the article:** *(context not located — check manually)*

---

### 9. `BM5E703FE473` — relative activity

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

### 10. `BM052CE598CA` — salinity effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | WP_193237005.1 (genbank_deposit_section_unique) |
| Organism | Vibrio parahaemolyticus |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 23.0 °C; salt = NaCl @ 171.115674 mM; ion = Na(+); salinity = 10.0 g/L; I = 0.171116 M (computed from 171.115674 mM NaCl) |
| Assay | — |
| **Value** | **1.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC12724144 · 10.1128/aem.01652-25 ·  2025 |

**Recorded evidence:** T6SS2 is activated under both cold and warm temperatures (23°C, 30°C, 37°C) in low-salinity (1%NaCl) conditions and positively regulated by ToxR, CalR, TfoX, OpaR, and a new quorum-sensing transcriptional factor QsvR, whereas it is repressed by surface sensing, H-NS, AphA, and CqsA-introduced quorum sensing.

**In the article:** …ed by DNA-binding protein H-NS, transcription regulators ToxR, CalR, and TfoX, as well as the quorum-sensing core regulators OpaR and AphA. T6SS2 is activated under both cold and warm temperatures (23°C, 30°C, 37°C) in low-salinity (1%NaCl) conditions and positively regulated by ToxR, CalR, TfoX, OpaR, and a new quorum-sensing transcriptional factor QsvR, whereas it is repressed by surface sensing, H-NS, AphA, and CqsA-introduced quorum sensing. Diagram illustrates regulation of T6SS1 and T6SS2 in Vibrio parahaemolyticus by environmental factors, surface sensing, DNA-binding protein H-NS, thymidylate kinase, transcription regulators, and quorum sensing pathways. Environmental factors Environmental cue…

---

### 11. `BM21A82FCC0F` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Mg(2+); exposure = 30.0 min |
| Assay | — |
| **Value** | **100.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Full EstRag activity (100%) was retained after 30 min of preincubation with 5 and 10 mM of Mg2+.

**In the article:** …n 2+ , K 2+ , and Mo 2+ separately, EstRag activity decreased significantly (42.883 ± 0.006, 68.71 ± 0.014, and 79.04 ± 0.03%) at P < 0.05. Full EstRag activity (100%) was retained after 30 min of preincubation with 5 and 10 mM of Mg 2+ . Preincubation of EstRag with EDTA at 5 and 10 mM for 30 min resulted in significantly enhanced activity of 196 ± 0.026 and 206.74 ± 0.033%, respectively (Table 2 ). Similarly, after 30 min of preincubation at 5 and 10 mM of β-mercaptoethanol, a significant stimulatory effect on EstRag activity (252.55 ± 0.006 and 225.11 ± 0.053%) was observed (Table 2 ). Table 2 Effect of some metal ions and inhibitors on Es…

---

### 12. `BMBC3CF1571B` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl decanoate (C10) |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **60.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl decanoate (C10) | Abbreviation=pNPD | Specific Activity, U/mg=60 ± 2

**In the article:** *(context not located — check manually)*

---

### 13. `BM49E8DC5804` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ni(2+) |
| Assay | — |
| **Value** | **36.99 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9606172 · 10.1186/s13568-022-01476-w ·  2022 |

**Recorded evidence:** Table in PMC9606172 — Table 1 :: Status=Ni2+ affinity chromatography | Vol. (mL)=9.0 | Total units=30.95 | Total mg protein=0.837 | Specific activity (U/mg)=36.99 | Fold=11.450 | Yield (%)=71.84 | Km (mM)=0.096 | kcat (s− 1)=63.06 | kcat/Km (s− 1.mM−1)=6.571 × 102

**In the article:** *(context not located — check manually)*

---

### 14. `BMAB985596C6` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PBS |
| Conditions | T = 30.0 °C; buffer = PBS; exposure = 1440.0 min |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **30.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9571400 · 10.3390/polym14193978 ·  2022 |

**Recorded evidence:** To determine the optimal temperature to degrade PBS, each microbe was precultured in an optimal liquid medium for 24 h at 30 °C.

**In the article:** …ulture to Monitor PBS Degradation To characterize and optimize each microorganism, clear zone tests with various conditions were performed. To determine the optimal temperature to degrade PBS, each microbe was precultured in an optimal liquid medium for 24 h at 30 °C. Next, paper discs (Toyo Roshi Kaisha, Tokyo, Japan) were placed on the plate [ 36 , 37 ] and 10 μL of precultured cells were inoculated on the paper disc and incubated at 20 °C, 30 °C, 37 °C, and 42 °C for 7 days. We also inoculated the precultured cells on plates with 1% carbon source and 1%, 2%, 3%, and 4% of NaCl concentration and incubated them at 30 °C. The radius of clear zones was confirmed by measuring the d…

---

### 15. `BM15B2B269A0` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | GAP38373.1 (genbank_deposit_section_unique) |
| Organism | Pseudideonella sakaiensis |
| Mutation | wild-type/unspecified |
| Substrate | PET |
| Conditions | T = 58.42 °C |
| Assay | HPLC/UPLC product release |
| **Value** | **58.42 degrees Celsius** |
| Tier | B_in_luke_heldout_test_only |
| Source | PMC10975908 · 10.3390/molecules29061338 ·  2024 |

**Recorded evidence:** This phenomenon was attributed to the higher thermostability of PETaseD186A (Tm = 58.42 °C) than PETaseD186H (Figure 3a) and the significantly higher activity of PETaseD186A than PETaseD186V (Figure 2).

**In the article:** …oncentration of PETase D186A was 1.05- and 1.45-fold higher than that of PETase D186H and PETase D186V , respectively, at 40 °C for 6 days. This phenomenon was attributed to the higher thermostability of PETase D186A ( T m = 58.42 °C) than PETase D186H ( Figure 3 a) and the significantly higher activity of PETase D186A than PETase D186V ( Figure 2 ). Therefore, it could be concluded that the higher product concentrations of PETase D186N and PETase D186H than the wild type at both 30 and 40 °C, especially for PETase D186N , were mainly attributed to the superimposed effects of higher activity and thermos…

---

### 16. `BM1947E30129` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | PET46 |
| UniProt | RLI42440.1 (genbank_unique_in_article) |
| Organism | Candidatus Bathyarchaeota archaeon |
| Mutation | wild-type/unspecified |
| Substrate | PET |
| Conditions | T = 70.0 °C; buffer = MES; salt = NaCl; ion = Na(+) |
| Assay | — |
| **Value** | **70.0 degrees Celsius** |
| Tier | A_fully_independent |
| Source | PMC13316681 · 10.1016/j.bidere.2026.100092 ·  2026 |

**Recorded evidence:** The hierarchical infographic illustrates the integration of three core design principles: (A) lid-domain promiscuity of archaeal extremozymes (PET46 and GuaPA) enabling efficient polymer and oligomer access under polyextreme conditions, (B) syntrophic cross-feeding with bacterial partners (exchange of hydrolytic products, cofactors, and reducing equivalents for complete mineralisation and methanogenesis), and (C) inherent polyextreme robustness (

**In the article:** …The Polyextreme Archaeal Syntrophy Framework: A Biodesign Strategy for Plastic Bioremediation in Extreme and Extraterrestrial Environments. The hierarchical infographic illustrates the integration of three core design principles: (A) lid-domain promiscuity of archaeal extremozymes (PET46 and GuaPA) enabling efficient polymer and oligomer access under polyextreme conditions, (B) syntrophic cross-feeding with bacterial partners (exchange of hydrolytic products, cofactors, and reducing equivalents for complete mineralisation and methanogenesis), and (C) inherent polyextreme robustness (thermostability up to 70 °C, halotolerance >200 g L -1 NaCl, anaerobiosis, pressure adaptation, radiation resistance, an…

---

### 17. `BMABF0611CAE` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = methanol |
| Assay | — |
| **Value** | **89.22 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 3 :: Organic solvent=Methanol | Residual activity (%) at=89.22 ± 0.011 | Log Pa=89.22 ± 0.011

**In the article:** *(context not located — check manually)*

---

### 18. `BMD0D805E25E` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | — |
| **Value** | **657.7 sec−1 mM−1** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 4 :: p-NP esters=p-NP-C2 | Specific activity (U/mg)=0.470 ± 0.0002 | Relative activity (%)=100.00 | Km (mM)=0.031 | Kcat (sec−1)=20.39 | Kcat/Km (sec−1 mM−1)=657.7

**In the article:** *(context not located — check manually)*

---

### 19. `BMB0000F0212` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ni(2+) |
| Assay | — |
| **Value** | **0.096 mM** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9606172 · 10.1186/s13568-022-01476-w ·  2022 |

**Recorded evidence:** Table in PMC9606172 — Table 1 :: Status=Ni2+ affinity chromatography | Vol. (mL)=9.0 | Total units=30.95 | Total mg protein=0.837 | Specific activity (U/mg)=36.99 | Fold=11.450 | Yield (%)=71.84 | Km (mM)=0.096 | kcat (s− 1)=63.06 | kcat/Km (s− 1.mM−1)=6.571 × 102

**In the article:** *(context not located — check manually)*

---

### 20. `BM097BED1F73` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PET |
| Conditions | pH = 7.0; buffer = potassium phosphate (100.0 mM); additive = Tween-80 |
| Assay | — |
| **Value** | **7.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC8767016 · 10.3389/fmicb.2021.803896 ·  2021 |

**Recorded evidence:** Concerning the optimal pH, PET27 was most active between pH 7–8 and PET30 between pH 6-8 when tested in 0.1 M potassium phosphate (Figure 3C).

**In the article:** …till showed a relative activity of 65% (PET30) and 73% (PET27). PET30 remained active at 4°C showing a relative activity of 42% on p NP-C6. Concerning the optimal pH, PET27 was most active between pH 7-8 and PET30 between pH 6-8 when tested in 0.1 M potassium phosphate ( Figure 3C ). FIGURE 3 Biochemical characterization of PET27 and PET30 using p NP-substrates. Data represent mean values of at least three independent samples. Substrate preference (A) was tested with p NP-butyrate (-C4) to -stearate (-C18). Temperatures (B) and pH (C) were tested with p NP-octanoate (-C8) for PET27 and with p NP-hexanoate (-C6) for PET30. All assays except B …

---

### 21. `BME7E3DA9213` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 4.0 °C; pH = 3.0; exposure = 60.0 min |
| Assay | — |
| **Value** | **3.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12428281 · 10.3390/ijms26178141 ·  2025 |

**Recorded evidence:** After incubation at 4 °C under different pH for 1 h, the activity of DehpH decreased significantly under acid conditions (pH 3.0 to 6.0), and DehpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 (Figure 4B).

**In the article:** … in Figure 4 A. The results indicated that the optimal pH was 8.0, and DehpH showed relatively high activity ranging from pH 6.0 to pH 9.0. After incubation at 4 °C under different pH for 1 h, the activity of DehpH decreased significantly under acid conditions (pH 3.0 to 6.0), and DehpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 ( Figure 4 B). The activity of DehpH increased in the temperature range of 10 °C to 30 °C and showed maximum activity at 30 °C ( Figure 4 C). Subsequently, the activity of DehpH decreased in the temperature range from 30 °C to 80 °C, and DehpH almost lost its activity under 80 °C. The thermostability…

---

### 22. `BMF83F2E9732` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | P26495 (accession_unique_in_article) |
| Organism | Ectopseudomonas oleovorans |
| Mutation | wild-type/unspecified |
| Substrate | PHBV |
| Conditions | — |
| Assay | — |
| **Value** | **70.82 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC10003648 · 10.3390/ijms24054501 ·  2023 |

**Recorded evidence:** Table in PMC10003648 — Table 3 :: Substrate=PHBV | Relative Activity (%) *=70.82 ± 3.6

**In the article:** *(context not located — check manually)*

---

### 23. `BMDDF8F750C0` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = NaCl; ion = Na(+) |
| Assay | — |
| **Value** | **1.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Table in PMC12898461 — Table 5 :: [NaCl] (M)=Ces1-ET | Relative Activity (%)=Est1-ET

**In the article:** *(context not located — check manually)*

---

### 24. `BM6D04EE6237` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | PHAZ |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = FeCl3; ion = Fe(3+) |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **87.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC4624153 · 10.1007/s13205-015-0287-4 ·  2015 |

**Recorded evidence:** Table in PMC4624153 — Table 2 :: Reagent=FeCl3 | Relative activity (%)=87

**In the article:** *(context not located — check manually)*

---

### 25. `BMDF3E9FE6E2` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | 4-Nitrophenyl acetate (C2) |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **16.0 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12896513 · 10.3390/biology15030276 ·  2026 |

**Recorded evidence:** Table in PMC12896513 — Table 3 :: Substrate=4-Nitrophenyl acetate (C2) | Abbreviation=pNPA | Specific Activity, U/mg=16 ± 1

**In the article:** *(context not located — check manually)*

---

### 26. `BM637F2110DA` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | Est1 |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 80.0 °C; additive = Tween-80 |
| Assay | — |
| **Value** | **80.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Est1-ET exhibited more than 70% activity between 60 and 80 °C, with optimal activity at 80 °C.

**In the article:** … of Ces1-ET activity was maintained above 50% between 40 and 70 °C, with an optimum at 60 °C, but retained less than 20% activity at 90 °C. Est1-ET exhibited more than 70% activity between 60 and 80 °C, with optimal activity at 80 °C. At 90 °C, Est1-ET retained approximately 50% activity. Plp1-ET showed catalytic activity between 40 and 90 °C, with an optimum at 70 °C, and retained nearly 50% activity at 80 °C and less than 20% at 90 °C ( Figure 4 A). Figure 4 Properties of Ces1-ET, Est1-ET, and Plp1-ET expressed in E. coli . ( A ) Effect of temperature on enzymatic activity in the range of 40-90 °C. ( B ) Effect of pH on enzyme activity using 50…

---

### 27. `BM712AA556EA` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 51.0 °C |
| Assay | — |
| **Value** | **51.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC7031157 · 10.3389/fmicb.2020.00114 ·  2020 |

**Recorded evidence:** The reduced activity of the variants was accompanied by a decrease in melting temperature of about 5–10°C (Supplementary Table S2) in comparison to the wild type enzyme (Tm at about 51°C), indicating a destabilizing effect of the mutations.

**In the article:** …t with the combined mutations also showed a significantly decreased esterase activity determined with p NPB as the substrate ( Figure 3A ). The reduced activity of the variants was accompanied by a decrease in melting temperature of about 5-10°C ( Supplementary Table S2 ) in comparison to the wild type enzyme (T m at about 51°C), indicating a destabilizing effect of the mutations. Variant PE-H S256N, I257S, and Y250S showed a less drastic decrease in melting temperature of about 1-3°C. FIGURE 3 Enzymatic activity of PE-H and different variants constructed by site directed mutagenesis. Substrates were (A) 4-nitrophenyl butyrate ( p NPB), (B) b…

---

### 28. `BM281585599B` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | Cut190 |
| UniProt | BAO42836.1 (genbank_deposit_section_unique) |
| Organism | Saccharomonospora viridis |
| Mutation | S184P/R186S |
| Substrate | PLA |
| Conditions | T = 60.0 °C; ion = Ca(2+); exposure = 3.1 min |
| Assay | HPLC/UPLC product release |
| **Value** | **60.0 degrees Celsius** |
| Tier | B_in_luke_heldout_test_only |
| Source | PMC9321771 · 10.1002/cssc.202102750 ·  2022 |

**Recorded evidence:** The combination of Ca2+ and sucrose played an important stabilizing role in Cut190 S184P/R186S, helping the enzyme keep 25 % of residual activity after 96 h at 60 °C as observed in Figure 6, without interfering with the coupled assay (Figure S5).

**In the article:** *(context not located — check manually)*

---

### 29. `BM4907679167` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | QIT07223.1 (genbank_unique_in_article) |
| Organism | Lysinibacillus sp. |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | additive = beta-mercaptoethanol |
| Assay | — |
| **Value** | **252.55 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC9452428 · 10.1007/s11274-022-03402-5 ·  2022 |

**Recorded evidence:** Table in PMC9452428 — Table 2 :: Effector=Β-mercaptoethanol | Residual activity (%) at=252.55 ± 0.006

**In the article:** *(context not located — check manually)*

---

### 30. `BM31156AC87C` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | MYD18970.1 (genbank_unique_in_article) |
| Organism | Rhodothermaceae bacterium |
| Mutation | wild-type/unspecified |
| Substrate | PBAT |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **0.257 mM** |
| Tier | A_fully_independent |
| Source | PMC12720421 · 10.1002/pro.70402 ·  2026 |

**Recorded evidence:** Table in PMC12720421 — TABLE 3 :: =shRp_EST | k cat (s−1)=25.0 ± 1.6 | K M (μM)=257 ± 43 | k cat/K M (s−1 M−1)=9.7 × 104

**In the article:** *(context not located — check manually)*

---

### 31. `BM34567040FA` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 7.5; additive = Tween-80 |
| Assay | — |
| **Value** | **7.5 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** In contrast, Plp1-ET showed more than 50% relative activity between pH 7.5 and 8.5, with its highest activity at pH 8.0 (Figure 4B).

**In the article:** …, Est1-ET revealed that the enzyme displays more than 50% relative activity within the pH range 7.0-9.0, with a maximum activity at pH 9.0. In contrast, Plp1-ET showed more than 50% relative activity between pH 7.5 and 8.5, with its highest activity at pH 8.0 ( Figure 4 B). 2.7. Kinetic Parameters of Enzymatic Activity The kinetic properties of the recombinant esterases Ces1-ET, Est1-ET, and Plp1-ET, as presented in Table 3 , reveal minor differences in their catalytic efficiencies and substrate affinities. Ces1-ET exhibits a maximum reaction velocity ( Vmax ) of 15 ± 4 μmoles p -nitrophenol/10 min/1 µg protein. In contrast, Est1-ET exhibits …

---

### 32. `BMC31B27FC98` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AOT80658.1 (hand_curated_from_article) |
| Organism | Bacillus licheniformis |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 10.0 |
| Assay | — |
| **Value** | **10.0 pH** |
| Tier | A_fully_independent |
| Source | PMC11651597 · 10.1371/journal.pone.0314556 ·  2024 |

**Recorded evidence:** However, exposure to pH 10 resulted in a marked decrease in activity, with only 51% residual activity observed after one h, and further decline to 22% at pH 11.

**In the article:** …ates that it remained stable between pH 6 and pH 9, retaining between 89% and 97% of its residual activity after 1 h of incubation at 35°C. However, exposure to pH 10 resulted in a marked decrease in activity, with only 51% residual activity observed after one h, and further decline to 22% at pH 11. Subsequently, the stability of MLipA was evaluated across pH levels of 6, 7, and pH 8 ( Fig 5B ). It exhibited the highest stability at pH 6 and pH 7, retaining 43% and 49% of its original activity, respectively, following 24 h of incubation at 35°C. Conversely, a substantial decrease in activity was observed at pH 8, with only 15% of the original activity remaining after 24 h. Effect of organic solvents o…

---

### 33. `BMAAE131A47B` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | polycaprolactone (PCL) |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **100.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC10046884 · 10.3390/biotech12010023 ·  2023 |

**Recorded evidence:** Table in PMC10046884 — Table 2 :: Metal Ions (5 mM)=Control | Relative Activity (%)=100 | Detergents, Inhibitors (5 mM)=Control | Relative Activity (%)=100

**In the article:** *(context not located — check manually)*

---

### 34. `BMFB6811A97F` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = NaCl @ 50.0 mM; ion = Na(+); salinity = 2.922 g/L; I = 0.05 M (computed from 50.0 mM NaCl) |
| Assay | — |
| **Value** | **110.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9065602 · 10.3389/fbioe.2022.854298 ·  2022 |

**Recorded evidence:** Table in PMC9065602 — TABLE 5 :: Modulators/reagents=NaCl | Final concentration=50 mM | Relative activity (%)=110 ± 1.1

**In the article:** *(context not located — check manually)*

---

### 35. `BMB86D05DF98` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = BaCl2; ion = Ba(2+) |
| Assay | — |
| **Value** | **111.0 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Table in PMC12898461 — Table 4 :: =BaCl2 | Relative Activity (%)=111 ± 14

**In the article:** *(context not located — check manually)*

---

### 36. `BMF21EE1D855` — specific activity

| Field | Recorded |
|---|---|
| Enzyme | IsPETase-Pp |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | MHET |
| Conditions | — |
| Assay | — |
| **Value** | **20.6 U/mg (as reported)** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9839772 · 10.1038/s42003-023-04413-0 ·  2023 |

**Recorded evidence:** Table in PMC9839772 — Table 1 :: Enzyme=IsPETase-Pp | TPA (mM)=0.2492 ± 0.0061 | MHET (mM)=0.0386 ± 0.0011 | Percentage of TPA (%)=86.60 ± 0.06 | specific activity (U/mg)=20.6 ± 0.74

**In the article:** *(context not located — check manually)*

---

### 37. `BM3839963246` — temperature optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | PET |
| Conditions | T = 37.0 °C; buffer = MES |
| Assay | weight loss / gravimetric |
| **Value** | **37.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC12871986 · 10.1371/journal.pone.0341623 ·  2026 |

**Recorded evidence:** The mesophilic operating conditions (37 °C) and optimized degradation efficiency of 11.15% demonstrate practical potential for PET-MP bioremediation in temperate environments where energy-intensive thermophilic treatments would be less feasible.

**In the article:** …he optimization-dependent nature of PET-MP biodegradation influenced by enzyme activity, substrate availability, and environmental factors. The mesophilic operating conditions (37 °C) and optimized degradation efficiency of 11.15% demonstrate practical potential for PET-MP bioremediation in temperate environments where energy-intensive thermophilic treatments would be less feasible. Characterization of PET-MP degradation by FTIR, SEM, and GC-MS To confirm the PET-MP degradation efficiency discussed previously, FTIR and GC-MS analyses were performed on the three most efficient strains (PETKKU2, PETKKU6, and PETKKU10) to examine chemical modifications and degradation by-products. In addition, SEM analys…

---

### 38. `BM87B4F8D322` — thermostability

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | T = 37.0 °C |
| Assay | — |
| **Value** | **37.0 degrees Celsius** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC11270687 · 10.1021/acsomega.4c04843 ·  2024 |

**Recorded evidence:** We further monitored the long-term stability of PD3, PD5, and PD8 by storing them at 37 or 42 °C and periodically checked their activities at 37 °C.

**In the article:** … data represent n = 3 technical replicates. Two-way ANOVA; ns, p > 0.05, * p < 0.1, ** p < 0.01. Error bars represent ± standard deviation. We further monitored the long-term stability of PD3, PD5, and PD8 by storing them at 37 or 42 °C and periodically checked their activities at 37 °C. Interestingly, PD3 exhibited increased esterase activity during the first week at 37 °C, which then returned to its original level after one month, retaining 79.0% activity after 4 months of incubation at 37 °C. Conversely, when stored at 42 °C for 1 week, PD3's activity significantly decreased, retaining only 56.4% activity ( Figure 2 C). PD5 and PD8 maintained their activity at 37 °C for at least two months, where…

---

### 39. `BMC6CE585496` — inhibition

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | polycaprolactone (PCL) |
| Conditions | additive = Tween-80 |
| Assay | — |
| **Value** | **86.8 % relative activity** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC8971842 · 10.3389/fbioe.2022.835847 ·  2022 |

**Recorded evidence:** Table in PMC8971842 — TABLE 3 :: Organic solvent=Tween-80 | Residual activity (%)=86.80 ± 0.20

**In the article:** *(context not located — check manually)*

---

### 40. `BMBA7CDC29DB` — kinetic constant

| Field | Recorded |
|---|---|
| Enzyme | Est1-ET |
| UniProt | XPQ45697.1 (hand_curated_from_article) |
| Organism | Thermus thermophilus |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | — |
| Assay | spectrophotometric p-nitrophenol release |
| **Value** | **0.2 mM** |
| Tier | A_fully_independent |
| Source | PMC12898461 · 10.3390/ijms27031372 ·  2026 |

**Recorded evidence:** Table in PMC12898461 — Table 3 :: Enzyme=Est1-ET | Vmax(µmoles p-Nitrophenol/10 min)=13 ± 2 | Km (mM)=0.20 ±0.01

**In the article:** *(context not located — check manually)*

---

### 41. `BM2646680E59` — pH optimum

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | — (unresolved) |
| Organism | — |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | pH = 6.0; buffer = MES |
| Assay | — |
| **Value** | **6.0 pH** |
| Tier | C_conditions_only_no_sequence |
| Source | PMC9772341 · 10.1038/s41467-022-35237-x ·  2022 |

**Recorded evidence:** For the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715), we further extended the pH screen.

**In the article:** …here is a breadth of activity across the pH and temperature ranges studied, with activity of at least one enzyme in every condition tested. For the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715), we further extended the pH screen. As shown in Supplementary Fig. 4 , the ICCG variant of LCC is active in buffered medium with a pH as low as 5.0, while 102 was not active at pH below 6.0, and 611, 702, and 715 all exhibit detectable activity at pH <6.0. Characterization of the best-performing enzymes highlights reactivity differences as a function of substrate We were also interested to learn if the best-performing enzymes from each phylogenetic gr…

---

### 42. `BM800815CC90` — pH stability

| Field | Recorded |
|---|---|
| Enzyme | IsPETase |
| UniProt | RLI42440.1 (genbank_unique_in_article) |
| Organism | Candidatus Bathyarchaeota archaeon |
| Mutation | wild-type/unspecified |
| Substrate | PET powder |
| Conditions | T = 70.0 °C; pH = 5.0 |
| Assay | — |
| **Value** | **5.0 pH** |
| Tier | A_fully_independent |
| Source | PMC13316681 · 10.1016/j.bidere.2026.100092 ·  2026 |

**Recorded evidence:** BHET, MHET oligomers; feruloyl estersComparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer70 °C/broad pH 5–8; thermostable at 60 °C for prolonged incubationUnique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding;

**In the article:** *(context not located — check manually)*

---

### 43. `BM3F0981E8AC` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | P26495 (accession_unique_in_article) |
| Organism | Ectopseudomonas oleovorans |
| Mutation | wild-type/unspecified |
| Substrate | LIP3 |
| Conditions | — |
| Assay | — |
| **Value** | **4.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC10003648 · 10.3390/ijms24054501 ·  2023 |

**Recorded evidence:** Table in PMC10003648 — Table 3 :: Substrate=LIP3 | Relative Activity (%) *=LIP4

**In the article:** *(context not located — check manually)*

---

### 44. `BME0758EF792` — relative activity

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | P26495 (accession_unique_in_article) |
| Organism | Ectopseudomonas oleovorans |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | salt = CaCl2; ion = Ca(2+) |
| Assay | — |
| **Value** | **93.0 % relative activity** |
| Tier | A_fully_independent |
| Source | PMC10003648 · 10.3390/ijms24054501 ·  2023 |

**Recorded evidence:** Table in PMC10003648 — Table 2 :: Modulators/Reagents=CaCl2 | Final Concentration=1 mmol L−1 | Relative Activity (%) *=93 ± 2.5

**In the article:** *(context not located — check manually)*

---

### 45. `BMA1AAAC0297` — salt effect

| Field | Recorded |
|---|---|
| Enzyme | — |
| UniProt | AOT80658.1 (hand_curated_from_article) |
| Organism | Bacillus licheniformis |
| Mutation | wild-type/unspecified |
| Substrate | — |
| Conditions | ion = Ca(2+) |
| Assay | — |
| **Value** | **5.0 mM** |
| Tier | A_fully_independent |
| Source | PMC11651597 · 10.1371/journal.pone.0314556 ·  2024 |

**Recorded evidence:** However, at a higher concentration of 5 mM, both Cu2+ and Co2+ caused a significant inhibition of lipase activity, while Ca2+ and Ba2+ only had a slight inhibitory effect.

**In the article:** …, 43 ]. In addition to Ca 2+ , Ba 2+ showed only a slight increase in activity of lipase, while Cu 2+ and Co 2+ had minimal effect at 1 mM. However, at a higher concentration of 5 mM, both Cu 2+ and Co 2+ caused a significant inhibition of lipase activity, while Ca 2+ and Ba 2+ only had a slight inhibitory effect. However, when the concentration of the metal ion rose, the presence of Mg 2+ led to an increase in lipase activity, which is consistent with the results of Olusesan et al., who observed that Mg 2+ marginally stimulated B . subtilis NS-8 lipase [ 104 ]. The lipase activity of MLipA was negative…

---

