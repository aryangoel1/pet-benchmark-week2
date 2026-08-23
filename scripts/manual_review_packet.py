#!/usr/bin/env python3
"""Build a human-readable review packet: for a sample of shipped entries, print the
recorded row next to the surrounding text of the ORIGINAL article, so a person can
judge whether the extraction is semantically right — not merely that the number
appears somewhere in the paper.

This is the check the automated verifier cannot do: it catches a correct number
attributed to the wrong enzyme, the wrong condition, or the wrong direction.

Usage: python3 scripts/manual_review_packet.py [N]   (default 40)
Output: MANUAL_REVIEW_PACKET.md
"""
import csv, json, os, re, sys, collections, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
VDIR = D("data", "verify_xml")


def norm(s):
    return " ".join((s or "").replace("–", "-").replace("−", "-").split())


def context(src, needle, width=420):
    n, s = norm(needle).lower(), norm(src)
    low = s.lower()
    for probe in (n[:150], n[:90], n[:50]):
        i = low.find(probe)
        if i >= 0:
            a, b = max(0, i - width // 3), min(len(s), i + len(probe) + width)
            return ("…" if a else "") + s[a:b] + ("…" if b < len(s) else "")
    return ""


def main():
    n_want = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rows = list(csv.DictReader(open(D("pet_benchmark_v2.csv"))))
    rows = [r for r in rows if r["verification"] == "source_verified"]

    # spread the sample over papers, measurement types and both electrolyte/non-electrolyte
    random.seed(20260821)
    buckets = collections.defaultdict(list)
    for r in rows:
        buckets[(r["measurement_type"], bool(r["ion_species"] or r["salt_species"] or r["salinity_raw"]))].append(r)
    for b in buckets.values():
        random.shuffle(b)
    sample, i = [], 0
    while len(sample) < min(n_want, len(rows)):
        added = False
        for k in sorted(buckets, key=str):
            if i < len(buckets[k]):
                sample.append(buckets[k][i]); added = True
                if len(sample) >= n_want:
                    break
        if not added:
            break
        i += 1

    cache = {}
    L = ["# Manual review packet\n",
         f"{len(sample)} shipped entries, spread across measurement types and across "
         "electrolyte / non-electrolyte rows. For each one: what the benchmark records, and the "
         "surrounding text of the original article so the extraction can be judged in context.\n",
         "The automated verifier confirms a value **is present** in the source. This packet is for "
         "confirming the value is **attributed correctly** — right enzyme, right condition, right "
         "direction.\n", "---\n"]
    for k, r in enumerate(sample, 1):
        pmcid = r["pmcid"]
        if pmcid not in cache:
            p = os.path.join(VDIR, f"{pmcid}.txt")
            cache[pmcid] = open(p).read() if os.path.exists(p) else ""
        ctx = context(cache[pmcid], r["evidence_quote"]) if cache[pmcid] else ""
        cond = []
        if r["temperature_c"]: cond.append(f"T = {r['temperature_c']} °C")
        if r["pH"]: cond.append(f"pH = {r['pH']}")
        if r["buffer_name"]: cond.append(f"buffer = {r['buffer_name']}"
                                         + (f" ({r['buffer_conc_mM']} mM)" if r["buffer_conc_mM"] else ""))
        if r["salt_species"]: cond.append(f"salt = {r['salt_species']}"
                                          + (f" @ {r['salt_conc_mM']} mM" if r["salt_conc_mM"] else ""))
        if r["ion_species"]: cond.append(f"ion = {r['ion_species']}")
        if r["salinity_g_per_L"]: cond.append(f"salinity = {r['salinity_g_per_L']} g/L")
        if r["ionic_strength_M"]: cond.append(f"I = {r['ionic_strength_M']} M ({r['ionic_strength_source']})")
        if r["additive"]: cond.append(f"additive = {r['additive']}")
        if r["exposure_time_min"]: cond.append(f"exposure = {r['exposure_time_min']} min")
        L += [f"### {k}. `{r['measurement_id']}` — {r['measurement_type']}\n",
              f"| Field | Recorded |", "|---|---|",
              f"| Enzyme | {r['enzyme_name'] or '—'} |",
              f"| UniProt | {r['uniprot_accession'] or '—'} ({r['sequence_resolution']}) |",
              f"| Organism | {r['organism'] or '—'} |",
              f"| Mutation | {r['mutation']} |",
              f"| Substrate | {r['substrate'] or '—'} |",
              f"| Conditions | {'; '.join(cond) or '—'} |",
              f"| Assay | {r['assay_method'] or '—'} |",
              f"| **Value** | **{r['value_std']} {r['value_unit_std']}** |",
              f"| Tier | {r['benchmark_tier']} |",
              f"| Source | {r['pmcid']} · {r['doi'] or '—'} · {r['journal']} {r['year']} |",
              f"\n**Recorded evidence:** {r['evidence_quote']}\n",
              f"**In the article:** {ctx or '*(context not located — check manually)*'}\n", "---\n"]
    open(D("MANUAL_REVIEW_PACKET.md"), "w").write("\n".join(L) + "\n")
    print(f"Wrote MANUAL_REVIEW_PACKET.md with {len(sample)} entries", file=sys.stderr)


if __name__ == "__main__":
    main()
