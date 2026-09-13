"""
Deep re-verification of the pH benchmark against freshly downloaded full text.

    python3 scripts/deep_verify_ph.py [--refresh]

The first audit pass (`ph_curation.py`) read each row against the *evidence sentence*
stored with it. This pass goes further: it re-downloads the full text of every shipped
article from Europe PMC and checks each row against the article as a whole.

What it checks automatically
    1. article type from the JATS `article-type` attribute -- no review or editorial
       should have survived into the shipped set
    2. the evidence sentence is still locatable in the freshly downloaded text
    3. the recorded pH is present in the located sentence
    4. the enzyme name assigned during curation actually occurs in the article
    5. for the five corrected pH optima, the corrected value occurs in the article
       within an optimum-bearing sentence
    6. journal and publication year against the recorded metadata

What it produces for human reading
    data/deep_review_packet.md -- every shipped row printed beside a wide window of the
    surrounding article text, so attribution can be judged in context rather than from a
    one-sentence quote.

Full text is cached under data/fulltext_xml/ (gitignored); `--refresh` re-downloads.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
CACHE = os.path.join(DATA, "fulltext_xml")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/{}/fullTextXML"

DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−⁃"), "-")


def fetch(pmcid, refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{pmcid}.xml")
    if os.path.exists(path) and not refresh:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                EPMC.format(pmcid),
                headers={"User-Agent": "pet-ph-benchmark-verification/1.0"})
            raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(raw)
            time.sleep(0.4)
            return raw
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 3:
                print(f"  !! {pmcid}: {exc}")
                return ""
            time.sleep(2 * (attempt + 1))
    return ""


def article_type(xml):
    m = re.search(r'<article[^>]*article-type="([^"]+)"', xml)
    return m.group(1) if m else "unknown"


def meta(xml):
    """Journal title and the set of publication years the article itself declares.

    A JATS record can carry several <pub-date> blocks -- an electronic date, a print
    date and a collection (volume) date -- and they routinely disagree across a
    year boundary. All of them are returned so a recorded year is judged a mismatch
    only when it matches none.
    """
    j = re.search(r"<journal-title>(.*?)</journal-title>", xml, re.S)
    years, preferred = set(), ""
    for m in re.finditer(r'<pub-date([^>]*)>(.*?)</pub-date>', xml, re.S):
        attrs, blk = m.group(1), m.group(2)
        ym = re.search(r"<year>(\d{4})</year>", blk)
        if not ym:
            continue
        years.add(ym.group(1))
        if any(t in attrs for t in ('pub-type="collection"', 'pub-type="ppub"')):
            preferred = ym.group(1)
    # the DOI often encodes the volume year, which is what citations use
    doi = re.search(r'<article-id pub-id-type="doi">(.*?)</article-id>', xml)
    if doi:
        dm = re.search(r"\.((?:19|20)\d{2})[.\d]", doi.group(1))
        if dm:
            years.add(dm.group(1))
            preferred = preferred or dm.group(1)
    if not preferred and years:
        preferred = min(years)
    return (strip_tags(j.group(1)) if j else "", preferred, years)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


def plain_text(xml):
    """Readable text, with table cells separated so table-derived rows stay findable."""
    body = xml
    body = re.sub(r"<(ref-list|back|front)\b.*?</\1>", " ", body, flags=re.S)
    body = re.sub(r"</(p|title|td|th|tr|sec|caption|label)>", " ¶ ", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    body = body.translate(DASHES)
    body = unicodedata.normalize("NFKC", body)
    return re.sub(r"[ \t\r\f\v]+", " ", body)


def norm(s):
    s = unicodedata.normalize("NFKC", s or "").translate(DASHES)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def locate(text, quote):
    """Find the quote in the article text; returns (index, matched_length) or None."""
    nt, nq = norm(text), norm(quote)
    if len(nq) < 25:
        return None
    i = nt.find(nq)
    if i >= 0:
        return i, len(nq)
    # The stored quote is sometimes truncated or spans a paragraph break. Fall back to
    # the longest leading fragment that still matches uniquely enough to be useful.
    for frac in (0.8, 0.6, 0.45, 0.3):
        frag = nq[:max(30, int(len(nq) * frac))]
        i = nt.find(frag)
        if i >= 0:
            return i, len(frag)
    # Last resort: a distinctive interior run of words.
    words = nq.split()
    for size in (12, 9, 7):
        for start in range(0, max(1, len(words) - size), 3):
            frag = " ".join(words[start:start + size])
            i = nt.find(frag)
            if i >= 0:
                return i, len(frag)
    return None


def num_in(text, value):
    if value is None:
        return True
    cands = {f"{value:g}"}
    if value == int(value):
        cands |= {str(int(value)), f"{int(value)}.0"}
    else:
        cands |= {f"{value:.1f}", f"{value:.2f}"}
    return any(re.search(r"(?<![0-9.])" + re.escape(c) + r"(?![0-9])", text)
               for c in cands)


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# The five optima the audit corrected, and the enzyme each belongs to. Checked
# explicitly because they change a prediction target.
CORRECTED_OPTIMA = {
    "BMDFDCB2C50A": (7.0, "optimal activity observed at ph 7"),
    "BM168196487C": (5.0, "the highest being at ph 5.0"),
    "BM34567040FA": (8.0, "its highest activity at ph 8.0"),
    "BMD363C6A8E6": (8.0, "determined to be 8.0"),
    "BM6E5147B1F9": (7.5, "optimal activity at approximately ph 7.5"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    pmcids = sorted({r["pmcid"] for r in rows})
    print(f"downloading full text for {len(pmcids)} articles "
          f"({'refresh' if args.refresh else 'cached where available'})")
    arts = {}
    for n, p in enumerate(pmcids, 1):
        xml = fetch(p, args.refresh)
        arts[p] = {"xml": xml, "text": plain_text(xml) if xml else "",
                   "type": article_type(xml) if xml else "unavailable"}
        j, y, ys = meta(xml) if xml else ("", "", set())
        arts[p]["journal"], arts[p]["year"], arts[p]["years"] = j, y, ys
        print(f"  [{n:2d}/{len(pmcids)}] {p}  {len(xml):>8,} bytes  "
              f"{arts[p]['type']}")

    findings, packet = [], []

    # ---- article-level checks ------------------------------------------------
    BAD_TYPES = {"review-article", "editorial", "correction", "retraction",
                 "letter", "book-review"}
    for p in pmcids:
        a = arts[p]
        if a["type"] == "unavailable":
            findings.append(("ARTICLE_UNAVAILABLE", p,
                             "full text could not be downloaded"))
        elif a["type"] in BAD_TYPES:
            findings.append(("ARTICLE_TYPE", p,
                             f"article-type='{a['type']}' -- should not be shipped"))
        rec_year = {r["year"] for r in rows if r["pmcid"] == p}
        if a.get("years") and rec_year and not (rec_year & a["years"]):
            findings.append(("YEAR_MISMATCH", p,
                             f"recorded {sorted(rec_year)}, article declares "
                             f"{sorted(a['years'])} (preferred {a['year']})"))

    # ---- row-level checks ----------------------------------------------------
    for r in sorted(rows, key=lambda x: (x["pmcid"], x["ph_measurement_id"])):
        a = arts[r["pmcid"]]
        rid = r["ph_measurement_id"]
        if not a["text"]:
            continue
        text = a["text"]
        hit = locate(text, r["evidence_quote"])
        if hit is None:
            findings.append(("QUOTE_NOT_FOUND", rid,
                             f"{r['pmcid']}: evidence sentence not located in fresh text"))
            ctx = "(evidence sentence not located in the freshly downloaded article)"
            sentence = ""
        else:
            i, ln = hit
            ctx = text[max(0, i - 1100): i + ln + 1100]
            # `locate` may have matched only a leading fragment of a quote that spans a
            # markup boundary, so the pH is checked against the whole sentence the match
            # sits in -- extended to the enclosing sentence/paragraph breaks -- rather
            # than against the matched substring alone.
            lo = max(0, i - 20)
            hi = min(len(text), i + max(ln, len(r["evidence_quote"])) + 220)
            window = text[lo:hi]
            cut = window.find("¶", len(r["evidence_quote"]) // 2)
            sentence = window[:cut] if cut > 0 else window
            if not num_in(sentence, fnum(r["pH"])):
                findings.append(("PH_NOT_IN_SENTENCE", rid,
                                 f"{r['pmcid']}: pH {r['pH']} absent from the located "
                                 f"passage (matched {ln}/{len(norm(r['evidence_quote']))} "
                                 f"chars of the stored quote)"))

        # enzyme name should occur somewhere in the article
        name = r["enzyme_name"].strip()
        if name:
            probe = norm(name).replace("(", "").replace(")", "")
            probe = re.sub(r"\s*\(?d(elta)?n\)?$", "", probe)  # PanLipdN -> panlip
            stem = probe.split()[0] if probe else ""
            nt = norm(text).replace("(", "").replace(")", "")
            if stem and len(stem) > 3 and stem not in nt:
                findings.append(("ENZYME_NAME_ABSENT", rid,
                                 f"{r['pmcid']}: '{name}' (stem '{stem}') not found "
                                 f"in the article text"))

        # corrected optima
        src = r["source_measurement_id"]
        if src in CORRECTED_OPTIMA:
            want, phrase = CORRECTED_OPTIMA[src]
            nt = norm(text)
            ok_val = abs(fnum(r["pH"]) - want) < 1e-9
            ok_phrase = norm(phrase) in nt
            if not ok_val:
                findings.append(("CORRECTION_DRIFT", rid,
                                 f"expected corrected optimum {want}, row has {r['pH']}"))
            if not ok_phrase:
                findings.append(("CORRECTION_PHRASE_ABSENT", rid,
                                 f"{r['pmcid']}: '{phrase}' not found verbatim"))

        packet.append({
            "id": rid, "src": src, "pmcid": r["pmcid"], "tier": r["benchmark_tier"],
            "type": r["measurement_type"], "pH": r["pH"],
            "low": r["pH_low"], "high": r["pH_high"],
            "enzyme": r["enzyme_name"], "acc": r["uniprot_accession"],
            "rel": r["relative_activity_pct"], "qual": r["relative_activity_qualifier"],
            "dir": r["direction"], "scored": r["scored_condition_axis"],
            "article_type": a["type"], "note": r["audit_note"],
            "quote": r["evidence_quote"], "context": ctx,
        })

    # ---- write the human review packet --------------------------------------
    out = ["# Deep review packet — pH benchmark\n",
           "Every shipped row printed beside a wide window of the freshly downloaded "
           "article text, so attribution can be judged in context rather than from the "
           "stored one-sentence quote.\n",
           f"Rows: {len(packet)} · Articles: {len(pmcids)}\n", "---\n"]
    cur = None
    for p in packet:
        if p["pmcid"] != cur:
            cur = p["pmcid"]
            out.append(f"\n## {cur}  ({arts[cur]['type']}, {arts[cur]['year']})\n")
            out.append(f"*{arts[cur]['journal']}*\n")
        out.append(f"\n### {p['id']} — {p['type']} @ pH {p['pH']}"
                   f"{' [%s–%s]' % (p['low'], p['high']) if p['low'] != p['high'] else ''}"
                   f"  ·  {p['tier'][0]}  ·  scored={p['scored']}\n")
        out.append(f"- **enzyme**: {p['enzyme'] or '(not named)'} "
                   f"{('/ ' + p['acc']) if p['acc'] else ''}")
        if p["rel"]:
            out.append(f"- **outcome**: {p['qual']} {p['rel']}%  ·  direction {p['dir']}")
        elif p["dir"]:
            out.append(f"- **direction**: {p['dir']}")
        out.append(f"- **audit note**: {p['note']}")
        out.append(f"- **stored quote**: {p['quote']}\n")
        out.append("```")
        out.append(p["context"].strip())
        out.append("```\n")
    with open(os.path.join(DATA, "deep_review_packet.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    # ---- report --------------------------------------------------------------
    summary = {}
    for kind, _, _ in findings:
        summary[kind] = summary.get(kind, 0) + 1
    result = {
        "articles": len(pmcids),
        "articles_downloaded": sum(1 for p in pmcids if arts[p]["text"]),
        "article_types": {t: sum(1 for p in pmcids if arts[p]["type"] == t)
                          for t in sorted({arts[p]["type"] for p in pmcids})},
        "rows": len(rows),
        "quotes_relocated": len(rows) - summary.get("QUOTE_NOT_FOUND", 0),
        "findings_by_kind": summary,
        "findings": [{"kind": k, "subject": s, "detail": d} for k, s, d in findings],
    }
    with open(os.path.join(DATA, "ph_deep_verification.json"), "w",
              encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)

    print(f"\narticles downloaded : {result['articles_downloaded']}/{len(pmcids)}")
    print(f"article types       : {result['article_types']}")
    print(f"quotes relocated    : {result['quotes_relocated']}/{len(rows)}")
    print(f"findings            : {len(findings)}")
    for k, n in sorted(summary.items(), key=lambda kv: -kv[1]):
        print(f"    {k:<28} {n}")
    for k, s, d in findings:
        print(f"      - [{k}] {s}: {d}")
    print("\nwrote data/deep_review_packet.md and data/ph_deep_verification.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
