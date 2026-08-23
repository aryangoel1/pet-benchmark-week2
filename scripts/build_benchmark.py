#!/usr/bin/env python3
"""Standardize units, attach sequences, and assemble the benchmark table.

Input : data/bench_rows.json (mined), data/sequences.json (resolved)
Output: data/bench_std.json  (one dict per row, canonical schema)

Rules kept from week 1 and enforced harder here:
  - a field the source did not state is left EMPTY, never defaulted
  - ionic strength that this script COMPUTES is labelled 'computed from ...'
    and never presented as a reported value
  - a row with no numeric value and no unit is dropped, not padded
"""
import hashlib, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standardize_units as U

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_ROWS = os.path.join(ROOT, "data", "bench_rows.json")
IN_SEQ = os.path.join(ROOT, "data", "sequences.json")
OUT = os.path.join(ROOT, "data", "bench_std.json")

# A benchmark must contain measurements the article ITSELF made. Two kinds of row
# fail that test and are removed here:
#   * rows from reviews/editorials — they restate results obtained elsewhere, which
#     means the "new" measurement is very likely already inside a training set,
#     laundered through a secondary source and no longer traceable to its conditions
#   * prose rows whose evidence sentence cites another paper for the number
# Data tables inside research articles are the article's own results and are kept.
SECONDARY_ARTICLE = {"review-article", "systematic-review", "editorial", "correction",
                     "letter", "book-review", "abstract", "other"}
CITES_OTHERS = re.compile(r"\[\d+(?:\s*[,\-–]\s*\d+)*\]|\bet al\.|\(\s*\d{4}\s*\)|"
                          r"\bref(?:erence)?s?\.?\s*\d|\bpreviously reported\b|"
                          r"\bhas been (?:reported|shown)\b|\bwas reported (?:by|to)\b", re.I)

PLASTIC_SUBSTRATE = re.compile(
    r"PET|terephthalate|BHET|MHET|polyester|polycaprolactone|PCL|PBAT|PLA|polylactic|"
    r"PHB|hydroxybutyrate|polyhydroxyalkanoate|nylon|polyamide|polyurethane|Impranil|"
    r"polyethylene|polystyrene|polybutylene|cutin", re.I)
PLASTIC_ENZYME = re.compile(
    r"PETase|MHETase|cutinase|LCC|TfCut|Cut190|polyester hydrolase|polyesterase|"
    r"depolymerase|PE-?H|Bhr|ICCG|DuraPETase|FAST-?PETase|HotPETase|TurboPETase", re.I)

# The benchmark is about PLASTIC-degrading enzyme performance. The wide queries also
# pulled in hydrolases with no plastic relevance at all (chitosanase, endolysin,
# beta-glucosidase, rhamnosidase). Their temperature/pH/salt numbers are real, but they
# are not what this benchmark is for, and shipping them would inflate it with off-target
# proteins. They are kept only when the row itself names a plastic substrate.
OFF_TARGET = re.compile(
    r"chitosanase|chitinase|endolysin|lysozyme|glucosidase|glucanase|amylase|cellulase|"
    r"xylanase|rhamnosidase|pectinase|invertase|catalase|urease|nuclease|phosphatase|"
    r"galactosidase|mannanase|inulinase|phytase|tannase|keratinase|collagenase|"
    r"aminopeptidase|carboxypeptidase|dehydrogenase|reductase|transferase|isomerase|"
    r"kinase|synthase|ligase|topoisomerase|polymerase", re.I)
ON_TARGET = re.compile(
    r"PETase|MHETase|cutinase|polyester\s*hydrolase|polyesterase|depolymerase|"
    r"carboxylesterase|\besterase\b|\blipase\b|alpha/beta\s*hydrolase|"
    r"LCC|TfCut|Cut190|arylesterase|acylhydrolase|GDSL", re.I)

# A reference marker stripped of its <xref> markup glues onto the number it follows
# ("pH 4.5" + ref 52 -> "4.552"). Physical pH and temperature are never reported to
# three decimals, so that precision is the signature of the corruption, not a real value.
def precision_ok(raw, max_decimals=2):
    m = re.search(r"\d+\.(\d+)", str(raw or ""))
    return not m or len(m.group(1)) <= max_decimals


# A Methods sentence states what the experimenters DID, not what they found. Reading
# "activity was measured in buffers at pH 4.0-6.0" as a pH optimum of 4.0 records the
# assay design as if it were a result. Prose rows must therefore carry outcome language,
# not just design language, to be treated as a measurement. Table cells are exempt —
# a data table is a result by construction.
DESIGN_LANG = re.compile(
    r"\bwas (?:assessed|evaluated|determined|studied|measured|identified|examined|"
    r"investigated|performed|conducted|carried out)\b|"
    r"\bwere (?:assessed|evaluated|determined|studied|measured|performed|conducted|"
    r"carried out|incubated|tested)\b|"
    r"\bto (?:determine|assess|evaluate|examine|investigate|test)\b|"
    r"\b(?:various|different|a range of|ranging from)\b.*\b(?:pH|temperature|buffer|concentration)|"
    r"\bassay was performed\b|\bscreening assay\b", re.I)
OUTCOME_LANG = re.compile(
    r"\b(?:optimum|optimal|maximum|maximal|highest|peak|most active)\b[^.]{0,70}?"
    r"\b(?:was|were|at|of|occurred|observed|found|obtained|is)\b|"
    r"\b(?:showed|exhibited|displayed|retained|maintained|reached|lost|decreased|"
    r"increased|dropped|remained)\b", re.I)

JUNK_NAME = re.compile(r"^\s*(?:none|control|blank|nd|n\.?a\.?|-+|total|mean|average|buffer|"
                       r"substrate|enzyme|protein|sample|\d+(?:\.\d+)?)\s*$", re.I)


# genus names that actually appear as enzyme sources in this literature; used only to
# detect a conflict, never to assign anything
GENUS_HINTS = {"Ideonella", "Thermobifida", "Humicola", "Fusarium", "Bacillus", "Pseudomonas",
               "Streptomyces", "Aspergillus", "Candida", "Halomonas", "Microbulbifer",
               "Lysinibacillus", "Geobacillus", "Rhodococcus", "Saccharomonospora",
               "Thermomonospora", "Piscinibacter", "Clostridium", "Comamonas", "Paenibacillus",
               "Alcaligenes", "Burkholderia", "Acinetobacter", "Vibrio", "Marinobacter",
               "Halobacterium", "Haloferax", "Pseudideonella", "Thermus", "Sulfolobus",
               "Escherichia", "Staphylococcus", "Serratia", "Enterobacter", "Klebsiella"}


def relevance(row):
    blob = f"{row.get('enzyme_name','')} {row.get('substrate','')} {row.get('paper_title','')}"
    if PLASTIC_ENZYME.search(blob) or PLASTIC_SUBSTRATE.search(row.get("substrate", "") or ""):
        return "direct_plastic_degrader"
    if PLASTIC_SUBSTRATE.search(blob):
        return "plastic_context_hydrolase"
    return "related_hydrolase"


def main():
    rows = json.load(open(IN_ROWS))
    at_path = os.path.join(ROOT, "data", "article_types.json")
    article_type = json.load(open(at_path)) if os.path.exists(at_path) else {}
    pr_path = os.path.join(ROOT, "data", "paper_relevance.json")
    paper_rel = json.load(open(pr_path)) if os.path.exists(pr_path) else {}
    pm_path = os.path.join(ROOT, "data", "paper_methods.json")
    paper_meth = json.load(open(pm_path)) if os.path.exists(pm_path) else {}
    seqs = json.load(open(IN_SEQ))
    by_acc, by_name = seqs["by_accession"], seqs["by_name"]
    p2 = os.path.join(ROOT, "data", "sequences_by_paper.json")
    second = json.load(open(p2)) if os.path.exists(p2) else {"by_paper": {}, "by_genbank": {}}
    by_paper, by_gb = second["by_paper"], second["by_genbank"]
    p3 = os.path.join(ROOT, "data", "sequences_rescan.json")
    third = json.load(open(p3)) if os.path.exists(p3) else {"uniprot": {}, "genbank": {}, "per_paper": {}}
    rs_u, rs_g, rs_paper = third["uniprot"], third["genbank"], third["per_paper"]
    print(f"{len(rows)} mined rows; {len(by_acc)} accession entries, {len(by_name)} name entries, "
          f"{len(by_paper)} paper cross-refs, {len(by_gb)} GenBank entries, "
          f"{len(rs_u)}+{len(rs_g)} deposit-section entries", file=sys.stderr)

    out, dropped = [], collections.Counter()
    for i, r in enumerate(rows, 1):
        # ---------------- value must exist and be numeric or an explicit direction
        val_raw = (r.get("value_raw") or "").strip()
        if not val_raw:
            dropped["no_value"] += 1
            continue

        # Some characterisation tables put the TREATMENT LEVEL in the cell the header
        # calls "residual activity" (e.g. "Residual activity (%) = 10 mM"). The number
        # is then a concentration, not an activity, and must not be recorded as one.
        q = r.get("evidence_quote", "")
        if r.get("measurement_type") in ("relative activity", "salt effect", "inhibition"):
            mcell = re.search(r"(?:residual|relative|remaining)\s*activity[^=|]*=\s*([^|]+)", q, re.I)
            if mcell and re.search(r"\d\s*(?:mM|M|mg/mL|g/L|%\s*\((?:v/v|w/v)\))\b",
                                   mcell.group(1), re.I):
                dropped["activity_cell_holds_a_concentration"] += 1
                continue

        # ---- primary-source gate -------------------------------------------
        atype = article_type.get(r.get("pmcid") or "", "")
        if atype in SECONDARY_ARTICLE:
            dropped[f"secondary_source_{atype}"] += 1
            continue
        if r.get("section") != "table" and CITES_OTHERS.search(r.get("evidence_quote", "")):
            dropped["value_attributed_to_another_paper"] += 1
            continue

        # ---- an electrolyte row must report an ACTIVITY OUTCOME --------------
        # "crystallization buffer (10 mM Tris, pH 7.4, 10 mM NaCl)" and "medium containing
        # NaCl 5 g/L" name a recipe. They were becoming salt-effect rows whose "value" was
        # just the concentration, with nothing measured. A salt/salinity/ionic-strength row
        # is only a measurement when the source says what happened to activity.
        if r.get("measurement_type") in ("salt effect", "salinity effect", "ionic strength effect"):
            has_outcome = (r.get("relative_activity_pct") is not None
                           or str(r.get("value_unit_raw", "")).startswith("%"))
            if not has_outcome and r.get("section") != "table":
                q = r.get("evidence_quote", "")
                if not re.search(r"\b(?:activity|activities)\b[^.]{0,80}?"
                                 r"\b(?:increas|decreas|declin|reduc|enhanc|stimulat|inhibit|"
                                 r"lost|retain|remain|drop|improv|suppress|abolish|peak|maxim)",
                                 q, re.I) and not re.search(
                                 r"\b(?:increas|decreas|declin|reduc|enhanc|stimulat|inhibit|"
                                 r"lost|retain|remain|drop|improv|suppress|abolish|peak|maxim)"
                                 r"[^.]{0,80}?\b(?:activity|activities)\b", q, re.I):
                    dropped["electrolyte_row_with_no_activity_outcome"] += 1
                    continue

        # ---- methods-vs-results gate ---------------------------------------
        if r.get("section") != "table":
            q = r.get("evidence_quote", "")
            if DESIGN_LANG.search(q) and not OUTCOME_LANG.search(q):
                dropped["experimental_design_not_a_result"] += 1
                continue

        # ---- corrupted-precision gate --------------------------------------
        if not precision_ok(r.get("pH")) or not precision_ok(r.get("temperature_c")):
            dropped["value_precision_implies_glued_reference_marker"] += 1
            continue

        # ---- on-target gate -------------------------------------------------
        blob = " ".join(str(r.get(k, "") or "") for k in
                        ("enzyme_name", "evidence_quote", "paper_title"))
        if OFF_TARGET.search(blob) and not ON_TARGET.search(blob) \
                and not PLASTIC_SUBSTRATE.search(str(r.get("substrate", "") or "")):
            dropped["off_target_enzyme_class"] += 1
            continue

        # Content-addressed, NOT positional. A row's id is derived from what the row says,
        # so it survives a rebuild that adds or drops other rows. Index-based ids silently
        # reshuffle on every change, which invalidates anything that references them —
        # the manual-review exclusion list most of all.
        fingerprint = "|".join(str(r.get(k, "")) for k in
                               ("pmcid", "measurement_type", "value_raw", "value_unit_raw",
                                "ion_species", "salt_species", "additive", "evidence_quote"))
        m = {"measurement_id": "BM" + hashlib.sha1(fingerprint.encode()).hexdigest()[:10].upper()}
        m["enzyme_name"] = "" if JUNK_NAME.match(r.get("enzyme_name") or "") else (r.get("enzyme_name") or "").strip()
        m["mutation"] = r.get("mutation") or "wild-type/unspecified"
        m["is_wild_type"] = "yes" if m["mutation"] == "wild-type/unspecified" else "no"
        m["substrate"] = r.get("substrate", "")
        m["substrate_form"] = r.get("substrate_form", "")

        # ---------------- temperature
        # The task forbids interpolated values, and the midpoint of a reported range is
        # interpolated: a paper that reports "optimal at 45-50 C" never reported 47.5 C.
        # The endpoints are kept as reported and the canonical value is the LOW endpoint,
        # with the span preserved in *_low / *_high and flagged by value_is_range.
        m["temperature_raw"] = r.get("temperature_c", "")
        lo, hi = r.get("temperature_c_low"), r.get("temperature_c_high")
        m["temperature_c"] = "" if lo is None else lo
        if m["temperature_c"] != "" and not U.plausible_temperature(m["temperature_c"]):
            m["temperature_c"] = ""
        m["temperature_c_low"], m["temperature_c_high"] = ("" if lo is None else lo), ("" if hi is None else hi)

        # ---------------- pH
        m["pH_raw"] = r.get("pH", "")
        plo, phi = r.get("pH_low"), r.get("pH_high")
        m["pH"] = "" if plo is None else plo
        if m["pH"] != "" and not U.plausible_ph(m["pH"]):
            m["pH"] = ""
        m["pH_low"], m["pH_high"] = ("" if plo is None else plo), ("" if phi is None else phi)

        # ---------------- buffer
        m["buffer_name"] = r.get("buffer_name", "")
        bc = U.buffer_concentration(r.get("evidence_quote", ""))
        m["buffer_conc_mM"] = bc if bc is not None else ""

        # ---------------- electrolyte
        m["salt_species"] = r.get("salt_species", "")
        m["ion_species"] = r.get("ion_species", "")
        m["ion_charge"] = r.get("ion_charge", "")
        m["salt_conc_raw"] = r.get("conc_raw", "")
        cval, cunit, cmM = U.parse_concentration(r.get("conc_raw", ""), m["salt_species"])
        m["salt_conc_mM"] = cmM if cmM is not None else ""

        comps = re.findall(r"\b(NaCl|KCl|CaCl2|MgCl2|MgSO4|MnCl2|ZnSO4|CuSO4|FeCl3|FeSO4|"
                           r"CoCl2|NiCl2|LiCl|BaCl2|Na2SO4|NH4Cl)\b", r.get("evidence_quote", ""))
        uniq = sorted(set(comps))
        m["mixed_electrolyte"] = "yes" if len(uniq) > 1 else ("no" if uniq else "")
        m["electrolyte_composition"] = "+".join(uniq)

        m["salinity_raw"] = r.get("salinity_raw", "")
        gpl, psu = U.parse_salinity(r.get("salinity_raw", ""))
        m["salinity_g_per_L"] = gpl if gpl is not None else ""
        m["salinity_psu"] = psu if psu is not None else ""
        m["seawater_type"] = r.get("seawater_type", "")

        # ionic strength: reported if the paper stated it, else COMPUTED and labelled
        istr = U.parse_ionic_strength(r.get("ionic_strength_raw", ""))
        if istr is not None:
            m["ionic_strength_M"], m["ionic_strength_source"] = istr, "reported in source"
        elif m["salt_species"] and m["salt_conc_mM"] != "":
            c = U.ionic_strength_from_salt(m["salt_species"], m["salt_conc_mM"])
            m["ionic_strength_M"] = c if c is not None else ""
            m["ionic_strength_source"] = (f"computed from {m['salt_conc_mM']} mM {m['salt_species']}"
                                          if c is not None else "")
        elif gpl is not None:
            c = U.ionic_strength_from_salinity(gpl)
            m["ionic_strength_M"] = c if c is not None else ""
            m["ionic_strength_source"] = (f"computed from salinity {gpl} g/L (seawater ion ratios)"
                                          if c is not None else "")
        else:
            m["ionic_strength_M"], m["ionic_strength_source"] = "", ""

        m["additive"] = r.get("additive", "")
        m["additive_conc_mM"] = cmM if (m["additive"] and not m["salt_species"] and cmM is not None) else ""

        # ---------------- time / assay
        m["exposure_time_raw"] = r.get("exposure_time_raw", "")
        tmin = U.parse_time(r.get("exposure_time_raw", ""))
        m["exposure_time_min"] = tmin if tmin is not None else ""
        # The assay is stated once in Methods and then used for the whole article, so it
        # is recovered at article level when the row itself does not name one. The scope is
        # recorded so a paper-level method is never mistaken for one stated on the row.
        m["assay_method"] = r.get("assay_method", "")
        m["assay_method_scope"] = "row" if m["assay_method"] else ""
        pm = paper_meth.get(r.get("pmcid") or "", {})
        if not m["assay_method"] and pm.get("assay"):
            m["assay_method"] = pm["assay"]
            m["assay_method_scope"] = "paper-level (from Methods section)"
        if not m["substrate"] and pm.get("substrate"):
            m["substrate"] = pm["substrate"]
            m["substrate_scope"] = "paper-level (from Methods section)"
        else:
            m["substrate_scope"] = "row" if m["substrate"] else ""

        # ---------------- value
        m["measurement_type"] = r.get("measurement_type", "")
        m["value_raw"] = val_raw
        m["value_unit_raw"] = r.get("value_unit_raw", "")
        m["value_is_range"] = "yes" if (
            (lo is not None and hi is not None and lo != hi)
            or (plo is not None and phi is not None and plo != phi)) else "no"
        m["value_std_high"] = ""
        m["relative_activity_pct"] = r.get("relative_activity_pct") if r.get("relative_activity_pct") is not None else ""
        m["direction"] = r.get("direction", "")
        m["kinetic_param"] = r.get("kinetic_param", "")

        vnum = re.match(r"^\s*(-?\d+(?:\.\d+)?)", val_raw)
        vnum = float(vnum.group(1)) if vnum else None
        mt = m["measurement_type"]
        if mt in ("temperature optimum", "thermostability") and m["temperature_c"] != "":
            m["value_std"], m["value_unit_std"] = m["temperature_c"], "degrees Celsius"
            m["value_std_high"] = m["temperature_c_high"] if m["value_is_range"] == "yes" else ""
        elif mt in ("pH optimum", "pH stability") and m["pH"] != "":
            m["value_std"], m["value_unit_std"] = m["pH"], "pH"
            m["value_std_high"] = m["pH_high"] if m["value_is_range"] == "yes" else ""
        elif m["relative_activity_pct"] != "":
            m["value_std"], m["value_unit_std"] = m["relative_activity_pct"], "% relative activity"
        elif mt == "kinetic constant" and vnum is not None:
            kp = m["kinetic_param"]
            if kp == "KM":
                conv = U.km_to_mM(vnum, m["value_unit_raw"])
                m["value_std"], m["value_unit_std"] = (conv, "mM") if conv is not None else (vnum, m["value_unit_raw"])
            elif kp == "kcat":
                conv = U.kcat_to_per_s(vnum, m["value_unit_raw"])
                m["value_std"], m["value_unit_std"] = (conv, "s^-1") if conv is not None else (vnum, m["value_unit_raw"])
            else:
                m["value_std"], m["value_unit_std"] = vnum, m["value_unit_raw"] or "as reported"
        elif vnum is not None:
            m["value_std"], m["value_unit_std"] = vnum, m["value_unit_raw"] or "as reported"
        else:
            m["value_std"], m["value_unit_std"] = val_raw, m["value_unit_raw"] or "qualitative"

        if m["value_std"] == "" or m["value_std"] is None:
            dropped["no_standardized_value"] += 1
            continue
        # A benchmark scores a model against numbers. A row whose only content is a
        # direction ("inhibition") cannot do that, so it is not shipped.
        if m["value_unit_std"] == "qualitative":
            dropped["qualitative_no_numeric_value"] += 1
            continue

        # ---------------- sequence resolution
        #
        # An accession printed in an article only identifies THIS row's enzyme when
        # the article names exactly one hydrolase-class accession. Papers that
        # characterise several enzymes would otherwise have every row tagged with
        # whichever accession happened to be listed first, which is how a benchmark
        # silently acquires wrong labels. When the article is ambiguous, the enzyme
        # NAME on the row has to do the work, and if it cannot, the row stays
        # unresolved rather than guessed.
        acc_rec, how = None, "unresolved"
        paper_accs = [a for a in (r.get("uniprot_in_text") or "").split(";") if a and a in by_acc]
        if len(paper_accs) == 1:
            acc_rec, how = by_acc[paper_accs[0]], "accession_unique_in_article"
        elif len(paper_accs) > 1 and m["enzyme_name"]:
            # accept only if the row's enzyme name matches exactly one of them
            nm = m["enzyme_name"].lower()
            hits = [a for a in paper_accs
                    if nm in (by_acc[a]["protein_name"] or "").lower()
                    or nm in (by_acc[a]["entry_name"] or "").lower()]
            if len(hits) == 1:
                acc_rec, how = by_acc[hits[0]], "accession_matched_by_enzyme_name"
        # UniProt curators link entries to the paper that characterised them; when a
        # paper links to exactly one hydrolase entry, that is a curated assertion
        # about THIS article's enzyme, which beats any name matching.
        if acc_rec is None and r.get("pmcid") in by_paper:
            acc_rec, how = by_paper[r["pmcid"]], "uniprot_pubmed_crossref"
        # accessions printed in the article's deposit / data-availability context.
        # Same discipline as above: accepted only when the article names exactly one
        # hydrolase record of that kind, so multi-enzyme papers cannot mislabel rows.
        if acc_rec is None:
            scan = rs_paper.get(r.get("pmcid") or "", {})
            hits_u = [a for a in scan.get("uniprot", []) if a in rs_u]
            hits_g = [a for a in scan.get("genbank", []) if a in rs_g]
            if len(hits_u) == 1:
                acc_rec, how = rs_u[hits_u[0]], "uniprot_deposit_section_unique"
            elif len(hits_g) == 1:
                acc_rec, how = rs_g[hits_g[0]], "genbank_deposit_section_unique"
            elif m["enzyme_name"] and len(m["enzyme_name"]) >= 3:
                # An article that deposits several hydrolases can still be resolved when
                # the row names its enzyme and that name picks out exactly ONE of them
                # ("Est30" -> "thermostable carboxylesterase Est30"). Requiring exactly
                # one match keeps the multi-enzyme papers from mislabelling rows; a name
                # that matches two candidates is still refused.
                nm = m["enzyme_name"].lower()
                pool = [(a, rs_u[a], "uniprot") for a in hits_u] + \
                       [(a, rs_g[a], "genbank") for a in hits_g]
                named = [(a, rec, kind) for a, rec, kind in pool
                         if nm in (rec.get("protein_name") or "").lower()
                         or nm in (rec.get("entry_name") or "").lower()
                         or nm == (rec.get("accession") or "").split(".")[0].lower()]
                if len(named) == 1:
                    acc_rec = named[0][1]
                    how = f"{named[0][2]}_disambiguated_by_enzyme_name"
        if acc_rec is None:
            gbs = [g for g in (r.get("genbank_in_text") or "").split(";") if g and g in by_gb]
            if len(gbs) == 1:
                acc_rec, how = by_gb[gbs[0]], "genbank_unique_in_article"
        if acc_rec is None and m["enzyme_name"] and m["enzyme_name"] in by_name:
            acc_rec, how = by_name[m["enzyme_name"]], "name_lookup"
        # A table row that names its own organism must agree with the accession the
        # article-level resolution picked, or the row belongs to a different enzyme and
        # the attribution is dropped rather than shipped wrong.
        if acc_rec and r.get("section") == "table":
            org_genus = (acc_rec.get("organism") or "").split()[:1]
            quote_genera = set(re.findall(r"\b([A-Z][a-z]{4,})\s+[a-z]{3,}\b",
                                          r.get("evidence_quote", "")))
            known = {g for g in quote_genera if g in GENUS_HINTS}
            if org_genus and known and org_genus[0] not in known:
                acc_rec, how = None, "unresolved_organism_conflict"

        m["uniprot_accession"] = acc_rec["accession"] if acc_rec else ""
        m["sequence"] = acc_rec["sequence"] if acc_rec else ""
        m["sequence_length"] = acc_rec["length"] if acc_rec else ""
        m["organism"] = acc_rec["organism"] if acc_rec else ""
        m["ec_number"] = acc_rec["ec"] if acc_rec else ""
        m["uniprot_protein_name"] = acc_rec["protein_name"] if acc_rec else ""
        m["reviewed_status_uniprot"] = acc_rec["reviewed"] if acc_rec else ""
        m["sequence_resolution"] = how

        # ---------------- provenance
        m["plastic_relevance"] = relevance(r)
        # This benchmark tests a PLASTIC-degradation screener. A row whose enzyme, whose
        # substrate and whose article title never mention a plastic or a polyester-active
        # enzyme is not what the model is being tested on — that bucket is where the
        # carbonic anhydrases, endolysins and drug-release papers ended up. It is dropped
        # rather than shipped as filler.
        # Relevance is judged from the ARTICLE's full text, not its title: a paper called
        # "a novel esterase from a soil metagenomic library" that assays PCL and PET films
        # throughout its results is on-topic, and its title never says so. A row is kept
        # when the row itself is plastic-linked OR its article sustains a named polymer.
        if m["plastic_relevance"] == "related_hydrolase" and \
                not paper_rel.get(r.get("pmcid") or "", {}).get("relevant"):
            dropped["no_plastic_relevance"] += 1
            continue
        if m["plastic_relevance"] == "related_hydrolase":
            m["plastic_relevance"] = "plastic_relevant_article"
        m["source_db"] = r.get("source_db", "")
        m["source_type"] = r.get("source_type", "")
        m["pmcid"] = r.get("pmcid", "")
        m["pubmed_id"] = r.get("pubmed_id", "")
        m["doi"] = r.get("doi", "")
        m["paper_title"] = r.get("paper_title", "")
        m["journal"] = r.get("journal", "")
        m["year"] = r.get("year", "")
        m["search_axis"] = r.get("axis", "")
        m["section"] = r.get("section", "")
        m["evidence_quote"] = r.get("evidence_quote", "")
        m["pdb_in_text"] = r.get("pdb_in_text", "")
        m["data_origin"] = "experimental measurement reported in a peer-reviewed open-access article"

        # confidence: what the row can actually support
        score = 0
        score += (2 if (how.startswith("accession_") or "unique" in how or "crossref" in how)
                  else 1 if how == "name_lookup" else 0)
        score += 1 if m["section"] == "table" else 0
        score += 1 if (m["temperature_c"] != "" and m["pH"] != "") else 0
        score += 1 if (m["ion_species"] or m["salt_species"] or m["salinity_raw"] or m["ionic_strength_M"] != "") else 0
        score += 1 if m["buffer_name"] else 0
        m["confidence"] = "High" if score >= 4 else "Medium-High" if score >= 3 else "Medium" if score >= 2 else "Low"
        out.append(m)

    print(f"\nStandardized {len(out)} rows (dropped: {dict(dropped)})", file=sys.stderr)
    for k in ("measurement_type", "sequence_resolution", "plastic_relevance", "confidence"):
        print(f"-- {k}: {collections.Counter(x[k] for x in out).most_common(10)}", file=sys.stderr)
    print(f"   with sequence: {sum(1 for x in out if x['sequence'])}", file=sys.stderr)
    print(f"   with T and pH: {sum(1 for x in out if x['temperature_c'] != '' and x['pH'] != '')}", file=sys.stderr)
    print(f"   with electrolyte: {sum(1 for x in out if x['ion_species'] or x['salt_species'] or x['salinity_raw'] or x['ionic_strength_M'] != '')}", file=sys.stderr)
    json.dump(out, open(OUT, "w"))
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
