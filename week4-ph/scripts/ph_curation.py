"""
Hand-curation table for the Week-4 pH benchmark.

Every one of the 105 candidate pH rows inherited from `pet_benchmark_v2.csv` was read
against its recorded `evidence_quote` and given an explicit verdict here. This file is
the audit's source of truth: `build_ph_benchmark.py` applies it mechanically and
`AUDIT_REPORT.md` is generated from it, so the shipped data and the documentation
cannot drift apart.

SCOPE. Three passes stand behind these verdicts.

  1. Evidence-sentence audit. All 105 candidates read against the quote the Week-2
     pipeline stored with them. Produced the exclusions and the field corrections.
  2. Deep re-read of the SHIPPED rows (`scripts/deep_verify_ph.py`). All 31 shipped
     articles re-downloaded and every shipped row re-checked in full context. Produced
     SEQUENCE_REJECTIONS below, the MLipA renaming, and one measurement-type fix.
  3. Deep re-read of the EXCLUSIONS (`scripts/deep_verify_exclusions.py`). All 37
     removals re-checked against full text with the article's own section structure.
     Reinstated BM85EC0EEFF2 (PD3); every other removal held.

What none of the passes does is re-derive a value from the underlying figure. Where a
row rests on prose summarising a figure, the prose is taken at its word.

Verdicts
    KEEP     row enters the benchmark, possibly with corrections in `set`
    EXCLUDE  row does not enter the benchmark

Exclusion rules
    PH-X1   methods_or_protocol_sentence   assay setup (buffer pH, incubation T, range
                                           assayed, normalisation basis), not an outcome
    PH-X2   range_endpoint_as_optimum      typed "pH optimum" but the value is a range
                                           endpoint and the source states a different
                                           optimum that cannot be recovered
    PH-X3   enzyme_attribution_mismatch    recorded enzyme/accession is not the enzyme
                                           the evidence describes
    PH-X4   ambiguous_multi_enzyme         evidence covers >=2 enzymes with different
                                           values, or has no enzyme referent at all
    PH-X5   model_predicted_value          a model/RSM prediction, not a measurement
    PH-X6   off_target_enzyme_class        not a carboxylester hydrolase or polymer
                                           depolymerase
    PH-X7   secondhand_or_review           restates another study, or a review article
    PH-X8   analytical_method_pH           pH of an analytical procedure, not an assay
    PH-X9   measurement_type_unsupported   evidence contains no measurement of that type
    PH-X10  duplicate_measurement          same enzyme + paper + type + pH already kept
    PH-X11  garbled_table_extraction       concatenated table cell, no field boundaries
    PH-X12  no_outcome_at_stated_pH        boundary word ("beyond", "above") with no
                                           outcome measured at the recorded pH

Correction rules
    PH-C1   optimum_corrected      pH optimum set to the value the source states
    PH-C2   type_reclassified      measurement_type changed to match the evidence
    PH-C3   outcome_recovered      residual/relative activity recovered from the evidence
    PH-C4   buffer_cleared         buffer not supported by the evidence and/or chemically
                                   incompatible with the recorded pH
    PH-C5   enzyme_named           enzyme_name set or corrected from the evidence
    PH-C6   range_bounds_set       pH_low/pH_high set to the stated interval
    PH-C7   direction_set          direction of the pH effect recorded

`set` keys map onto the output schema. `rel_pct` / `rel_pct_high` / `rel_qual` carry the
outcome at that pH; `rel_qual` is one of exact, approx, gte, lte, range.
"""

EXCLUSION_RULES = {
    "PH-X1":  "methods_or_protocol_sentence",
    "PH-X2":  "range_endpoint_as_optimum",
    "PH-X3":  "enzyme_attribution_mismatch",
    "PH-X4":  "ambiguous_multi_enzyme",
    "PH-X5":  "model_predicted_value",
    "PH-X6":  "off_target_enzyme_class",
    "PH-X7":  "secondhand_or_review",
    "PH-X8":  "analytical_method_pH",
    "PH-X9":  "measurement_type_unsupported",
    "PH-X10": "duplicate_measurement",
    "PH-X11": "garbled_table_extraction",
    "PH-X12": "no_outcome_at_stated_pH",
}
CORRECTION_RULES = {
    "PH-C1": "optimum_corrected",
    "PH-C2": "type_reclassified",
    "PH-C3": "outcome_recovered",
    "PH-C4": "buffer_cleared",
    "PH-C5": "enzyme_named",
    "PH-C6": "range_bounds_set",
    "PH-C7": "direction_set",
}

# ---------------------------------------------------------------------------------
# Sequence attributions rejected by the deep re-read of the full articles
# (`scripts/deep_verify_ph.py`, 2026-09-12).
#
# The Week-2 pipeline accepted an accession when an article named exactly one hydrolase
# record. That rule cannot tell an accession an article DEPOSITS (its own enzyme) from
# one it CITES -- as a phylogenetic-tree neighbour, a structural-modelling template, or
# a comparison enzyme. Re-reading each accession in full context found three that are
# citations, not deposits. In every case the recorded ORGANISM independently corroborates
# the error: it is the organism of the cited protein, not of the enzyme assayed.
#
# The measurements themselves are sound -- only the protein identity was wrong -- so the
# rows keep their value and lose the sequence, dropping to the no-sequence tier.
# ---------------------------------------------------------------------------------
SEQUENCE_REJECTIONS = {
    "P26495": {
        "pmcid": "PMC10003648",
        "enzyme": "PhaZ",
        "reason": "P26495 is the AlphaFold structural-modelling TEMPLATE, not the "
                  "article's enzyme: 'the poly(3-hydroxyalkanoate) depolymerase from "
                  "Pseudomonas oleovorans (Alpha-Fold code AF-P26495-F1) was used as a "
                  "template for modelling PhaZ'. The article's own PhaZ is from "
                  "Pseudomonas chlororaphis PA23 (genome CP008696, locus EY04_*) and is "
                  "not deposited under a standalone protein accession.",
        "organism": "Pseudomonas chlororaphis PA23",
    },
    "AAB51445.1": {
        "pmcid": "PMC10707221",
        "enzyme": "SeLipC",
        "reason": "AAB51445.1 is a phylogenetic-tree NEIGHBOUR, not the article's "
                  "enzyme: 'SeM11Lip: Lipase from S. exfoliatus M11 (AAB51445.1)' in the "
                  "Figure 9 caption -- a different strain's already-characterised lipase. "
                  "SeLipC is lipC from the S. exfoliatus DSMZ 41693 draft genome "
                  "(GenBank AZSS00000000, contig 334 nt 12616-13485).",
        "organism": "Streptomyces exfoliatus DSMZ 41693",
    },
    "WP_054022242.1": {
        "pmcid": "PMC11611003",
        "enzyme": "SbPETase",
        "reason": "WP_054022242 is IsPETase, the COMPARISON enzyme: 'The genes encoding "
                  "IsPETase (accession number WP_054022242) and Kil protein were "
                  "chemically synthesized'. The article's own enzyme, SbPETase, 'was "
                  "amplified from the genome of S. brevitalea sp. nov.' and is a "
                  "different protein. This was the only tier-B attribution, so removing "
                  "it also removes the benchmark's only overlap with a held-out split.",
        "organism": "Schlegelella brevitalea",
    },
}

K = "KEEP"
X = "EXCLUDE"


def _k(rules=(), note="", **set_fields):
    return {"verdict": K, "rules": list(rules), "note": note, "set": set_fields}


def _x(rules, note):
    return {"verdict": X, "rules": list(rules), "note": note, "set": {}}


CURATION = {

# ---------------------------------------------------------------------------------
# PMC11651597 -- Bacillus licheniformis IBRL-CHS2 lipase (AOT80658.1), tier A
# The article reports BOTH an activity-vs-pH profile and a separate pH-stability
# profile; the Week-2 extraction collapsed them into one `pH stability` type.
# ---------------------------------------------------------------------------------
"BM0A3FCD8E37": _x(["PH-X9"],
    "35 deg C is the incubation temperature of the pH-stability assay in this sentence; "
    "recorded as a thermostability measurement of 35 deg C. No thermostability value is "
    "stated."),
"BM0D67FCB6F6": _k(["PH-C2", "PH-C3", "PH-C6", "PH-C5"],
    "Range statement 'stable between pH 6 and pH 9, retaining 89-97%'. Typed as a "
    "pH-stability range; pH 9.0 is the upper endpoint of range group R-11651597-a.",
    enzyme_name="MLipA", measurement_type="pH stability range",
    pH_low=6.0, pH_high=9.0, pH_is_range="yes", ph_range_group="R-11651597-a",
    rel_pct=89.0, rel_pct_high=97.0, rel_qual="range", direction="stabilising",
    exposure_time_min=60.0, temperature_c=35.0),
"BMF54859EFAF": _k(["PH-C2", "PH-C3", "PH-C6", "PH-C5"],
    "Lower endpoint of the same range statement as BM0D67FCB6F6 (range group "
    "R-11651597-a). Kept as a separate endpoint row to match Luke's one-row-per-endpoint "
    "convention for pH ranges.",
    enzyme_name="MLipA", measurement_type="pH stability range",
    pH_low=6.0, pH_high=9.0, pH_is_range="yes", ph_range_group="R-11651597-a",
    rel_pct=89.0, rel_pct_high=97.0, rel_qual="range", direction="stabilising",
    exposure_time_min=60.0, temperature_c=35.0),
"BM499AE86AAE": _k(["PH-C2", "PH-C3", "PH-C5"],
    "'retaining 93% of its activity at pH 6 and 82% at pH 8' is the activity-vs-pH "
    "profile, not the post-incubation stability profile. Reclassified to pH activity.",
    enzyme_name="MLipA", measurement_type="pH activity",
    rel_pct=82.0, rel_qual="exact"),
"BMFBD1521130": _k(["PH-C2", "PH-C3", "PH-C5"],
    "Same sentence as BM499AE86AAE, pH 6 point. Reclassified to pH activity.",
    enzyme_name="MLipA", measurement_type="pH activity",
    rel_pct=93.0, rel_qual="exact"),
"BM71030D2A05": _x(["PH-X1"],
    "Normalisation sentence: 'activity at pH 7 was set as 100% ... for pH stability the "
    "activity without pre-incubation was set at 100%'. Defines the assay baseline, not a "
    "measured outcome. The optimum it implies is captured by the corrected BMDFDCB2C50A."),
"BM73CD9BDECC": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'further decline to 22% at pH 11' -- residual activity after 1 h.",
    enzyme_name="MLipA", rel_pct=22.0, rel_qual="exact",
    direction="destabilising", exposure_time_min=60.0),
"BMC31B27FC98": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'only 51% residual activity observed after one h' at pH 10.",
    enzyme_name="MLipA", rel_pct=51.0, rel_qual="exact",
    direction="destabilising", exposure_time_min=60.0),
"BMDFDCB2C50A": _k(["PH-C1", "PH-C5", "PH-C6"],
    "Recorded pH optimum 5.0 was the LOW END of the activity range. The same sentence "
    "states 'optimal activity observed at pH 7'. Optimum corrected 5.0 -> 7.0, "
    "active range 5.0-9.0 retained as bounds.",
    enzyme_name="MLipA", pH=7.0, pH_low=5.0, pH_high=9.0,
    value_std=7.0, direction="optimum"),

# ---------------------------------------------------------------------------------
# PMC9709933 -- alkaline esterase, tier C. Five clean residual-activity points.
# ---------------------------------------------------------------------------------
"BM0E71BF8DE3": _k(["PH-C3", "PH-C7"], "97% residual after 3 h at pH 6.0.",
    rel_pct=97.0, rel_qual="approx", direction="stabilising", exposure_time_min=180.0),
"BM321B809084": _k(["PH-C3", "PH-C7"], "82% residual after 3 h at pH 8.0.",
    rel_pct=82.0, rel_qual="exact", direction="stabilising", exposure_time_min=180.0),
"BM60B9ABF4DB": _k(["PH-C3", "PH-C7"], "74% residual after 1 h at pH 4.0.",
    rel_pct=74.0, rel_qual="exact", direction="stabilising", exposure_time_min=60.0),
"BM9F253201A6": _k(["PH-C3", "PH-C7"], "~100% residual after 1 h at pH 7.0.",
    rel_pct=100.0, rel_qual="approx", direction="stabilising", exposure_time_min=60.0),
"BMAFA2119D8D": _k(["PH-C3", "PH-C7"], "55% residual after 1 h at pH 11.0.",
    rel_pct=55.0, rel_qual="exact", direction="destabilising", exposure_time_min=60.0),

# ---------------------------------------------------------------------------------
# PMC10146132 -- KoFAE feruloyl esterase, tier C
# ---------------------------------------------------------------------------------
"BM22F8594502": _k(["PH-C2", "PH-C3", "PH-C6", "PH-C5"],
    "'A pH of 6.0~10.0 had good stability ... more than 60%' is a coarse range summary "
    "that the same article contradicts with 'when pH 10.0, less than 50% retained' "
    "(BM7E8AC1F540). Kept as a range row, flagged internal_conflict, NOT scored.",
    enzyme_name="KoFAE", measurement_type="pH stability range",
    pH_low=6.0, pH_high=10.0, pH_is_range="yes", ph_range_group="R-10146132-a",
    rel_pct=60.0, rel_qual="gte", direction="stabilising", internal_conflict="yes"),
"BMFA666F5868": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'pH 8.0, the best stability of enzyme activity, could retain about 80%'.",
    enzyme_name="KoFAE", rel_pct=80.0, rel_qual="approx", direction="stabilising"),
"BM355F56FDED": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'about 90% of the enzyme activity was retained when pH = 9.0'.",
    enzyme_name="KoFAE", rel_pct=90.0, rel_qual="approx", direction="stabilising"),
"BM7E8AC1F540": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'When pH 10.0, less than 50% of the enzyme activity was retained'.",
    enzyme_name="KoFAE", rel_pct=50.0, rel_qual="lte", direction="destabilising"),
"BMB113AB078A": _k(["PH-C2", "PH-C3", "PH-C5", "PH-C6", "PH-C7"],
    "'less stable when pH was 3.0 to 5.0 ... lost when pH was 3.0 ... less than 50% "
    "when pH was 4.0 to 5.0'. A destabilising range, not a point.",
    enzyme_name="KoFAE", measurement_type="pH stability range",
    pH_low=3.0, pH_high=5.0, pH_is_range="yes", ph_range_group="R-10146132-b",
    rel_pct=50.0, rel_qual="lte", direction="destabilising"),

# ---------------------------------------------------------------------------------
# PMC12896513 -- rEST-24 / rEST-28 GDSL esterases, tier C
# ---------------------------------------------------------------------------------
"BM43A7E54ACA": _x(["PH-X1"],
    "'The residual activity was then measured at 40 deg C in 50 mM sodium phosphate "
    "(pH 7.0)' is the assay readout condition. Recorded as thermostability = 40 deg C."),
"BM4FD5205F58": _x(["PH-X1"],
    "Same methods sentence, recorded as pH stability = 7.0. pH 7.0 is the readout buffer."),
"BM7EDDB0F663": _x(["PH-X1", "PH-X10"],
    "Second copy of the same methods statement ('residual activity measured in 50 mM "
    "sodium phosphate buffer at pH 7.0'); duplicate of BM4FD5205F58 and equally unusable."),
"BM5D7F089EA5": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'residual activity of rEST-24 did not exceed 30%' across the pH values tested, of "
    "which 4.0 is one. Attributable to rEST-24; coarse upper bound only.",
    enzyme_name="rEST-24", rel_pct=30.0, rel_qual="lte", direction="destabilising",
    attribution_certainty="single_enzyme_named"),
"BME50151456E": _k(["PH-C5"],
    "'rEST-24 esterase exhibited maximum activity at pH 7.0 only'. The co-named rEST-28 "
    "has a different reported optimum (6.0-7.0), so the row is attributed to rEST-24.",
    enzyme_name="rEST-24", direction="optimum",
    attribution_certainty="single_enzyme_named"),

# ---------------------------------------------------------------------------------
# PMC10385968 -- EstD04, HSL family IV esterase, tier C
# ---------------------------------------------------------------------------------
"BM961F2AE8B7": _k(["PH-C5"],
    "Covariate row: temperature optimum 40 deg C restated in the kinetics sentence, "
    "assayed at pH 8.",
    enzyme_name="EstD04"),
"BMBE4B247046": _k(["PH-C5"], "'The optimal pH for EstD04 activity was pH 8.'",
    enzyme_name="EstD04", direction="optimum"),
"BMC71D9F94EF": _x(["PH-X10"],
    "pH optimum 8.0 for EstD04 restated in the kinetics sentence -- same enzyme, paper, "
    "type and value as BMBE4B247046, which comes from the direct statement."),
"BMA7FF240F0C": _k(["PH-C2", "PH-C3", "PH-C6", "PH-C5", "PH-C7"],
    "'favorable pH stability between pH 8 to pH 11 ... retained at least 80% activity'. "
    "Lower endpoint of range group R-10385968-a.",
    enzyme_name="EstD04", measurement_type="pH stability range",
    pH_low=8.0, pH_high=11.0, pH_is_range="yes", ph_range_group="R-10385968-a",
    rel_pct=80.0, rel_qual="gte", direction="stabilising"),
"BMF8D20A14F6": _k(["PH-C2", "PH-C3", "PH-C6", "PH-C5", "PH-C7"],
    "Upper endpoint of range group R-10385968-a.",
    enzyme_name="EstD04", measurement_type="pH stability range",
    pH_low=8.0, pH_high=11.0, pH_is_range="yes", ph_range_group="R-10385968-a",
    rel_pct=80.0, rel_qual="gte", direction="stabilising"),

# ---------------------------------------------------------------------------------
# PMC10003648 -- Pseudomonas chloroaphis PA23 polymer-degrading enzymes, tier A
# `buffer_name = MES` was attached from elsewhere in the article; MES buffers pH 5.5-6.7
# and cannot hold pH 8, and the evidence sentence names no buffer.
# ---------------------------------------------------------------------------------
"BM6E32E848BD": _k(["PH-C4"],
    "Covariate row: temperature optimum 45-50 deg C at pH 8. Buffer MES cleared -- not in "
    "the evidence and outside its buffering range at pH 8.",
    buffer_name="", attribution_certainty="multiple_enzymes_same_value"),
"BM9A302CF0A9": _k(["PH-C4"],
    "'LIP3 and PhaZ ... optimal activity at pH 8'. Both enzymes share the stated optimum, "
    "so attribution to PhaZ is safe but flagged. Buffer MES cleared.",
    buffer_name="", direction="optimum",
    attribution_certainty="multiple_enzymes_same_value"),
"BM94ACC9E0C2": _k(["PH-C2", "PH-C6", "PH-C7"],
    "'PhaZ showing higher relative activity at pH 8.0-10.0' -- a range, not a point.",
    measurement_type="pH activity range", pH_low=8.0, pH_high=10.0, pH_is_range="yes",
    ph_range_group="R-10003648-a", direction="stabilising"),
"BME732B05FC1": _x(["PH-X3"],
    "Accession P26495 is PhaZ, but the evidence sentence is about LIP4: 'LIP4 retained "
    "more activity (>80%) at pH 5.0-6.0'. A tier-A sequence misattribution -- the worst "
    "class of defect a benchmark can carry."),

# ---------------------------------------------------------------------------------
# PMC7936011 -- Tan410 metagenomic esterase, tier C
# ---------------------------------------------------------------------------------
"BM0DB57418F4": _x(["PH-X1"],
    "'assayed by incubating ... at different temperatures in a range of 25-65 deg C' is "
    "the range tested. Recorded as temperature optimum = 25 deg C."),
"BM310A734B15": _x(["PH-X1", "PH-X10"],
    "Same methods sentence; pH 7.0 is the assay buffer, recorded as a pH optimum. The "
    "real optimum for Tan410 is captured by BM5BBF965026."),
"BM4EE39ACAFC": _x(["PH-X1"],
    "'the pre-incubated solution was regulated to pH 7.0 ... and analyzed for residual "
    "activity' -- the readout pH of the stability assay, not a stability result."),
"BM5BBF965026": _k(["PH-C5"],
    "'esterase Tan410 showed its highest activity at pH 7.0'.",
    enzyme_name="Tan410", direction="optimum"),

# ---------------------------------------------------------------------------------
# PMC10495362 -- PET46 archaeal feruloyl esterase, tier A
# ---------------------------------------------------------------------------------
"BM0578A48B89": _x(["PH-X7", "PH-X3"],
    "'In their study, the PET46-like 211 released ...' -- a secondhand sentence about a "
    "different enzyme (PET46-like 211), carrying PET46's accession RLI42440.1."),
"BM6A82469C45": _x(["PH-X7", "PH-X3"], "Same secondhand sentence, temperature axis."),
"BMB8B8558C40": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'it also retained high activities (50%) at pH 5' -- the article's own enzyme.",
    enzyme_name="PET46", rel_pct=50.0, rel_qual="approx", direction="stabilising"),

# ---------------------------------------------------------------------------------
# PMC13316681 -- review article, comparison table. All three rows unusable.
# ---------------------------------------------------------------------------------
"BM1F7BD124DF": _x(["PH-X11", "PH-X7", "PH-X3"],
    "Evidence is a concatenated review comparison-table cell ('...IsPETase and LCC; "
    "higher activity on BHET ...70 deg C/broad pH 5-8; thermostable at 60 deg C...') with "
    "no field boundaries. enzyme_name 'IsPETase' carries PET46's accession RLI42440.1."),
"BM800815CC90": _x(["PH-X11", "PH-X7", "PH-X3"], "Same garbled review table cell."),
"BMEF46DA6C6C": _x(["PH-X11", "PH-X7", "PH-X3"], "Same garbled review table cell."),

# ---------------------------------------------------------------------------------
# PMC9772341 -- thermotolerant PET hydrolase scaffolds, tier C
# ---------------------------------------------------------------------------------
"BM037C0E4939": _x(["PH-X1"],
    "'For enzymes with peak activity at pH 6.0, an extended pH screening assay was "
    "performed using ...' -- a methods sentence describing which enzymes were screened."),
"BM2646680E59": _x(["PH-X4"],
    "'the four enzymes that exhibited optimal or near optimal activity at pH 6.0 (102, "
    "611, 702, 715)' -- four distinct enzymes collapsed into one unattributed row."),
"BM3A4FF0E21E": _x(["PH-X1", "PH-X9"],
    "value_std 2.9 '% relative activity' was parsed from '2.9% loading by mass of "
    "amorphous PET film' -- a substrate loading, not an activity. Unit misparse."),

# ---------------------------------------------------------------------------------
# PMC10146679 -- BbPETaseCD. One sentence describing a temperature profile produced
# three rows, none of which is a measurement of its recorded type.
# ---------------------------------------------------------------------------------
"BM06A72D7AB0": _x(["PH-X9"],
    "pH 7.0 is the assay condition of a thermal statement; no pH-stability measurement."),
"BM9DD54D4438": _x(["PH-X9"],
    "'activity increased from 30 deg C to 40 deg C' -- 30 is a profile boundary, not a "
    "thermostability value."),
"BMAD704A1BA4": _x(["PH-X9"], "Same sentence; 40 is the other profile boundary."),

# ---------------------------------------------------------------------------------
# PMC12734981 -- PanLip(dN), a CALB-LIKE lipase. enzyme_name was set to 'CALB' itself.
# ---------------------------------------------------------------------------------
"BM097BBDB7F2": _x(["PH-X12"],
    "'A rapid decline in activity was detected beyond pH 8.0' -- no outcome is measured "
    "AT pH 8.0; the only quantified point in the sentence is pH 9.0 (BM51F74D231E)."),
"BM51F74D231E": _k(["PH-C2", "PH-C3", "PH-C5"],
    "'less than 15% residual activity at pH 9.0'. Deep re-read of the full paragraph "
    "shows this is a point on the activity-vs-pH profile ('The effect of pH on the "
    "catalytic activity ... was investigated in the pH range of 4.0-9.0'), not a "
    "post-incubation stability assay, so the type is pH activity. enzyme_name corrected "
    "CALB -> PanLipdN: the article characterises a CALB-LIKE enzyme, not CALB.",
    enzyme_name="PanLipdN", measurement_type="pH activity",
    rel_pct=15.0, rel_qual="lte"),
"BMDC3A7C490D": _k(["PH-C5"],
    "'The maximum activity was observed at pH 8.0, indicating that PanLipdN is an "
    "alkaline-preferring lipase'. enzyme_name corrected CALB -> PanLipdN.",
    enzyme_name="PanLipdN", direction="optimum"),

# ---------------------------------------------------------------------------------
# PMC4624153 -- PHAZ(Pen) PHB depolymerase from Penicillium expansum (2015)
# ---------------------------------------------------------------------------------
"BM0CC453F3E1": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'stable at pH 4.0, 5.0 and 6.0 and 55 deg C for 1 h with a residual activity of "
    "almost 70-80%'. pH 4.0 is one of the three stated points.",
    enzyme_name="PHAZ(Pen)", rel_pct=70.0, rel_pct_high=80.0, rel_qual="range",
    direction="stabilising", exposure_time_min=60.0, temperature_c=55.0),
"BM168196487C": _k(["PH-C1", "PH-C5", "PH-C6"],
    "Recorded optimum 4.0 was the low end of the range. Same sentence: 'the highest "
    "being at pH 5.0'. Optimum corrected 4.0 -> 5.0, active range 4.0-6.0 kept as bounds.",
    enzyme_name="PHAZ(Pen)", pH=5.0, pH_low=4.0, pH_high=6.0, value_std=5.0,
    direction="optimum"),
"BM31C0BAD528": _k(["PH-C5"],
    "Covariate row: genuine thermostability statement (stable 1 h at 55 deg C) assayed "
    "at pH 4.0.",
    enzyme_name="PHAZ(Pen)", exposure_time_min=60.0),

# ---------------------------------------------------------------------------------
# PMC9104356 -- BaAXE acetyl xylan esterase (EC 3.1.1.72, a carboxylester hydrolase)
# ---------------------------------------------------------------------------------
"BM435E17667D": _k(["PH-C2", "PH-C3", "PH-C5", "PH-C6", "PH-C7"],
    "'At pH 7 and 9, BaAXE retained over 80% activity after incubating for 4 h'.",
    enzyme_name="BaAXE", measurement_type="pH stability range",
    pH_low=7.0, pH_high=9.0, pH_is_range="yes", ph_range_group="R-9104356-a",
    rel_pct=80.0, rel_qual="gte", direction="stabilising", exposure_time_min=240.0),
"BM501B8B50BC": _k(["PH-C5"], "'BaAXE showed optimal activity at pH 8 and 40 deg C.'",
    enzyme_name="BaAXE", direction="optimum"),
"BMA3AAF6B915": _k(["PH-C5"],
    "Covariate row: temperature optimum 40 deg C, assayed at pH 8.", enzyme_name="BaAXE"),

# ---------------------------------------------------------------------------------
# PMC12428281 -- DehpH, di(2-ethylhexyl) phthalate hydrolase (plasticiser)
# ---------------------------------------------------------------------------------
"BM47946FE1B3": _x(["PH-X9"],
    "4 deg C is the incubation temperature of a pH-stability experiment, recorded as a "
    "thermostability measurement of 4 deg C."),
"BME71810CC95": _k(["PH-C5", "PH-C6"],
    "'the optimal pH was 8.0, and DehpH showed relatively high activity ranging from "
    "pH 6.0 to pH 9.0'.",
    enzyme_name="DehpH", pH_low=6.0, pH_high=9.0, direction="optimum"),
"BME7E3DA9213": _k(["PH-C2", "PH-C5", "PH-C6", "PH-C7"],
    "'activity decreased significantly under acid conditions (pH 3.0 to 6.0) and almost "
    "lost all of its activity under pH 3.0'. The loss is qualitative -- the sentence "
    "gives no percentage -- so no outcome value is recorded, only the direction.",
    enzyme_name="DehpH", measurement_type="pH stability range",
    pH_low=3.0, pH_high=6.0, pH_is_range="yes", ph_range_group="R-12428281-a",
    direction="destabilising", exposure_time_min=60.0, temperature_c=4.0),

# ---------------------------------------------------------------------------------
# PMC9606172 -- AXE-HAS10 recombinant acetylxylan esterase
# ---------------------------------------------------------------------------------
"BM49FA9E5B1A": _k(["PH-C5"], "'AXE-HAS10's optimal activity was at pH 8.5 and 40 deg C.'",
    enzyme_name="AXE-HAS10", direction="optimum"),
"BM5358038896": _k(["PH-C2", "PH-C3", "PH-C5", "PH-C6", "PH-C7"],
    "'100 and 100% of the enzyme activity could be retained after pre-incubation at "
    "pH 8.0 and 9.0 for 15 h'.",
    enzyme_name="AXE-HAS10", measurement_type="pH stability range",
    pH_low=8.0, pH_high=9.0, pH_is_range="yes", ph_range_group="R-9606172-a",
    rel_pct=100.0, rel_qual="exact", direction="stabilising", exposure_time_min=900.0),
"BM97AABCC81D": _k(["PH-C5"],
    "Covariate row: temperature optimum 40 deg C, assayed at pH 8.5.",
    enzyme_name="AXE-HAS10"),

# ---------------------------------------------------------------------------------
# PMC10707221 -- SeLipC, Streptomyces exfoliatus lipase, tier A
# ---------------------------------------------------------------------------------
"BM4464247939": _k(["PH-C5"],
    "'The lipase was found to be most active at pH 8.5'.",
    enzyme_name="SeLipC", direction="optimum"),
"BM4E1ACC14B4": _k(["PH-C5", "PH-C7"],
    "'activity of SeLipC was abruptly decreased after incubation at pH 10.0, whereas it "
    "was stable when incubated at pH 5.0 to 9.5'. pH 10.0 is where stability is LOST -- "
    "without direction this row reads as if pH 10 were a stable point.",
    enzyme_name="SeLipC", direction="destabilising"),

# ---------------------------------------------------------------------------------
# PMC11611003 -- SbPETase, tier B (protein sits in Luke's held-out test split)
# ---------------------------------------------------------------------------------
"BM845CAE36B3": _k(["PH-C5"],
    "'at 30 deg C, pH 7.0 (BHET as substrate) ... SbPETase showed the highest activity'. "
    "The article also reports pH 8.0 on PET film; this row is the BHET optimum.",
    enzyme_name="SbPETase", substrate="BHET", direction="optimum"),
"BMFAB6DCB606": _k(["PH-C5"],
    "Covariate row: temperature optimum 30 deg C at pH 7.0 on BHET.",
    enzyme_name="SbPETase", substrate="BHET"),

# ---------------------------------------------------------------------------------
# PMC11782994 -- anaerobic Thermoanaerobacterales hydrolase
# ---------------------------------------------------------------------------------
"BM0DD7EB00EA": _k([], "Covariate row: temperature optimum 60 deg C at pH 8."),
"BM7F64B2576A": _k(["PH-C7"],
    "'highest activity of 152.5 U/mg was found on 100 mM KPO pH 8 and 60 deg C'.",
    direction="optimum"),

# ---------------------------------------------------------------------------------
# PMC10607177 -- Aspergillus fumigatus PVC depolymerases
# ---------------------------------------------------------------------------------
"BM10FE78B273": _k(["PH-C4"],
    "Covariate row: two of three isolates share optimum 50 deg C / pH 7. Buffer MES "
    "cleared -- not named in the evidence and outside its range at pH 7.",
    buffer_name="", attribution_certainty="multiple_enzymes_same_value"),
"BM4006C9D9B6": _k(["PH-C4", "PH-C7"],
    "'depolymerase enzymes produced by two of our A. fumigatus isolates exhibited optimal "
    "activity at pH 7'. Two enzymes, one shared value. Buffer MES cleared.",
    buffer_name="", direction="optimum",
    attribution_certainty="multiple_enzymes_same_value"),

# ---------------------------------------------------------------------------------
# PMC12898461 -- Thermus thermophilus esterases. Both rows carried the wrong enzyme.
# ---------------------------------------------------------------------------------
"BM34567040FA": _k(["PH-C1", "PH-C5", "PH-C6"],
    "'Plp1-ET showed more than 50% relative activity between pH 7.5 and 8.5, with its "
    "highest activity at pH 8.0'. Recorded optimum 7.5 was the range low end; "
    "corrected to 8.0.",
    enzyme_name="Plp1-ET", pH=8.0, pH_low=7.5, pH_high=8.5, value_std=8.0,
    direction="optimum"),
"BM6E5147B1F9": _k(["PH-C1", "PH-C3", "PH-C5", "PH-C6"],
    "Recorded as enzyme_name 'Est1' with range 7.0-8.5, but 7.0-8.5 is Ces1-ET's range "
    "('Ces1-ET exhibited more than 50% relative activity at pH between 7.0 and 8.5, "
    "reaching its optimal activity at approximately pH 7.5'). Est1-ET's own range is "
    "7.0-9.0 with a maximum at pH 9.0. Re-attributed to Ces1-ET, optimum set to 7.5.",
    enzyme_name="Ces1-ET", pH=7.5, pH_low=7.0, pH_high=8.5, value_std=7.5,
    rel_pct=50.0, rel_qual="gte", direction="optimum"),

# ---------------------------------------------------------------------------------
# PMC12188634 -- commercial Savinase degrading PLA
# ---------------------------------------------------------------------------------
"BM37E9907878": _k(["PH-C5", "PH-C7"],
    "'optimum conditions for the PLA-degrading activity of Savinase ... pH 8.5 and 42 C'.",
    enzyme_name="Savinase", direction="optimum"),
"BM9F5746819C": _k(["PH-C5"],
    "Covariate row: temperature optimum 42 deg C at pH 8.5.", enzyme_name="Savinase"),

# ---------------------------------------------------------------------------------
# PMC13323979 -- PS lipase and FM-10 lipase on an enzyme@MOF platform
# ---------------------------------------------------------------------------------
"BM6CC5D054EB": _k(["PH-C7"],
    "'PS lipase and FM-10 lipase exhibited the best ... activity with optimal reaction "
    "conditions of T = 40-55 deg C and pH = 6.8'. Two lipases, one shared value.",
    direction="optimum", attribution_certainty="multiple_enzymes_same_value"),
"BME948DB4347": _k([],
    "Covariate row: temperature optimum 40-55 deg C at pH 6.8.",
    attribution_certainty="multiple_enzymes_same_value"),

# ---------------------------------------------------------------------------------
# PMC12960341 -- CaFaeA, promiscuous feruloyl esterase
# ---------------------------------------------------------------------------------
"BM8A4F230105": _k(["PH-C5", "PH-C7"],
    "'CaFaeA exhibits maximal activity at pH 8.0'.",
    enzyme_name="CaFaeA", direction="optimum"),
"BMA6514460C1": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'retains over 90% activity after 30 min incubation at pH 10.0'.",
    enzyme_name="CaFaeA", rel_pct=90.0, rel_qual="gte", direction="stabilising",
    exposure_time_min=30.0),

# ---------------------------------------------------------------------------------
# PMC10418727 -- EaEst2, BHET-degrading carboxylesterase
# ---------------------------------------------------------------------------------
"BME3583FB244": _k(["PH-C2", "PH-C5", "PH-C7"],
    "'EaEst2 showed its maximal activity at pH 7.0' is a pH OPTIMUM, not pH stability.",
    enzyme_name="EaEst2", measurement_type="pH optimum", direction="optimum"),
"BM8D124B9FCE": _k(["PH-C2", "PH-C3", "PH-C5"],
    "'only ~40% of its maximal activity was retained at pH 8.0' is a point on the "
    "activity-pH profile.",
    enzyme_name="EaEst2", measurement_type="pH activity",
    rel_pct=40.0, rel_qual="approx"),

# ---------------------------------------------------------------------------------
# Single-row articles -- kept
# ---------------------------------------------------------------------------------
"BM95627C2801": _k(["PH-C5", "PH-C7"],
    "'The optimum pH for enzyme activity was realized at pH 8.0' -- EstRag, tier A.",
    enzyme_name="EstRag", direction="optimum"),
"BM097BED1F73": _k(["PH-C2", "PH-C5", "PH-C6", "PH-C7"],
    "'PET27 was most active between pH 7-8 and PET30 between pH 6-8'. The recorded "
    "7.0-8.0 is PET27's interval exactly, so the row is attributed to PET27 and "
    "reclassified from a point optimum to an activity range.",
    enzyme_name="PET27", measurement_type="pH activity range",
    pH_low=7.0, pH_high=8.0, pH_is_range="yes", ph_range_group="R-8767016-a",
    direction="optimum", attribution_certainty="single_enzyme_named"),
"BM7E25455D3E": _k(["PH-C2", "PH-C5", "PH-C6"],
    "'TflNylA was most active against pNPH between pH 5.5 and 8.5 and exhibited a "
    "bell-shaped pH-rate profile'. This is the >50%-activity interval, not a point "
    "optimum; the article does not state a single optimum in this sentence.",
    enzyme_name="TflNylA", measurement_type="pH activity range",
    pH_low=5.5, pH_high=8.5, pH_is_range="yes", ph_range_group="R-12767561-a",
    substrate="pNPH"),
"BM837DB27EC1": _k(["PH-C7"],
    "'enzymatic activity was optimal for all the chimeras at pH 7.5' -- several MHETase "
    "chimeras share the stated optimum.",
    direction="optimum", attribution_certainty="multiple_enzymes_same_value"),
"BMBF693ED6C8": _k(["PH-C5", "PH-C7"],
    "'LipC displayed optimal activity at pH 3.5' -- acidophilic lipase.",
    enzyme_name="LipC", direction="optimum"),
"BMD363C6A8E6": _k(["PH-C1", "PH-C5", "PH-C6"],
    "'The optimal pH for PCLase0801 activity was determined to be 8.0, with relatively "
    "high activity maintained between pH 7.0 and 9.0'. Recorded optimum 7.0 was the "
    "range low end; corrected to 8.0.",
    enzyme_name="PCLase0801", pH=8.0, pH_low=7.0, pH_high=9.0, value_std=8.0,
    direction="optimum"),
"BME8E31FAE60": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'PCLase I showed remarkable stability at pH 12.0 with activity of approximately "
    "100%'. Attributed to PCLase I, which the sentence names for this value.",
    enzyme_name="PCLase I", rel_pct=100.0, rel_qual="approx", direction="stabilising",
    attribution_certainty="single_enzyme_named"),
"BMF2FE995DB3": _k(["PH-C3", "PH-C5", "PH-C7"],
    "'The pure enzyme retains its activity after 3 h at pH 10 above 85%'. The trailing "
    "clause ('but its activity decreases to below 50%') has no stated condition and is "
    "not used.",
    enzyme_name="ANCUT1", rel_pct=85.0, rel_qual="gte", direction="stabilising",
    exposure_time_min=180.0),

# ---------------------------------------------------------------------------------
# Single-row articles -- excluded
# ---------------------------------------------------------------------------------
"BM03DE403B9C": _x(["PH-X2", "PH-X7"],
    "'a standard bell-shaped activity-pH profile with an optimum around 7.5.51 When "
    "starting from a lower pH (usually buffers of pH 3.5-5.0 ...)'. The recorded "
    "3.5-5.0 is the STARTING BUFFER range; the stated optimum is 7.5. The trailing '51' "
    "is a stripped reference marker, so the claim is secondhand as well."),
"BM539CC031EB": _x(["PH-X5"],
    "'The MODEL PREDICTED maximum biodegradation at pH 7.5' -- an RSM optimisation "
    "output, and about whole-cell biodegradation rather than an enzyme. Shipping it "
    "would breach the benchmark's own no-predicted-values integrity statement."),
"BMFE76762A46": _x(["PH-X8"],
    "pH 3.54 is the buffer of an absorption/1H-NMR quantification method for TPA, not an "
    "enzyme assay condition."),
"BMEEB3F89D6F": _x(["PH-X7"],
    "'The AUTHORS FOUND that the pH of the solution dropped ...' in a review article; "
    "restates another study's observation."),
"BM85EC0EEFF2": _k(["PH-C5", "PH-C7"],
    "REINSTATED by the deep re-read of the exclusions. Pass 1 dropped this under PH-X4 "
    "because the sentence 'The optimal activity was at pH 7.5 (Figure S3C)' carries no "
    "enzyme subject and the article characterises eight candidates. The full paragraph "
    "resolves it beyond doubt: 'Since PD3 possesses the best long-term stability, further "
    "characterization of PD3's esterase activity was performed ... Higher activities of "
    "PD3 were observed when using p-NPB and p-NPH at 42 deg C compared with 37 deg C "
    "(Figure S3B). The optimal activity was at pH 7.5 (Figure S3C).' Every sentence in the "
    "paragraph takes PD3 as its subject, and the figure panels run in sequence S3A-S3D on "
    "PD3. Attributed to PD3.",
    enzyme_name="PD3", direction="optimum",
    attribution_certainty="single_enzyme_named"),
"BM44DA9B1565": _x(["PH-X6", "PH-X4"],
    "Ulvan lyase -- a polysaccharide lyase, not a carboxylester hydrolase. 'all three "
    "ulvan lyases' is also unattributable."),
"BM60E20E768C": _x(["PH-X6"],
    "'half-life of quinone release ... at pH 5' -- self-immolative linker chemistry, "
    "no enzyme."),
"BM3A1A41F1DA": _x(["PH-X6"],
    "Invertase (beta-fructofuranosidase, a glycoside hydrolase) immobilised on a PHB "
    "carrier. The polymer is the support, not the substrate."),
"BMC0FC218AB8": _x(["PH-X6"], "Same invertase article."),
"BM488F8758D1": _x(["PH-X6", "PH-X1"],
    "rXynS1 is a GH11 xylanase (glycoside hydrolase), off-target; and pH 5.0 is the "
    "assay pH ('assayed at pH 5.0'), not an optimum."),
"BM5B4789AA54": _x(["PH-X6", "PH-X1"], "Same GH11 xylanase article."),
"BMB86BE59C99": _x(["PH-X6"],
    "Cytochrome P450BM3 monooxygenase degrading gossypol, a plant polyphenol. Neither "
    "the enzyme class nor the substrate is in scope."),
"BMDDBDC51F4A": _x(["PH-X6"], "Same P450/gossypol article."),
"BM7D11018C05": _x(["PH-X1"],
    "'the enzyme was incubated in 1 mL of 100 mM KH2PO4 buffer (pH 8.0) at 50, 55, 60, "
    "65 and 70 deg C ... followed by determining the residual activity' -- pH 8.0 is the "
    "buffer of a thermostability protocol."),
"BMC3719577E5": _x(["PH-X1"],
    "Same methods sentence; 70 deg C is the highest temperature tested, recorded as a "
    "thermostability value."),
}


def counts():
    keep = [m for m, c in CURATION.items() if c["verdict"] == K]
    drop = [m for m, c in CURATION.items() if c["verdict"] == X]
    return len(CURATION), len(keep), len(drop)


if __name__ == "__main__":
    total, keep, drop = counts()
    print(f"curated rows : {total}")
    print(f"  KEEP       : {keep}")
    print(f"  EXCLUDE    : {drop}")
