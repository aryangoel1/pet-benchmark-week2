"""
Deep re-read of the 38 EXCLUDED candidates against freshly downloaded full text.

    python3 scripts/deep_verify_exclusions.py [--refresh]

`deep_verify_ph.py` re-checked the 67 shipped rows. This does the same for the rows the
audit threw away, closing the asymmetry noted in docs/LIMITATIONS.md: a wrongly excluded
row costs coverage rather than correctness, but "38 removed under twelve rules" is a
published claim and every one of those removals should survive a second look.

The decisive addition here is **section awareness**. Thirteen rows were removed under
`PH-X1` (the value came from a methods or protocol sentence rather than a result). That
call can be checked objectively: JATS marks up its own section structure, so if the
sentence sits under a "Materials and Methods" heading, the rule fired correctly. Pass 1
had no section information beyond a coarse `section` field inherited from Week 2.

Per-rule automated cross-checks

    PH-X1   is the sentence inside a methods/protocol section?
    PH-X5   does the sentence contain prediction language?
    PH-X6   do the article's title and abstract name an in-scope enzyme class?
    PH-X7   is the article a review, or does the sentence carry secondhand markers?
    PH-X10  does a shipped row with the same article/type/pH actually exist?
    PH-X11  does the quote show table-concatenation signatures?
    PH-X3/4 how many distinct enzyme names appear near the sentence?

Outputs
    data/exclusion_review_packet.md   every excluded row beside its article context
    data/ph_exclusion_verification.json
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deep_verify_ph import (fetch, article_type, norm, locate, DASHES)  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

METHODS_RE = re.compile(
    r"(materials?\s+and\s+methods|methods?\s+and\s+materials|^\s*methods?\s*$|"
    r"experimental\s+(section|procedures?|design)|^\s*materials?\s*$|"
    r"enzyme\s+assays?|assay\s+conditions|protein\s+(expression|purification)|"
    r"cloning|statistical\s+analysis|sample\s+preparation)", re.I)
RESULTS_RE = re.compile(r"(results?|discussion|characteri[sz]ation|"
                        r"biochemical\s+propert)", re.I)
PREDICTION_RE = re.compile(
    r"(model predicted|predicted maximum|response surface|rsm|in silico|"
    r"was predicted|optimi[sz]ation model)", re.I)
SECONDHAND_RE = re.compile(
    r"(the authors? (found|reported|observed|showed)|in their study|"
    r"previously reported|has been reported|reported that|et al\.)", re.I)
IN_SCOPE_RE = re.compile(
    r"(esterase|lipase|cutinase|petase|depolymerase|hydrolase|"
    r"carboxylesterase|nylonase|polyesterase)", re.I)
OFF_TARGET_RE = re.compile(
    r"(xylanase|glycoside hydrolase|ulvan lyase|polysaccharide lyase|invertase|"
    r"fructofuranosidase|cytochrome p450|monooxygenase|carbonic anhydrase)", re.I)


def sectioned_text(xml):
    """Plain text plus (offset, section-path) marks that follow the article's real
    <sec> nesting, so a match can be placed in its true enclosing section rather than
    beside whichever heading happened to precede it in document order.

    A figure caption or table sitting inside Results would otherwise make a Methods
    sentence look like a Results sentence, and vice versa.
    """
    xml = re.sub(r"<(ref-list|back)\b.*?</\1>", " ", xml, flags=re.S)
    out, marks = [], []
    pos = 0
    stack = []          # one slot per open <sec>; filled by that sec's first <title>
    depth_titled = []   # whether the sec at each depth already took its title
    token = re.compile(r"<(/?)([a-zA-Z0-9:-]+)[^>]*?(/?)>|([^<]+)", re.S)
    pending_title = False
    title_buf = []

    def record():
        marks.append((pos, tuple(s for s in stack if s)))

    for m in token.finditer(xml):
        close, name, selfclose, text = m.groups()
        if text is not None:
            txt = html.unescape(text)
            if pending_title:
                title_buf.append(txt)
            out.append(txt)
            pos += len(txt)
            continue
        if name == "sec" and not close and not selfclose:
            stack.append("")
            depth_titled.append(False)
            record()
        elif name == "sec" and close:
            if stack:
                stack.pop()
                depth_titled.pop()
            record()
        elif name == "title" and not close:
            pending_title, title_buf = True, []
        elif name == "title" and close:
            t = re.sub(r"\s+", " ", "".join(title_buf)).strip()
            pending_title = False
            # a title belongs to the innermost <sec> that has not taken one yet
            if t and stack and not depth_titled[-1]:
                stack[-1] = t
                depth_titled[-1] = True
                record()
        if name in ("p", "title", "td", "th", "tr", "sec", "caption",
                    "label", "abstract") and close:
            out.append(" ¶ ")
            pos += 3
    text = unicodedata.normalize("NFKC", "".join(out)).translate(DASHES)
    return text, marks


def section_path(marks, offset):
    """The <sec> title path enclosing this offset, outermost first."""
    path = ()
    for off, p in marks:
        if off <= offset:
            path = p
        else:
            break
    return list(path)


def heading_for(marks, offset):
    p = section_path(marks, offset)
    return p[-1] if p else ""


def enclosing_headings(marks, offset, n=4):
    return section_path(marks, offset)[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    with open(os.path.join(DATA, "ph_excluded_v1.csv"),
              encoding="utf-8", newline="") as fh:
        excl = list(csv.DictReader(fh))
    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        kept = list(csv.DictReader(fh))

    pmcids = sorted({r["pmcid"] for r in excl})
    print(f"re-reading {len(excl)} excluded rows across {len(pmcids)} articles")

    arts = {}
    for n, p in enumerate(pmcids, 1):
        xml = fetch(p, args.refresh)
        if not xml:
            arts[p] = {"text": "", "marks": [], "type": "unavailable",
                       "title": "", "abstract": ""}
            print(f"  [{n:2d}/{len(pmcids)}] {p}  UNAVAILABLE")
            continue
        text, marks = sectioned_text(xml)
        at = re.search(r"<article-title>(.*?)</article-title>", xml, re.S)
        ab = re.search(r"<abstract\b.*?</abstract>", xml, re.S)
        arts[p] = {
            "text": text, "marks": marks, "type": article_type(xml),
            "title": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "",
                                                html.unescape(at.group(1)))) if at else "",
            "abstract": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                                   html.unescape(ab.group(0)))) if ab else "",
        }
        print(f"  [{n:2d}/{len(pmcids)}] {p}  {arts[p]['type']:<18} "
              f"{len(marks):3d} headings")

    kept_keys = {(r["pmcid"], r["measurement_type"], r["pH"]) for r in kept}
    kept_by_paper = {}
    for r in kept:
        kept_by_paper.setdefault(r["pmcid"], []).append(r)

    findings, packet = [], []
    for r in sorted(excl, key=lambda x: (x["pmcid"], x["source_measurement_id"])):
        a = arts[r["pmcid"]]
        rid = r["source_measurement_id"]
        rules = [c for c in r["exclusion_rules"].split(";") if c]
        checks = []

        if not a["text"]:
            findings.append(("ARTICLE_UNAVAILABLE", rid, r["pmcid"]))
            packet.append({**r, "heading": "", "context": "(article unavailable)",
                           "checks": ["article could not be downloaded"]})
            continue

        hit = locate(a["text"], r["evidence_quote"])
        if hit is None:
            findings.append(("QUOTE_NOT_FOUND", rid,
                             f"{r['pmcid']}: quote not located in fresh text"))
            heading, ctx, headings = "", "(quote not located)", []
        else:
            i, ln = hit
            heading = heading_for(a["marks"], i)
            headings = enclosing_headings(a["marks"], i)
            ctx = a["text"][max(0, i - 1000): i + ln + 1000]

        top = headings[0] if headings else ""
        path = " / ".join(headings)
        # the outermost heading decides; sub-headings like "Effect of pH on
        # activity" occur under both Methods and Results
        in_methods = bool(METHODS_RE.search(top)) or (
            not RESULTS_RE.search(top) and bool(METHODS_RE.search(path)))
        in_results = bool(RESULTS_RE.search(top))

        # ---- per-rule cross-checks ------------------------------------------
        if "PH-X1" in rules:
            if in_methods:
                checks.append(f"CONFIRMED: enclosed by a methods section -- '{path}'")
            elif in_results:
                checks.append(f"CHALLENGED: enclosed by a results section -- '{path}'")
                findings.append(("X1_IN_RESULTS_SECTION", rid,
                                 f"{r['pmcid']}: PH-X1 row sits under '{path}'"))
            else:
                checks.append(f"UNCLEAR: section path '{path or '(none)'}' is neither "
                              f"clearly methods nor results")
                findings.append(("X1_SECTION_UNCLEAR", rid,
                                 f"{r['pmcid']}: '{path}'"))

        if "PH-X5" in rules:
            ok = bool(PREDICTION_RE.search(r["evidence_quote"]))
            checks.append(("CONFIRMED" if ok else "CHALLENGED")
                          + ": prediction language in the quote")
            if not ok:
                findings.append(("X5_NO_PREDICTION_LANGUAGE", rid, r["pmcid"]))

        if "PH-X6" in rules:
            blob = a["title"] + " " + a["abstract"]
            off = OFF_TARGET_RE.findall(blob)
            ins = IN_SCOPE_RE.findall(blob)
            if off:
                checks.append(f"CONFIRMED: title/abstract name off-target class "
                              f"{sorted(set(x.lower() for x in off))}")
            else:
                checks.append(f"CHALLENGED: no off-target class in title/abstract; "
                              f"in-scope terms present {sorted(set(x.lower() for x in ins))}")
                findings.append(("X6_NO_OFFTARGET_TERM", rid,
                                 f"{r['pmcid']}: {a['title'][:70]}"))

        if "PH-X7" in rules:
            is_review = a["type"] in ("review-article", "editorial")
            marker = bool(SECONDHAND_RE.search(r["evidence_quote"]))
            if is_review:
                checks.append(f"CONFIRMED: article-type='{a['type']}'")
            elif marker:
                checks.append("CONFIRMED: secondhand marker in the quote "
                              "(article is a research-article)")
            else:
                checks.append(f"CHALLENGED: article-type='{a['type']}' and no "
                              f"secondhand marker in the quote")
                findings.append(("X7_NOT_REVIEW_NO_MARKER", rid,
                                 f"{r['pmcid']} type={a['type']}"))

        if "PH-X10" in rules:
            key = (r["pmcid"], r["measurement_type"], r["pH"])
            twin = [k for k in kept_keys if k[0] == r["pmcid"] and k[2] == r["pH"]]
            if twin:
                checks.append(f"CONFIRMED: a shipped row covers {twin[0]}")
            else:
                checks.append("CHALLENGED: no shipped row with this article/pH -- "
                              "the measurement may have been lost entirely")
                findings.append(("X10_NO_SURVIVING_TWIN", rid,
                                 f"{r['pmcid']} pH={r['pH']} type={r['measurement_type']}"))

        if "PH-X11" in rules:
            q = r["evidence_quote"]
            sig = bool(re.search(r"[a-z][A-Z]", q)) or q.count(";") >= 2
            checks.append(("CONFIRMED" if sig else "CHALLENGED")
                          + ": table-concatenation signature in the quote")
            if not sig:
                findings.append(("X11_NO_CONCAT_SIGNATURE", rid, r["pmcid"]))

        if any(x in rules for x in ("PH-X3", "PH-X4")):
            names = set(re.findall(r"\b([A-Z][A-Za-z]{1,7}\d{0,4}(?:-[A-Z]{2})?)\b",
                                   r["evidence_quote"]))
            names = {n for n in names
                     if not re.fullmatch(r"(The|This|At|In|For|Fig|Table|However|"
                                         r"When|About|And|But|Next|Results|Their|"
                                         r"Since|Concerning|Further|Regarding|PET|"
                                         r"Beyond|Moreover|All|Its|It)", n)}
            checks.append(f"enzyme-like tokens in the quote: {sorted(names) or 'none'}")

        packet.append({**r, "heading": heading, "headings": headings,
                       "context": ctx, "checks": checks,
                       "article_type": a["type"], "article_title": a["title"]})

    # ---- packet -------------------------------------------------------------
    out = ["# Exclusion review packet\n",
           f"All {len(excl)} excluded candidates, each printed beside the freshly "
           "downloaded article text and the section heading it sits under.\n",
           "`CONFIRMED` / `CHALLENGED` are automated cross-checks of the rule that fired; "
           "they are evidence for a human decision, not the decision.\n", "---\n"]
    cur = None
    for p in packet:
        if p["pmcid"] != cur:
            cur = p["pmcid"]
            out.append(f"\n## {cur} — {p.get('article_type', '?')}\n")
            out.append(f"*{p.get('article_title', '')[:120]}*\n")
        out.append(f"\n### {p['source_measurement_id']} — dropped by "
                   f"`{p['exclusion_rules']}`\n")
        out.append(f"- **was**: {p['measurement_type']} @ pH {p['pH']} "
                   f"= {p['value_std']} {p['value_unit_std']}")
        out.append(f"- **section**: {' / '.join(p.get('headings', [])) or '(none)'}")
        for c in p["checks"]:
            out.append(f"- **check**: {c}")
        out.append(f"- **reason given**: {p['reason']}")
        out.append(f"- **quote**: {p['evidence_quote']}\n")
        out.append("```")
        out.append(re.sub(r"[ \t]+", " ", p["context"]).strip())
        out.append("```\n")
    with open(os.path.join(DATA, "exclusion_review_packet.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(out))

    summary = {}
    for k, _, _ in findings:
        summary[k] = summary.get(k, 0) + 1
    result = {
        "excluded_rows": len(excl),
        "articles": len(pmcids),
        "article_types": {t: sum(1 for p in pmcids if arts[p]["type"] == t)
                          for t in sorted({arts[p]["type"] for p in pmcids})},
        "quotes_relocated": len(excl) - summary.get("QUOTE_NOT_FOUND", 0),
        "challenges_by_kind": summary,
        "challenges": [{"kind": k, "row": s, "detail": d} for k, s, d in findings],
    }
    with open(os.path.join(DATA, "ph_exclusion_verification.json"), "w",
              encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)

    print(f"\nquotes relocated : {result['quotes_relocated']}/{len(excl)}")
    print(f"article types    : {result['article_types']}")
    print(f"challenges       : {len(findings)}")
    for k, n in sorted(summary.items(), key=lambda kv: -kv[1]):
        print(f"    {k:<28} {n}")
    for k, s, d in findings:
        print(f"      - [{k}] {s}: {d}")
    print("\nwrote data/exclusion_review_packet.md and "
          "data/ph_exclusion_verification.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
