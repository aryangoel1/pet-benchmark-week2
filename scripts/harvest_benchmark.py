#!/usr/bin/env python3
"""Harvest NEW experimental measurements from Europe PMC open-access full text.

Week-2 rules that did not apply in week 1:

  1. Any PMCID/PMID already in the exclusion index is skipped BEFORE it is fetched.
     That removes all 199 papers week-1 mined and all 6,941 papers cited by the
     seven shared datasets / Luke's training set.
  2. The query grid is rebuilt around the electrolyte + marine axes and around
     enzyme families week 1 under-covered (PUR/PE/PS/PLA esterases, halophilic
     and marine hydrolases, ionic-liquid tolerance).
  3. Every row must carry a numeric value, a unit, and the verbatim source text.
     Nothing is inferred, defaulted, averaged or interpolated.

Output: data/bench_rows.json, data/bench_papers.json, data/fulltext_xml/*.xml
"""
import json, os, re, sqlite3, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_DIR = os.path.join(ROOT, "data", "fulltext_xml")
EXCL_DB = os.path.join(ROOT, "data", "exclusions.sqlite")
OUT_ROWS = os.path.join(ROOT, "data", "bench_rows.json")
OUT_PAPERS = os.path.join(ROOT, "data", "bench_papers.json")

TARGET_PAPERS = int(os.environ.get("TARGET_PAPERS", "420"))
SKIPPED_TABLES, SKIPPED_SECTIONS, SKIPPED_SENTENCES = [], [], []
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
UA = {"User-Agent": "pet-labs-week2-benchmark/1.0 (research)"}

# ---------------------------------------------------------------- query grid
ENZ_CORE = ('(PETase OR "PET hydrolase" OR "PET-degrading" OR MHETase OR cutinase OR '
            '"polyester hydrolase" OR "polyesterase" OR "plastic-degrading enzyme" OR '
            '"plastic degrading enzyme")')
ENZ_WIDE = ('(esterase OR lipase OR cutinase OR hydrolase OR depolymerase OR "carboxylesterase")')
POLY = ('(PET OR "polyethylene terephthalate" OR polyurethane OR "PHB" OR '
        '"polyhydroxyalkanoate" OR polycaprolactone OR PBAT OR "polylactic acid" OR '
        'nylon OR polyamide OR "polybutylene succinate")')

QUERY_AXES = [
    # --- electrolyte axis (the thinnest axis in week 1) -----------------------
    (f'{ENZ_CORE} AND ("metal ion" OR "metal ions" OR CaCl2 OR MgCl2 OR MnCl2 OR ZnSO4 OR CuSO4)', "metal ions"),
    (f'{ENZ_WIDE} AND {POLY} AND ("effect of metal ions" OR "metal ion effect")', "metal ions (wide)"),
    (f'{ENZ_CORE} AND (NaCl OR "sodium chloride" OR "salt concentration")', "NaCl"),
    (f'{ENZ_WIDE} AND {POLY} AND (salinity OR seawater OR "sea water" OR marine)', "salinity/marine"),
    (f'{ENZ_WIDE} AND (halophilic OR halotolerant OR haloadapted) AND (esterase OR lipase OR cutinase)', "halophilic"),
    (f'{ENZ_CORE} AND ("ionic strength" OR "ionic liquid" OR kosmotropic OR chaotropic OR Hofmeister)', "ionic strength"),
    (f'{ENZ_WIDE} AND {POLY} AND (EDTA OR "chelating agent" OR "divalent cation" OR "calcium binding")', "chelator/cation"),
    # --- temperature axis ----------------------------------------------------
    (f'{ENZ_CORE} AND ("optimal temperature" OR "temperature optimum" OR "optimum temperature")', "temperature optimum"),
    (f'{ENZ_CORE} AND ("thermal stability" OR thermostability OR "melting temperature" OR "half-life")', "thermostability"),
    (f'{ENZ_WIDE} AND {POLY} AND ("thermal inactivation" OR "residual activity" OR "T50")', "thermal inactivation"),
    (f'{ENZ_CORE} AND (thermophilic OR psychrophilic OR "cold-adapted" OR "cold active")', "temperature adaptation"),
    # --- pH axis -------------------------------------------------------------
    (f'{ENZ_CORE} AND ("optimal pH" OR "pH optimum" OR "pH stability" OR "alkaline pH")', "pH"),
    (f'{ENZ_WIDE} AND {POLY} AND ("pH profile" OR "pH-dependent" OR "pH dependence")', "pH profile"),
    # --- engineering / mutants ----------------------------------------------
    (f'{ENZ_CORE} AND (variant OR mutant OR "site-directed mutagenesis" OR engineering)', "variants"),
    (f'{ENZ_CORE} AND ("disulfide bond" OR "calcium binding site" OR "salt bridge")', "stabilising mutations"),
    # --- assays / kinetics ---------------------------------------------------
    (f'{ENZ_CORE} AND (kcat OR Michaelis OR "kinetic parameters" OR "specific activity")', "kinetics"),
    (f'{ENZ_CORE} AND ("Britton-Robinson" OR "Tris-HCl" OR "glycine-NaOH" OR "phosphate buffer")', "buffer"),
    (f'{ENZ_WIDE} AND {POLY} AND (HPLC AND (terephthalate OR "TPA release" OR MHET OR BHET))', "TPA/MHET release"),
    # --- newly characterised enzymes ----------------------------------------
    (f'{ENZ_WIDE} AND {POLY} AND ("novel" AND (characterization OR characterisation) AND (purified OR "recombinant"))', "new characterisation"),
    (f'{ENZ_WIDE} AND {POLY} AND (metagenome OR metagenomic OR "compost" OR "activated sludge")', "metagenomic"),
    # --- salinity, targeted -------------------------------------------------
    # The salinity axis stayed thin because papers report NaCl molarity rather than a
    # salinity. These axes go after the studies that DO state one: marine degradation
    # work, artificial-seawater assays, and halophilic enzyme characterisation.
    (f'{ENZ_WIDE} AND {POLY} AND ("artificial seawater" OR "synthetic seawater" OR '
     f'"seawater medium" OR "marine broth")', "artificial seawater"),
    (f'{ENZ_WIDE} AND ("salinity" AND (activity OR stability) AND (esterase OR lipase OR '
     f'cutinase OR hydrolase OR depolymerase))', "salinity vs activity"),
    (f'{ENZ_WIDE} AND {POLY} AND ("g/L NaCl" OR "%% NaCl" OR "practical salinity" OR '
     f'"PSU" OR "ppt salinity" OR "salt concentration ranging")', "salinity units"),
    (f'{ENZ_WIDE} AND (halophilic OR haloarchaea OR Haloferax OR Halomonas OR '
     f'Halobacterium) AND (esterase OR lipase OR cutinase OR "poly")', "haloarchaeal"),
    (f'{ENZ_CORE} AND ("marine environment" OR "ocean" OR "seawater degradation" OR '
     f'"marine plastic")', "marine PET"),
]

# ---------------------------------------------------------------- vocabularies
BUFFERS = ["Britton-Robinson", "Britton Robinson", "glycine-NaOH", "glycine/NaOH", "Tris-HCl",
           "Tris/HCl", "Tris–HCl", "Tris HCl", "sodium phosphate", "potassium phosphate",
           "phosphate buffer", "citrate-phosphate", "citrate phosphate", "sodium citrate",
           "citrate buffer", "acetate buffer", "sodium acetate", "MOPS", "HEPES", "MES", "CHES",
           "CAPS", "bicine", "tricine", "carbonate-bicarbonate", "glycine buffer", "borate",
           "McIlvaine", "universal buffer", "phosphate-citrate", "PBS", "ammonium bicarbonate",
           "bis-Tris", "TAPS", "PIPES"]
SUBSTRATES = ["amorphous PET", "PET film", "PET powder", "PET nanoparticle", "GfPET",
              "post-consumer PET", "poly(ethylene terephthalate)", "BHET",
              "bis(2-hydroxyethyl) terephthalate", "MHET", "mono(2-hydroxyethyl) terephthalate",
              "3PET", "pNP-butyrate", "pNP-acetate", "pNP-palmitate", "pNP-laurate",
              "p-nitrophenyl butyrate", "p-nitrophenyl acetate", "p-nitrophenyl palmitate",
              "pNPB", "pNPP", "pNPA", "p-nitrophenyl", "para-nitrophenyl", "polycaprolactone",
              "PCL", "PBAT", "PBS", "PLA", "polylactic acid", "cutin", "olive oil", "triolein",
              "tributyrin", "PHB", "poly(3-hydroxybutyrate)", "PHBV", "nylon", "polyurethane",
              "Impranil", "polyethylene", "polystyrene", "PET"]
SUBSTRATE_FORMS = [("amorphous film", r"amorphous\s+(?:PET\s+)?film|GfPET"), ("film", r"\bfilm\b"),
                   ("powder", r"\bpowder\b"), ("nanoparticle", r"nanoparticle|nanospher"),
                   ("pellet", r"\bpellet"), ("bottle-grade", r"bottle[- ]grade|post-consumer"),
                   ("soluble ester", r"pNP|p-nitrophenyl|para-nitrophenyl|tributyrin|BHET|MHET")]
ASSAY_METHODS = [("HPLC/UPLC product release", r"\bHPLC\b|\bUPLC\b|liquid chromatograph"),
                 ("spectrophotometric p-nitrophenol release", r"p-?nitrophen|pNP\b|405\s*nm|410\s*nm|348\s*nm"),
                 ("pH-stat titration", r"pH[- ]stat"),
                 ("weight loss / gravimetric", r"weight loss|mass loss|gravimetric"),
                 ("turbidimetric / clearing zone", r"turbidimetric|clearing zone|halo\b|plate assay"),
                 ("DSC / thermal denaturation", r"\bDSC\b|differential scanning|nanoDSF|thermofluor"),
                 ("circular dichroism", r"circular dichroism|\bCD\b spectr"),
                 ("fluorescence", r"fluorescen|fluorimetric"),
                 ("SEM surface analysis", r"\bSEM\b|scanning electron"),
                 ("titration of released acid", r"titrat")]
IONS = [("Na(+)", r"\bNaCl\b|sodium chloride|\bNa\+|\bNa2SO4\b", 1),
        ("K(+)", r"\bKCl\b|potassium chloride|\bK\+", 1),
        ("Ca(2+)", r"\bCaCl2?\b|\bCa2\+|\bCa\(2\+\)|calcium", 2),
        ("Mg(2+)", r"\bMgCl2?\b|\bMgSO4\b|\bMg2\+|magnesium", 2),
        ("Mn(2+)", r"\bMnCl2?\b|\bMnSO4\b|\bMn2\+|manganese", 2),
        ("Zn(2+)", r"\bZnSO4\b|\bZnCl2\b|\bZn2\+|zinc", 2),
        ("Cu(2+)", r"\bCuSO4\b|\bCuCl2\b|\bCu2\+|copper", 2),
        ("Fe(3+)", r"\bFeCl3\b|\bFe3\+|ferric", 3),
        ("Fe(2+)", r"\bFeSO4\b|\bFe2\+|ferrous", 2),
        ("Co(2+)", r"\bCoCl2\b|\bCo2\+|cobalt", 2),
        ("Ni(2+)", r"\bNiCl2\b|\bNiSO4\b|\bNi2\+|nickel", 2),
        ("Hg(2+)", r"\bHgCl2\b|\bHg2\+|mercur", 2),
        ("Li(+)", r"\bLiCl\b|lithium", 1), ("NH4(+)", r"\bNH4\b|ammonium", 1),
        ("Ba(2+)", r"\bBaCl2\b|\bBa2\+|barium", 2), ("Cd(2+)", r"\bCdCl2\b|\bCd2\+|cadmium", 2),
        ("Ag(+)", r"\bAgNO3\b|\bAg\+|silver", 1), ("Al(3+)", r"\bAlCl3\b|\bAl3\+|aluminium|aluminum", 3),
        ("Cr(3+)", r"\bCrCl3\b|\bCr3\+|chromium", 3), ("Pb(2+)", r"\bPb2\+|\blead\b", 2)]
ADDITIVES = [("EDTA", r"\bEDTA\b"), ("SDS", r"\bSDS\b|sodium dodecyl"), ("PMSF", r"\bPMSF\b"),
             ("DTT", r"\bDTT\b|dithiothreitol"), ("Triton X-100", r"Triton"), ("Tween-80", r"Tween"),
             ("urea", r"\burea\b"), ("DMSO", r"\bDMSO\b"), ("beta-mercaptoethanol", r"mercaptoethanol"),
             ("guanidine HCl", r"guanidin"), ("glycerol", r"glycerol"), ("methanol", r"methanol"),
             ("ethanol", r"\bethanol\b"), ("ethylene glycol", r"ethylene glycol"),
             ("imidazole", r"imidazole"), ("ionic liquid", r"ionic liquid|\[BMIM\]|\[EMIM\]")]

NAMED_VARIANT = re.compile(
    r"\b(ICCG|WCCG|LCC[-‑ ]?ICCG|LCC[-‑ ]?WCCG|ThermoPETase|DuraPETase|FAST[- ]?PETase|"
    r"HotPETase|TurboPETase|PETaseM?\d*|LCC|IsPETase|Is[- ]?PETase|TfCut2?|TfH|Cut190\*?|PE-?H|"
    r"PES[- ]?H1|PES[- ]?H2|Bhr[- ]?PETase|LC[-‑ ]?cutinase|Tfu_0883|Thc_Cut1|Thc_Cut2|"
    r"MHETase|PETase|Cbotu_EstA|Cbotu_EstB|PpEst|PmC|Est119|Est1|CalB|TcCut|HiC|FsC|"
    r"Ple628|Ple629|Mors1|PET2|PET6|PET12|PET46|IsPETase[- ]?\w*|BurPL|PhaZ\w*)\b", re.I)
POINT_MUT = re.compile(r"\b([ACDEFGHIKLMNPQRSTVWY]\d{1,4}[ACDEFGHIKLMNPQRSTVWY]"
                       r"(?:[/+][ACDEFGHIKLMNPQRSTVWY]\d{1,4}[ACDEFGHIKLMNPQRSTVWY])*)\b")
ACC_RE = re.compile(r"\b([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})\b")
PDB_RE = re.compile(r"\b(?:PDB(?:\s*(?:ID|code|entry))?[:\s]*)([0-9][A-Za-z0-9]{3})\b")
GB_RE = re.compile(r"\b((?:[A-Z]{3}\d{5}|[A-Z]{2}_?\d{6,9})(?:\.\d+)?)\b")

NUM = r"\d+(?:\.\d+)?"
TEMP_RE = re.compile(rf"({NUM})\s*(?:-|to|–)?\s*({NUM})?\s*(?:°\s*C\b|°C|degrees?\s*C(?:elsius)?)", re.I)
PH_RE = re.compile(rf"pH\s*(?:of|is|was|around|about|between|=|:)?\s*({NUM})\s*(?:(?:-|to|and|–)\s*({NUM}))?", re.I)
CONC_RE = re.compile(rf"({NUM})\s*(mM|μM|µM|uM|nM|M|%\s*\(w/v\)|%\s*\(v/v\)|%|mg/mL|mg/ml|g/L|g/l|ppt|PSU|psu)\b")
TIME_RE = re.compile(rf"({NUM})\s*(seconds?|secs?|s|minutes?|mins?|min|hours?|hrs?|h|days?|d|weeks?)\b", re.I)
PCT_RE = re.compile(rf"({NUM})\s*%")

# JATS strips <xref> markup, so a reference marker survives as a bare number glued to
# the sentence ("optimal activity at 75 C and pH 4.5 52"). That both marks the claim as
# somebody else's AND corrupts the parsed value ("pH 4.552"), so such sentences are
# refused outright rather than repaired.
# Physical constants of a solvent or polymer are properties of the CHEMICAL, not of the
# enzyme, and must not become an enzyme optimum or thermostability value.
# Reagent recipes from cloning/PCR/electrophoresis are laboratory logistics, not enzyme
# condition measurements: "the reaction mixture contained 3 uL of 25 mM MgCl2" is not a
# magnesium effect on a plastic-degrading enzyme.
MOLBIO_METHOD = re.compile(
    r"\bPCR\b|primer|plasmid|\bvector\b|cloning|transform(?:ed|ation)|competent cell|"
    r"SDS-?PAGE|electrophoresis|agarose|\bgel\b|sequencing (?:reaction|mixture)|"
    r"reaction mixture \(?\d*\s*[uµ]L|\bkit\b|manufacturer.s instruction|"
    r"Ni-?NTA|His-?tag|imidazole gradient|elution buffer|lysis buffer|"
    r"crystalli[sz]ation|hanging drop|mineral salt medium|\bMSM\b|culture medium|"
    r"growth medium|medium containing|buffer containing|storage buffer|"
    r"centrifug|resuspend|overnight culture|\bLB\b medium|inoculat", re.I)
# Drug-delivery / pharmacology papers use the same vocabulary (pH, stability, release)
# about compounds rather than enzymes.
PHARMA_CONTEXT = re.compile(
    r"drug release|prodrug|tumou?r|lapachone|micelle|liposome|cytotox|IC50|"
    r"pharmacokinetic|in vivo (?:mouse|mice|rat)|antiprolifer|apoptosi|"
    r"\brelease of \d|phenolate|linker|payload|conjugat(?:e|ion) (?:was|of)", re.I)

CHEM_CONSTANT = re.compile(r"boiling point|melting point of|freezing point|flash point|"
                           r"vapou?r pressure|molecular weight of|glass transition", re.I)

SECONDHAND = re.compile(
    r"\bet\s+al\b|\[\d+(?:\s*[,\-–]\s*\d+)*\]|\(\s*\d{4}\s*\)|"
    r"\b(?:previous|earlier|another|other)\s+(?:study|studies|work|report|research)|"
    r"\bpreviously\s+(?:reported|shown|described|characteri[sz]ed|found)|"
    r"\bhas\s+(?:also\s+)?been\s+(?:reported|shown|described|demonstrated|observed)|"
    r"\bwere\s+(?:reported|described)\s+(?:by|in|to)|"
    r"\bin\s+(?:the\s+)?literature|\baccording\s+to\b|"
    r"\bwas\s+(?:found|reported|shown)\s+(?:to\s+\w+\s+)?(?:in|by|with)\s+a?\s*previous",
    re.I)

OPT_RE = re.compile(r"optim|maximal|maximum activity|most active|highest activity|peak activity", re.I)
# "active over the whole analyzed range (10-75 C)" states the range that was TESTED.
# Averaging it into a 42.5 C "optimum" invents a number the paper never reported.
TESTED_RANGE_RE = re.compile(r"\b(?:over|across|within|throughout)\s+(?:the\s+)?"
                             r"(?:whole\s+|entire\s+|analy[sz]ed\s+|tested\s+|examined\s+)?"
                             r"(?:range|temperatures?|pH\s+values?)|"
                             r"\b(?:analy[sz]ed|tested|examined|investigated|assayed|screened)\s+"
                             r"(?:temperature|pH)?\s*range\b|\brange\s+of\s+temperatures\b", re.I)
STAB_RE = re.compile(r"stable|stabilit|retain|residual|half-life|remaining activity|denatur|thermostab|melting", re.I)
ACT_RE = re.compile(r"activ|hydroly|degrad|depolymeri|convers|release|turnover", re.I)


def _ok(x, lo, hi):
    try:
        return lo <= float(x) <= hi
    except (TypeError, ValueError):
        return False


def find_one(t, vocab):
    low = (t or "").lower()
    for v in vocab:
        if v.lower() in low:
            return v
    return ""


def find_pattern(t, pairs):
    for label, pat in pairs:
        if re.search(pat, t or "", re.I):
            return label
    return ""


def find_ion(t):
    for sp, pat, ch in IONS:
        if re.search(pat, t or "", re.I):
            return sp, ch
    return "", ""


def salt_formula(t):
    for f in ["NaCl", "KCl", "CaCl2", "MgCl2", "MgSO4", "MnCl2", "MnSO4", "ZnSO4", "ZnCl2",
              "CuSO4", "CuCl2", "FeCl3", "FeSO4", "CoCl2", "NiCl2", "NiSO4", "LiCl", "BaCl2",
              "CdCl2", "HgCl2", "Na2SO4", "AgNO3", "AlCl3", "K2SO4", "NH4Cl", "(NH4)2SO4"]:
        if re.search(re.escape(f).replace(r"\ ", " "), t or "", re.I):
            return f
    return ""


# ---------------------------------------------------------------- fetching
def get(url, timeout=60, retries=3):
    last = None
    for a in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:
            last = ex
            time.sleep(1.5 * (a + 1))
    raise last


def load_excluded_papers():
    db = sqlite3.connect(EXCL_DB)
    ids = {r[0] for r in db.execute("SELECT ident FROM paper")}
    db.close()
    return ids


def search_papers(excluded):
    per_axis, skipped = {}, 0
    for q_axis, label in QUERY_AXES:
        hits = []
        for page in range(1, 4):                       # up to 300 candidates per axis
            q = f"{q_axis} AND (OPEN_ACCESS:y AND HAS_FT:y AND IN_EPMC:y)"
            url = (f"{EPMC}/search?format=json&pageSize=100&page={page}&resultType=core&query="
                   + urllib.parse.quote(q))
            try:
                d = json.loads(get(url, timeout=60))
            except Exception as ex:
                print(f"  search failed [{label} p{page}]: {ex}", file=sys.stderr)
                break
            res = d.get("resultList", {}).get("result", [])
            if not res:
                break
            for r in res:
                pmcid, pmid = r.get("pmcid"), (r.get("pmid") or "")
                if not pmcid:
                    continue
                if pmcid.upper() in excluded or (pmid and pmid.upper() in excluded):
                    continue
                hits.append({"pmcid": pmcid, "doi": r.get("doi", ""),
                             "title": (r.get("title", "") or "")[:200], "year": r.get("pubYear", ""),
                             "journal": (r.get("journalTitle", "") or "")[:90],
                             "pmid": pmid, "axis": label})
            time.sleep(0.34)
        per_axis[label] = hits
        print(f"  [{label:24}] {len(hits):>4} new OA candidates", file=sys.stderr)

    roster, seen, i = [], set(), 0
    while len(roster) < TARGET_PAPERS:
        added = False
        for label in per_axis:
            lst = per_axis[label]
            if i < len(lst):
                added = True
                p = lst[i]
                if p["pmcid"] not in seen:
                    seen.add(p["pmcid"])
                    roster.append(p)
                    if len(roster) >= TARGET_PAPERS:
                        break
        if not added:
            break
        i += 1
    return roster


def full_text(pmcid):
    path = os.path.join(XML_DIR, f"{pmcid}.xml")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return open(path).read()
    xml = get(f"{EPMC}/{pmcid}/fullTextXML", timeout=90)
    open(path, "w").write(xml)
    time.sleep(0.34)
    return xml


def parse_xml(xml):
    try:
        return ET.fromstring(xml)
    except ET.ParseError:
        return ET.fromstring(re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", "&amp;", xml))


# Only the sections where an article reports its OWN experiments may contribute prose.
# Introductions and conclusions restate the field's results; mining them produced
# "measurements" that were really background sentences about other people's enzymes.
OWN_WORK_SEC = re.compile(r"result|characteri[sz]ation|characteri[sz]ing|effect of|"
                          r"material|method|experimental|assay|purification|expression|"
                          r"biochemical|enzymatic|activity|stability|optimi[sz]ation|"
                          r"kinetic|screening|discussion", re.I)
BACKGROUND_SEC = re.compile(r"introduction|background|conclusion|outlook|perspective|"
                            r"future|abbreviation|acknowledg|supplementary|availability|"
                            r"declaration|funding|conflict|reference|abstract|"
                            r"literature\s+review|state\s+of\s+the\s+art", re.I)


def section_ok(title):
    """Background sections are refused even if they also look like results sections."""
    t = " ".join((title or "").split())
    if not t:
        return True                      # untitled body text: keep, the sentence filters apply
    if BACKGROUND_SEC.search(t):
        return False
    return True


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.;])\s+(?=[A-Z0-9(])", t or "") if s.strip()]


# ---------------------------------------------------------------- row building
def base_row(paper, section, quote):
    return {"enzyme_name": "", "mutation": "wild-type/unspecified", "substrate": "",
            "substrate_form": "", "temperature_c": "", "temperature_c_low": None,
            "temperature_c_high": None, "pH": "", "pH_low": None, "pH_high": None,
            "buffer_name": "", "salt_species": "", "ion_species": "", "ion_charge": "",
            "conc_raw": "", "salinity_raw": "", "seawater_type": "", "ionic_strength_raw": "",
            "additive": "", "exposure_time_raw": "", "assay_method": "",
            "relative_activity_pct": None, "measurement_type": "", "value_raw": "",
            "value_unit_raw": "", "direction": "", "kinetic_param": "",
            "uniprot_in_text": "", "pdb_in_text": "", "genbank_in_text": "",
            "source_db": "Europe PMC",
            "source_type": f"primary literature (OA full text, {section})",
            "pmcid": paper["pmcid"], "doi": paper.get("doi", ""), "pubmed_id": paper.get("pmid", ""),
            "paper_title": paper.get("title", ""), "year": paper.get("year", ""),
            "journal": paper.get("journal", ""), "axis": paper.get("axis", ""), "section": section,
            "evidence_quote": " ".join((quote or "").split())[:450],
            "reviewed_status": "primary-literature"}


def enzyme_from(text, paper):
    m = NAMED_VARIANT.search(text or "")
    if m:
        return m.group(1)
    m = NAMED_VARIANT.search(paper.get("title", ""))
    if m:
        return m.group(1)
    return ""


def annotate(row, text, paper_ids):
    row["buffer_name"] = find_one(text, BUFFERS)
    row["substrate"] = row["substrate"] or find_one(text, SUBSTRATES)
    row["substrate_form"] = find_pattern(text, SUBSTRATE_FORMS)
    row["assay_method"] = row["assay_method"] or find_pattern(text, ASSAY_METHODS)
    ion, ch = find_ion(text)
    row["ion_species"], row["ion_charge"] = row["ion_species"] or ion, row["ion_charge"] or (str(ch) if ch else "")
    row["salt_species"] = row["salt_species"] or salt_formula(text)
    row["additive"] = row["additive"] or find_pattern(text, ADDITIVES)
    if re.search(r"seawater|sea water", text, re.I):
        row["seawater_type"] = "artificial" if re.search(r"artificial|synthetic", text, re.I) else "natural"
    ms = (re.search(rf"salinit\w*\s*(?:of|was|at|:|=|to)?\s*({NUM})\s*(%|ppt|PSU|psu|g/L|g/l)", text, re.I)
          or re.search(rf"({NUM})\s*(%|ppt|PSU|psu|g/L|g/l)\s*(?:\w+\s+){{0,3}}salinit", text, re.I)
          or re.search(rf"salinit\w*[^.]{{0,40}}?({NUM})\s*(%|ppt|PSU|psu|g/L|g/l)", text, re.I))
    if ms:
        row["salinity_raw"] = f"{ms.group(1)} {ms.group(2)}"
    mi = re.search(rf"ionic strength\s*(?:of|was|at|:|=)?\s*({NUM})\s*(mM|M)?", text, re.I)
    if mi:
        row["ionic_strength_raw"] = f"{mi.group(1)} {mi.group(2) or 'M'}"
    mp = POINT_MUT.search(text)
    if mp:
        row["mutation"] = mp.group(1)
    mt = TIME_RE.search(text)
    if mt and re.search(r"incubat|treat|expos|pre-?incubat|after|for\s", text, re.I):
        row["exposure_time_raw"] = f"{mt.group(1)} {mt.group(2)}"
    mc = CONC_RE.search(text)
    if mc and (row["ion_species"] or row["salt_species"] or row["additive"]):
        row["conc_raw"] = row["conc_raw"] or f"{mc.group(1)} {mc.group(2)}"
    # identifiers seen anywhere in the paper — used later to resolve a sequence
    row["uniprot_in_text"] = ";".join(paper_ids.get("uniprot", [])[:6])
    row["pdb_in_text"] = ";".join(paper_ids.get("pdb", [])[:6])
    row["genbank_in_text"] = ";".join(paper_ids.get("genbank", [])[:6])
    return row


def rows_from_sentence(sent, paper, ids):
    out = []
    is_opt, is_stab, has_act = bool(OPT_RE.search(sent)), bool(STAB_RE.search(sent)), bool(ACT_RE.search(sent))
    if not has_act:
        return out
    enz = enzyme_from(sent, paper)

    # "The optimum pH was established by assaying activity in buffers pH 5-9" names the
    # METHOD. The outcome words in it describe the intent, not a result, so this phrasing
    # overrides any outcome match downstream.
    if re.search(r"\bwas\s+(?:also\s+)?(?:determined|established|identified|assessed|"
                 r"evaluated|investigated|measured)\s+by\b|\bwere\s+(?:determined|"
                 r"established|identified|assessed|evaluated|measured)\s+by\b", sent, re.I):
        return out

    # a span quoted inside a "range (...)" clause is a range, never a single optimum
    # "LIP1 and LIP2 were optimally active at pH 9.0 and 8.0, respectively" carries two
    # measurements for two enzymes. Emitting one row averages them into a value neither
    # enzyme has, so the sentence is refused rather than mis-attributed.
    if re.search(r"\brespectively\b", sent, re.I):
        return out

    tested_range = bool(TESTED_RANGE_RE.search(sent)) or bool(
        re.search(r"\brange\b[^.]{0,40}\(", sent, re.I))
    if is_opt or is_stab:
        temps = []
        for m in TEMP_RE.finditer(sent):
            lo, hi = m.group(1), m.group(2)
            if not _ok(lo, -20, 150):
                continue
            temps.append((f"{lo}-{hi}", float(lo), float(hi)) if (hi and _ok(hi, -20, 150))
                         else (lo, float(lo), float(lo)))
        for val, lo, hi in (temps[:1] if (is_opt and not is_stab) else temps[:2]):
            if tested_range and lo != hi:
                continue                      # a tested span, not a measured optimum
            r = base_row(paper, "results text", sent)
            r["enzyme_name"] = enz
            r["measurement_type"] = "temperature optimum" if (is_opt and not is_stab) else "thermostability"
            r["temperature_c"], r["temperature_c_low"], r["temperature_c_high"] = val, lo, hi
            r["value_raw"], r["value_unit_raw"] = val, "degrees Celsius"
            mp = PH_RE.search(sent)
            if mp and _ok(mp.group(1), 0, 14):
                r["pH"] = mp.group(1); r["pH_low"] = r["pH_high"] = float(mp.group(1))
            pct = PCT_RE.search(sent)
            if pct and _ok(pct.group(1), 0, 500) and re.search(r"activ", sent, re.I):
                r["relative_activity_pct"] = float(pct.group(1))
            out.append(annotate(r, sent, ids))

        phs = []
        for m in PH_RE.finditer(sent):
            lo, hi = m.group(1), m.group(2)
            if not _ok(lo, 0, 14):
                continue
            phs.append((f"{lo}-{hi}", float(lo), float(hi)) if (hi and _ok(hi, 0, 14))
                       else (lo, float(lo), float(lo)))
        for val, lo, hi in (phs[:1] if (is_opt and not is_stab) else phs[:2]):
            if tested_range and lo != hi:
                continue
            r = base_row(paper, "results text", sent)
            r["enzyme_name"] = enz
            r["measurement_type"] = "pH optimum" if (is_opt and not is_stab) else "pH stability"
            r["pH"], r["pH_low"], r["pH_high"] = val, lo, hi
            r["value_raw"], r["value_unit_raw"] = val, "pH"
            mt = TEMP_RE.search(sent)
            if mt and _ok(mt.group(1), -20, 150):
                r["temperature_c"] = mt.group(1); r["temperature_c_low"] = r["temperature_c_high"] = float(mt.group(1))
            out.append(annotate(r, sent, ids))

    ion, ch = find_ion(sent)
    salt = salt_formula(sent)
    has_sal = bool(re.search(r"salinit|seawater|sea water", sent, re.I))
    has_is = bool(re.search(r"ionic strength", sent, re.I))
    # an explicit salinity with an activity outcome is a measurement even when no salt
    # formula is named ("activity dropped to 40% at 3.5% salinity")
    explicit_sal = bool(re.search(rf"salinit\w*[^.]{{0,40}}?({NUM})\s*(%|ppt|PSU|psu|g/L|g/l)|"
                                  rf"({NUM})\s*(%|ppt|PSU|psu|g/L|g/l)[^.]{{0,25}}?salinit", sent, re.I))
    if (ion or salt or has_sal or has_is or explicit_sal):
        conc, pct = CONC_RE.search(sent), PCT_RE.search(sent)
        if conc or has_sal or has_is:
            r = base_row(paper, "results text", sent)
            r["enzyme_name"] = enz
            r["measurement_type"] = ("ionic strength effect" if has_is else
                                     "salinity effect" if has_sal else "salt effect")
            if re.search(r"inhibit|reduc|decreas|abolish|loss|suppress|impair", sent, re.I):
                r["direction"] = "inhibition"
            elif re.search(r"activat|enhanc|increas|stimulat|improv|promot", sent, re.I):
                r["direction"] = "activation"
            else:
                r["direction"] = "none"
            if pct and _ok(pct.group(1), 0, 500) and re.search(r"activ", sent, re.I):
                r["relative_activity_pct"] = float(pct.group(1))
                r["value_raw"], r["value_unit_raw"] = pct.group(1), "% relative activity"
            elif conc:
                r["value_raw"], r["value_unit_raw"] = conc.group(1), conc.group(2)
            else:
                r["value_raw"], r["value_unit_raw"] = r["direction"], "qualitative"
            mt = TEMP_RE.search(sent)
            if mt and _ok(mt.group(1), -20, 150):
                r["temperature_c"] = mt.group(1); r["temperature_c_low"] = r["temperature_c_high"] = float(mt.group(1))
            mp = PH_RE.search(sent)
            if mp and _ok(mp.group(1), 0, 14):
                r["pH"] = mp.group(1); r["pH_low"] = r["pH_high"] = float(mp.group(1))
            out.append(annotate(r, sent, ids))
    return out


# ---------------------------------------------------------------- table mining
HEADER_KINDS = [("ion", r"metal\s*ion|^ions?$|ions?\b|reagent|additive|chemical|compound|effector|salt|treatment"),
                ("relative_activity", r"relative\s*activit|residual\s*activit|remaining\s*activit|activity\s*\(%\)|%\s*activit"),
                ("specific_activity", r"specific\s*activit"),
                ("temp_opt", r"(?:t\s*opt|topt|optimal?\s*temp|temp.*optim)"),
                ("ph_opt", r"(?:ph\s*opt|phopt|optimal?\s*ph|ph.*optim)"),
                ("temperature", r"^temp|temperature|°c"), ("ph", r"^ph$|^ph\b"),
                ("enzyme", r"enzyme|protein|variant|mutant|biocatalyst|name|strain|construct"),
                ("conc", r"concentration|\bconc\b|\bmM\b|dose"), ("km", r"^\s*k\s*m\s*(?:\(|$)|michaelis|^km$"),
                ("kcat", r"kcat|turnover"), ("kcatkm", r"kcat/km|catalytic efficiency"),
                ("time", r"^time|incubation|duration"), ("substrate", r"substrate"),
                ("buffer", r"buffer"), ("salinity", r"salinit|nacl|seawater"),
                ("half_life", r"half[- ]life|t1/2|t½"), ("tm", r"^tm\b|melting|\bt\s*m\b|t50")]


def header_kind(h):
    hl = " ".join((h or "").lower().split())
    for kind, pat in HEADER_KINDS:
        if re.search(pat, hl):
            return kind
    return ""


def table_caption(tw):
    for tag in ("label", "caption", "title"):
        for el in tw.iter(tag):
            t = " ".join("".join(el.itertext()).split())
            if t:
                return t[:250]
    return ""


# A table is NOT this article's own experimental data when it carries a Reference
# column (a literature comparison — the numbers belong to other papers, and its rows
# name other people's enzymes) or when it is an in-silico annotation table (TPM/FPKM
# expression, isoelectric point, predicted optimum). Both kinds were shipping wrong
# values before: a "pH Optimum" column in an annotation table is PREDICTED, not
# measured, which the no-synthetic-data rule forbids outright.
COMPARISON_HDR = re.compile(r"^\s*(?:reference|references|source|literature|citation|"
                            r"reported\s+by|refs?\.?)\s*$", re.I)
# A polymer characterisation table reports the MATERIAL's properties. Its "TM" column is
# the plastic's melting temperature, which is not an enzyme thermostability measurement.
POLYMER_HDR = re.compile(r"^\s*(?:ld|bt|bf|eab|ts|ym|wvtr|otr|mfi|crystallinity|xc|"
                         r"tensile|elongation|young|modulus|thickness|haze|opacity)\s*$", re.I)

INSILICO_HDR = re.compile(r"\btpm\b|\bfpkm\b|\brpkm\b|isoelectric|^\s*pi\s*$|"
                          r"gene\s*id|locus[_ ]?tag|contig|scaffold|signal\s*peptide|"
                          r"predicted|in\s*silico|molecular\s*weight\s*\(?k?da", re.I)


SUPPLIER_HDR = re.compile(r"supplier|manufacturer|cat(?:alog|\.)?\s*(?:no|number)|\bcas\b|"
                          r"purity|vendor|company|product\s*(?:no|code)", re.I)
PURIFICATION_HDR = re.compile(r"purification\s*(?:step|fold)|total\s*(?:protein|activit)|"
                              r"\byield\b|fold\s*purif|purification\s*\(fold\)", re.I)


def table_is_secondary(headers, caption):
    if any(SUPPLIER_HDR.search(h or "") for h in headers):
        return "reagent supplier table"
    # A purification summary tabulates recovery across chromatography steps. Its
    # "specific activity" column varies with purity, not with temperature, pH or salt,
    # so it is not a condition-dependent measurement.
    if sum(1 for h in headers if PURIFICATION_HDR.search(h or "")) >= 2:
        return "purification summary table"
    if re.search(r"purification\s+(?:summary|table|of)|summary\s+of\s+.{0,20}purification|"
                 r"reagents?\s+(?:and|used)|chemicals?\s+used", caption or "", re.I):
        return "purification / reagent table"
    return _table_is_secondary_rules(headers, caption)


def _table_is_secondary_rules(headers, caption):
    if any(COMPARISON_HDR.match(h or "") for h in headers):
        return "literature comparison table"
    if any(INSILICO_HDR.search(h or "") for h in headers):
        return "in-silico annotation table"
    if sum(1 for h in headers if POLYMER_HDR.match(h or "")) >= 2:
        return "polymer material-property table"
    if re.search(r"mechanical|tensile|barrier|thermal propert|film propert|"
                 r"physicochemical propert(?:y|ies)\s+of\s+(?:the\s+)?(?:film|polymer|blend)",
                 caption or "", re.I):
        return "polymer material-property table"
    if re.search(r"compar\w+\s+(?:of|with|to)\s+.*(?:reported|literature|other|previous)|"
                 r"reported\s+(?:in\s+)?(?:the\s+)?literature|previously\s+(?:reported|characteri)",
                 caption or "", re.I):
        return "literature comparison table"
    return ""


def rows_from_table(tw, paper, ids):
    out, caption = [], table_caption(tw)
    for table in tw.iter("table"):
        trs = list(table.iter("tr"))
        if len(trs) < 2:
            continue
        headers = ["".join(c.itertext()).strip() for c in list(trs[0])]
        why = table_is_secondary(headers, caption)
        if why:
            SKIPPED_TABLES.append((paper["pmcid"], why, caption[:90]))
            continue
        kinds = [header_kind(h) for h in headers]
        useful = {"relative_activity", "specific_activity", "temp_opt", "ph_opt", "km", "kcat",
                  "kcatkm", "half_life", "tm"}
        if not (useful & set(kinds)):
            continue
        col = {k: i for i, k in enumerate(kinds) if k}
        for tr in trs[1:]:
            cells = ["".join(c.itertext()).strip() for c in list(tr)]
            if not cells or all(not c for c in cells):
                continue

            def cell(k):
                i = col.get(k)
                return cells[i] if (i is not None and i < len(cells)) else ""

            label_cell = cell("ion") or cell("enzyme") or cells[0]
            ctx = f"{caption} | {' | '.join(headers)} | {' | '.join(cells)}"
            quote = (f"Table in {paper['pmcid']} — {caption[:110]} :: "
                     + " | ".join(f"{h}={c}" for h, c in zip(headers, cells) if c))[:450]

            if "relative_activity" in col or "specific_activity" in col:
                akind = "relative_activity" if "relative_activity" in col else "specific_activity"
                raw = cell(akind)
                mnum = re.search(rf"(-?{NUM})", raw.replace(",", ""))
                if mnum:
                    ion, ch = find_ion(label_cell)
                    salt, add = salt_formula(label_cell), find_pattern(label_cell, ADDITIVES)
                    r = base_row(paper, "table", quote)
                    r["enzyme_name"] = cell("enzyme") or enzyme_from(caption, paper)
                    r["ion_species"], r["ion_charge"] = ion, str(ch) if ch else ""
                    r["salt_species"], r["additive"] = salt, add
                    r["measurement_type"] = ("salt effect" if (ion or salt) else
                                             "inhibition" if add else
                                             "salinity effect" if re.search(r"salinit|nacl|seawater", label_cell, re.I)
                                             else "relative activity")
                    if akind == "specific_activity" and r["measurement_type"] == "relative activity":
                        r["measurement_type"] = "specific activity"
                    if akind == "relative_activity" and _ok(mnum.group(1), 0, 1000):
                        v = float(mnum.group(1))
                        r["relative_activity_pct"], r["value_unit_raw"] = v, "% relative activity"
                        r["direction"] = "activation" if v > 105 else "inhibition" if v < 95 else "none"
                    else:
                        r["value_unit_raw"] = "U/mg (as reported)"
                    r["value_raw"] = mnum.group(1)
                    mc = CONC_RE.search(caption)
                    r["conc_raw"] = cell("conc") or (f"{mc.group(1)} {mc.group(2)}" if mc else "")
                    if cell("temperature"):
                        mt = TEMP_RE.search(cell("temperature")) or re.search(rf"({NUM})", cell("temperature"))
                        if mt and _ok(mt.group(1), -20, 150):
                            r["temperature_c"] = mt.group(1); r["temperature_c_low"] = r["temperature_c_high"] = float(mt.group(1))
                    if cell("ph"):
                        mp = re.search(rf"({NUM})", cell("ph"))
                        if mp and _ok(mp.group(1), 0, 14):
                            r["pH"] = mp.group(1); r["pH_low"] = r["pH_high"] = float(mp.group(1))
                    if cell("time"):
                        r["exposure_time_raw"] = cell("time")
                    if cell("substrate"):
                        r["substrate"] = cell("substrate")[:70]
                    out.append(annotate(r, ctx, ids))

            for kind, mtype, unit in (("temp_opt", "temperature optimum", "degrees Celsius"),
                                      ("ph_opt", "pH optimum", "pH"),
                                      ("tm", "thermostability", "degrees Celsius"),
                                      ("half_life", "thermostability", "as reported"),
                                      ("km", "kinetic constant", "as reported"),
                                      ("kcat", "kinetic constant", "as reported"),
                                      ("kcatkm", "kinetic constant", "as reported")):
                if kind not in col:
                    continue
                raw = cell(kind)
                if not raw:
                    continue
                mnum = re.search(rf"({NUM})\s*(?:-|to|–)?\s*({NUM})?", raw.replace(",", ""))
                if not mnum:
                    continue
                lo, hi = mnum.group(1), mnum.group(2)
                if kind in ("temp_opt", "tm") and not _ok(lo, -20, 150):
                    continue
                if kind == "ph_opt" and not _ok(lo, 0, 14):
                    continue
                r = base_row(paper, "table", quote)
                r["enzyme_name"] = cell("enzyme") or enzyme_from(caption, paper)
                r["measurement_type"] = mtype
                r["value_raw"] = f"{lo}-{hi}" if hi else lo
                r["value_unit_raw"] = unit
                if kind in ("temp_opt", "tm"):
                    r["temperature_c"] = r["value_raw"]
                    r["temperature_c_low"], r["temperature_c_high"] = float(lo), float(hi) if hi else float(lo)
                if kind == "ph_opt":
                    r["pH"] = r["value_raw"]
                    r["pH_low"], r["pH_high"] = float(lo), float(hi) if hi else float(lo)
                if kind in ("km", "kcat", "kcatkm"):
                    r["kinetic_param"] = {"km": "KM", "kcat": "kcat", "kcatkm": "kcat/KM"}[kind]
                    mu = re.search(r"\(([^)]+)\)", headers[col[kind]])
                    r["value_unit_raw"] = mu.group(1) if mu else "as reported"
                    if cell("temperature"):
                        mt = re.search(rf"({NUM})", cell("temperature"))
                        if mt and _ok(mt.group(1), -20, 150):
                            r["temperature_c"] = mt.group(1); r["temperature_c_low"] = r["temperature_c_high"] = float(mt.group(1))
                    if cell("ph"):
                        mp = re.search(rf"({NUM})", cell("ph"))
                        if mp and _ok(mp.group(1), 0, 14):
                            r["pH"] = mp.group(1); r["pH_low"] = r["pH_high"] = float(mp.group(1))
                if cell("substrate"):
                    r["substrate"] = cell("substrate")[:70]
                out.append(annotate(r, ctx, ids))
    return out


def paper_identifiers(root):
    """UniProt / PDB / GenBank accessions stated anywhere in the article."""
    txt = " ".join(" ".join(el.itertext()) for el in root.iter())
    txt = " ".join(txt.split())
    ids = {"uniprot": [], "pdb": [], "genbank": []}
    seen = set()
    for m in ACC_RE.finditer(txt):
        a = m.group(1).upper()
        if a not in seen:
            seen.add(a); ids["uniprot"].append(a)
    for m in PDB_RE.finditer(txt):
        p = m.group(1).upper()
        if p not in seen:
            seen.add(p); ids["pdb"].append(p)
    for m in GB_RE.finditer(txt):
        g = m.group(1).upper()
        if g not in seen and re.match(r"^[A-Z]{3}\d{5}", g):
            seen.add(g); ids["genbank"].append(g)
    return ids


def main():
    os.makedirs(XML_DIR, exist_ok=True)
    excluded = load_excluded_papers()
    print(f"Exclusion index holds {len(excluded)} paper identifiers already used.\n"
          f"Searching Europe PMC for papers NOT among them...", file=sys.stderr)
    papers = search_papers(excluded)
    print(f"\nRoster: {len(papers)} previously-unused OA papers\n", file=sys.stderr)

    rows, ok = [], []
    for i, paper in enumerate(papers, 1):
        try:
            root = parse_xml(full_text(paper["pmcid"]))
        except Exception as ex:
            print(f"[{i:>3}/{len(papers)}] {paper['pmcid']} skip ({type(ex).__name__})", file=sys.stderr)
            continue
        before = len(rows)
        ids = paper_identifiers(root)

        # walk <sec> blocks so each paragraph is judged by the section it sits in
        def paragraphs_with_section(node, title=""):
            for child in node:
                if child.tag == "sec":
                    st = ""
                    for tl in child:
                        if tl.tag == "title":
                            st = " ".join("".join(tl.itertext()).split())
                            break
                    yield from paragraphs_with_section(child, st or title)
                elif child.tag == "p":
                    yield title, " ".join("".join(child.itertext()).split())
                else:
                    yield from paragraphs_with_section(child, title)

        body = root.find(".//body")
        paras = list(paragraphs_with_section(body)) if body is not None else []
        for sec_title, t in paras:
            if len(t) < 25 or not section_ok(sec_title):
                if len(t) >= 25:
                    SKIPPED_SECTIONS.append((paper["pmcid"], sec_title[:60]))
                continue
            for s in sentences(t):
                if len(s) < 25:
                    continue
                if not re.search(r"pH|°C|degrees|mM\b|\bM\b|NaCl|salinit|ionic strength|"
                                 r"metal|activit|temperatur", s, re.I):
                    continue
                if MOLBIO_METHOD.search(s) or PHARMA_CONTEXT.search(s):
                    SKIPPED_SENTENCES.append((paper["pmcid"], "not-a-measurement: " + s[:80]))
                    continue
                if CHEM_CONSTANT.search(s):
                    SKIPPED_SENTENCES.append((paper["pmcid"], "chem-constant: " + s[:80]))
                    continue
                if SECONDHAND.search(s):
                    SKIPPED_SENTENCES.append((paper["pmcid"], s[:90]))
                    continue
                try:
                    rows.extend(rows_from_sentence(s, paper, ids))
                except Exception:
                    pass
        for tw in root.iter("table-wrap"):
            try:
                rows.extend(rows_from_table(tw, paper, ids))
            except Exception:
                pass
        n = len(rows) - before
        ok.append(dict(paper, rows=n, uniprot_in_paper=len(ids["uniprot"])))
        print(f"[{i:>3}/{len(papers)}] {paper['pmcid']} +{n:<4} {paper['title'][:62]}", file=sys.stderr)

    seen, dd = set(), []
    for r in rows:
        k = (r["pmcid"], r["measurement_type"], r["enzyme_name"][:40], r["value_raw"],
             r["ion_species"], r["additive"], r["evidence_quote"][:100])
        if k not in seen:
            seen.add(k); dd.append(r)

    import collections
    print(f"\nRaw benchmark rows: {len(dd)} from {len(ok)} papers", file=sys.stderr)
    for k, v in collections.Counter(r["measurement_type"] for r in dd).most_common():
        print(f"   {v:>6}  {k}", file=sys.stderr)
    print(f"   refused: {len(SKIPPED_TABLES)} secondary tables, "
          f"{len(SKIPPED_SECTIONS)} background paragraphs, "
          f"{len(SKIPPED_SENTENCES)} secondhand sentences", file=sys.stderr)
    json.dump({"tables": SKIPPED_TABLES[:400], "sections": SKIPPED_SECTIONS[:400],
               "sentences": SKIPPED_SENTENCES[:400]},
              open(os.path.join(ROOT, "data", "refused.json"), "w"), indent=1)
    json.dump(dd, open(OUT_ROWS, "w"))
    json.dump(ok, open(OUT_PAPERS, "w"), indent=1)
    print(f"Wrote {OUT_ROWS}", file=sys.stderr)


if __name__ == "__main__":
    main()
