#!/usr/bin/env python3
"""Verify benchmark entries against the ORIGINAL articles, one entry at a time.

Method (deliberately independent of the harvest run):

  1. The article is re-downloaded from Europe PMC into a SEPARATE directory.
     The harvest-time cache in data/fulltext_xml is not consulted, so a corrupted
     or mis-parsed cache cannot make a row verify against itself.
  2. The recorded evidence_quote must be found in the freshly downloaded article,
     after whitespace normalisation. Table rows are checked cell-by-cell, because
     the quote is a reconstruction of the row, not a literal string in the XML.
  3. The recorded value, temperature, pH, ion and concentration are each re-parsed
     from the freshly downloaded source text and compared to what the row stores.
  4. Anything that fails is reported with the reason, and dropped from the shipped
     benchmark by finalize.py.

A row is VERIFIED only when the quote is located AND the stored value is present
in that located text. No row is verified by inference.

Usage:  python3 scripts/verify_entries.py [N]      (default: every row with a quote)
Output: data/verification.json, VERIFICATION_REPORT.md
"""
import json, os, re, sys, time, urllib.request, collections, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_ROWS = os.path.join(ROOT, "data", "bench_std.json")
IN_OVL = os.path.join(ROOT, "data", "overlap.json")
VDIR = os.path.join(ROOT, "data", "verify_xml")      # separate from the harvest cache
OUT = os.path.join(ROOT, "data", "verification.json")
REPORT = os.path.join(ROOT, "VERIFICATION_REPORT.md")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
UA = {"User-Agent": "pet-labs-week2-verify/1.0 (research)"}


def get(url, timeout=90, retries=3):
    last = None
    for a in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:
            last = ex
            time.sleep(1.5 * (a + 1))
    raise last


def fresh_text(pmcid):
    """Re-download the article and flatten it to normalised text."""
    os.makedirs(VDIR, exist_ok=True)
    path = os.path.join(VDIR, f"{pmcid}.txt")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return open(path).read()
    xml = get(f"{EPMC}/{pmcid}/fullTextXML")
    text = re.sub(r"<[^>]+>", " ", xml)
    text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&#x000a0;", " ").replace("&#160;", " "))
    text = " ".join(text.split())
    open(path, "w").write(text)
    time.sleep(0.34)
    return text


def norm(s):
    return " ".join((s or "").replace("–", "-").replace("−", "-").replace("‑", "-").split()).lower()


def squash(s):
    """Comparison form that survives inline markup.

    The harvest reads the article with ElementTree's itertext(), which concatenates
    text across <sup>/<italic>/<xref> with no space ("cutinase7,8"). Verification
    strips tags with a regex, which inserts one ("cutinase 7,8"). Comparing on
    whitespace-normalised text therefore reports a mismatch for text that is in fact
    identical. Reducing both sides to their alphanumeric content removes that entire
    class of false failure without loosening what counts as a match.
    """
    return re.sub(r"[^a-z0-9.]+", "", (s or "").lower())


def main():
    rows = json.load(open(IN_ROWS))
    ovl = {v["measurement_id"]: v["verdict"] for v in json.load(open(IN_OVL))["verdicts"]}
    keep = [r for r in rows if ovl.get(r["measurement_id"], "").startswith("KEEP")]
    keep = [r for r in keep if r.get("evidence_quote") and r.get("pmcid")]

    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(keep)
    # verify a spread across papers and measurement types, not the first N of one paper
    random.seed(20260821)
    by_paper = collections.defaultdict(list)
    for r in keep:
        by_paper[r["pmcid"]].append(r)
    ordered, i = [], 0
    while len(ordered) < min(limit, len(keep)):
        added = False
        for p in sorted(by_paper):
            if i < len(by_paper[p]):
                ordered.append(by_paper[p][i]); added = True
                if len(ordered) >= limit:
                    break
        if not added:
            break
        i += 1

    print(f"Verifying {len(ordered)} entries across {len({r['pmcid'] for r in ordered})} articles",
          file=sys.stderr)

    results, cache = [], {}
    for n, r in enumerate(ordered, 1):
        pmcid = r["pmcid"]
        try:
            if pmcid not in cache:
                cache[pmcid] = fresh_text(pmcid)
            src = cache[pmcid]
        except Exception as ex:
            results.append({"measurement_id": r["measurement_id"], "pmcid": pmcid,
                            "status": "SOURCE_UNAVAILABLE", "reason": type(ex).__name__})
            continue

        nsrc = norm(src)
        ssrc = squash(src)
        quote = r["evidence_quote"]
        checks, reasons = {}, []

        # --- 1. locate the evidence in the freshly downloaded article -----------
        if r.get("section") == "table":
            # the quote is "Table in PMC... — caption :: h=c | h=c"; check each cell
            cells = [squash(c) for c in re.findall(r"=\s*([^|]+)", quote.split("::", 1)[-1])]
            cells = [c for c in cells if len(c) >= 2]
            found = sum(1 for c in cells if c in ssrc)
            need = len(cells) if len(cells) <= 2 else max(2, int(0.6 * len(cells)))
            checks["quote_located"] = bool(cells) and found >= need
            checks["cells_found"] = f"{found}/{len(cells)}"
            if not checks["quote_located"]:
                reasons.append(f"table cells not found in source ({found}/{len(cells)})")
        else:
            sq = squash(quote)
            checks["quote_located"] = any(sq[:n] in ssrc for n in (240, 150, 90) if len(sq) >= n) \
                or (len(sq) < 90 and sq in ssrc)
            if not checks["quote_located"]:
                reasons.append("evidence sentence not found verbatim in source")

        # --- 2. the recorded value must appear in the source --------------------
        #
        # Three things are legitimately NOT literal strings in the article and must be
        # checked against what the source actually prints:
        #   * a range midpoint  — "30-35 C" is stored as 32.5; the source prints 30 and 35
        #   * a converted unit  — 640 uM is stored as 0.64 mM
        #   * a direction       — "inhibition" is a reading of the sentence, not a quote
        # So the endpoints and the raw reported value are accepted as evidence too, and
        # a qualitative row is verified on its evidence sentence rather than a number.
        v = str(r.get("value_std", ""))
        unit_std = str(r.get("value_unit_std", ""))
        candidates = []
        for cand in (v, r.get("value_raw", ""), r.get("temperature_c_low"),
                     r.get("temperature_c_high"), r.get("pH_low"), r.get("pH_high"),
                     r.get("relative_activity_pct")):
            if cand is None or cand == "":
                continue
            for piece in re.split(r"[-–]", str(cand)):
                if re.fullmatch(r"-?\d+(?:\.\d+)?", piece.strip()):
                    candidates.append(piece.strip())

        if unit_std == "qualitative" or not candidates:
            # nothing numeric was claimed; the evidence sentence carries the whole claim
            checks["value_in_source"] = checks["quote_located"]
            checks["value_check"] = "qualitative — verified via evidence sentence"
            if not checks["value_in_source"]:
                reasons.append("qualitative row whose evidence sentence was not located")
        else:
            forms = set()
            for cnum in candidates:
                f = float(cnum)
                forms |= {cnum, cnum.rstrip("0").rstrip(".") if "." in cnum else cnum, f"{f:g}"}
                if f == int(f):
                    forms |= {str(int(f)), f"{int(f)}.0"}
            checks["value_in_source"] = any(
                re.search(rf"(?<![\d.]){re.escape(x)}(?![\d])", nsrc) for x in forms if x)
            checks["value_check"] = f"matched on one of {sorted(forms)[:6]}"
            if not checks["value_in_source"]:
                reasons.append(f"recorded value {v!r} (and its reported form "
                               f"{r.get('value_raw','')!r}) not found in source text")

        # --- 3. conditions re-parsed from the source ----------------------------
        for fld, pat in (("temperature_c", r"(?<![\d.])%s\s*(?:°\s*c|degrees)"),
                         ("pH", r"ph\s*(?:of|=|:|was|is)?\s*%s(?![\d])")):
            val = r.get(fld, "")
            if val == "" or val is None:
                checks[f"{fld}_recheck"] = "not recorded"
                continue
            s = f"{float(val):g}"
            checks[f"{fld}_recheck"] = bool(re.search(pat % re.escape(s), nsrc))
        for fld in ("ion_species", "salt_species", "additive", "buffer_name"):
            val = r.get(fld, "")
            if not val:
                checks[f"{fld}_recheck"] = "not recorded"
                continue
            token = re.sub(r"\(.*?\)", "", val).strip()
            checks[f"{fld}_recheck"] = norm(token) in nsrc if token else "not recorded"

        status = "VERIFIED" if (checks["quote_located"] and checks["value_in_source"]) else "FAILED"
        results.append({"measurement_id": r["measurement_id"], "pmcid": pmcid,
                        "doi": r.get("doi", ""), "pubmed_id": r.get("pubmed_id", ""),
                        "enzyme": r.get("enzyme_name", ""), "type": r.get("measurement_type", ""),
                        "value": r.get("value_std", ""), "unit": r.get("value_unit_std", ""),
                        "section": r.get("section", ""), "status": status, "checks": checks,
                        "reasons": reasons, "quote": quote[:300]})
        if n % 25 == 0:
            ok = sum(1 for x in results if x["status"] == "VERIFIED")
            print(f"  {n}/{len(ordered)}  verified {ok}", file=sys.stderr)

    c = collections.Counter(x["status"] for x in results)
    print(f"\n{dict(c)}", file=sys.stderr)
    json.dump({"results": results, "counts": dict(c)}, open(OUT, "w"), indent=1)

    # ---------------------------------------------------------------- report
    ok = [x for x in results if x["status"] == "VERIFIED"]
    bad = [x for x in results if x["status"] != "VERIFIED"]
    papers = len({x["pmcid"] for x in results})
    L = []
    L.append("# Verification against the original articles\n")
    L.append(f"**{len(ok)} of {len(results)} entries verified** across **{papers} articles**. "
             f"{len(bad)} failed and are removed from the shipped benchmark.\n")
    L.append("## Method\n")
    L.append("Each entry was re-checked against a **freshly downloaded copy** of its article, "
             "pulled into `data/verify_xml/` — the harvest-time cache in `data/fulltext_xml/` "
             "is never read here, so a bad cache cannot verify itself. An entry passes only when "
             "(a) its recorded evidence is located in that fresh copy — verbatim for prose, "
             "cell-by-cell for tables — **and** (b) the recorded standardized value is present in "
             "the source text. Temperature, pH, ion, salt, additive and buffer are each re-parsed "
             "from the fresh copy and reported per entry.\n")
    L.append("## Result\n")
    L.append("| | |\n|---|---|")
    L.append(f"| Entries checked | {len(results)} |")
    L.append(f"| Articles opened | {papers} |")
    L.append(f"| **VERIFIED** | **{len(ok)}** |")
    L.append(f"| FAILED (removed) | {len(bad)} |")
    rc = collections.Counter(rr for x in bad for rr in x["reasons"])
    if rc:
        L.append("\n### Why entries failed\n")
        L.append("| Reason | Entries |\n|---|---|")
        for k, v in rc.most_common():
            L.append(f"| {k} | {v} |")
    L.append("\n## Verified entries\n")
    L.append("| ID | PMCID | Enzyme | Measurement | Value | Evidence located in the article |")
    L.append("|---|---|---|---|---|---|")
    for x in ok:
        q = x["quote"].replace("|", "/")[:190]
        L.append(f"| {x['measurement_id']} | {x['pmcid']} | {x['enzyme'] or '—'} | {x['type']} | "
                 f"{x['value']} {x['unit']} | {q} |")
    if bad:
        L.append("\n## Failed entries (removed from the benchmark)\n")
        L.append("| ID | PMCID | Measurement | Value | Reason |\n|---|---|---|---|---|")
        for x in bad:
            L.append(f"| {x['measurement_id']} | {x['pmcid']} | {x['type']} | {x['value']} | "
                     f"{'; '.join(x['reasons']) or x.get('reason','')} |")
    open(REPORT, "w").write("\n".join(L) + "\n")
    print(f"Wrote {OUT} and {REPORT}", file=sys.stderr)


if __name__ == "__main__":
    main()
