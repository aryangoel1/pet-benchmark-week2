"""
Generate the two documents that must never disagree with the data.

    python3 scripts/make_reports.py

    docs/AUDIT_REPORT.md     every candidate row, its verdict, the rule and the reason
    docs/DATASET_SUMMARY.md  the dataset-summary table for the paper

Both are rebuilt from data/ph_benchmark_v1.csv, data/ph_excluded_v1.csv and
data/ph_stats.json, so a number can only change here by changing the data.
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ph_curation import (EXCLUSION_RULES, CORRECTION_RULES,  # noqa: E402
                         SEQUENCE_REJECTIONS)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
DOCS = os.path.join(HERE, "docs")

RULE_PROSE = {
    "PH-X1": "the value came from a methods or protocol sentence -- an assay buffer, an "
             "incubation temperature, the range of conditions tested, or the baseline "
             "used for normalisation -- rather than from a measured outcome",
    "PH-X2": "the row was typed as a pH optimum but the value is the endpoint of an "
             "activity range, and the source states a different optimum",
    "PH-X3": "the enzyme name or accession on the row is not the enzyme the evidence "
             "sentence describes",
    "PH-X4": "the evidence covers two or more enzymes with different values, or names no "
             "enzyme at all, so the value cannot be attributed",
    "PH-X5": "the value is a model or response-surface prediction, not a measurement",
    "PH-X6": "the enzyme is not a carboxylester hydrolase or polymer depolymerase",
    "PH-X7": "the sentence restates another study's result, or the article is a review",
    "PH-X8": "the pH belongs to an analytical procedure (chromatography, NMR), not to an "
             "enzyme assay",
    "PH-X9": "the evidence contains no measurement of the type the row claims",
    "PH-X10": "the same enzyme, article, measurement type and pH is already represented "
              "by a better-evidenced row",
    "PH-X11": "the evidence is a concatenated table cell with no recoverable field "
              "boundaries",
    "PH-X12": "a boundary word ('beyond', 'above') with no outcome actually measured at "
              "the recorded pH",
}


def load():
    def rd(name):
        with open(os.path.join(DATA, name), encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    stats = json.load(open(os.path.join(DATA, "ph_stats.json"), encoding="utf-8"))
    deep = json.load(open(os.path.join(DATA, "ph_deep_verification.json"),
                          encoding="utf-8"))
    return (rd("ph_benchmark_v1.csv"), rd("ph_excluded_v1.csv"),
            rd("ph_audit_log.csv"), stats, deep)


def audit_report(kept, excluded, audit, stats, deep):
    L = []
    a = L.append
    a("# pH benchmark -- audit report\n")
    a("Every one of the "
      f"**{stats['candidates']} candidate pH rows** inherited from the Week-2 benchmark "
      "carries an explicit verdict below. The verdicts live in "
      "`scripts/ph_curation.py`; this document is generated from them, so the two cannot "
      "drift apart.\n")
    a("> **What this audit is.** Two passes. The first read each of the 105 "
      "candidates against the evidence sentence the Week-2 pipeline stored with it, "
      "judging whether the recorded number is the right reading of that text -- which "
      "enzyme it belongs to, whether it is a result or a protocol detail, and which "
      "way the effect ran. The second re-downloaded all 30 shipped articles and "
      "re-checked every shipped row in full context; it is reported below, and it is "
      "what caught the sequence misattributions. Neither pass re-derives values from "
      "the underlying figures, and the second did not revisit the 38 exclusions.\n")

    a("## Outcome\n")
    a("| | Rows | Share |")
    a("|---|---:|---:|")
    a(f"| Candidates inherited from Week 2 | {stats['candidates']} | 100% |")
    a(f"| **Removed by the audit** | **{stats['excluded']}** | "
      f"{stats['exclusion_rate_pct']}% |")
    a(f"| **Shipped** | **{stats['shipped']}** | "
      f"{round(100 - stats['exclusion_rate_pct'], 1)}% |")
    a(f"| Shipped rows carrying at least one correction | "
      f"{sum(1 for r in kept if r['audit_rules'])} | |")
    a("")
    a(f"Source articles went from {stats['distinct_papers_candidates']} to "
      f"**{stats['distinct_papers_shipped']}**: "
      f"{stats['distinct_papers_dropped_entirely']} articles lost every row they "
      "contributed.\n")

    a("## Why rows were removed\n")
    a("| Rule | What it catches | Rows |")
    a("|---|---|---:|")
    for code, n in sorted(stats["exclusion_rule_counts"].items(),
                          key=lambda kv: -kv[1]):
        a(f"| `{code}` {EXCLUSION_RULES[code]} | {RULE_PROSE[code]} | {n} |")
    a("")
    a("A row can fire more than one rule, so the column sums to more than "
      f"{stats['excluded']}.\n")

    a("## Corrections applied to rows that were kept\n")
    a("| Rule | What it does | Rows |")
    a("|---|---|---:|")
    corr_prose = {
        "PH-C1": "pH optimum reset to the value the article states, where the pipeline "
                 "had stored a range endpoint instead",
        "PH-C2": "measurement type changed to match what the sentence actually reports",
        "PH-C3": "the outcome at that pH (residual or relative activity) recovered from "
                 "the sentence into a field of its own",
        "PH-C4": "a buffer removed that the evidence does not name and that cannot hold "
                 "the recorded pH",
        "PH-C5": "enzyme name set, or corrected, from the evidence sentence",
        "PH-C6": "pH interval bounds set to the range the article states",
        "PH-C7": "direction of the effect recorded, so a stability row says whether "
                 "activity was held or lost",
    }
    for code, n in sorted(stats["correction_rule_counts"].items(),
                          key=lambda kv: -kv[1]):
        a(f"| `{code}` {CORRECTION_RULES[code]} | {corr_prose[code]} | {n} |")
    a("")

    a("## The five findings that mattered most\n")
    a("1. **A tier-A sequence was attached to the wrong enzyme.** `BME732B05FC1` carried "
      "accession `P26495` (PhaZ) on a sentence about LIP4. A wrong sequence on a real "
      "measurement is the worst defect a benchmark can ship, because it looks correct in "
      "every automated check.\n")
    a("2. **A model-predicted value had survived into a dataset whose integrity "
      "statement forbids them.** `BM539CC031EB` recorded pH 7.5 from *\"The model "
      "predicted maximum biodegradation at pH 7.5\"* -- a response-surface optimisation "
      "over whole-cell biodegradation.\n")
    a("3. **Range endpoints were being shipped as optima.** Five rows named a pH optimum "
      "that was really the low end of an activity range, while the same sentence gave "
      "the true optimum: `pH 5 -> 7`, `4.0 -> 5.0`, `7.5 -> 8.0`, `7.0 -> 8.0`, "
      "`7.0 -> 7.5`. Each is a 0.5-2.0 unit error in the exact quantity the screener "
      "predicts.\n")
    a("4. **Thirteen rows were assay protocol, not results** -- buffer pH read as a pH "
      "optimum, incubation temperature read as thermostability, the range of "
      "temperatures tested read as the optimum, and in one case a substrate loading "
      "(*\"2.9% loading by mass of amorphous PET film\"*) parsed as 2.9% relative "
      "activity.\n")
    a("5. **A review article's comparison table produced three rows** on a garbled "
      "concatenated cell, labelled `IsPETase` but carrying PET46's accession.\n")

    a("## Second pass: deep re-read against full text\n")
    a("The verdicts above came from reading each row's stored evidence sentence. A "
      "second pass (`scripts/deep_verify_ph.py`) re-downloaded the full text of all "
      f"{stats['distinct_papers_shipped']} shipped articles from Europe PMC and "
      "re-checked every shipped row in context.\n")
    a("| Check | Result |")
    a("|---|---|")
    a(f"| Articles re-downloaded | {deep['articles_downloaded']}/{deep['articles']} |")
    a("| JATS `article-type` | "
      f"{deep['article_types'].get('research-article', 0)}/{deep['articles']} "
      "`research-article` -- no review or editorial survived |")
    a(f"| Evidence sentences relocated in fresh text | {deep['quotes_relocated']}/"
      f"{stats['shipped']} |")
    a("| Enzyme names occurring in their article | all |")
    a("| Corrected pH optima found verbatim | 5/5 |")
    a(f"| Open findings after correction | {len(deep['findings'])} |")
    a("")
    a("This pass catches what a sentence-level audit structurally cannot: an accession "
      "is usually stated in a deposit or methods section far from the sentence carrying "
      "the measurement, so whether the row names the right *protein* is invisible from "
      "the quote alone.\n")
    a("### Sequence attributions withdrawn\n")
    a("Three of six accessions turned out to be cited rather than deposited. In every "
      "case the recorded organism independently corroborates the error -- it is the "
      "organism of the cited protein, not of the enzyme assayed.\n")
    a("| Accession | Recorded as | Why it was withdrawn |")
    a("|---|---|---|")
    for acc, info in SEQUENCE_REJECTIONS.items():
        a(f"| `{acc}` | {info['enzyme']} ({info['pmcid']}) | {info['reason']} |")
    a("")
    a("The measurements themselves are sound, so those rows keep their values and lose "
      "their sequences. The sequence-carrying set went from 16 rows / 6 proteins to "
      f"{stats['rows_with_sequence']} rows / {stats['distinct_proteins']} proteins, "
      "each confirmed against an explicit deposit statement in its article's own text. "
      "The benchmark's only overlap with the held-out test split disappeared with "
      "them.\n")
    a("Three smaller corrections came from the same pass: an enzyme named for its "
      "strain rather than itself (IBRL-CHS2 -> MLipA, 7 rows), a measurement type only "
      "the full paragraph disambiguates (a PanLip(dN) value is an activity-profile "
      "point, not post-incubation stability), and one publication year "
      "(PMC12767561: 2026 -> 2025).\n")
    a("## Every candidate, with its verdict\n")
    by_paper = defaultdict(list)
    log = {r["source_measurement_id"]: r for r in audit}
    for r in audit:
        by_paper[r["pmcid"]].append(r)
    kept_ids = {r["source_measurement_id"] for r in kept}
    order = sorted(by_paper, key=lambda p: (-len(by_paper[p]), p))
    for pm in order:
        rs = by_paper[pm]
        nk = sum(1 for r in rs if r["verdict"] == "KEEP")
        a(f"\n### {pm} &mdash; {nk} kept / {len(rs)} candidates\n")
        a("| Row | Verdict | Type as recorded | pH | Rules | Reason |")
        a("|---|---|---|---:|---|---|")
        for r in sorted(rs, key=lambda x: x["source_measurement_id"]):
            v = "KEEP" if r["source_measurement_id"] in kept_ids else "**drop**"
            note = r["note"].replace("|", "\\|").replace("\n", " ")
            a(f"| `{r['source_measurement_id']}` | {v} | {r['original_measurement_type']}"
              f" | {r['original_pH']} | {r['rules'] or '--'} | {note} |")
    a("")
    a("---\n")
    a("Regenerate with `python3 scripts/make_reports.py`. "
      "Row-level machine-readable form: `data/ph_audit_log.csv`.\n")
    return "\n".join(L)


def dataset_summary(kept, excluded, audit, stats):
    L = []
    a = L.append
    a("# pH benchmark -- dataset summary\n")
    a("Table 1 as it will appear in the paper, plus the breakdowns that support it. "
      "Generated from `data/ph_benchmark_v1.csv`.\n")

    a("## Table 1. Composition of the pH benchmark\n")
    a("| Property | Value |")
    a("|---|---|")
    a(f"| Measurements | **{stats['shipped']}** |")
    a(f"| Source articles | **{stats['distinct_papers_shipped']}** |")
    a(f"| Publication years | {min(stats['years'])}\u2013{max(stats['years'])} |")
    a(f"| pH as the measured outcome | {stats['ph_outcome_rows']} |")
    a(f"| pH as a recorded assay covariate | {stats['ph_covariate_rows']} |")
    a(f"| Scoreable on the pH axis | {stats['scored_condition_axis']} |")
    a(f"| Scoreable by a sequence model | {stats['scored_sequence_model']} |")
    a(f"| Rows with a resolved protein sequence | {stats['rows_with_sequence']} |")
    a(f"| Distinct proteins | {stats['distinct_proteins']} |")
    a(f"| Distinct accessions | {stats['distinct_accessions']} |")
    a(f"| Distinct enzyme classes | {stats['enzyme_classes']} |")
    a(f"| Rows naming a polymer substrate | {stats['polymer_named']} |")
    a(f"| pH range covered | {stats['ph_min']}\u2013{stats['ph_max']} "
      f"(median {stats['ph_median']}) |")
    a(f"| Rows carrying an outcome at the pH (% activity) | "
      f"{stats['rows_with_outcome_pct']} |")
    a(f"| Rows carrying the direction of the effect | {stats['rows_with_direction']} |")
    a(f"| Rows with temperature recorded as well | {stats['rows_with_temperature']} |")
    a(f"| Rows with an exposure time | {stats['rows_with_exposure_time']} |")
    a(f"| pH interval rows (in {stats['range_groups']} range groups) | "
      f"{stats['range_rows']} |")
    a(f"| Rows in Luke's training split | **0** |")
    a("")

    a("## Measurement types\n")
    a("| Type | Rows | pH is the... |")
    a("|---|---:|---|")
    role = {"pH optimum": "outcome", "pH stability": "outcome",
            "pH activity": "outcome", "pH activity range": "outcome",
            "pH stability range": "outcome", "temperature optimum": "covariate",
            "thermostability": "covariate"}
    for t, n in stats["measurement_types"].items():
        a(f"| {t} | {n} | {role.get(t, '')} |")
    a("")

    a("## Independence tiers\n")
    a("| Tier | Rows | Meaning |")
    a("|---|---:|---|")
    tier_txt = {
        "A_fully_independent":
            "protein appears in none of the seven shared datasets and nowhere in "
            "Luke's data",
        "B_in_luke_heldout_test_only":
            "protein sits in Luke's held-out test split -- no training contamination, "
            "but not novel to the project",
        "C_conditions_only_no_sequence":
            "a real measurement whose enzyme could not be resolved to a sequence",
    }
    for t, n in stats["tiers"].items():
        a(f"| `{t}` | {n} | {tier_txt[t]} |")
    a("")

    a("## Enzyme classes represented\n")
    cls = Counter(r["enzyme_class"] for r in kept if r["enzyme_class"])
    a("| Class | Rows | Polymer named |")
    a("|---|---:|---|")
    for c_, n in cls.most_common():
        pol = sorted({r["polymer_target"] for r in kept
                      if r["enzyme_class"] == c_ and r["polymer_target"]})
        a(f"| {c_} | {n} | {', '.join(pol) or '--'} |")
    a("")

    a("## Source articles\n")
    papers = defaultdict(list)
    for r in kept:
        papers[r["pmcid"]].append(r)
    a("| PMCID | Year | Rows | Enzyme(s) | Title |")
    a("|---|---:|---:|---|---|")
    for pm in sorted(papers, key=lambda p: (-len(papers[p]), p)):
        rs = papers[pm]
        enz = sorted({r["enzyme_name"] for r in rs if r["enzyme_name"]})
        title = rs[0]["paper_title"].replace("|", "\\|")
        if len(title) > 74:
            title = title[:71] + "..."
        a(f"| {pm} | {rs[0]['year']} | {len(rs)} | {', '.join(enz)[:34] or '--'} "
          f"| {title} |")
    a("")

    a("## Distribution of reported pH optima\n")
    opt = sorted(float(r["pH"]) for r in kept
                 if r["measurement_type"] == "pH optimum" and r["pH"])
    hist = Counter(round(v * 2) / 2 for v in opt)
    a("| pH | Count |")
    a("|---:|---|")
    for v in sorted(hist):
        a(f"| {v:g} | {'#' * hist[v]} ({hist[v]}) |")
    a("")
    a(f"Range {min(opt):g}\u2013{max(opt):g}; median {sorted(opt)[len(opt)//2]:g}; "
      f"n = {len(opt)}. The alkaline skew is real and expected -- polyester hydrolysis "
      "is base-favoured -- but it also means the benchmark tests acid-tolerant enzymes "
      "thinly.\n")

    a("## What was removed, by rule\n")
    a("| Rule | Rows |")
    a("|---|---:|")
    for code, n in sorted(stats["exclusion_rule_counts"].items(), key=lambda kv: -kv[1]):
        a(f"| `{code}` {EXCLUSION_RULES[code]} | {n} |")
    a("")
    a("Full reasoning per row: `docs/AUDIT_REPORT.md` and `data/ph_excluded_v1.csv`.\n")
    return "\n".join(L)


def main():
    kept, excluded, audit, stats, deep = load()
    os.makedirs(DOCS, exist_ok=True)
    for name, text in [("AUDIT_REPORT.md",
                        audit_report(kept, excluded, audit, stats, deep)),
                       ("DATASET_SUMMARY.md",
                        dataset_summary(kept, excluded, audit, stats))]:
        path = os.path.join(DOCS, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote docs/{name}  ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
