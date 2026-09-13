# Exclusion review packet

All 37 excluded candidates, each printed beside the freshly downloaded article text and the section heading it sits under.

`CONFIRMED` / `CHALLENGED` are automated cross-checks of the rule that fired; they are evidence for a human decision, not the decision.

---


## PMC10003648 — research-article

*Polymer-Degrading Enzymes of Pseudomonas chloroaphis PA23 Display Broad Substrate Preferences*


### BME732B05FC1 — dropped by `PH-X3`

- **was**: pH stability @ pH 5.0 = 5.0 pH
- **section**: 2. Results / 2.3. Characterization of the Recombinant LIP3, LIP4, and PhaZ
- **check**: enzyme-like tokens in the quote: ['LIP4']
- **reason given**: Accession P26495 is PhaZ, but the evidence sentence is about LIP4: 'LIP4 retained more activity (>80%) at pH 5.0-6.0'. A tier-A sequence misattribution -- the worst class of defect a benchmark can carry.
- **quote**: However, LIP4 retained more activity (>80%) atpH 5.0–6.0 compared with activity at an alkaline pH 8.0–10.0 (<40%).

```
osed and lacks the closing lid domain. ¶ To better illustrate the substrate binding pocket, the closing lid domain is not shown in Supplementary Figures S1B and S2B. It should also be noted that Supplementary Figures S1C, S2C and S3C present the surface of the lipases and PhaZ, clearly showing that the substrate binding pocket for LIP3 and LIP4 is buried by the lid domain. The binding energy for the substrate to LIP3, LIP4, and PhaZ determined in the docking experiment was calculated to be -6.2 kcal/mol, -5.8 kcal/mol, and -5.7 kcal/mol, respectively.A negative free energy of binding means that the substrates dock spontaneously. ¶ ¶ 2.3. Characterization of the Recombinant LIP3, LIP4, and PhaZ ¶ LIP3, LIP4, and PhaZ were active over a wide pH range (pH 4.0 to 10.0) with optimal activity at pH 8.0 for LIP3 and PhaZ, and pH 6.0 for LIP4 (Figure 6A). LIP3 and PhaZ retained more than 50% of their activity over a pH range from 7.0 to 9.0, with PhaZ showing higher relative activity at pH 8.0-10.0. However, LIP4 retained more activity (>80%) atpH 5.0-6.0 compared with activity at an alkaline pH 8.0-10.0 (<40%). ¶ LIP3, LIP4, and PhaZ were optimally active at 45 °C to 50 °C and retained more than 70% activity when the reaction was performed at 55 °C (Figure 6B). In addition, thermal inactivation experiments showed that the enzymes retained nearly 70% activity for 24 h at 45 °C (Figure 6C). LIP3 and PhaZ, on the other hand, were very stable and retained more than 80% of their activity for 24 h at 45 °C. LIP3 exhibited higher activation energy (Ea = 28.2 KJ mol-1) than LIP4 (26.4 KJ mol-1) and PhaZ (19.9 KJ mol-1) for the thermo-inactivation process within the temperature range of 25-50 °C. ¶ When pNP-octanoate was used as a substrate, the purified enzymes were found to be very stable and retained almost 100% of their activities after four months of incubation at 4 °C and two months of incubation at 30 °C. The pNP-octanoate was also used as a substrate to determine the kinetics of each enzyme. The Vmax and Km for LIP3 were 625.0 μM mg-1 min-1 and 0.375 mmol L-1, respectively; the Vmax a
```


## PMC10146679 — research-article

*Rational Design of Disulfide Bridges in BbPETaseCD for Enhancing the Enzymatic Performance in PET Degradation*


### BM06A72D7AB0 — dropped by `PH-X9`

- **was**: pH stability @ pH 7.0 = 7.0 pH
- **section**: 2. Results and Discussion / 2.2. Activity and Stability of BbPETaseCD and Its Variants
- **reason given**: pH 7.0 is the assay condition of a thermal statement; no pH-stability measurement.
- **quote**: At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature.

```
e S4b,c demonstrates that the bacterial lysates and precipitates of all the four variants except the N364C/D418C variant contain darker bands around 30 kDa, while their supernatants obtained after centrifugation have only very light bands around 30 kDa. This indicates that all the four variants produced many inclusion bodies during the expression. This result confirmed our conjecture that the four variants were less expressed in soluble form. ¶ ¶ 2.2. Activity and Stability of BbPETaseCD and Its Variants ¶ The activity of BbPETaseCD and its variants was evaluated using bis(Hydroxyethyl) Terephthalate (BHET) as substrate. The N364C/D418C variant had the highest activity in most cases, and no significant difference was observed between the other variants (Figure 1). At pH 9.0, the activity increased with increasing temperature. Meanwhile, at each temperature tested (30, 40, 50 °C), the activity at pH 9.0 was higher than that at pH 7.0, indicating that pH 9.0 is more suitable for the reaction. At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature. ¶ To evaluate the thermal stability, these enzymes were then incubated at 50 °C for 1, 2, 4, and 6 h following by the examination of residual activity. Meanwhile, these enzymes were incubated for 1, 2, 4, 6, 9, 12, and 24 h at 40 °C (the temperature used for the long reaction time in PET degradation experiments). The residual activity of these enzymes decreased as the temperature of the incubation increased, but the magnitude of the decrease varied. At both 40 °C and 50 °C, the residual activity of the N364C/D418C variant was higher than that of the BbPETaseCD (Figure 2a,b). The optimal reaction pH for BbPETaseCD and its variants is mostly alkaline. Therefore, these enzymes are more able to maintain their activity at pH 9.0. The Tm values of these enzymes were obtained by CD (Figure S5), which showed that the Tm value of the N364C/D418C variant was 71.3 °C (Figure 2c), significantly higher than that of the BbPETaseCD (56.5 °C) and other variants. Compared to the Tm value of BbP
```


### BM9DD54D4438 — dropped by `PH-X9`

- **was**: thermostability @ pH 7.0 = 30.0 degrees Celsius
- **section**: 2. Results and Discussion / 2.2. Activity and Stability of BbPETaseCD and Its Variants
- **reason given**: 'activity increased from 30 deg C to 40 deg C' -- 30 is a profile boundary, not a thermostability value.
- **quote**: At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature.

```
e S4b,c demonstrates that the bacterial lysates and precipitates of all the four variants except the N364C/D418C variant contain darker bands around 30 kDa, while their supernatants obtained after centrifugation have only very light bands around 30 kDa. This indicates that all the four variants produced many inclusion bodies during the expression. This result confirmed our conjecture that the four variants were less expressed in soluble form. ¶ ¶ 2.2. Activity and Stability of BbPETaseCD and Its Variants ¶ The activity of BbPETaseCD and its variants was evaluated using bis(Hydroxyethyl) Terephthalate (BHET) as substrate. The N364C/D418C variant had the highest activity in most cases, and no significant difference was observed between the other variants (Figure 1). At pH 9.0, the activity increased with increasing temperature. Meanwhile, at each temperature tested (30, 40, 50 °C), the activity at pH 9.0 was higher than that at pH 7.0, indicating that pH 9.0 is more suitable for the reaction. At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature. ¶ To evaluate the thermal stability, these enzymes were then incubated at 50 °C for 1, 2, 4, and 6 h following by the examination of residual activity. Meanwhile, these enzymes were incubated for 1, 2, 4, 6, 9, 12, and 24 h at 40 °C (the temperature used for the long reaction time in PET degradation experiments). The residual activity of these enzymes decreased as the temperature of the incubation increased, but the magnitude of the decrease varied. At both 40 °C and 50 °C, the residual activity of the N364C/D418C variant was higher than that of the BbPETaseCD (Figure 2a,b). The optimal reaction pH for BbPETaseCD and its variants is mostly alkaline. Therefore, these enzymes are more able to maintain their activity at pH 9.0. The Tm values of these enzymes were obtained by CD (Figure S5), which showed that the Tm value of the N364C/D418C variant was 71.3 °C (Figure 2c), significantly higher than that of the BbPETaseCD (56.5 °C) and other variants. Compared to the Tm value of BbP
```


### BMAD704A1BA4 — dropped by `PH-X9`

- **was**: thermostability @ pH 7.0 = 40.0 degrees Celsius
- **section**: 2. Results and Discussion / 2.2. Activity and Stability of BbPETaseCD and Its Variants
- **reason given**: Same sentence; 40 is the other profile boundary.
- **quote**: At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature.

```
e S4b,c demonstrates that the bacterial lysates and precipitates of all the four variants except the N364C/D418C variant contain darker bands around 30 kDa, while their supernatants obtained after centrifugation have only very light bands around 30 kDa. This indicates that all the four variants produced many inclusion bodies during the expression. This result confirmed our conjecture that the four variants were less expressed in soluble form. ¶ ¶ 2.2. Activity and Stability of BbPETaseCD and Its Variants ¶ The activity of BbPETaseCD and its variants was evaluated using bis(Hydroxyethyl) Terephthalate (BHET) as substrate. The N364C/D418C variant had the highest activity in most cases, and no significant difference was observed between the other variants (Figure 1). At pH 9.0, the activity increased with increasing temperature. Meanwhile, at each temperature tested (30, 40, 50 °C), the activity at pH 9.0 was higher than that at pH 7.0, indicating that pH 9.0 is more suitable for the reaction. At pH 7.0, the activity of BbPETaseCD increased from 30 °C to 40 °C, and then decreased when the temperature increased to 50 °C, indicating the poor stability of BbPETaseCD at high temperature. ¶ To evaluate the thermal stability, these enzymes were then incubated at 50 °C for 1, 2, 4, and 6 h following by the examination of residual activity. Meanwhile, these enzymes were incubated for 1, 2, 4, 6, 9, 12, and 24 h at 40 °C (the temperature used for the long reaction time in PET degradation experiments). The residual activity of these enzymes decreased as the temperature of the incubation increased, but the magnitude of the decrease varied. At both 40 °C and 50 °C, the residual activity of the N364C/D418C variant was higher than that of the BbPETaseCD (Figure 2a,b). The optimal reaction pH for BbPETaseCD and its variants is mostly alkaline. Therefore, these enzymes are more able to maintain their activity at pH 9.0. The Tm values of these enzymes were obtained by CD (Figure S5), which showed that the Tm value of the N364C/D418C variant was 71.3 °C (Figure 2c), significantly higher than that of the BbPETaseCD (56.5 °C) and other variants. Compared to the Tm value of BbP
```


## PMC10385968 — research-article

*Enzymatic Characterization of a Novel HSL Family IV Esterase EstD04 from Pseudomonas sp. D01 in Mealworm Gut Microbiota*


### BMC71D9F94EF — dropped by `PH-X10`

- **was**: pH optimum @ pH 8.0 = 8.0 pH
- **section**: 2. Results / 2.4. Effects of Substrate Chain Length, Temperature, and pH Value on EstD04 Activity and Stability as Well as the Enzyme’s Kinetic Analyses
- **check**: CONFIRMED: a shipped row covers ('PMC10385968', 'pH optimum', '8.0')
- **reason given**: pH optimum 8.0 for EstD04 restated in the kinetics sentence -- same enzyme, paper, type and value as BMBE4B247046, which comes from the direct statement.
- **quote**: By using the optimal conditions for its function, we analyzed the kinetics of EstD04 for the hydrolysis of C4 substrates at 40 °C and pH 8.

```
05410-g006.gif?>?cloudpmc-bucket cdn?>Next, we determined the optimal temperature and pH for the EstD04 esterase function. The different temperatures used to measure the activity of EstD04 were between 20 °C-70 °C. As shown in Figure 6B, EstD04 exhibited optimal enzymatic activity at 40 °C. Moreover, between 20 °C and 40 °C, the enzyme was stable and retained over 82% activity. However, the stability of EstD04, measured by the tolerance of the enzyme to different temperatures, dropped drastically between 50 °C to 70 °C (Figure 6B). The optimal pH for EstD04 activity was pH 8. Finally, we also demonstrated the pH stability (or tolerance) of EstD04 esterase by measuring its enzymatic activity after pre-incubation with buffers of various pH values (Figure 6C). EstD04 exhibited favorable pH stability between pH 8 to pH 11, in which the enzyme retained at least 80% activity. The maximal stability was maintained at pH 10 (Figure 6C), suggesting that this enzyme could be an alkaline lipolytic enzyme. ¶ By using the optimal conditions for its function, we analyzed the kinetics of EstD04 for the hydrolysis of C4 substrates at 40 °C and pH 8. The Km, Vmax, and kcat values were determined as 0.488 ± 0.001 mM, 64.4 ± 0.9 μMmin-1, and 3.01 × 103 ± 40 s-1, respectively. The enzyme efficiency, kcat/Km value, was thus calculated to be 6.17 × 103 mM-1 s-1 (Figure 6D). ¶ ¶ 2.5. Effects of Cations, Organic Solvents, and Detergents on EstD04 Activity ¶ Effects of cations on EstD04 activity are demonstrated in Figure 7A. Compared to the standard determination condition, the enzyme activity of EstD04 increased to about 110% and 115%, respectively, with the addition of Mg2+ or NH4+ to the reaction. EstD04 possessed approximately 80% activity in the presence of metal ions Mn2+, Ni2+, Na+, Ca2+, or Co2+. On the other hand, it was noticed that Zn2+ partially inhibited the catalytic activity of EstD04, and Cu2+, Fe2+, and Fe3+ strongly inhibited the EstD04 enzyme activity (Figure 7A). All of these metal ions were added to the reaction medium at a concentration of 2 mM. Thus, in this study, some of the inhibitory activities we
```


## PMC10495362 — research-article

*An archaeal lid-containing feruloyl esterase degrades polyethylene terephthalate*


### BM0578A48B89 — dropped by `PH-X7;PH-X3`

- **was**: pH optimum @ pH 6.0 = 6.0 pH
- **section**: Discussion
- **check**: CONFIRMED: secondhand marker in the quote (article is a research-article)
- **check**: enzyme-like tokens in the quote: ['PET46']
- **reason given**: 'In their study, the PET46-like 211 released ...' -- a secondhand sentence about a different enzyme (PET46-like 211), carrying PET46's accession RLI42440.1.
- **quote**: In their study, the PET46-like 211 released up to 85.23 mg L−1 aromatic products from crystalline PET powder at 60 °C and pH6 (optimal conditions).

```
mily with FAEs, and they bear a lid domain of varying length. They can hydrolyze MHET into TPA and EG. One of the best-studied examples is the MHETase derived from the gram-negative bacterium I. sakaiensis (IsMHETase). This enzyme acts efficiently on MHET, but recently an exo-function on PET pentamers was described64. It also hydrolyzed BHET in a concentration-dependent manner, and its three-dimensional structure shows a much larger lid domain involving more than 200 aa (Supplementary Fig. 5). A new study by Erickson et al.60 searched for new thermotolerant PET hydrolase scaffolds following a similar searching strategy as in our study. They reported the metagenome-derived enzymes 204 and 211, but did not investigate their taxonomic affiliation nor their conserved domains in detail. PETase 204 is 97.93% identical to WP_187147021.1 and WP_148684612.1 from Thermophilum adornatum, while 211 is 99.62% identical to MBS7639053.1 from a Cand. Bathyarchaeota archaeon, both archaea. PET46 shares 34.92% and 65.78% sequence identity, respectively (Fig. 1), but their structure is very similar (Supplementary Fig. 11). In their study, the PET46-like 211 released up to 85.23 mg L-1 aromatic products from crystalline PET powder at 60 °C and pH6 (optimal conditions). This equals to 0.52 mM assuming all of it is TPA, which is less but in the range of the amount of product that we measured with PET46 (1.6 mM; Fig. 4). As for PET46, no activity was detected on amorphous PET foil. ¶ PET46 is encoded in a marine Bathyarcheota MAG. Microorganisms affiliated with the Bathyarchaeota are globally occurring and widespread in marine and terrestrial anoxic sediments65. They can use a wide range of polymers as carbon and energy sources, and they are well known to be very versatile with respect to metabolic capabilities. They are further known to be abundant in some marine sediments. Because of their huge metabolic potential, it is further assumed that they may play a significant role in global carbon biogeochemical cycling65-68. Interestingly, Bathyarcheota have been associated with the degradation of the biopolymer lignocellulose previousl
```


### BM6A82469C45 — dropped by `PH-X7;PH-X3`

- **was**: temperature optimum @ pH 6.0 = 60.0 degrees Celsius
- **section**: Discussion
- **check**: CONFIRMED: secondhand marker in the quote (article is a research-article)
- **check**: enzyme-like tokens in the quote: ['PET46']
- **reason given**: Same secondhand sentence, temperature axis.
- **quote**: In their study, the PET46-like 211 released up to 85.23 mg L−1 aromatic products from crystalline PET powder at 60 °C and pH6 (optimal conditions).

```
mily with FAEs, and they bear a lid domain of varying length. They can hydrolyze MHET into TPA and EG. One of the best-studied examples is the MHETase derived from the gram-negative bacterium I. sakaiensis (IsMHETase). This enzyme acts efficiently on MHET, but recently an exo-function on PET pentamers was described64. It also hydrolyzed BHET in a concentration-dependent manner, and its three-dimensional structure shows a much larger lid domain involving more than 200 aa (Supplementary Fig. 5). A new study by Erickson et al.60 searched for new thermotolerant PET hydrolase scaffolds following a similar searching strategy as in our study. They reported the metagenome-derived enzymes 204 and 211, but did not investigate their taxonomic affiliation nor their conserved domains in detail. PETase 204 is 97.93% identical to WP_187147021.1 and WP_148684612.1 from Thermophilum adornatum, while 211 is 99.62% identical to MBS7639053.1 from a Cand. Bathyarchaeota archaeon, both archaea. PET46 shares 34.92% and 65.78% sequence identity, respectively (Fig. 1), but their structure is very similar (Supplementary Fig. 11). In their study, the PET46-like 211 released up to 85.23 mg L-1 aromatic products from crystalline PET powder at 60 °C and pH6 (optimal conditions). This equals to 0.52 mM assuming all of it is TPA, which is less but in the range of the amount of product that we measured with PET46 (1.6 mM; Fig. 4). As for PET46, no activity was detected on amorphous PET foil. ¶ PET46 is encoded in a marine Bathyarcheota MAG. Microorganisms affiliated with the Bathyarchaeota are globally occurring and widespread in marine and terrestrial anoxic sediments65. They can use a wide range of polymers as carbon and energy sources, and they are well known to be very versatile with respect to metabolic capabilities. They are further known to be abundant in some marine sediments. Because of their huge metabolic potential, it is further assumed that they may play a significant role in global carbon biogeochemical cycling65-68. Interestingly, Bathyarcheota have been associated with the degradation of the biopolymer lignocellulose previousl
```


## PMC10599323 — review-article

*Accelerating the Biodegradation of Poly(lactic acid) through the Inclusion of Plant Fibers: A Review of Recent Advances*


### BMEEB3F89D6F — dropped by `PH-X7`

- **was**: pH stability @ pH 6.5 = 6.5 pH
- **section**: End-of-Life Degradation / Biodegradation of PLA and PLA-Plant Fiber Composites
- **check**: CONFIRMED: article-type='review-article'
- **reason given**: 'The AUTHORS FOUND that the pH of the solution dropped ...' in a review article; restates another study's observation.
- **quote**: The authors found that the pH of the solution dropped during degradation due to lactic acid formation; enzyme denaturization occurred below pH 6.5, impeding further degradation until the solution was refreshed.

```
ultural soil and sources
of microbial consortia (80:20 mass
ratio) ¶ ¶ ¶ ¶ ¶ Temp: thermophilic (58 °C) ¶ ¶ ¶ ¶ ¶ Duration: 45 days ¶ ¶ ¶ Gunti et al. compared the biodegradability of PLA-short
jute fiber
composites by lipase PS at 38 °C and in soil burial at room temperature.37 Their results showed that degradation proceeded
at a much higher rate in enzyme-enriched environments than in soil;
however, it is important to note that the impact of the different
temperatures was not accounted for in the interpretation of results.
In these enzymatic environments, composites containing alkaline-treated
fibers degraded slower than samples containing untreated fibers at
the same wt %, and samples treated with 15% NaOH also degraded slower
than those treated using a lower NaOH concentration. More aggressive
alkali treatments lead to a higher removal of hydrophilic components,
resulting in stronger polymer-fiber interactions, which in turn makes
the materials harder to degrade. ¶ Hegyesi et al. looked at the
degradation of PLA-cellulose nanocrystals
composites by proteinase K and lipase at 37 °C.102 Only proteinase K was found to degrade the composites effectively.
The authors found that the pH of the solution dropped during degradation
due to lactic acid formation; enzyme denaturization occurred below
pH 6.5, impeding further degradation until the solution was refreshed.
All samples containing cellulose nanocrystals underwent rapid disintegration
within a few days, making it difficult to track mass loss. ¶ A
recent study suggested that cellulases can act as nonspecific
enzymes, catalyzing the degradation of both components of PLA-jute
fiber composites,103 although it remains
unclear whether this observation can be generalized to all cellulases.
PLA-woven jute fiber composites were degraded in an aqueous environment
in the presence of cellulase at 30 °C. After four months, cellulase-treated
PLA samples underwent a 55% decrease in thickness while cellulase-treated
PLA-jute fiber composites underwent a 61% decrease in thickness. In
comparison, control samples incubated in a buffer without enzymes
maintained their thickness throughout the study. Evidence of chain
sciss
```


## PMC10927764 — research-article

*New combined absorption/1H NMR method for qualitative and quantitative analysis of PET degradation products*


### BMFE76762A46 — dropped by `PH-X8`

- **was**: pH optimum @ pH 3.54 = 3.54 pH
- **section**: Results / Optimization of the measurement conditions
- **reason given**: pH 3.54 is the buffer of an absorption/1H-NMR quantification method for TPA, not an enzyme assay condition.
- **quote**: Since TPA constitutes an important part of the degradation products, the optimal conditions for the measurement of the mixture were the buffer with pH 3.54 in combination with freeze or heat drying, as the sensitivity was very high for the 3 products in this case.

```
he future for the detection of the enzymatic activity of PETase and MHETase as well as PETase homologs, so the reaction buffer proved to be indispensable. The spectrum of the lowest concentration of MHET could be determined with the freeze-drying procedure, with no differences between the two pH values. BHET showed the best result at pH 9 in combination with freeze-drying. Since TPA crystallized at pH 9 and could not be measured by either method, the optimum conditions for this product could be determined to be pH 3.54 in combination with freeze-drying or heat-drying. In general, both drying methods showed little difference, yet each method has its advantages and disadvantages. While freeze-drying requires more materials such as nitrogen and is therefore more expensive, heat-drying requires considerably more time and could possibly destroy components, which was not the case with PET, however. Also, the pH values did not show much difference for MHET and BHET, but for TPA, only pH 3.54 could be used. Since TPA constitutes an important part of the degradation products, the optimal conditions for the measurement of the mixture were the buffer with pH 3.54 in combination with freeze or heat drying, as the sensitivity was very high for the 3 products in this case. The absorption measurement also provided the best results under these conditions. ¶ ?disp-level 3?>Fig. 2 ¶ Optimization strategy for absorption and 1H NMR measurements. Different solvents, pH values and drying processes were investigated to determine the optimum conditions for the measurement of the degradation products, shown in coloured lines. The best results for TPA and MHET were achieved in buffer pH 3.54 after freeze-drying. For MHET, equal sensitivity was demonstrated in buffer pH 9. The optimal conditions for BHET were at pH 9 in combination with freeze-drying. Nevertheless, sensitivity was also very high in buffer pH 3.54 combined with freeze-drying, so that these conditions proved to be the most suitable ¶ ¶ ?cloudpmc-path blobs/bea5/10927764/47413455165f/11356_2024_32481_Fig2_HTML.jpg?>?cloudpmc-bucket cdn?>?image-server-status LOAD_COMPLETED?>?original-height 770?>?original-width 1769?>?scaled-height 308?>?scaled-width 707?>?cloudpmc-path blobs/bea5/109277
```


## PMC10941194 — review-article

*Exploring Emergent Properties in Enzymatic Reaction Networks: Design and Control of Dynamic Functional Systems*


### BM03DE403B9C — dropped by `PH-X2;PH-X7`

- **was**: pH optimum @ pH 3.5 = 3.5 pH
- **section**: Complex Nonlinear Behavior in Artificial ERNs / Networks Based on the Urea–Urease Reaction
- **check**: CONFIRMED: article-type='review-article'
- **reason given**: 'a standard bell-shaped activity-pH profile with an optimum around 7.5.51 When starting from a lower pH (usually buffers of pH 3.5-5.0 ...)'. The recorded 3.5-5.0 is the STARTING BUFFER range; the stated optimum is 7.5. The trailing '51' is a stripped reference marker, so the claim is secondhand as well.
- **quote**: The enzyme has a standard bell-shaped activity–pH profile with an optimum around 7.5.51 When starting from a lower pH (usually buffers of pH 3.5–5.0 with low buffer capacity), the enzyme basifies the solution, thereby overcoming the buffer and increasing its own activity, up to pH 7.5.

```
d to obtain (for instance, clock
behavior (Figure 3e1)
or pulse-like response (Figure 3e2)), some other types are rare (chaos as shown in Figure 3e6 is, to the best
of our knowledge, only obtained in peroxidase-oxidase reaction
(section 3.3)). ¶ In order to provide the reader with a readily accessible overview,
we grouped the synthetic ERNs with complex nonlinear behavior according
to the central enzymatic reaction around which the network is built.
For all of the discussed networks, we refer to the motifs they contain
and behavior types they produce, as per Figure 3. ¶ 3.1 ¶ Networks Based on the Urea-Urease Reaction ¶ In general, enzymes producing acid or base are a fruitful ground
for designing systems with complex dynamics due to the nonlinear kinetics
intrinsic to pH-reactive systems.48-50 A simple and well-studied
enzymatic network that produces nonlinear behavior is the urea-urease
network. The enzyme urease (Ur) is found in many bacteria and plants.
It catalyzes the hydrolysis of urea into carbon dioxide and ammonia,
resulting in an increase in pH. The enzyme has a standard bell-shaped
activity-pH profile with an optimum around 7.5.51 When starting from a lower pH (usually buffers
of pH 3.5-5.0 with low buffer capacity), the enzyme basifies
the solution, thereby overcoming the buffer and increasing its own
activity, up to pH 7.5. As the reaction proceeds further to even higher
pH values, the Ur activity drops again and the final pH of about 8.5
is that of ammonia/ammonium buffer. This process creates an autocatalytic
sigmoidal signature in pH vs time, and the time of the steep transition
from low to high pH state is addressed in the literature as “clock
time” (Figure 3e1).51,52 The increase in Ur activity due to the Ur
reaction is an example of product autoactivation (Figure 3b2). ¶ Compartmentalization
and coupling to diffusion enrich the range of complex behaviors obtained
in Ur networks. Effectively, the simple combination of the Ur nonlinear
core (Figure 3b2) with
transport phenomena (Figure 3c4) yields five types of complex behavior (Figure 3e1-e7), particularly
because diffusion coefficients for H+ and other species
are very different. Ur-loaded millimeter-sized particles exhibit quorum-sensing-like
autoactivation (similarly to Figu
```


## PMC11651597 — research-article

*Characterization of a novel subfamily 1.4 lipase from Bacillus licheniformis IBRL-CHS2: Cloning and expression optimizat*


### BM0A3FCD8E37 — dropped by `PH-X9`

- **was**: thermostability @ pH 6.0 = 35.0 degrees Celsius
- **section**: Results / Characterization of recombinant MLipA / Effect of pH on MLipA activity and stability
- **reason given**: 35 deg C is the incubation temperature of the pH-stability assay in this sentence; recorded as a thermostability measurement of 35 deg C. No thermostability value is stated.
- **quote**: Fig 5A illustrates that it remained stable between pH 6 and pH 9, retaining between 89% and 97% of its residual activity after 1 h of incubation at 35°C.

```
ase was incubated for 24 hours in 35°C in 0.1M phosphate buffer (pH 6 and pH 7) and 0.1M Tris-Cl buffer (pH 8). Aliquots were taken at specified intervals. Residual activity was assayed at the optimum temperature, 35°C. The specific activity of lipase without pre-incubation (325.7 U/mg) was set at 100%. Symbols used are: (♦) for pH 6, (■) for pH 7 and (▲) for pH 8. ¶ ¶ ?image-name pone.0314556.g005.jpg?>?image-size 97536?>?image-md5 0bcc1863a87a7f6096e98de604dcc9f3?>?image-image-server-status LOAD_COMPLETED?>?image-original-height 2400?>?image-original-width 1727?>?image-scaled-height 959?>?image-scaled-width 690?>?image-cloudpmc-urn urn:cdn:blobs/a634/11651597/0bcc1863a87a/pone.0314556.g005.jpg?>?thumb-name pone.0314556.g005.gif?>?thumb-size 11025?>?thumb-md5 f3545265c2685b86c7fa8dd5471dc0f7?>?thumb-image-server-status NEVER_LOAD?>?thumb-scaled-height 139?>?thumb-scaled-width 100?>?thumb-cloudpmc-urn urn:cdn:blobs/a634/11651597/f3545265c268/pone.0314556.g005.gif?>The lipase’s stability was assessed across various pH levels. Fig 5A illustrates that it remained stable between pH 6 and pH 9, retaining between 89% and 97% of its residual activity after 1 h of incubation at 35°C. However, exposure to pH 10 resulted in a marked decrease in activity, with only 51% residual activity observed after one h, and further decline to 22% at pH 11. Subsequently, the stability of MLipA was evaluated across pH levels of 6, 7, and pH 8 (Fig 5B). It exhibited the highest stability at pH 6 and pH 7, retaining 43% and 49% of its original activity, respectively, following 24 h of incubation at 35°C. Conversely, a substantial decrease in activity was observed at pH 8, with only 15% of the original activity remaining after 24 h. ¶ ¶ Effect of organic solvents on MLipA activity ¶ MLipA stability in 10 different organic solvents with varying Log P values was evaluated over one and 24-h periods. Log P values indicate a solvent’s hydrophilicity or hydrophobicity, with more positive values denoting greater hydrophobicity and more negative values indicating higher hydrophilicity. As shown in Table 2, the recombinant lipase from Bacillus lichen
```


### BM71030D2A05 — dropped by `PH-X1`

- **was**: pH stability @ pH 7.0 = 7.0 pH
- **section**: Results / Characterization of recombinant MLipA / Effect of pH on MLipA activity and stability
- **check**: CHALLENGED: enclosed by a results section -- 'Results / Characterization of recombinant MLipA / Effect of pH on MLipA activity and stability'
- **reason given**: Normalisation sentence: 'activity at pH 7 was set as 100% ... for pH stability the activity without pre-incubation was set at 100%'. Defines the assay baseline, not a measured outcome. The optimum it implies is captured by the corrected BMDFDCB2C50A.
- **quote**: Specific lipase activity at pH 7 was set as 100% (321.2 U/mg) for optimum pH while for pH stability, the activity of lipase without pre-incubation (325.7 U/mg) was set at 100%.

```
was just 9% after 24 h, indicating significant instability with increasing temperature. Despite this, MLipA exhibits moderate thermolabile behavior, notably retaining activity at 35°C. ¶ ¶ Effect of pH on MLipA activity and stability ¶ The recombinant lipase exhibited activity across a wide pH spectrum, ranging from pH 5 to pH 9, with optimal activity observed at pH 7 (Fig 5A). It maintained high activity levels, retaining 93% of its activity at pH 6 and 82% at pH 8. However, its relative activities decreased significantly at pH 4 (11%) and pH 5 (45%). Beyond pH 9, a sharp decline in activity was observed, with relative activities of 46%, 22%, and 8% at pH 9, pH 10, and pH 11, respectively. ¶ 10.1371/journal.pone.0314556.g005Fig 5 ¶ pH profile and stability of MLipAB.licheniformis. ¶ (A) pH profile of MLipAB.licheniformis (♦) and pH stability study of the lipase (▲). For stability study, the purified lipase was incubated for 1 hour in 35°C in suitable buffers. Residual activity was assayed at the optimum temperature, 35°C. Specific lipase activity at pH 7 was set as 100% (321.2 U/mg) for optimum pH while for pH stability, the activity of lipase without pre-incubation (325.7 U/mg) was set at 100%. (B) Stability study of MLipAB.licheniformis at pH 6, pH 7 and pH 8. For stability study, the purified lipase was incubated for 24 hours in 35°C in 0.1M phosphate buffer (pH 6 and pH 7) and 0.1M Tris-Cl buffer (pH 8). Aliquots were taken at specified intervals. Residual activity was assayed at the optimum temperature, 35°C. The specific activity of lipase without pre-incubation (325.7 U/mg) was set at 100%. Symbols used are: (♦) for pH 6, (■) for pH 7 and (▲) for pH 8. ¶ ¶ ?image-name pone.0314556.g005.jpg?>?image-size 97536?>?image-md5 0bcc1863a87a7f6096e98de604dcc9f3?>?image-image-server-status LOAD_COMPLETED?>?image-original-height 2400?>?image-original-width 1727?>?image-scaled-height 959?>?image-scaled-width 690?>?image-cloudpmc-urn urn:cdn:blobs/a634/11651597/0bcc1863a87a/pone.0314556.g005.jpg?>?thumb-name pone.0314556.g005.gif?>?thumb-size 11025?>?thumb-md5 f3545265c2685b86c7fa8dd5471dc0f7?>?thumb-image-server-status NEVER_LOAD?>?thumb-s
```


## PMC12115826 — research-article

*Heterologous Overexpression of Cytochrome P450BM3 from Bacillus megaterium and Its Role in Gossypol Reduction*


### BMB86BE59C99 — dropped by `PH-X6`

- **was**: temperature optimum @ pH 5.0 = 30.0 degrees Celsius
- **section**: 3. Discussion / 3.2. Optimization of Cytochrome P450BM3-Catalyzed Gossypol Degradation Conditions
- **check**: CONFIRMED: title/abstract name off-target class ['cytochrome p450']
- **reason given**: Cytochrome P450BM3 monooxygenase degrading gossypol, a plant polyphenol. Neither the enzyme class nor the substrate is in scope.
- **quote**: The optimal conditions for gossypol degradation were found to be 30 °C, pH 5.0, and 90 min.

```
egaterium’s optimal growth temperature [25]. Thus, 30 °C was selected as the induction temperature, consistent with findings in studies of CYP102A16 [26]. Induction duration was identified as a critical factor for expression: prolonged induction disrupts cellular metabolism, leading to cell lysis or protein degradation [27]. A 12 h induction period was determined to be optimal, consistent with prior research [26]. The purified P450BM3 displayed a ~119 kDa band on SDS-PAGE, in line with earlier findings [28]. Therefore, appropriate induction temperature and induction time are more conducive to the expression of the protein. ¶ ¶ 3.2. Optimization of Cytochrome P450BM3-Catalyzed Gossypol Degradation Conditions ¶ P450BM3 is a versatile enzyme. Its catalytic activity was first verified using palmitic acid as a model substrate before being applied to gossypol reduction, a validation approach consistent with previous research [13,29]. Since enzymatic efficiency depends on multiple factors, temperature, pH, and reaction time were optimized systematically. The optimal conditions for gossypol degradation were found to be 30 °C, pH 5.0, and 90 min. For instance, a prior study reported that the optimal conditions for Helicoverpa armigera CYP9A12 were 30 °C and pH 6.0 [12]. Such differences in optimal pH values likely result from variations in substrate-enzyme specificity among P450 isoforms. In the context of other cytochrome P450-related studies, various reaction conditions and efficiencies have been documented. At pH 7 and 35 °C, P450BM3 achieved a 44.08% indigo conversion [25]. CYP119 showed a kcat of 78.2 min-1 for styrene oxidation at 70 °C and pH 8.5 [30]. CYP102A16 degraded 34.9% of 50 ppm naphthalene at 37 °C within 60 h, while P450DA-G4 demonstrated 76% hydroxylation efficiency for 1-chloro-2-phenylethane at 30 °C and pH 8.5 [26,31]. These diverse findings underscore the significant influence of substrate chemistry and enzyme-substrate interactions on reaction conditions. By using purified P450BM3, potential interference from amines and proteins in crude ly
```


### BMDDBDC51F4A — dropped by `PH-X6`

- **was**: pH optimum @ pH 5.0 = 5.0 pH
- **section**: 3. Discussion / 3.2. Optimization of Cytochrome P450BM3-Catalyzed Gossypol Degradation Conditions
- **check**: CONFIRMED: title/abstract name off-target class ['cytochrome p450']
- **reason given**: Same P450/gossypol article.
- **quote**: The optimal conditions for gossypol degradation were found to be 30 °C, pH 5.0, and 90 min.

```
egaterium’s optimal growth temperature [25]. Thus, 30 °C was selected as the induction temperature, consistent with findings in studies of CYP102A16 [26]. Induction duration was identified as a critical factor for expression: prolonged induction disrupts cellular metabolism, leading to cell lysis or protein degradation [27]. A 12 h induction period was determined to be optimal, consistent with prior research [26]. The purified P450BM3 displayed a ~119 kDa band on SDS-PAGE, in line with earlier findings [28]. Therefore, appropriate induction temperature and induction time are more conducive to the expression of the protein. ¶ ¶ 3.2. Optimization of Cytochrome P450BM3-Catalyzed Gossypol Degradation Conditions ¶ P450BM3 is a versatile enzyme. Its catalytic activity was first verified using palmitic acid as a model substrate before being applied to gossypol reduction, a validation approach consistent with previous research [13,29]. Since enzymatic efficiency depends on multiple factors, temperature, pH, and reaction time were optimized systematically. The optimal conditions for gossypol degradation were found to be 30 °C, pH 5.0, and 90 min. For instance, a prior study reported that the optimal conditions for Helicoverpa armigera CYP9A12 were 30 °C and pH 6.0 [12]. Such differences in optimal pH values likely result from variations in substrate-enzyme specificity among P450 isoforms. In the context of other cytochrome P450-related studies, various reaction conditions and efficiencies have been documented. At pH 7 and 35 °C, P450BM3 achieved a 44.08% indigo conversion [25]. CYP119 showed a kcat of 78.2 min-1 for styrene oxidation at 70 °C and pH 8.5 [30]. CYP102A16 degraded 34.9% of 50 ppm naphthalene at 37 °C within 60 h, while P450DA-G4 demonstrated 76% hydroxylation efficiency for 1-chloro-2-phenylethane at 30 °C and pH 8.5 [26,31]. These diverse findings underscore the significant influence of substrate chemistry and enzyme-substrate interactions on reaction conditions. By using purified P450BM3, potential interference from amines and proteins in crude ly
```


## PMC12428281 — research-article

*Identification and Characterization of a Novel Di-(2-ethylhexyl) Phthalate Hydrolase from a Marine Bacterial Strain Myco*


### BM47946FE1B3 — dropped by `PH-X9`

- **was**: thermostability @ pH 3.0 = 4.0 degrees Celsius
- **section**: 2. Results / 2.5. Biochemical Characterization of DehpH
- **reason given**: 4 deg C is the incubation temperature of a pH-stability experiment, recorded as a thermostability measurement of 4 deg C.
- **quote**: After incubation at 4 °C under different pH for 1 h, the activity of DehpH decreased significantly under acid conditions (pH 3.0 to 6.0), and DehpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 (Figure 4B).

```
colicibacterium strains. ¶ Concurrently, the dehpH gene was successfully inserted into pET28a(+) and transformed into E. coli BL21 (DE3) for gene expression. Subsequently, the DehpH gene was induced by IPTG, and the recombinant DehpH was purified using His60 Ni Magnetic Beads (TaKaRa, Beijing, China). The SDS-PAGE analysis revealed that a lane of protein with a molecular weight of ~46 kDa was obtained (Figure 3B). The recombinant DehpH most likely corresponded to the 6 kDa of His-Thrombin tag (N-terminal) and His tag (C-terminal) sequences fused to the expected 40 kDa of the dehpH gene product. ¶ ¶ 2.5. Biochemical Characterization of DehpH ¶ The effects of different environmental factors on the activity of DehpH were determined, and the optimal conditions for DehpH were proposed thereafter (Section 4.8). The effects of pH on the activity of DehpH were shown in Figure 4A. The results indicated that the optimal pH was 8.0, and DehpH showed relatively high activity ranging from pH 6.0 to pH 9.0. After incubation at 4 °C under different pH for 1 h, the activity of DehpH decreased significantly under acid conditions (pH 3.0 to 6.0), and DehpH almost lost all of its activity under pH 3.0, while DehpH retained more than 70.0% residual activity under pH 7.0 to 9.0 (Figure 4B). The activity of DehpH increased in the temperature range of 10 °C to 30 °C and showed maximum activity at 30 °C (Figure 4C). Subsequently, the activity of DehpH decreased in the temperature range from 30 °C to 80 °C, and DehpH almost lost its activity under 80 °C. The thermostability experiment showed that the activity of DehpH decreased with the increasing of the incubation time, and the higher the temperature, the greater the loss of activity (Figure 4D). After 5 h incubation, approximately 64.0% of DehpH activity was retained under 20 °C, while only 11.4% of DehpH activity was there under 60 °C. ¶ The effects of metal ions on the activity of DehpH were shown in Figure 4E. The results demonstrated that Co2+ could significantly promote the activity of DehpH, while Mg2+ and Mn2+ showed no significant influence on the activity of DehpH. On the contrary, Ca2+, Cu2+, Fe2+, and Zn2+ could decrease the activity of DehpH by 8.5% (Ca2+) to 15.4% (Zn2+). DehpH showed weak tolerance
```


## PMC12734981 — research-article

*A CALB-like Cold-Active Lipolytic Enzyme from Pseudonocardia antarctica: Expression, Biochemical Characterization, and A*


### BM097BBDB7F2 — dropped by `PH-X12`

- **was**: pH stability @ pH 8.0 = 8.0 pH
- **section**: 2. Results and Discussion / 2.3. Biochemical Characterization of PanLipΔN
- **reason given**: 'A rapid decline in activity was detected beyond pH 8.0' -- no outcome is measured AT pH 8.0; the only quantified point in the sentence is pH 9.0 (BM51F74D231E).
- **quote**: A rapid decline in activity was detected beyond pH 8.0, with less than 15% residual activity at pH 9.0.

```
erides and displays measurable lipase-like activity. This ability to act on structurally diverse and bulkier substrates may reflect an increased conformational flexibility near the active site, a feature commonly associated with cold-adapted lipolytic enzymes [63] and consistent with psychrophilic catalytic strategies that compensate for reduced thermal energy [15]. These results further support the classification of PanLipΔN as a lipase-family esterase with both esterase-type substrate preference and lipase-like catalytic capability. ¶ The optimal temperature for hydrolytic activity of PanLipΔN was found to be at ~25 °C (Figure 4c). The effect of pH on the catalytic activity of PanLipΔN was investigated in the pH range of 4.0-9.0 (Figure 4d). The enzyme exhibited relatively low activity under acidic conditions (pH 4.0-6.0), but the activity increased sharply at near-neutral to alkaline pH. The maximum activity was observed at pH 8.0, indicating that PanLipΔN is an alkaline-preferring lipase. A rapid decline in activity was detected beyond pH 8.0, with less than 15% residual activity at pH 9.0. ¶ The thermal stability of PanLipΔN was examined at the different temperatures (20 °C, 40 °C, 60 °C, and 80 °C) for up to 60 min (Figure 5a). The enzyme was stable below 40 °C, maintaining over 80% of its initial activity. However, activity decreased markedly at 60 °C and was completely lost at 80 °C within 15 min. These results indicate that PanLipΔN has moderate thermal tolerance, consistent with other cold-active bacterial lipases [18,21,55,59,60,62]. The freeze-thaw stability of recombinant PanLipΔN was evaluated over twelve consecutive cycles (Figure 5b). The enzyme retained over 85% of its initial activity even after 12 cycles, showing only minor fluctuations in activity throughout the process. This result indicates that PanLipΔN not only possesses excellent structural robustness and refolding capability during repeated freezing and thawing, but also is comparable to other cold-active lipolytic enzymes. For example, the cold-active SGNH-type lipase HaSGNH1 from Halocynth
```


## PMC12766730 — research-article

*Controlled Self-Immolative Release of β‑Lapachone via an Optimized para-Hydroxybenzyl Linker for Targeted Pancreatic Can*


### BM60E20E768C — dropped by `PH-X6`

- **was**: pH stability @ pH 5.0 = 5.0 pH
- **section**: Results and Discussion / Release Rate Comparison of Self-Immolative Linkers
- **check**: CHALLENGED: no off-target class in title/abstract; in-scope terms present []
- **reason given**: 'half-life of quinone release ... at pH 5' -- self-immolative linker chemistry, no enzyme.
- **quote**: The half-life of quinone release was decreased from 101 ± 7 h for 4 to 1.86 ± 0.06 h for 25 at pH 5.

```
kest
acceleration of the TS stabilizing derivatives. ¶ The addition
of an intramolecular “quenching tether”
(3j, Figure S3) demonstrated
none of the release rate increase in comparison to its nontethered
analogue 3f that was observed by Rose et al. for an analogous but mechanistically distinct
reaction. The kinetics of 3j instead demonstrated that
the attachment of a PEG spacer to the meta oxygen
atom has very little effect on quinone release rate, further proving
that in our case, the reaction is kinetically controlled and that
1,6-elimination is the rate-limiting step rather than quinone methide
quenching. ¶ To examine whether the structure-activity
relationship (SAR)
findings made with the PHB linker could translate to PAB-β-lapachone
prodrugs as well, the PAB meta methoxy derivative 25 was compared to the first-generation plain PAB prodrug
(4) developed by Dunsmore.
 ¶ Following the same trends observed with the PHB linker, 25 released β-lapachone around 2 orders of magnitude
faster than 4 (Figure 
f). It also maintained the same pH dependence as 4,
with the release rate increasing as pH decreased. The half-life of
quinone release was decreased from 101 ± 7 h for 4 to 1.86 ± 0.06 h for 25 at pH 5. As the TME is
known to be acidic,
-


25 possesses an optimal release profile,
with faster release at acidic tumor pH 5.5-6.5 and slower release
at circulation pH 7.4. However, it lacks the solubility and therapeutic
window widening benefits of β-glucuronide masking. ¶ Besides
the phenol ring, the other position that proved to have
a largely beneficial effect on the observed release rate was the benzylic
position. Similarly to what Hay et al. found with PAB linkers, the attachment of a methyl group to the benzylic
position of the PHB linker dramatically increased the release rate
of 3i in comparison to 3a. A benzylic methyl
group had a larger accelerating effect on the release rate than a
single meta methoxy substituent (3f),
but a smaller effect than two meta methoxy groups
(3g). The half-life of drug release at tumor relevant
pH 6 was decreased from 2371 ± 502 h fo
```


## PMC12871986 — research-article

*Biodegradation of polyethylene terephthalate microplastics by Paenibacillus naphthalenovorans PETKKU2: Response surface *


### BM539CC031EB — dropped by `PH-X5`

- **was**: pH optimum @ pH 7.5 = 7.5 pH
- **section**: Results and discussion / Response surface optimization of PET-MP biodegradation
- **check**: CONFIRMED: prediction language in the quote
- **reason given**: 'The MODEL PREDICTED maximum biodegradation at pH 7.5' -- an RSM optimisation output, and about whole-cell biodegradation rather than an enzyme. Shipping it would breach the benchmark's own no-predicted-values integrity statement.
- **quote**: The model predicted maximum biodegradation at pH 7.5, 1.25 g/L NH₄NO₃, and 0.55% PET-MP, achieving 11.15% efficiency compared to 6.09% under non-optimized conditions (pH 7.0, 1.0 g/L NH₄NO₃, 1.0% PET-MP).

```
fectively colonize and degrade the polymer under challenging conditions. ¶ Comparing P. naphthalenovorans PR-N1 [64] from The Bacterial Diversity Metadatabase (BacDive) (https://bacdive.dsmz.de/strain/136597) with PETKKU2, both strains share several biochemical similarities, but differences in Arginine, Arabinose, and Trehalose metabolism highlight PETKKU2’s specific capabilities. PETKKU2’s ability to metabolize Trehalose but not Arabinose, while the BacDive strain can metabolize Arabinose, suggests differences in their metabolic flexibility. These variations could influence their suitability for different biodegradation processes, particularly for PET degradation under varying environmental conditions. ¶ ¶ Response surface optimization of PET-MP biodegradation ¶ RSM optimization of PET-MP biodegradation by P. naphthalenovorans PETKKU2 yielded degradation efficiencies ranging from 2.85% to 11.15%. The second-order polynomial model demonstrated strong statistical significance (F = 21.14, p = 0.0003) with excellent predictive power (R2 = 0.9645, adjusted R2 = 0.9189). The model predicted maximum biodegradation at pH 7.5, 1.25 g/L NH4NO3, and 0.55% PET-MP, achieving 11.15% efficiency compared to 6.09% under non-optimized conditions (pH 7.0, 1.0 g/L NH4NO3, 1.0% PET-MP). Experimental validation near optimal conditions resulted in 9.48 ± 0.21% degradation, closely matching the predicted value of 10.38% (95% prediction interval: 8.42-12.34%). ¶ Among tested variables, PET-MP concentration had the greatest impact on biodegradation (p = 0.0033), followed by NH4NO3 concentration (p = 0.0116). Although pH alone was not statistically significant (p = 0.0635), its interactions with other factors showed important effects (S3 Table). Significant synergistic interactions were observed between PET-MP concentration and pH, as well as between PET-MP and NH4NO3 concentration (Fig 5). Residual analysis and diagnostic plots (Residuals vs. Predicted, Normal Plot of Residuals, predicted vs. actual; S5 Fig) were generated to confirm model adequacy, homoscedasticity, and normality of residuals. Quadratic terms for pH and NH4NO3 were also significant (p < 0.001), indicating non-linear effec
```


## PMC12896513 — research-article

*Cloning and Characterization of GDSL Esterases from Bacillus paralicheniformis T7*


### BM43A7E54ACA — dropped by `PH-X1`

- **was**: thermostability @ pH 7.0 = 40.0 degrees Celsius
- **section**: 2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases
- **check**: CONFIRMED: enclosed by a methods section -- '2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases'
- **reason given**: 'The residual activity was then measured at 40 deg C in 50 mM sodium phosphate (pH 7.0)' is the assay readout condition. Recorded as thermostability = 40 deg C.
- **quote**: The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0).

```
ctivity and Stability of Recombinant Esterases ¶ Enzyme activity was measured within a pH range of 3.0-11.0. The following buffer systems were used: citrate buffer (pH 3.0-5.0), sodium phosphate buffer (pH 6.0-7.0), and glycine-NaOH buffer (pH 8.0-11.0). The obtained values were converted to relative units, with the maximum value set at 100%. For the pH stability experiments, the enzyme extract was pre-incubated for 2 h at 23 °C in 10 mM citrate buffer at pH 4.0 and 6.0 and in 50 mM Tris-HCl buffer at pH 8.0 and 10.0. The residual activity was then measured in 50 mM sodium phosphate buffer at pH 7.0. The results were expressed as a percentage of the activity of the unpreincubated extract, set at 100%. The effect of temperature on esterase activity was assessed in the range of 30-80 °C in intervals of 5 °C. The maximum enzymatic activity was taken as 100%. To analyse the thermal stability, the enzyme extract was pre-incubated for 5 h at 40, 50, 60 or 70 °C in 50 mM Tris-HCl buffer solution (pH 7.0). The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0). The results were expressed as a percentage of the activity of the extract not subjected to thermal incubation. All experiments were performed in triplicate. ¶ ¶ 2.9. Effect of Metal Ions and Detergents on Esterase Activity ¶ The effect of metal ions on esterase activity was determined using the following ions: Ca2+, Mg2+, Mn2+, Cu2+, Zn2+, and Fe2+. The effect of the metal ions, the reducing agents β-mercaptoethanol and dithiothreitol (DTT), the inhibitor phenylmethylsulfonyl fluoride, the chelating agent ethylenediaminetetraacetic acid (EDTA), and the detergents Tween-20, Tween-80, Triton X-100, and SDS on enzymatic activity was determined by adding the reagents to the reaction mixture. Enzymatic activity was then assessed at 40 °C in a 50 mM sodium phosphate-buffered solution (pH 7.0). Activity values in the absence of metal ions and chemicals were considered 100% activity. ¶ ¶ 2.10. Substrate Specificity of Recombinant Esterases ¶ The substrate specificity of the re
```


### BM4FD5205F58 — dropped by `PH-X1`

- **was**: pH stability @ pH 7.0 = 7.0 pH
- **section**: 2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases
- **check**: CONFIRMED: enclosed by a methods section -- '2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases'
- **reason given**: Same methods sentence, recorded as pH stability = 7.0. pH 7.0 is the readout buffer.
- **quote**: The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0).

```
ctivity and Stability of Recombinant Esterases ¶ Enzyme activity was measured within a pH range of 3.0-11.0. The following buffer systems were used: citrate buffer (pH 3.0-5.0), sodium phosphate buffer (pH 6.0-7.0), and glycine-NaOH buffer (pH 8.0-11.0). The obtained values were converted to relative units, with the maximum value set at 100%. For the pH stability experiments, the enzyme extract was pre-incubated for 2 h at 23 °C in 10 mM citrate buffer at pH 4.0 and 6.0 and in 50 mM Tris-HCl buffer at pH 8.0 and 10.0. The residual activity was then measured in 50 mM sodium phosphate buffer at pH 7.0. The results were expressed as a percentage of the activity of the unpreincubated extract, set at 100%. The effect of temperature on esterase activity was assessed in the range of 30-80 °C in intervals of 5 °C. The maximum enzymatic activity was taken as 100%. To analyse the thermal stability, the enzyme extract was pre-incubated for 5 h at 40, 50, 60 or 70 °C in 50 mM Tris-HCl buffer solution (pH 7.0). The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0). The results were expressed as a percentage of the activity of the extract not subjected to thermal incubation. All experiments were performed in triplicate. ¶ ¶ 2.9. Effect of Metal Ions and Detergents on Esterase Activity ¶ The effect of metal ions on esterase activity was determined using the following ions: Ca2+, Mg2+, Mn2+, Cu2+, Zn2+, and Fe2+. The effect of the metal ions, the reducing agents β-mercaptoethanol and dithiothreitol (DTT), the inhibitor phenylmethylsulfonyl fluoride, the chelating agent ethylenediaminetetraacetic acid (EDTA), and the detergents Tween-20, Tween-80, Triton X-100, and SDS on enzymatic activity was determined by adding the reagents to the reaction mixture. Enzymatic activity was then assessed at 40 °C in a 50 mM sodium phosphate-buffered solution (pH 7.0). Activity values in the absence of metal ions and chemicals were considered 100% activity. ¶ ¶ 2.10. Substrate Specificity of Recombinant Esterases ¶ The substrate specificity of the re
```


### BM7EDDB0F663 — dropped by `PH-X1;PH-X10`

- **was**: pH stability @ pH 7.0 = 7.0 pH
- **section**: 2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases
- **check**: CONFIRMED: enclosed by a methods section -- '2. Materials and Methods / 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases'
- **check**: CONFIRMED: a shipped row covers ('PMC12896513', 'pH optimum', '7.0')
- **reason given**: Second copy of the same methods statement ('residual activity measured in 50 mM sodium phosphate buffer at pH 7.0'); duplicate of BM4FD5205F58 and equally unusable.
- **quote**: The residual activity was then measured in 50 mM sodium phosphate buffer at pH 7.0.

```
L of 50 mM sodium phosphate buffer at pH 7.0. The mixture was then incubated at 40 °C for 10 min, and the reaction was stopped by adding 1 mL of ethanol. The solution was then centrifuged at 1000× g for 3 min, and the absorbance was measured at 410 nm using a UV1900i spectrophotometer (Shimadzu, Kyoto, Japan). One unit of esterase activity corresponded to the formation of 1 μmol of 4-nitrophenol (pNP) per minute under these conditions. ¶ ¶ 2.8. Effect of Temperature and pH on Enzyme Activity and Stability of Recombinant Esterases ¶ Enzyme activity was measured within a pH range of 3.0-11.0. The following buffer systems were used: citrate buffer (pH 3.0-5.0), sodium phosphate buffer (pH 6.0-7.0), and glycine-NaOH buffer (pH 8.0-11.0). The obtained values were converted to relative units, with the maximum value set at 100%. For the pH stability experiments, the enzyme extract was pre-incubated for 2 h at 23 °C in 10 mM citrate buffer at pH 4.0 and 6.0 and in 50 mM Tris-HCl buffer at pH 8.0 and 10.0. The residual activity was then measured in 50 mM sodium phosphate buffer at pH 7.0. The results were expressed as a percentage of the activity of the unpreincubated extract, set at 100%. The effect of temperature on esterase activity was assessed in the range of 30-80 °C in intervals of 5 °C. The maximum enzymatic activity was taken as 100%. To analyse the thermal stability, the enzyme extract was pre-incubated for 5 h at 40, 50, 60 or 70 °C in 50 mM Tris-HCl buffer solution (pH 7.0). The residual activity was then measured at 40 °C in 50 mM sodium phosphate-buffered solution (pH 7.0). The results were expressed as a percentage of the activity of the extract not subjected to thermal incubation. All experiments were performed in triplicate. ¶ ¶ 2.9. Effect of Metal Ions and Detergents on Esterase Activity ¶ The effect of metal ions on esterase activity was determined using the following ions: Ca2+, Mg2+, Mn2+, Cu2+, Zn2+, and Fe2+. The effect of the metal ions, the reducing agents β-mercaptoethanol and dithiothreitol (DTT), the inhibitor phenylmethylsul
```


## PMC13050008 — research-article

*Biocatalytic ulvan degradation by Pseudoalteromonas marina: exploring a marine polysaccharide bioconversion system*


### BM44DA9B1565 — dropped by `PH-X6;PH-X4`

- **was**: pH optimum @ pH 8.0 = 8.0 pH
- **section**: Results / Biochemical characterization of ulvan lyases
- **check**: CONFIRMED: title/abstract name off-target class ['glycoside hydrolase', 'polysaccharide lyase', 'ulvan lyase']
- **check**: enzyme-like tokens in the quote: ['HCl', 'Tris']
- **reason given**: Ulvan lyase -- a polysaccharide lyase, not a carboxylester hydrolase. 'all three ulvan lyases' is also unattributable.
- **quote**: Regarding pH optimization, all three ulvan lyases displayed maximum activity at pH 8.0 in 50 mM Tris-HCl buffer, indicating a preference for slightly alkaline conditions (Fig.

```
t proteins ¶ All His-tag fused ulvan lyases were successfully expressed as soluble proteins in E. coli BL21(DE3). Following purification, the protein concentrations were determined to be 1.06 mg/mL for PmUL24, 9.87 mg/mL for PmUL25, and 8.01 mg/mL for PmUL40. SDS-PAGE analysis (Supplementary Fig. 3) confirmed the purity of the proteins and revealed apparent molecular weights of 120 kDa for PmUL24, 55 kDa for PmUL25, and 100 kDa for PmUL40, which closely align with their respective theoretical molecular weights. The yield of soluble PmUL24 protein was notably lower compared to the other ulvan lyases. ¶ ¶ Biochemical characterization of ulvan lyases ¶ The biochemical characterization of purified ulvan lyases revealed distinct temperature profiles, with both PmUL24 and PmUL25 exhibiting maximum activity at 50 °C, while PmUL40 showed the highest activity at 35 °C (Fig. 2A). Among the three enzymes, thermal stability profiles were similar, with PmUL25 and PmUL40 exhibiting comparatively higher stability than PmUL24 (Fig. 2B). Regarding pH optimization, all three ulvan lyases displayed maximum activity at pH 8.0 in 50 mM Tris-HCl buffer, indicating a preference for slightly alkaline conditions (Fig. 3C). Generally, ulvan lyases function in marine environments, and the influence of NaCl concentration is a critical parameter in their biochemical characterization (Fig. 3). PmUL24 and PmUL25 showed peak activities at 100 mM NaCl, following similar trends but with notable differences in salt tolerance. PmUL24 activity decreased rapidly beyond the optimal concentration, retaining only 25% activity at 1 M NaCl, whereas PmUL25 demonstrated greater salt tolerance, exhibiting a gradual decline in activity up to 1 M NaCl. PmUL40 displayed the highest NaCl tolerance among the three enzymes, with maximum activity at 250 mM NaCl. ¶ 
Fig. 2 ¶ Biochemical characterization of recombinant ulvan lyases. A Temperature optimization showing the relative activity of each enzyme across a temperature range. B Thermal stability profiles indicating residual activity after pre-incubation at different temperatures. C pH optimization demonstrating the effect of pH on enzy
```


## PMC13220297 — research-article

*Immobilization of an Invertase Produced by a Bacterium Isolated from the Peach Palm Fruit (Bactris gasipaes): Influence *


### BM3A1A41F1DA — dropped by `PH-X6`

- **was**: pH stability @ pH 6.5 = 6.5 pH
- **section**: Results and Discussion / pH Stability
- **check**: CONFIRMED: title/abstract name off-target class ['invertase']
- **reason given**: Invertase (beta-fructofuranosidase, a glycoside hydrolase) immobilised on a PHB carrier. The polymer is the support, not the substrate.
- **quote**: The enzyme immobilized on PHB demonstrated greater stability at pH values between 5.0 and 6.0, whereas at pH 4.5 and pH 6.5, it retained approximately 50% of its activity.

```
eld may be affected by
impurities in the crude extract, including amino acids, low-weight
polypeptides, and carbohydrates, substances that may possibly interact
with the enzyme and the support. ¶ It is important to emphasize
that the enzyme preparation used in
this study consisted of a crude extracellular extract and was not
subjected to purification prior to being immobilized. Therefore, the
immobilization efficiency was evaluated based on enzymatic activity
recovery (IY and RA), which reflects the catalytically active fraction
effectively retained on the support. Crude extracts may contain additional
proteins and low-molecular-weight compounds capable of interacting
with the support surface, potentially influencing the immobilization
yield. Nevertheless, the retained catalytic performance observed for
both supports suggests that the active invertase fraction was successfully
immobilized. ¶ ¶ pH Stability ¶ The pH stability results
regarding the
incubation of the invertase immobilized on PHB and SG functionalized
with glutaraldehyde are presented in Figure 
. The enzyme immobilized on PHB demonstrated
greater stability at pH values between 5.0 and 6.0, whereas at pH
4.5 and pH 6.5, it retained approximately 50% of its activity. On
the other hand, the enzyme immobilized on SG presented its highest
stability at pH 5.0 and an activity reduction of approximately 75%
at pH 5.5 and pH 6.5, indicating a smaller pH stability range. ¶ ?disp-level 3?>4 ¶ Stability of
the invertase from B. tequilensis (PP6)
immobilized on functionalized SG (■) and PHB (gray
triangle) after 24 h of incubation at 4 °C at different pH values,
with the maximum enzymatic activity of 2.30 U/g. ¶ ¶ ?cloudpmc-path blobs/81ad/13220297/7ce73752b0d6/jf6c02898_0004.jpg?>?cloudpmc-bucket cdn?>?image-server-status LOAD_COMPLETED?>?original-height 1486?>?original-width 1983?>?scaled-height 594?>?scaled-width 793?>?cloudpmc-path blobs/81ad/13220297/4313f91064af/jf6c02898_0004.gif?>?cloudpmc-bucket cdn?>Immobilization tends to protect the structure of
the enzyme from
the effects of pH; thus, higher pH stability favors storage and industrial
applications. As observed for ther
```


### BMC0FC218AB8 — dropped by `PH-X6`

- **was**: pH stability @ pH 4.5 = 4.5 pH
- **section**: Results and Discussion / pH Stability
- **check**: CONFIRMED: title/abstract name off-target class ['invertase']
- **reason given**: Same invertase article.
- **quote**: The enzyme immobilized on PHB demonstrated greater stability at pH values between 5.0 and 6.0, whereas at pH 4.5 and pH 6.5, it retained approximately 50% of its activity.

```
eld may be affected by
impurities in the crude extract, including amino acids, low-weight
polypeptides, and carbohydrates, substances that may possibly interact
with the enzyme and the support. ¶ It is important to emphasize
that the enzyme preparation used in
this study consisted of a crude extracellular extract and was not
subjected to purification prior to being immobilized. Therefore, the
immobilization efficiency was evaluated based on enzymatic activity
recovery (IY and RA), which reflects the catalytically active fraction
effectively retained on the support. Crude extracts may contain additional
proteins and low-molecular-weight compounds capable of interacting
with the support surface, potentially influencing the immobilization
yield. Nevertheless, the retained catalytic performance observed for
both supports suggests that the active invertase fraction was successfully
immobilized. ¶ ¶ pH Stability ¶ The pH stability results
regarding the
incubation of the invertase immobilized on PHB and SG functionalized
with glutaraldehyde are presented in Figure 
. The enzyme immobilized on PHB demonstrated
greater stability at pH values between 5.0 and 6.0, whereas at pH
4.5 and pH 6.5, it retained approximately 50% of its activity. On
the other hand, the enzyme immobilized on SG presented its highest
stability at pH 5.0 and an activity reduction of approximately 75%
at pH 5.5 and pH 6.5, indicating a smaller pH stability range. ¶ ?disp-level 3?>4 ¶ Stability of
the invertase from B. tequilensis (PP6)
immobilized on functionalized SG (■) and PHB (gray
triangle) after 24 h of incubation at 4 °C at different pH values,
with the maximum enzymatic activity of 2.30 U/g. ¶ ¶ ?cloudpmc-path blobs/81ad/13220297/7ce73752b0d6/jf6c02898_0004.jpg?>?cloudpmc-bucket cdn?>?image-server-status LOAD_COMPLETED?>?original-height 1486?>?original-width 1983?>?scaled-height 594?>?scaled-width 793?>?cloudpmc-path blobs/81ad/13220297/4313f91064af/jf6c02898_0004.gif?>?cloudpmc-bucket cdn?>Immobilization tends to protect the structure of
the enzyme from
the effects of pH; thus, higher pH stability favors storage and industrial
applications. As observed for ther
```


## PMC13316681 — review-article

*Archaea-driven bioremediation of polyolefins and polyesters in extreme environments*


### BM1F7BD124DF — dropped by `PH-X11;PH-X7;PH-X3`

- **was**: thermostability @ pH 5.0 = 60.0 degrees Celsius
- **section**: Archaeal enzymes and pathways for polyester and polyolefin degradation / Metagenomic discovery and structural characterisation of archaeal PETases
- **check**: CONFIRMED: article-type='review-article'
- **check**: CONFIRMED: table-concatenation signature in the quote
- **check**: enzyme-like tokens in the quote: ['BHET', 'IsPETase', 'LCC', 'MHET']
- **reason given**: Evidence is a concatenated review comparison-table cell ('...IsPETase and LCC; higher activity on BHET ...70 deg C/broad pH 5-8; thermostable at 60 deg C...') with no field boundaries. enzyme_name 'IsPETase' carries PET46's accession RLI42440.1.
- **quote**: BHET, MHET oligomers; feruloyl estersComparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer70 °C/broad pH 5–8; thermostable at 60 °C for prolonged incubationUnique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding;

```
rchaeia lineages and the evidentiary gap for polyolefin-active enzymes. Structural uniqueness, including the flexible lid domain and metal-cofactor interactions, confers advantages under extreme conditions in which bacterial counterparts lose activity. Nevertheless, reliance on metagenomic inference without widespread cultivation of the source organisms remains a methodological limitation, as noted in the anaerobic degradation context.Table 2 ¶ Reported archaeal taxa/enzymes with evidence of plastic-related degradation activity. ¶ ¶ Table 2Archaeal taxon/MAG origin ¶ Enzyme name/Accession ¶ Enzyme class/family ¶ Primary substrate(s) ¶ Key activity/products released ¶ Optimal conditions (temperature/pH) ¶ Structural/functional notes ¶ References ¶ ¶ Candidatus Bathyarchaeota (Guaymas Basin deep-sea hydrothermal sediments, uncultured) ¶ PET46 (RLI42440.1) ¶ Promiscuous feruloyl esterase (α/β-hydrolase fold with lid domain) ¶ Semi-crystalline PET powder; BHET, MHET oligomers; feruloyl esters ¶ Comparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer ¶ 70 °C/broad pH 5-8; thermostable at 60 °C for prolonged incubation ¶ Unique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding; Zn2+-dependent; promiscuous hydrolase adapted from plant cell wall degradation pathways ¶ Perez-Garcia et al. [10] ¶ ¶ Bathyarchaeia (Guaymas Basin deep-sea sediments, uncultured MAG) ¶ GuaPA ¶ PETase (distinct class, predicted novel structural features) ¶ Low-crystallinity PET film (BC-PET); releases TPA, MHET, and BHET ¶ Depolymerises PET film, releasing combined 4.4 mM TPA + MHET + BHET after 48 h incubation ¶ Not fully optimised in the primary report; activity at the mesophilic to thermophilic range inferred ¶ First archaeal enzyme shown to depolymerise PET film; belongs to a unique enzyme class differing from feruloyl esterases and bacterial PETases ¶ Acosta et al. [11] ¶ ¶ Halophilic archaea (general, e.g., Haloferax, Halobacterium spp. in hypersaline contexts
```


### BM800815CC90 — dropped by `PH-X11;PH-X7;PH-X3`

- **was**: pH stability @ pH 5.0 = 5.0 pH
- **section**: Archaeal enzymes and pathways for polyester and polyolefin degradation / Metagenomic discovery and structural characterisation of archaeal PETases
- **check**: CONFIRMED: article-type='review-article'
- **check**: CONFIRMED: table-concatenation signature in the quote
- **check**: enzyme-like tokens in the quote: ['BHET', 'IsPETase', 'LCC', 'MHET']
- **reason given**: Same garbled review table cell.
- **quote**: BHET, MHET oligomers; feruloyl estersComparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer70 °C/broad pH 5–8; thermostable at 60 °C for prolonged incubationUnique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding;

```
rchaeia lineages and the evidentiary gap for polyolefin-active enzymes. Structural uniqueness, including the flexible lid domain and metal-cofactor interactions, confers advantages under extreme conditions in which bacterial counterparts lose activity. Nevertheless, reliance on metagenomic inference without widespread cultivation of the source organisms remains a methodological limitation, as noted in the anaerobic degradation context.Table 2 ¶ Reported archaeal taxa/enzymes with evidence of plastic-related degradation activity. ¶ ¶ Table 2Archaeal taxon/MAG origin ¶ Enzyme name/Accession ¶ Enzyme class/family ¶ Primary substrate(s) ¶ Key activity/products released ¶ Optimal conditions (temperature/pH) ¶ Structural/functional notes ¶ References ¶ ¶ Candidatus Bathyarchaeota (Guaymas Basin deep-sea hydrothermal sediments, uncultured) ¶ PET46 (RLI42440.1) ¶ Promiscuous feruloyl esterase (α/β-hydrolase fold with lid domain) ¶ Semi-crystalline PET powder; BHET, MHET oligomers; feruloyl esters ¶ Comparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer ¶ 70 °C/broad pH 5-8; thermostable at 60 °C for prolonged incubation ¶ Unique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding; Zn2+-dependent; promiscuous hydrolase adapted from plant cell wall degradation pathways ¶ Perez-Garcia et al. [10] ¶ ¶ Bathyarchaeia (Guaymas Basin deep-sea sediments, uncultured MAG) ¶ GuaPA ¶ PETase (distinct class, predicted novel structural features) ¶ Low-crystallinity PET film (BC-PET); releases TPA, MHET, and BHET ¶ Depolymerises PET film, releasing combined 4.4 mM TPA + MHET + BHET after 48 h incubation ¶ Not fully optimised in the primary report; activity at the mesophilic to thermophilic range inferred ¶ First archaeal enzyme shown to depolymerise PET film; belongs to a unique enzyme class differing from feruloyl esterases and bacterial PETases ¶ Acosta et al. [11] ¶ ¶ Halophilic archaea (general, e.g., Haloferax, Halobacterium spp. in hypersaline contexts
```


### BMEF46DA6C6C — dropped by `PH-X11;PH-X7;PH-X3`

- **was**: thermostability @ pH 5.0 = 70.0 degrees Celsius
- **section**: Archaeal enzymes and pathways for polyester and polyolefin degradation / Metagenomic discovery and structural characterisation of archaeal PETases
- **check**: CONFIRMED: article-type='review-article'
- **check**: CONFIRMED: table-concatenation signature in the quote
- **check**: enzyme-like tokens in the quote: ['BHET', 'IsPETase', 'LCC', 'MHET']
- **reason given**: Same garbled review table cell.
- **quote**: BHET, MHET oligomers; feruloyl estersComparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer70 °C/broad pH 5–8; thermostable at 60 °C for prolonged incubationUnique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding;

```
rchaeia lineages and the evidentiary gap for polyolefin-active enzymes. Structural uniqueness, including the flexible lid domain and metal-cofactor interactions, confers advantages under extreme conditions in which bacterial counterparts lose activity. Nevertheless, reliance on metagenomic inference without widespread cultivation of the source organisms remains a methodological limitation, as noted in the anaerobic degradation context.Table 2 ¶ Reported archaeal taxa/enzymes with evidence of plastic-related degradation activity. ¶ ¶ Table 2Archaeal taxon/MAG origin ¶ Enzyme name/Accession ¶ Enzyme class/family ¶ Primary substrate(s) ¶ Key activity/products released ¶ Optimal conditions (temperature/pH) ¶ Structural/functional notes ¶ References ¶ ¶ Candidatus Bathyarchaeota (Guaymas Basin deep-sea hydrothermal sediments, uncultured) ¶ PET46 (RLI42440.1) ¶ Promiscuous feruloyl esterase (α/β-hydrolase fold with lid domain) ¶ Semi-crystalline PET powder; BHET, MHET oligomers; feruloyl esters ¶ Comparable PET powder hydrolysis to wild-type bacterial IsPETase and LCC; higher activity on BHET and MHET than on polymer ¶ 70 °C/broad pH 5-8; thermostable at 60 °C for prolonged incubation ¶ Unique flexible lid domain (three α-helices, two anti-parallel β-strands) enhances substrate binding; Zn2+-dependent; promiscuous hydrolase adapted from plant cell wall degradation pathways ¶ Perez-Garcia et al. [10] ¶ ¶ Bathyarchaeia (Guaymas Basin deep-sea sediments, uncultured MAG) ¶ GuaPA ¶ PETase (distinct class, predicted novel structural features) ¶ Low-crystallinity PET film (BC-PET); releases TPA, MHET, and BHET ¶ Depolymerises PET film, releasing combined 4.4 mM TPA + MHET + BHET after 48 h incubation ¶ Not fully optimised in the primary report; activity at the mesophilic to thermophilic range inferred ¶ First archaeal enzyme shown to depolymerise PET film; belongs to a unique enzyme class differing from feruloyl esterases and bacterial PETases ¶ Acosta et al. [11] ¶ ¶ Halophilic archaea (general, e.g., Haloferax, Halobacterium spp. in hypersaline contexts
```


## PMC7936011 — research-article

*A novel esterase from a soil metagenomic library displaying a broad substrate range*


### BM0DB57418F4 — dropped by `PH-X1`

- **was**: temperature optimum @ pH 7.0 = 25.0 degrees Celsius
- **section**: Materials and methods
- **check**: CONFIRMED: enclosed by a methods section -- 'Materials and methods'
- **reason given**: 'assayed by incubating ... at different temperatures in a range of 25-65 deg C' is the range tested. Recorded as temperature optimum = 25 deg C.
- **quote**: The optimum temperature for esterase activity of Tan410 was assayed by incubating the enzyme in 50 mM phosphate buffer (pH 7.0) at different temperatures in a range of 25–65 °C.

```
er library (phenyl acetate, ethyl acetate, propyl acetate, butyl acetate, isobutyl acetate, ethyl butyrate, ethyl hexanoate, ethyl octanoate, ethyl decanoate, ethyl oleate, vinyl acetate, vinyl butyrate, vinyl decanoate, vinyl pivalate, isopropenyl acetate, glyceryl triacetate, glyceryl tributyrate, methyl bromoacetate, ethyl bromoacetate and methyl glycolate) with p-nitrophenol used as a pH indicator to monitor ester hydrolysis colorimetrically (Esteban-Torres et al. 2013). Blank reactions with 1 mM sodium phosphate buffer (pH 7.0) were carried out for each substrate. ¶ Esterase activity on gallate esters (tannase activity) was determined using a rhodamine assay specific for gallic acid (Inoue and Hagerman 1988). And the amount of gallic acid in reaction mixture was determined as described previously (Yao et al. 2011). One unit of tannase activity was defined as the amount of enzyme required to release 1 μmol of gallic acid per minute. ¶ ¶ Effect of temperature and pH on esterase activity ¶ The optimum temperature for esterase activity of Tan410 was assayed by incubating the enzyme in 50 mM phosphate buffer (pH 7.0) at different temperatures in a range of 25-65 °C. Thermostability of Tan410 was investigated by pre-incubating the enzyme at 25-65 °C for 1 h and then analyzing the residual activity. The optimal pH values of Tan410 was measuring its activity at different pH values (4.0-9.0). Following buffers were used for the assay: 50 mM sodium acetate buffer (pH 4.0-6.0); 50 mM phosphate buffer (pH 5.5-8.0); 50 mM Tris-HCl buffer (pH 7.5-9.0). To study pH stability, Tan410 was incubated in different buffers (pH4.0-12.0) for 1 h. Then the pre-incubated solution was regulated to pH 7.0 with 500 mM phosphate buffer and analyzed for the residual activity. ¶ ¶ Effect of metal ions, detergents, inhibitor and organic solvents on esterase activity ¶ Effects of metal ions (Mg2+, Mn2+, Cu2+, Co2+, Zn2+, K+, Fe2+, Ni2+, Ca2+, Ag+ and Pb2+), detergents [CTAB (Cetyltrimethylammonium bromide) and SDS (Sodium dodecyl sulfate)] and inhibitor phenylmethylsulfonyl fluoride (PMSF) on esterase activity were investigated. Reaction solutions were assayed by i
```


### BM310A734B15 — dropped by `PH-X1;PH-X10`

- **was**: pH optimum @ pH 7.0 = 7.0 pH
- **section**: Materials and methods
- **check**: CONFIRMED: enclosed by a methods section -- 'Materials and methods'
- **check**: CONFIRMED: a shipped row covers ('PMC7936011', 'pH optimum', '7.0')
- **reason given**: Same methods sentence; pH 7.0 is the assay buffer, recorded as a pH optimum. The real optimum for Tan410 is captured by BM5BBF965026.
- **quote**: The optimum temperature for esterase activity of Tan410 was assayed by incubating the enzyme in 50 mM phosphate buffer (pH 7.0) at different temperatures in a range of 25–65 °C.

```
er library (phenyl acetate, ethyl acetate, propyl acetate, butyl acetate, isobutyl acetate, ethyl butyrate, ethyl hexanoate, ethyl octanoate, ethyl decanoate, ethyl oleate, vinyl acetate, vinyl butyrate, vinyl decanoate, vinyl pivalate, isopropenyl acetate, glyceryl triacetate, glyceryl tributyrate, methyl bromoacetate, ethyl bromoacetate and methyl glycolate) with p-nitrophenol used as a pH indicator to monitor ester hydrolysis colorimetrically (Esteban-Torres et al. 2013). Blank reactions with 1 mM sodium phosphate buffer (pH 7.0) were carried out for each substrate. ¶ Esterase activity on gallate esters (tannase activity) was determined using a rhodamine assay specific for gallic acid (Inoue and Hagerman 1988). And the amount of gallic acid in reaction mixture was determined as described previously (Yao et al. 2011). One unit of tannase activity was defined as the amount of enzyme required to release 1 μmol of gallic acid per minute. ¶ ¶ Effect of temperature and pH on esterase activity ¶ The optimum temperature for esterase activity of Tan410 was assayed by incubating the enzyme in 50 mM phosphate buffer (pH 7.0) at different temperatures in a range of 25-65 °C. Thermostability of Tan410 was investigated by pre-incubating the enzyme at 25-65 °C for 1 h and then analyzing the residual activity. The optimal pH values of Tan410 was measuring its activity at different pH values (4.0-9.0). Following buffers were used for the assay: 50 mM sodium acetate buffer (pH 4.0-6.0); 50 mM phosphate buffer (pH 5.5-8.0); 50 mM Tris-HCl buffer (pH 7.5-9.0). To study pH stability, Tan410 was incubated in different buffers (pH4.0-12.0) for 1 h. Then the pre-incubated solution was regulated to pH 7.0 with 500 mM phosphate buffer and analyzed for the residual activity. ¶ ¶ Effect of metal ions, detergents, inhibitor and organic solvents on esterase activity ¶ Effects of metal ions (Mg2+, Mn2+, Cu2+, Co2+, Zn2+, K+, Fe2+, Ni2+, Ca2+, Ag+ and Pb2+), detergents [CTAB (Cetyltrimethylammonium bromide) and SDS (Sodium dodecyl sulfate)] and inhibitor phenylmethylsulfonyl fluoride (PMSF) on esterase activity were investigated. Reaction solutions were assayed by i
```


### BM4EE39ACAFC — dropped by `PH-X1`

- **was**: pH stability @ pH 7.0 = 7.0 pH
- **section**: Materials and methods / Effect of temperature and pH on esterase activity
- **check**: CONFIRMED: enclosed by a methods section -- 'Materials and methods / Effect of temperature and pH on esterase activity'
- **reason given**: 'the pre-incubated solution was regulated to pH 7.0 ... and analyzed for residual activity' -- the readout pH of the stability assay, not a stability result.
- **quote**: Then the pre-incubated solution was regulated to pH 7.0 with 500 mM phosphate buffer and analyzed for the residual activity.

```
ing a rhodamine assay specific for gallic acid (Inoue and Hagerman 1988). And the amount of gallic acid in reaction mixture was determined as described previously (Yao et al. 2011). One unit of tannase activity was defined as the amount of enzyme required to release 1 μmol of gallic acid per minute. ¶ ¶ Effect of temperature and pH on esterase activity ¶ The optimum temperature for esterase activity of Tan410 was assayed by incubating the enzyme in 50 mM phosphate buffer (pH 7.0) at different temperatures in a range of 25-65 °C. Thermostability of Tan410 was investigated by pre-incubating the enzyme at 25-65 °C for 1 h and then analyzing the residual activity. The optimal pH values of Tan410 was measuring its activity at different pH values (4.0-9.0). Following buffers were used for the assay: 50 mM sodium acetate buffer (pH 4.0-6.0); 50 mM phosphate buffer (pH 5.5-8.0); 50 mM Tris-HCl buffer (pH 7.5-9.0). To study pH stability, Tan410 was incubated in different buffers (pH4.0-12.0) for 1 h. Then the pre-incubated solution was regulated to pH 7.0 with 500 mM phosphate buffer and analyzed for the residual activity. ¶ ¶ Effect of metal ions, detergents, inhibitor and organic solvents on esterase activity ¶ Effects of metal ions (Mg2+, Mn2+, Cu2+, Co2+, Zn2+, K+, Fe2+, Ni2+, Ca2+, Ag+ and Pb2+), detergents [CTAB (Cetyltrimethylammonium bromide) and SDS (Sodium dodecyl sulfate)] and inhibitor phenylmethylsulfonyl fluoride (PMSF) on esterase activity were investigated. Reaction solutions were assayed by incubating Tan410 and various metal ions (5 mM) for 1 h (at 4 °C) in 50 mM phosphate buffer (pH 7.0) and then analyzing the residual activity. To estimate the organic solvent tolerance of Tan410, enzyme solutions were mixed with various organic solvents (N,N- dimethyl formamide, ethyl acetate, isopropyl alcohol, isobutyl alcohol, isoamyl alcohol, acetone, methanol and ethanol) at a final concentration of 10%, and incubated at 4 °C for 1 h. Then the residual activity was assayed. Esterase activity measured in absence of any additive was taken as a control and was given a value of 100%. The ex
```


## PMC8265113 — research-article

*Characterization of glycoside hydrolase family 11 xylanase from Streptomyces sp. strain J103; its synergetic effect with*


### BM488F8758D1 — dropped by `PH-X6;PH-X1`

- **was**: temperature optimum @ pH 5.0 = 55.0 degrees Celsius
- **section**: Results / Effect of pH and temperature on rXynS1 activity
- **check**: CHALLENGED: enclosed by a results section -- 'Results / Effect of pH and temperature on rXynS1 activity'
- **check**: CONFIRMED: title/abstract name off-target class ['glycoside hydrolase', 'xylanase']
- **reason given**: rXynS1 is a GH11 xylanase (glycoside hydrolase), off-target; and pH 5.0 is the assay pH ('assayed at pH 5.0'), not an optimum.
- **quote**: 3a). rXynS1 showed optimal activity at 55 °C (assayed at pH 5.0), with the enzyme still displaying over 80% of its activity in the temperature range of 50–60 °C (Fig.

```
with 1 mM and 0.01 mM IPTG. The lane abbreviations indicate the followings: M, protein marker; T, whole cell lysate after IPTG induction; S, soluble protein after IPTG induction; IN, insoluble protein after IPTG induction; E, protein purified using the His·Bind® Resin Chromatography Kit (5 times diluted) ¶ ¶ ?cloudpmc-path blobs/ebc6/8265113/ba1e0a5027ca/12934_2021_1619_Fig2_HTML.jpg?>?cloudpmc-bucket cdn?>?image-server-status LOAD_COMPLETED?>?original-height 1346?>?original-width 1594?>?scaled-height 673?>?scaled-width 797?>?cloudpmc-path blobs/ebc6/8265113/a4b391863f20/12934_2021_1619_Fig2_HTML.gif?>?cloudpmc-bucket cdn?> ¶ Effect of pH and temperature on rXynS1 activity ¶ The effect of pH and temperature on the release of reducing sugars from beechwood xylan is shown in Fig. 3. Maximum relative activity was observed at pH 5.0, and the enzyme had a relative activity of over 58% at pH 6.0 and 7.0. Relative activities were drastically decreased for pH values below a pH of 4.0 and over a pH of 8.0 (Fig. 3a). rXynS1 showed optimal activity at 55 °C (assayed at pH 5.0), with the enzyme still displaying over 80% of its activity in the temperature range of 50-60 °C (Fig. 3b). According to the pH stability assay results, the relative activities were higher than 65% for the pH range starting from 4.0-7.0 and 5.0-7.0 after an incubation period of 1 h and 2 h, respectively (Fig. 3c). The enzyme was incubated with phosphate citrate buffer (pH 5.0) at 50 °C, 55 °C, and 60 °C (Fig. 3d) to test the thermal stability. The relative activity of rXynS1 was retained over 80% and 40% throughout the incubation period at 50 °C and 55 °C respectively, within 120 min. After a 40 min incubation period at 60 °C, the enzyme had lost its activity. Commercial xylanase (cXyl) with a concentration similar to that of rXynS1 was used to study rXynS1 activity at different pH and temperatures (see Additional file 1). cXyl exhibited an optimal pH at 7.0 and optimal temperature at 70 °C. The estimated Km and Vmax values at optimal conditions were 51.4 mg/mL and 898.2 U/mg, respectively (see Additional file 2). ¶ ?disp-level 3?>Fig. 3 ¶ Effect of pH and temperatu
```


### BM5B4789AA54 — dropped by `PH-X6;PH-X1`

- **was**: pH optimum @ pH 5.0 = 5.0 pH
- **section**: Results / Effect of pH and temperature on rXynS1 activity
- **check**: CHALLENGED: enclosed by a results section -- 'Results / Effect of pH and temperature on rXynS1 activity'
- **check**: CONFIRMED: title/abstract name off-target class ['glycoside hydrolase', 'xylanase']
- **reason given**: Same GH11 xylanase article.
- **quote**: 3a). rXynS1 showed optimal activity at 55 °C (assayed at pH 5.0), with the enzyme still displaying over 80% of its activity in the temperature range of 50–60 °C (Fig.

```
with 1 mM and 0.01 mM IPTG. The lane abbreviations indicate the followings: M, protein marker; T, whole cell lysate after IPTG induction; S, soluble protein after IPTG induction; IN, insoluble protein after IPTG induction; E, protein purified using the His·Bind® Resin Chromatography Kit (5 times diluted) ¶ ¶ ?cloudpmc-path blobs/ebc6/8265113/ba1e0a5027ca/12934_2021_1619_Fig2_HTML.jpg?>?cloudpmc-bucket cdn?>?image-server-status LOAD_COMPLETED?>?original-height 1346?>?original-width 1594?>?scaled-height 673?>?scaled-width 797?>?cloudpmc-path blobs/ebc6/8265113/a4b391863f20/12934_2021_1619_Fig2_HTML.gif?>?cloudpmc-bucket cdn?> ¶ Effect of pH and temperature on rXynS1 activity ¶ The effect of pH and temperature on the release of reducing sugars from beechwood xylan is shown in Fig. 3. Maximum relative activity was observed at pH 5.0, and the enzyme had a relative activity of over 58% at pH 6.0 and 7.0. Relative activities were drastically decreased for pH values below a pH of 4.0 and over a pH of 8.0 (Fig. 3a). rXynS1 showed optimal activity at 55 °C (assayed at pH 5.0), with the enzyme still displaying over 80% of its activity in the temperature range of 50-60 °C (Fig. 3b). According to the pH stability assay results, the relative activities were higher than 65% for the pH range starting from 4.0-7.0 and 5.0-7.0 after an incubation period of 1 h and 2 h, respectively (Fig. 3c). The enzyme was incubated with phosphate citrate buffer (pH 5.0) at 50 °C, 55 °C, and 60 °C (Fig. 3d) to test the thermal stability. The relative activity of rXynS1 was retained over 80% and 40% throughout the incubation period at 50 °C and 55 °C respectively, within 120 min. After a 40 min incubation period at 60 °C, the enzyme had lost its activity. Commercial xylanase (cXyl) with a concentration similar to that of rXynS1 was used to study rXynS1 activity at different pH and temperatures (see Additional file 1). cXyl exhibited an optimal pH at 7.0 and optimal temperature at 70 °C. The estimated Km and Vmax values at optimal conditions were 51.4 mg/mL and 898.2 U/mg, respectively (see Additional file 2). ¶ ?disp-level 3?>Fig. 3 ¶ Effect of pH and temperatu
```


## PMC9772341 — research-article

*Sourcing thermotolerant poly(ethylene terephthalate) hydrolase scaffolds from natural diversity*


### BM037C0E4939 — dropped by `PH-X1`

- **was**: pH optimum @ pH 6.0 = 6.0 pH
- **section**: Methods / Screening for activity on amorphous PET film
- **check**: CONFIRMED: enclosed by a methods section -- 'Methods / Screening for activity on amorphous PET film'
- **reason given**: 'For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using ...' -- a methods sentence describing which enzymes were screened.
- **quote**: For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5).

```
or each analyte was analyzed every 12-24 samples to ensure the integrity of the initial calibration. Samples were diluted with ultrapure water for analysis and maintained at 15 °C during the analysis. ¶ ¶ Screening for activity on amorphous PET film ¶ In each screening reaction, 2.9% loading by mass of an amorphous PET film (Goodfellow) was incubated with 10 μg enzyme of interest (0.7 mg enzyme/g PET), unless noted otherwise in Supplementary Table 11 due to low expression levels. Reactions were performed in polypropylene tubes containing 100 mM NaCl and 50 mM buffering agent (citrate at pH 6.0, NaH2PO4 at pH 7.0, NaH2PO4 at pH 7.5, HEPES at pH 7.5, bicine at pH 8.0, and glycine at pH 9.0) and incubated at 30, 40, 50, 60, or 70 °C. All reactions were terminated after 96 h by the addition of an equal volume of 100% methanol and PET was removed from the reaction solution. Soluble fractions were filtered through 0.2 μm nylon filters for monomer quantitation. All PET hydrolysis screening reactions were performed in triplicate. ¶ For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 μg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5). The reactions were again stopped at 96 h by the additional of an equal volume of 100% methanol and worked up in the same manner as described directly above. ¶ Aromatic product release data are reported throughout relative to background aromatic product release detected in no-enzyme control reactions at each pH and temperature. Background aromatic product release for both amorphous PET film and crystalline PET powder was below the detection limit for all pH and temperature combinations tested. ¶ ¶ Characterization of PET hydrolysis activity on varied substrates with time resolution ¶ Using the reaction conditions (buffer and temperature combination) where peak PET hydrolysis activity was measured from the screening assays, a selection of enzymes was further characterized over a 168 h reaction on amorphous PET film (Goodfellow), crystalline PET powder (Goodfellow), and an amorphous PET powder produced in-house through cryomilling of the Goodfell
```


### BM2646680E59 — dropped by `PH-X4`

- **was**: pH optimum @ pH 6.0 = 6.0 pH
- **section**: Results / Screening on amorphous PET shows that PET hydrolysis activity is distributed among all seven phylogenetic groups
- **check**: enzyme-like tokens in the quote: none
- **reason given**: 'the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715)' -- four distinct enzymes collapsed into one unattributed row.
- **quote**: For the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715), we further extended the pH screen.

```
and reaction temperature (30, 40, 50, 60, or 70 °C). The heat maps for all other enzymes tested on amorphous PET film are shown in Supplementary Fig. 3. Source data are provided as a Source Data file. ¶ ¶ ?image-name 41467_2022_35237_Fig2_HTML.jpg?>?image-size 80078?>?image-md5 70a73ddf00cfd497377f4ee374979fbb?>?image-image-server-status LOAD_COMPLETED?>?image-original-height 1310?>?image-original-width 1999?>?image-scaled-height 524?>?image-scaled-width 799?>?image-cloudpmc-urn urn:cdn:blobs/2743/9772341/70a73ddf00cf/41467_2022_35237_Fig2_HTML.jpg?>?thumb-name 41467_2022_35237_Fig2_HTML.gif?>?thumb-size 5461?>?thumb-md5 07d984344b5a0e642ab820bcdb0b4f72?>?thumb-image-server-status NEVER_LOAD?>?thumb-scaled-height 80?>?thumb-scaled-width 122?>?thumb-cloudpmc-urn urn:cdn:blobs/2743/9772341/07d984344b5a/41467_2022_35237_Fig2_HTML.gif?> ¶ As shown in Fig. 2, there is a breadth of activity across the pH and temperature ranges studied, with activity of at least one enzyme in every condition tested. For the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715), we further extended the pH screen. As shown in Supplementary Fig. 4, the ICCG variant of LCC is active in buffered medium with a pH as low as 5.0, while 102 was not active at pH below 6.0, and 611, 702, and 715 all exhibit detectable activity at pH <6.0. ¶ ¶ Characterization of the best-performing enzymes highlights reactivity differences as a function of substrate ¶ We were also interested to learn if the best-performing enzymes from each phylogenetic group would exhibit different reactivity profiles as a function of PET substrate. For these comparisons, we used two commercially available substrates that have been thoroughly characterized59, namely a crystalline Goodfellow PET powder and the same Goodfellow amorphous PET film used for screening. This set included 12 enzymes selected to represent a diverse group for which the highest extents of conversion were observed during screening, and hydrolysis reactions utilized the single best reaction condition identified during screening on amorphous PET film (Supp
```


### BM3A4FF0E21E — dropped by `PH-X1;PH-X9`

- **was**: salt effect @ pH 6.0 = 2.9 % relative activity
- **section**: Methods / Screening for activity on amorphous PET film
- **check**: CONFIRMED: enclosed by a methods section -- 'Methods / Screening for activity on amorphous PET film'
- **reason given**: value_std 2.9 '% relative activity' was parsed from '2.9% loading by mass of amorphous PET film' -- a substrate loading, not an activity. Unit misparse.
- **quote**: For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 µg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5).

```
or each analyte was analyzed every 12-24 samples to ensure the integrity of the initial calibration. Samples were diluted with ultrapure water for analysis and maintained at 15 °C during the analysis. ¶ ¶ Screening for activity on amorphous PET film ¶ In each screening reaction, 2.9% loading by mass of an amorphous PET film (Goodfellow) was incubated with 10 μg enzyme of interest (0.7 mg enzyme/g PET), unless noted otherwise in Supplementary Table 11 due to low expression levels. Reactions were performed in polypropylene tubes containing 100 mM NaCl and 50 mM buffering agent (citrate at pH 6.0, NaH2PO4 at pH 7.0, NaH2PO4 at pH 7.5, HEPES at pH 7.5, bicine at pH 8.0, and glycine at pH 9.0) and incubated at 30, 40, 50, 60, or 70 °C. All reactions were terminated after 96 h by the addition of an equal volume of 100% methanol and PET was removed from the reaction solution. Soluble fractions were filtered through 0.2 μm nylon filters for monomer quantitation. All PET hydrolysis screening reactions were performed in triplicate. ¶ For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using 2.9% loading by mass of amorphous PET film (Goodfellow) and 10 μg enzyme of interest (0.7 mg enzyme/g PET enzyme loading) in polypropylene tubes containing 100 mM NaCl and 50 mM citrate (pH 5.5 and pH 5.0) or 50 mM sodium acetate (pH 5.0 and pH 4.5). The reactions were again stopped at 96 h by the additional of an equal volume of 100% methanol and worked up in the same manner as described directly above. ¶ Aromatic product release data are reported throughout relative to background aromatic product release detected in no-enzyme control reactions at each pH and temperature. Background aromatic product release for both amorphous PET film and crystalline PET powder was below the detection limit for all pH and temperature combinations tested. ¶ ¶ Characterization of PET hydrolysis activity on varied substrates with time resolution ¶ Using the reaction conditions (buffer and temperature combination) where peak PET hydrolysis activity was measured from the screening assays, a selection of enzymes was further characterized over a 168 h reaction on amorphous PET film (Goodfellow), crystalline PET powder (Goodfellow), and an amorphous PET powder produced in-house through cryomilling of the Goodfell
```


## PMC9839772 — research-article

*Improving the activity and thermostability of PETase from Ideonella sakaiensis through modulating its post-translational*


### BM7D11018C05 — dropped by `PH-X1`

- **was**: pH stability @ pH 8.0 = 8.0 pH
- **section**: Methods / Analysis of the thermostability of IsPETase and Fast-PETase
- **check**: CONFIRMED: enclosed by a methods section -- 'Methods / Analysis of the thermostability of IsPETase and Fast-PETase'
- **reason given**: 'the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 deg C ... followed by determining the residual activity' -- pH 8.0 is the buffer of a thermostability protocol.
- **quote**: Next, 0.4 mg of the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 °C for 3, 6, 9, and 12 h, followed by determining the residual activity.

```
n, the supernatant was collected after 120 h and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C and the protein concentration in the protein was determined using the Bradford kit (Beyotime, China), followed by digestion with Endo H for half an hour. Next, 0.1 mg of the enzyme was incubated in 1 mL of 50 mM glycine-NaOH buffer (pH 9.0) at 50, 60 and 70 °C for 2 h (sampling every 0.5 h), followed by determining the residue activity. To analyze the thermostability of IsPETase from the high-density fermentation, the supernatant was collected and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C, followed by treated with Endo H for half an hour. Next, 0.4 mg of the enzyme was incubated in 1 mL of 50 mM glycine-NaOH buffer (pH 9.0) at 40, 45 and 50 °C for 1, 3, 6, 9, and 12 h, followed by determining the residue activity. To analyze the thermostability of Fast-PETase, the supernatant was collected and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C, followed by treated with Endo H for half an hour. Next, 0.4 mg of the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 °C for 3, 6, 9, and 12 h, followed by determining the residual activity. Enzymes without treatment was used as the negative control. All of the experiments were carried out in triplicate. ¶ ¶ Kinetic analysis ¶ To obtain kinetic parameters for MHET and BHET, a pseudo-one-substrate kinetic model was used as described previously30. The kinetic parameters were determined from three independent initial rate measurements performed with the same batch of purified enzymes. The protein concentration was determined using the Bradford kit (Beyotime, China). For parital-deglyco IsPETase-Pp, the concentration of MHET and BHET were 0.08 mM to 3 mM. The reaction was carried out at 30 °C for 2 h in 50 mM glycine-NaOH buffer (pH 9.0). For IsPETase-Ec, the concentration of MHET and BHET were 0.08 mM to 1.5 mM and 0.06 mM to 2 mM. The reaction was carried out at 30 °C in 50 mM glycine-NaOH buffer (pH 9.0) for 3 and 1 h, respectively. The initial rate was measured by measuring the released TPA using HPLC. Initial rate data were fitted to
```


### BMC3719577E5 — dropped by `PH-X1`

- **was**: thermostability @ pH 8.0 = 70.0 degrees Celsius
- **section**: Methods / Analysis of the thermostability of IsPETase and Fast-PETase
- **check**: CONFIRMED: enclosed by a methods section -- 'Methods / Analysis of the thermostability of IsPETase and Fast-PETase'
- **reason given**: Same methods sentence; 70 deg C is the highest temperature tested, recorded as a thermostability value.
- **quote**: Next, 0.4 mg of the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 °C for 3, 6, 9, and 12 h, followed by determining the residual activity.

```
n, the supernatant was collected after 120 h and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C and the protein concentration in the protein was determined using the Bradford kit (Beyotime, China), followed by digestion with Endo H for half an hour. Next, 0.1 mg of the enzyme was incubated in 1 mL of 50 mM glycine-NaOH buffer (pH 9.0) at 50, 60 and 70 °C for 2 h (sampling every 0.5 h), followed by determining the residue activity. To analyze the thermostability of IsPETase from the high-density fermentation, the supernatant was collected and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C, followed by treated with Endo H for half an hour. Next, 0.4 mg of the enzyme was incubated in 1 mL of 50 mM glycine-NaOH buffer (pH 9.0) at 40, 45 and 50 °C for 1, 3, 6, 9, and 12 h, followed by determining the residue activity. To analyze the thermostability of Fast-PETase, the supernatant was collected and dialyzed with a Millipore 10-kDa cut-off membrane at 4 °C, followed by treated with Endo H for half an hour. Next, 0.4 mg of the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 °C for 3, 6, 9, and 12 h, followed by determining the residual activity. Enzymes without treatment was used as the negative control. All of the experiments were carried out in triplicate. ¶ ¶ Kinetic analysis ¶ To obtain kinetic parameters for MHET and BHET, a pseudo-one-substrate kinetic model was used as described previously30. The kinetic parameters were determined from three independent initial rate measurements performed with the same batch of purified enzymes. The protein concentration was determined using the Bradford kit (Beyotime, China). For parital-deglyco IsPETase-Pp, the concentration of MHET and BHET were 0.08 mM to 3 mM. The reaction was carried out at 30 °C for 2 h in 50 mM glycine-NaOH buffer (pH 9.0). For IsPETase-Ec, the concentration of MHET and BHET were 0.08 mM to 1.5 mM and 0.06 mM to 2 mM. The reaction was carried out at 30 °C in 50 mM glycine-NaOH buffer (pH 9.0) for 3 and 1 h, respectively. The initial rate was measured by measuring the released TPA using HPLC. Initial rate data were fitted to
```
