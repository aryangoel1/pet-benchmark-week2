# pH benchmark -- audit report

Every one of the **105 candidate pH rows** inherited from the Week-2 benchmark carries an explicit verdict below. The verdicts live in `scripts/ph_curation.py`; this document is generated from them, so the two cannot drift apart.

> **What this audit is.** Each candidate was read against the evidence sentence that the Week-2 pipeline stored with it. That pipeline had already located every sentence in a freshly downloaded copy of its article, so the quote is reliable as *text*. What this pass adds is a judgement about whether the recorded number is the right reading of that text -- which enzyme it belongs to, whether it is a result or a protocol detail, and which way the effect ran. It is **not** a re-reading of all 44 source articles end to end.

## Outcome

| | Rows | Share |
|---|---:|---:|
| Candidates inherited from Week 2 | 105 | 100% |
| **Removed by the audit** | **38** | 36.2% |
| **Shipped** | **67** | 63.8% |
| Shipped rows carrying at least one correction | 65 | |

Source articles went from 44 to **30**: 14 articles lost every row they contributed.

## Why rows were removed

| Rule | What it catches | Rows |
|---|---|---:|
| `PH-X1` methods_or_protocol_sentence | the value came from a methods or protocol sentence -- an assay buffer, an incubation temperature, the range of conditions tested, or the baseline used for normalisation -- rather than from a measured outcome | 13 |
| `PH-X6` off_target_enzyme_class | the enzyme is not a carboxylester hydrolase or polymer depolymerase | 8 |
| `PH-X7` secondhand_or_review | the sentence restates another study's result, or the article is a review | 7 |
| `PH-X3` enzyme_attribution_mismatch | the enzyme name or accession on the row is not the enzyme the evidence sentence describes | 6 |
| `PH-X9` measurement_type_unsupported | the evidence contains no measurement of the type the row claims | 6 |
| `PH-X10` duplicate_measurement | the same enzyme, article, measurement type and pH is already represented by a better-evidenced row | 3 |
| `PH-X11` garbled_table_extraction | the evidence is a concatenated table cell with no recoverable field boundaries | 3 |
| `PH-X4` ambiguous_multi_enzyme | the evidence covers two or more enzymes with different values, or names no enzyme at all, so the value cannot be attributed | 3 |
| `PH-X12` no_outcome_at_stated_pH | a boundary word ('beyond', 'above') with no outcome actually measured at the recorded pH | 1 |
| `PH-X2` range_endpoint_as_optimum | the row was typed as a pH optimum but the value is the endpoint of an activity range, and the source states a different optimum | 1 |
| `PH-X5` model_predicted_value | the value is a model or response-surface prediction, not a measurement | 1 |
| `PH-X8` analytical_method_pH | the pH belongs to an analytical procedure (chromatography, NMR), not to an enzyme assay | 1 |

A row can fire more than one rule, so the column sums to more than 38.

## Corrections applied to rows that were kept

| Rule | What it does | Rows |
|---|---|---:|
| `PH-C7` direction_set | direction of the effect recorded, so a stability row says whether activity was held or lost | 54 |
| `PH-C5` enzyme_named | enzyme name set, or corrected, from the evidence sentence | 52 |
| `PH-C3` outcome_recovered | the outcome at that pH (residual or relative activity) recovered from the sentence into a field of its own | 29 |
| `PH-C6` range_bounds_set | pH interval bounds set to the range the article states | 18 |
| `PH-C2` type_reclassified | measurement type changed to match what the sentence actually reports | 16 |
| `PH-C1` optimum_corrected | pH optimum reset to the value the article states, where the pipeline had stored a range endpoint instead | 5 |
| `PH-C4` buffer_cleared | a buffer removed that the evidence does not name and that cannot hold the recorded pH | 4 |

## The five findings that mattered most

1. **A tier-A sequence was attached to the wrong enzyme.** `BME732B05FC1` carried accession `P26495` (PhaZ) on a sentence about LIP4. A wrong sequence on a real measurement is the worst defect a benchmark can ship, because it looks correct in every automated check.

2. **A model-predicted value had survived into a dataset whose integrity statement forbids them.** `BM539CC031EB` recorded pH 7.5 from *"The model predicted maximum biodegradation at pH 7.5"* -- a response-surface optimisation over whole-cell biodegradation.

3. **Range endpoints were being shipped as optima.** Five rows named a pH optimum that was really the low end of an activity range, while the same sentence gave the true optimum: `pH 5 -> 7`, `4.0 -> 5.0`, `7.5 -> 8.0`, `7.0 -> 8.0`, `7.0 -> 7.5`. Each is a 0.5-2.0 unit error in the exact quantity the screener predicts.

4. **Thirteen rows were assay protocol, not results** -- buffer pH read as a pH optimum, incubation temperature read as thermostability, the range of temperatures tested read as the optimum, and in one case a substrate loading (*"2.9% loading by mass of amorphous PET film"*) parsed as 2.9% relative activity.

5. **A review article's comparison table produced three rows** on a garbled concatenated cell, labelled `IsPETase` but carrying PET46's accession.

## Every candidate, with its verdict


### PMC11651597 &mdash; 7 kept / 9 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0A3FCD8E37` | **drop** | thermostability | 6.0 | PH-X9 | 35 deg C is the incubation temperature of the pH-stability assay in this sentence; recorded as a thermostability measurement of 35 deg C. No thermostability value is stated. |
| `BM0D67FCB6F6` | KEEP | pH stability | 9.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | Range statement 'stable between pH 6 and pH 9, retaining 89-97%'. Typed as a pH-stability range; pH 9.0 is the upper endpoint of range group R-11651597-a. |
| `BM499AE86AAE` | KEEP | pH stability | 8.0 | PH-C2;PH-C3;PH-C5 | 'retaining 93% of its activity at pH 6 and 82% at pH 8' is the activity-vs-pH profile, not the post-incubation stability profile. Reclassified to pH activity. |
| `BM71030D2A05` | **drop** | pH stability | 7.0 | PH-X1 | Normalisation sentence: 'activity at pH 7 was set as 100% ... for pH stability the activity without pre-incubation was set at 100%'. Defines the assay baseline, not a measured outcome. The optimum it implies is captured by the corrected BMDFDCB2C50A. |
| `BM73CD9BDECC` | KEEP | pH stability | 11.0 | PH-C3;PH-C5;PH-C7 | 'further decline to 22% at pH 11' -- residual activity after 1 h. |
| `BMC31B27FC98` | KEEP | pH stability | 10.0 | PH-C3;PH-C5;PH-C7 | 'only 51% residual activity observed after one h' at pH 10. |
| `BMDFDCB2C50A` | KEEP | pH optimum | 5.0 | PH-C1;PH-C5;PH-C6;PH-C7 | Recorded pH optimum 5.0 was the LOW END of the activity range. The same sentence states 'optimal activity observed at pH 7'. Optimum corrected 5.0 -> 7.0, active range 5.0-9.0 retained as bounds. |
| `BMF54859EFAF` | KEEP | pH stability | 6.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | Lower endpoint of the same range statement as BM0D67FCB6F6 (range group R-11651597-a). Kept as a separate endpoint row to match Luke's one-row-per-endpoint convention for pH ranges. |
| `BMFBD1521130` | KEEP | pH stability | 6.0 | PH-C2;PH-C3;PH-C5 | Same sentence as BM499AE86AAE, pH 6 point. Reclassified to pH activity. |

### PMC10146132 &mdash; 5 kept / 5 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM22F8594502` | KEEP | pH stability | 6.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | 'A pH of 6.0~10.0 had good stability ... more than 60%' is a coarse range summary that the same article contradicts with 'when pH 10.0, less than 50% retained' (BM7E8AC1F540). Kept as a range row, flagged internal_conflict, NOT scored. |
| `BM355F56FDED` | KEEP | pH stability | 9.0 | PH-C3;PH-C5;PH-C7 | 'about 90% of the enzyme activity was retained when pH = 9.0'. |
| `BM7E8AC1F540` | KEEP | pH stability | 10.0 | PH-C3;PH-C5;PH-C7 | 'When pH 10.0, less than 50% of the enzyme activity was retained'. |
| `BMB113AB078A` | KEEP | pH stability | 3.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | 'less stable when pH was 3.0 to 5.0 ... lost when pH was 3.0 ... less than 50% when pH was 4.0 to 5.0'. A destabilising range, not a point. |
| `BMFA666F5868` | KEEP | pH stability | 8.0 | PH-C3;PH-C5;PH-C7 | 'pH 8.0, the best stability of enzyme activity, could retain about 80%'. |

### PMC10385968 &mdash; 4 kept / 5 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM961F2AE8B7` | KEEP | temperature optimum | 8.0 | PH-C5 | Covariate row: temperature optimum 40 deg C restated in the kinetics sentence, assayed at pH 8. |
| `BMA7FF240F0C` | KEEP | pH stability | 8.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | 'favorable pH stability between pH 8 to pH 11 ... retained at least 80% activity'. Lower endpoint of range group R-10385968-a. |
| `BMBE4B247046` | KEEP | pH optimum | 8.0 | PH-C5;PH-C7 | 'The optimal pH for EstD04 activity was pH 8.' |
| `BMC71D9F94EF` | **drop** | pH optimum | 8.0 | PH-X10 | pH optimum 8.0 for EstD04 restated in the kinetics sentence -- same enzyme, paper, type and value as BMBE4B247046, which comes from the direct statement. |
| `BMF8D20A14F6` | KEEP | pH stability | 11.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | Upper endpoint of range group R-10385968-a. |

### PMC12896513 &mdash; 2 kept / 5 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM43A7E54ACA` | **drop** | thermostability | 7.0 | PH-X1 | 'The residual activity was then measured at 40 deg C in 50 mM sodium phosphate (pH 7.0)' is the assay readout condition. Recorded as thermostability = 40 deg C. |
| `BM4FD5205F58` | **drop** | pH stability | 7.0 | PH-X1 | Same methods sentence, recorded as pH stability = 7.0. pH 7.0 is the readout buffer. |
| `BM5D7F089EA5` | KEEP | pH stability | 4.0 | PH-C3;PH-C5;PH-C7 | 'residual activity of rEST-24 did not exceed 30%' across the pH values tested, of which 4.0 is one. Attributable to rEST-24; coarse upper bound only. |
| `BM7EDDB0F663` | **drop** | pH stability | 7.0 | PH-X1;PH-X10 | Second copy of the same methods statement ('residual activity measured in 50 mM sodium phosphate buffer at pH 7.0'); duplicate of BM4FD5205F58 and equally unusable. |
| `BME50151456E` | KEEP | pH optimum | 7.0 | PH-C5;PH-C7 | 'rEST-24 esterase exhibited maximum activity at pH 7.0 only'. The co-named rEST-28 has a different reported optimum (6.0-7.0), so the row is attributed to rEST-24. |

### PMC9709933 &mdash; 5 kept / 5 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0E71BF8DE3` | KEEP | pH stability | 6.0 | PH-C3;PH-C7 | 97% residual after 3 h at pH 6.0. |
| `BM321B809084` | KEEP | pH stability | 8.0 | PH-C3;PH-C7 | 82% residual after 3 h at pH 8.0. |
| `BM60B9ABF4DB` | KEEP | pH stability | 4.0 | PH-C3;PH-C7 | 74% residual after 1 h at pH 4.0. |
| `BM9F253201A6` | KEEP | pH stability | 7.0 | PH-C3;PH-C7 | ~100% residual after 1 h at pH 7.0. |
| `BMAFA2119D8D` | KEEP | pH stability | 11.0 | PH-C3;PH-C7 | 55% residual after 1 h at pH 11.0. |

### PMC10003648 &mdash; 3 kept / 4 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM6E32E848BD` | KEEP | temperature optimum | 8.0 | PH-C4 | Covariate row: temperature optimum 45-50 deg C at pH 8. Buffer MES cleared -- not in the evidence and outside its buffering range at pH 8. |
| `BM94ACC9E0C2` | KEEP | pH stability | 8.0 | PH-C2;PH-C6;PH-C7 | 'PhaZ showing higher relative activity at pH 8.0-10.0' -- a range, not a point. |
| `BM9A302CF0A9` | KEEP | pH optimum | 8.0 | PH-C4;PH-C7 | 'LIP3 and PhaZ ... optimal activity at pH 8'. Both enzymes share the stated optimum, so attribution to PhaZ is safe but flagged. Buffer MES cleared. |
| `BME732B05FC1` | **drop** | pH stability | 5.0 | PH-X3 | Accession P26495 is PhaZ, but the evidence sentence is about LIP4: 'LIP4 retained more activity (>80%) at pH 5.0-6.0'. A tier-A sequence misattribution -- the worst class of defect a benchmark can carry. |

### PMC7936011 &mdash; 1 kept / 4 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0DB57418F4` | **drop** | temperature optimum | 7.0 | PH-X1 | 'assayed by incubating ... at different temperatures in a range of 25-65 deg C' is the range tested. Recorded as temperature optimum = 25 deg C. |
| `BM310A734B15` | **drop** | pH optimum | 7.0 | PH-X1;PH-X10 | Same methods sentence; pH 7.0 is the assay buffer, recorded as a pH optimum. The real optimum for Tan410 is captured by BM5BBF965026. |
| `BM4EE39ACAFC` | **drop** | pH stability | 7.0 | PH-X1 | 'the pre-incubated solution was regulated to pH 7.0 ... and analyzed for residual activity' -- the readout pH of the stability assay, not a stability result. |
| `BM5BBF965026` | KEEP | pH optimum | 7.0 | PH-C5;PH-C7 | 'esterase Tan410 showed its highest activity at pH 7.0'. |

### PMC10146679 &mdash; 0 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM06A72D7AB0` | **drop** | pH stability | 7.0 | PH-X9 | pH 7.0 is the assay condition of a thermal statement; no pH-stability measurement. |
| `BM9DD54D4438` | **drop** | thermostability | 7.0 | PH-X9 | 'activity increased from 30 deg C to 40 deg C' -- 30 is a profile boundary, not a thermostability value. |
| `BMAD704A1BA4` | **drop** | thermostability | 7.0 | PH-X9 | Same sentence; 40 is the other profile boundary. |

### PMC10495362 &mdash; 1 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0578A48B89` | **drop** | pH optimum | 6.0 | PH-X7;PH-X3 | 'In their study, the PET46-like 211 released ...' -- a secondhand sentence about a different enzyme (PET46-like 211), carrying PET46's accession RLI42440.1. |
| `BM6A82469C45` | **drop** | temperature optimum | 6.0 | PH-X7;PH-X3 | Same secondhand sentence, temperature axis. |
| `BMB8B8558C40` | KEEP | pH stability | 5.0 | PH-C3;PH-C5;PH-C7 | 'it also retained high activities (50%) at pH 5' -- the article's own enzyme. |

### PMC12428281 &mdash; 2 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM47946FE1B3` | **drop** | thermostability | 3.0 | PH-X9 | 4 deg C is the incubation temperature of a pH-stability experiment, recorded as a thermostability measurement of 4 deg C. |
| `BME71810CC95` | KEEP | pH optimum | 8.0 | PH-C5;PH-C6;PH-C7 | 'the optimal pH was 8.0, and DehpH showed relatively high activity ranging from pH 6.0 to pH 9.0'. |
| `BME7E3DA9213` | KEEP | pH stability | 3.0 | PH-C2;PH-C5;PH-C6;PH-C7 | 'activity decreased significantly under acid conditions (pH 3.0 to 6.0) and almost lost all of its activity under pH 3.0'. The loss is qualitative -- the sentence gives no percentage -- so no outcome value is recorded, only the direction. |

### PMC12734981 &mdash; 2 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM097BBDB7F2` | **drop** | pH stability | 8.0 | PH-X12 | 'A rapid decline in activity was detected beyond pH 8.0' -- no outcome is measured AT pH 8.0; the only quantified point in the sentence is pH 9.0 (BM51F74D231E). |
| `BM51F74D231E` | KEEP | pH stability | 9.0 | PH-C3;PH-C5;PH-C7 | 'less than 15% residual activity at pH 9.0'. enzyme_name corrected CALB -> PanLipdN: the article characterises a CALB-LIKE enzyme, not CALB. |
| `BMDC3A7C490D` | KEEP | pH optimum | 8.0 | PH-C5;PH-C7 | 'The maximum activity was observed at pH 8.0, indicating that PanLipdN is an alkaline-preferring lipase'. enzyme_name corrected CALB -> PanLipdN. |

### PMC13316681 &mdash; 0 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM1F7BD124DF` | **drop** | thermostability | 5.0 | PH-X11;PH-X7;PH-X3 | Evidence is a concatenated review comparison-table cell ('...IsPETase and LCC; higher activity on BHET ...70 deg C/broad pH 5-8; thermostable at 60 deg C...') with no field boundaries. enzyme_name 'IsPETase' carries PET46's accession RLI42440.1. |
| `BM800815CC90` | **drop** | pH stability | 5.0 | PH-X11;PH-X7;PH-X3 | Same garbled review table cell. |
| `BMEF46DA6C6C` | **drop** | thermostability | 5.0 | PH-X11;PH-X7;PH-X3 | Same garbled review table cell. |

### PMC4624153 &mdash; 3 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0CC453F3E1` | KEEP | pH stability | 4.0 | PH-C3;PH-C5;PH-C7 | 'stable at pH 4.0, 5.0 and 6.0 and 55 deg C for 1 h with a residual activity of almost 70-80%'. pH 4.0 is one of the three stated points. |
| `BM168196487C` | KEEP | pH optimum | 4.0 | PH-C1;PH-C5;PH-C6;PH-C7 | Recorded optimum 4.0 was the low end of the range. Same sentence: 'the highest being at pH 5.0'. Optimum corrected 4.0 -> 5.0, active range 4.0-6.0 kept as bounds. |
| `BM31C0BAD528` | KEEP | thermostability | 4.0 | PH-C5 | Covariate row: genuine thermostability statement (stable 1 h at 55 deg C) assayed at pH 4.0. |

### PMC9104356 &mdash; 3 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM435E17667D` | KEEP | pH stability | 7.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | 'At pH 7 and 9, BaAXE retained over 80% activity after incubating for 4 h'. |
| `BM501B8B50BC` | KEEP | pH optimum | 8.0 | PH-C5;PH-C7 | 'BaAXE showed optimal activity at pH 8 and 40 deg C.' |
| `BMA3AAF6B915` | KEEP | temperature optimum | 8.0 | PH-C5 | Covariate row: temperature optimum 40 deg C, assayed at pH 8. |

### PMC9606172 &mdash; 3 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM49FA9E5B1A` | KEEP | pH optimum | 8.5 | PH-C5;PH-C7 | 'AXE-HAS10's optimal activity was at pH 8.5 and 40 deg C.' |
| `BM5358038896` | KEEP | pH stability | 8.0 | PH-C2;PH-C3;PH-C5;PH-C6;PH-C7 | '100 and 100% of the enzyme activity could be retained after pre-incubation at pH 8.0 and 9.0 for 15 h'. |
| `BM97AABCC81D` | KEEP | temperature optimum | 8.5 | PH-C5 | Covariate row: temperature optimum 40 deg C, assayed at pH 8.5. |

### PMC9772341 &mdash; 0 kept / 3 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM037C0E4939` | **drop** | pH optimum | 6.0 | PH-X1 | 'For enzymes with peak activity at pH 6.0, an extended pH screening assay was performed using ...' -- a methods sentence describing which enzymes were screened. |
| `BM2646680E59` | **drop** | pH optimum | 6.0 | PH-X4 | 'the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, 611, 702, 715)' -- four distinct enzymes collapsed into one unattributed row. |
| `BM3A4FF0E21E` | **drop** | salt effect | 6.0 | PH-X1;PH-X9 | value_std 2.9 '% relative activity' was parsed from '2.9% loading by mass of amorphous PET film' -- a substrate loading, not an activity. Unit misparse. |

### PMC10418727 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM8D124B9FCE` | KEEP | pH stability | 8.0 | PH-C2;PH-C3;PH-C5;PH-C7 | 'only ~40% of its maximal activity was retained at pH 8.0' is a point on the activity-pH profile. |
| `BME3583FB244` | KEEP | pH stability | 7.0 | PH-C2;PH-C5;PH-C7 | 'EaEst2 showed its maximal activity at pH 7.0' is a pH OPTIMUM, not pH stability. |

### PMC10607177 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM10FE78B273` | KEEP | temperature optimum | 7.0 | PH-C4 | Covariate row: two of three isolates share optimum 50 deg C / pH 7. Buffer MES cleared -- not named in the evidence and outside its range at pH 7. |
| `BM4006C9D9B6` | KEEP | pH optimum | 7.0 | PH-C4;PH-C7 | 'depolymerase enzymes produced by two of our A. fumigatus isolates exhibited optimal activity at pH 7'. Two enzymes, one shared value. Buffer MES cleared. |

### PMC10707221 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM4464247939` | KEEP | pH optimum | 8.5 | PH-C5;PH-C7 | 'The lipase was found to be most active at pH 8.5'. |
| `BM4E1ACC14B4` | KEEP | pH stability | 10.0 | PH-C5;PH-C7 | 'activity of SeLipC was abruptly decreased after incubation at pH 10.0, whereas it was stable when incubated at pH 5.0 to 9.5'. pH 10.0 is where stability is LOST -- without direction this row reads as if pH 10 were a stable point. |

### PMC11611003 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM845CAE36B3` | KEEP | pH optimum | 7.0 | PH-C5;PH-C7 | 'at 30 deg C, pH 7.0 (BHET as substrate) ... SbPETase showed the highest activity'. The article also reports pH 8.0 on PET film; this row is the BHET optimum. |
| `BMFAB6DCB606` | KEEP | temperature optimum | 7.0 | PH-C5 | Covariate row: temperature optimum 30 deg C at pH 7.0 on BHET. |

### PMC11782994 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM0DD7EB00EA` | KEEP | temperature optimum | 8.0 | -- | Covariate row: temperature optimum 60 deg C at pH 8. |
| `BM7F64B2576A` | KEEP | pH optimum | 8.0 | PH-C7 | 'highest activity of 152.5 U/mg was found on 100 mM KPO pH 8 and 60 deg C'. |

### PMC12115826 &mdash; 0 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMB86BE59C99` | **drop** | temperature optimum | 5.0 | PH-X6 | Cytochrome P450BM3 monooxygenase degrading gossypol, a plant polyphenol. Neither the enzyme class nor the substrate is in scope. |
| `BMDDBDC51F4A` | **drop** | pH optimum | 5.0 | PH-X6 | Same P450/gossypol article. |

### PMC12188634 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM37E9907878` | KEEP | pH optimum | 8.5 | PH-C5;PH-C7 | 'optimum conditions for the PLA-degrading activity of Savinase ... pH 8.5 and 42 C'. |
| `BM9F5746819C` | KEEP | temperature optimum | 8.5 | PH-C5 | Covariate row: temperature optimum 42 deg C at pH 8.5. |

### PMC12898461 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM34567040FA` | KEEP | pH optimum | 7.5 | PH-C1;PH-C5;PH-C6;PH-C7 | 'Plp1-ET showed more than 50% relative activity between pH 7.5 and 8.5, with its highest activity at pH 8.0'. Recorded optimum 7.5 was the range low end; corrected to 8.0. |
| `BM6E5147B1F9` | KEEP | pH optimum | 7.0 | PH-C1;PH-C3;PH-C5;PH-C6;PH-C7 | Recorded as enzyme_name 'Est1' with range 7.0-8.5, but 7.0-8.5 is Ces1-ET's range ('Ces1-ET exhibited more than 50% relative activity at pH between 7.0 and 8.5, reaching its optimal activity at approximately pH 7.5'). Est1-ET's own range is 7.0-9.0 with a maximum at pH 9.0. Re-attributed to Ces1-ET, optimum set to 7.5. |

### PMC12960341 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM8A4F230105` | KEEP | pH optimum | 8.0 | PH-C5;PH-C7 | 'CaFaeA exhibits maximal activity at pH 8.0'. |
| `BMA6514460C1` | KEEP | pH stability | 10.0 | PH-C3;PH-C5;PH-C7 | 'retains over 90% activity after 30 min incubation at pH 10.0'. |

### PMC13220297 &mdash; 0 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM3A1A41F1DA` | **drop** | pH stability | 6.5 | PH-X6 | Invertase (beta-fructofuranosidase, a glycoside hydrolase) immobilised on a PHB carrier. The polymer is the support, not the substrate. |
| `BMC0FC218AB8` | **drop** | pH stability | 4.5 | PH-X6 | Same invertase article. |

### PMC13323979 &mdash; 2 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM6CC5D054EB` | KEEP | pH optimum | 6.8 | PH-C7 | 'PS lipase and FM-10 lipase exhibited the best ... activity with optimal reaction conditions of T = 40-55 deg C and pH = 6.8'. Two lipases, one shared value. |
| `BME948DB4347` | KEEP | temperature optimum | 6.8 | -- | Covariate row: temperature optimum 40-55 deg C at pH 6.8. |

### PMC8265113 &mdash; 0 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM488F8758D1` | **drop** | temperature optimum | 5.0 | PH-X6;PH-X1 | rXynS1 is a GH11 xylanase (glycoside hydrolase), off-target; and pH 5.0 is the assay pH ('assayed at pH 5.0'), not an optimum. |
| `BM5B4789AA54` | **drop** | pH optimum | 5.0 | PH-X6;PH-X1 | Same GH11 xylanase article. |

### PMC9839772 &mdash; 0 kept / 2 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM7D11018C05` | **drop** | pH stability | 8.0 | PH-X1 | 'the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, 65 and 70 deg C ... followed by determining the residual activity' -- pH 8.0 is the buffer of a thermostability protocol. |
| `BMC3719577E5` | **drop** | thermostability | 8.0 | PH-X1 | Same methods sentence; 70 deg C is the highest temperature tested, recorded as a thermostability value. |

### PMC10599323 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMEEB3F89D6F` | **drop** | pH stability | 6.5 | PH-X7 | 'The AUTHORS FOUND that the pH of the solution dropped ...' in a review article; restates another study's observation. |

### PMC10927764 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMFE76762A46` | **drop** | pH optimum | 3.54 | PH-X8 | pH 3.54 is the buffer of an absorption/1H-NMR quantification method for TPA, not an enzyme assay condition. |

### PMC10941194 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM03DE403B9C` | **drop** | pH optimum | 3.5 | PH-X2;PH-X7 | 'a standard bell-shaped activity-pH profile with an optimum around 7.5.51 When starting from a lower pH (usually buffers of pH 3.5-5.0 ...)'. The recorded 3.5-5.0 is the STARTING BUFFER range; the stated optimum is 7.5. The trailing '51' is a stripped reference marker, so the claim is secondhand as well. |

### PMC11055803 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMF2FE995DB3` | KEEP | pH stability | 10.0 | PH-C3;PH-C5;PH-C7 | 'The pure enzyme retains its activity after 3 h at pH 10 above 85%'. The trailing clause ('but its activity decreases to below 50%') has no stated condition and is not used. |

### PMC11270687 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM85EC0EEFF2` | **drop** | pH optimum | 7.5 | PH-X4 | 'The optimal activity was at pH 7.5 (Figure S3C)' -- the sentence has no enzyme subject at all and the article characterises several marine-bacterial enzymes. |

### PMC12741466 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMD363C6A8E6` | KEEP | pH optimum | 7.0 | PH-C1;PH-C5;PH-C6;PH-C7 | 'The optimal pH for PCLase0801 activity was determined to be 8.0, with relatively high activity maintained between pH 7.0 and 9.0'. Recorded optimum 7.0 was the range low end; corrected to 8.0. |

### PMC12766730 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM60E20E768C` | **drop** | pH stability | 5.0 | PH-X6 | 'half-life of quinone release ... at pH 5' -- self-immolative linker chemistry, no enzyme. |

### PMC12767561 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM7E25455D3E` | KEEP | pH optimum | 5.5 | PH-C2;PH-C5;PH-C6 | 'TflNylA was most active against pNPH between pH 5.5 and 8.5 and exhibited a bell-shaped pH-rate profile'. This is the >50%-activity interval, not a point optimum; the article does not state a single optimum in this sentence. |

### PMC12871986 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM539CC031EB` | **drop** | pH optimum | 7.5 | PH-X5 | 'The MODEL PREDICTED maximum biodegradation at pH 7.5' -- an RSM optimisation output, and about whole-cell biodegradation rather than an enzyme. Shipping it would breach the benchmark's own no-predicted-values integrity statement. |

### PMC13035632 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BMBF693ED6C8` | KEEP | pH optimum | 3.5 | PH-C5;PH-C7 | 'LipC displayed optimal activity at pH 3.5' -- acidophilic lipase. |

### PMC13050008 &mdash; 0 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM44DA9B1565` | **drop** | pH optimum | 8.0 | PH-X6;PH-X4 | Ulvan lyase -- a polysaccharide lyase, not a carboxylester hydrolase. 'all three ulvan lyases' is also unattributable. |

### PMC8767016 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM097BED1F73` | KEEP | pH optimum | 7.0 | PH-C2;PH-C5;PH-C6;PH-C7 | 'PET27 was most active between pH 7-8 and PET30 between pH 6-8'. The recorded 7.0-8.0 is PET27's interval exactly, so the row is attributed to PET27 and reclassified from a point optimum to an activity range. |

### PMC8971842 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BME8E31FAE60` | KEEP | pH stability | 12.0 | PH-C3;PH-C5;PH-C7 | 'PCLase I showed remarkable stability at pH 12.0 with activity of approximately 100%'. Attributed to PCLase I, which the sentence names for this value. |

### PMC9452428 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM95627C2801` | KEEP | pH optimum | 8.0 | PH-C5;PH-C7 | 'The optimum pH for enzyme activity was realized at pH 8.0' -- EstRag, tier A. |

### PMC9805092 &mdash; 1 kept / 1 candidates

| Row | Verdict | Type as recorded | pH | Rules | Reason |
|---|---|---|---:|---|---|
| `BM837DB27EC1` | KEEP | pH optimum | 7.5 | PH-C7 | 'enzymatic activity was optimal for all the chimeras at pH 7.5' -- several MHETase chimeras share the stated optimum. |

---

Regenerate with `python3 scripts/make_reports.py`. Row-level machine-readable form: `data/ph_audit_log.csv`.
