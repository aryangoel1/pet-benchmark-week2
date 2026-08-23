#!/usr/bin/env python3
"""Unit standardisation for the plastic-enzyme conditions benchmark.

TASK.txt requires all units standardised. Canonical units chosen here:

    temperature         degrees Celsius (°C)
    pH                  dimensionless (0-14)
    concentration       millimolar (mM)
    salinity            g/L  and  PSU
    ionic strength      molar (M)
    time                minutes
    KM                  mM
    kcat                s^-1
    Vmax                umol/min/mg
    activity (relative) % of the paper's own maximum/control

Conversions are arithmetic only — they never change what a source reported.
Percent (w/v) is converted to mM only for salts whose formula weight is known;
otherwise the raw string is preserved and the standardised field is left empty.
"""
import re

NUM = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"

# Formula weights (g/mol) for salts and additives seen in enzyme characterisation work.
MW = {
    "NaCl": 58.44, "KCl": 74.55, "CaCl2": 110.98, "MgCl2": 95.21, "MnCl2": 125.84,
    "ZnSO4": 161.47, "ZnCl2": 136.29, "CuSO4": 159.61, "CuCl2": 134.45, "FeCl3": 162.20,
    "FeSO4": 151.91, "CoCl2": 129.84, "NiCl2": 129.60, "LiCl": 42.39, "BaCl2": 208.23,
    "CdCl2": 183.32, "HgCl2": 271.50, "Na2SO4": 142.04, "NH4Cl": 53.49, "KBr": 119.00,
    "EDTA": 292.24, "SDS": 288.37, "urea": 60.06, "DTT": 154.25, "PMSF": 174.19,
    "glycerol": 92.09, "DMSO": 78.13, "methanol": 32.04, "ethylene glycol": 62.07,
}

# Ion stoichiometry per formula unit: salt -> [(ion, charge, count), ...]
SALT_IONS = {
    "NaCl": [("Na(+)", 1, 1), ("Cl(-)", -1, 1)],
    "KCl": [("K(+)", 1, 1), ("Cl(-)", -1, 1)],
    "LiCl": [("Li(+)", 1, 1), ("Cl(-)", -1, 1)],
    "NH4Cl": [("NH4(+)", 1, 1), ("Cl(-)", -1, 1)],
    "CaCl2": [("Ca(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "MgCl2": [("Mg(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "MnCl2": [("Mn(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "ZnCl2": [("Zn(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "CoCl2": [("Co(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "NiCl2": [("Ni(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "BaCl2": [("Ba(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "CdCl2": [("Cd(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "HgCl2": [("Hg(2+)", 2, 1), ("Cl(-)", -1, 2)],
    "FeCl3": [("Fe(3+)", 3, 1), ("Cl(-)", -1, 3)],
    "ZnSO4": [("Zn(2+)", 2, 1), ("SO4(2-)", -2, 1)],
    "CuSO4": [("Cu(2+)", 2, 1), ("SO4(2-)", -2, 1)],
    "FeSO4": [("Fe(2+)", 2, 1), ("SO4(2-)", -2, 1)],
    "Na2SO4": [("Na(+)", 1, 2), ("SO4(2-)", -2, 1)],
}

# Seawater is ~35 g/L total salts, ~0.6 M NaCl-equivalent, ionic strength ~0.7 M.
SEAWATER_SALINITY_G_L = 35.0
SEAWATER_IONIC_STRENGTH_M = 0.70


def _f(x):
    try:
        v = float(x)
        return v if v == v and abs(v) != float("inf") else None
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ temperature
def to_celsius(value, unit=""):
    """Convert a temperature to degrees Celsius. Accepts K / F / C."""
    v = _f(value)
    if v is None:
        return None
    u = (unit or "").strip().lower().replace("°", "")
    if u.startswith("k") or (v > 200 and not u):        # Kelvin
        return round(v - 273.15, 2)
    if u.startswith("f"):
        return round((v - 32.0) * 5.0 / 9.0, 2)
    return round(v, 2)


def plausible_temperature(c):
    return c is not None and -20.0 <= c <= 150.0


def plausible_ph(p):
    return p is not None and 0.0 <= p <= 14.0


# ---------------------------------------------------------------- concentration
def to_mM(value, unit, species=""):
    """Convert a concentration to mM. Returns None when conversion needs an unknown MW."""
    v = _f(value)
    if v is None or v < 0:      # a negative concentration is always a parsing artefact
        return None
    u = " ".join((unit or "").split()).lower().replace("μ", "u").replace("µ", "u")
    if u in ("mm", "mmol/l", "mmol/liter"):
        return round(v, 6)
    if u in ("m", "mol/l", "molar"):
        return round(v * 1000.0, 6)
    if u in ("um", "umol/l", "micromolar"):
        return round(v / 1000.0, 6)
    if u in ("nm", "nmol/l"):
        return round(v / 1_000_000.0, 9)
    if u in ("pm",):
        return round(v / 1_000_000_000.0, 12)
    mw = MW.get(species) or MW.get((species or "").strip())
    if u in ("mg/ml", "g/l"):
        return round(v * 1000.0 / mw, 6) if mw else None      # g/L / (g/mol) -> mol/L -> mM
    if u in ("ug/ml", "mg/l"):
        return round(v / mw, 6) if mw else None
    if u.startswith("%"):
        # % (w/v) == g per 100 mL == 10 g/L
        if "v/v" in u:
            return None
        return round(10.0 * v * 1000.0 / mw, 6) if mw else None
    return None


# -------------------------------------------------------------------- salinity
def salinity_to_g_per_L(value, unit):
    """Convert a reported salinity to g/L. PSU and ppt are numerically ~g/kg ~ g/L."""
    v = _f(value)
    if v is None:
        return None
    u = (unit or "").strip().lower()
    if u in ("g/l", "g/kg", "ppt", "psu", "‰"):
        return round(v, 3)
    if u.startswith("%"):
        return round(v * 10.0, 3)          # 1 % (w/v) = 10 g/L
    if u in ("mm",):                        # a NaCl molarity given as salinity
        return round(v / 1000.0 * MW["NaCl"], 3)
    if u in ("m",):
        return round(v * MW["NaCl"], 3)
    return None


def g_per_L_to_psu(g_per_l):
    """PSU is defined on the practical salinity scale; for seawater-like samples it
    tracks g/kg closely enough that oceanographic papers use them interchangeably."""
    return round(g_per_l, 3) if g_per_l is not None else None


# -------------------------------------------------------------- ionic strength
def ionic_strength_from_salt(salt, conc_mM):
    """I = 0.5 * sum(c_i * z_i^2), in M, for a single fully-dissociated salt."""
    if conc_mM is None or salt not in SALT_IONS:
        return None
    c_M = conc_mM / 1000.0
    total = sum(count * c_M * (charge ** 2) for _, charge, count in SALT_IONS[salt])
    return round(0.5 * total, 6)


def ionic_strength_from_composition(components):
    """components: [(salt_formula, conc_mM), ...] -> ionic strength in M, or None."""
    vals = [ionic_strength_from_salt(s, c) for s, c in components]
    vals = [v for v in vals if v is not None]
    return round(sum(vals), 6) if vals else None


def ionic_strength_from_salinity(g_per_l):
    """Lewis & Randall relation for seawater-like samples:
       I (mol/kg) = 19.92 * S / (1000 - 1.005 * S), S in g/kg.
    Used only when a paper reports a salinity but no explicit ionic strength;
    always tagged `computed_from_salinity` so it is never read as a reported value."""
    s = _f(g_per_l)
    if s is None or s <= 0 or s > 300:
        return None
    return round(19.92 * s / (1000.0 - 1.005 * s), 6)


def parse_ionic_strength(raw):
    """Parse a reported ionic strength string into M."""
    if not raw:
        return None
    m = re.search(rf"({NUM})\s*(mM|M|mm|m)?", raw)
    if not m:
        return None
    v = _f(m.group(1))
    if v is None:
        return None
    unit = (m.group(2) or "M").strip()
    return round(v / 1000.0, 6) if unit.lower() == "mm" else round(v, 6)


# ------------------------------------------------------------------------ time
def to_minutes(value, unit):
    v = _f(value)
    if v is None:
        return None
    u = (unit or "").strip().lower()
    if u in ("s", "sec", "secs", "second", "seconds"):
        return round(v / 60.0, 4)
    if u in ("min", "mins", "minute", "minutes"):
        return round(v, 4)
    if u in ("h", "hr", "hrs", "hour", "hours"):
        return round(v * 60.0, 4)
    if u in ("d", "day", "days"):
        return round(v * 1440.0, 4)
    if u in ("week", "weeks", "wk"):
        return round(v * 10080.0, 4)
    return None


def parse_time(raw):
    if not raw:
        return None
    m = re.search(rf"({NUM})\s*([A-Za-z]+)", raw)
    return to_minutes(m.group(1), m.group(2)) if m else None


# -------------------------------------------------------------------- kinetics
def km_to_mM(value, unit):
    return to_mM(value, unit)


def kcat_to_per_s(value, unit):
    v = _f(value)
    if v is None:
        return None
    u = (unit or "").strip().lower().replace(" ", "")
    if u in ("sec(-1)", "s(-1)", "s-1", "1/s", "s^-1", "persecond"):
        return round(v, 6)
    if u in ("min(-1)", "min-1", "1/min", "min^-1"):
        return round(v / 60.0, 6)
    if u in ("h(-1)", "h-1", "1/h"):
        return round(v / 3600.0, 8)
    return None


def vmax_to_umol_min_mg(value, unit):
    v = _f(value)
    if v is None:
        return None
    u = (unit or "").strip().lower().replace(" ", "").replace("μ", "u").replace("µ", "u")
    u = u.replace("·", "/").replace("^-1", "").replace("(-1)", "")
    if u in ("umol/min/mg", "umolmin/mg", "u/mg", "umol/min/mgprotein"):
        return round(v, 6)
    if u in ("nmol/min/mg",):
        return round(v / 1000.0, 6)
    if u in ("mmol/min/mg",):
        return round(v * 1000.0, 6)
    if u in ("umol/s/mg",):
        return round(v * 60.0, 6)
    return None


# ------------------------------------------------------------- parsing helpers
CONC_PAT = re.compile(rf"({NUM})\s*(mM|mmol/L|M|mol/L|uM|µM|μM|nM|pM|%\s*\(w/v\)|"
                      r"%\s*\(v/v\)|%|mg/mL|mg/ml|ug/mL|g/L|g/l)", re.I)


def parse_concentration(raw, species=""):
    """'5 mM' / '0.5 %' -> (value, unit, mM or None)."""
    if not raw:
        return None, "", None
    m = CONC_PAT.search(raw)
    if not m:
        return None, "", None
    value, unit = _f(m.group(1)), " ".join(m.group(2).split())
    return value, unit, to_mM(value, unit, species)


def parse_salinity(raw):
    if not raw:
        return None, None
    m = re.search(rf"({NUM})\s*(%|ppt|PSU|psu|g/L|g/l|g/kg|mM|M)", raw)
    if not m:
        return None, None
    g = salinity_to_g_per_L(m.group(1), m.group(2))
    return g, g_per_L_to_psu(g)


def buffer_concentration(raw):
    """Pull the buffer molarity out of a phrase like '50 mM Tris-HCl'.

    The number must not be glued to a preceding word or hyphen, or enzyme names like
    'PET2-7M for ...' parse as a -7 M buffer."""
    if not raw:
        return None
    m = re.search(r"(?<![\w.\-])(\d+(?:\.\d+)?)\s*(mM|M|mmol/L)\s+[A-Za-z]", raw)
    if not m:
        return None
    return to_mM(m.group(1), m.group(2))


if __name__ == "__main__":
    # Self-test: these must all hold for the standardisation to be trustworthy.
    assert to_celsius(323.15, "K") == 50.0
    assert to_celsius(122, "F") == 50.0
    assert to_celsius("55") == 55.0
    assert to_mM(1, "M") == 1000.0
    assert to_mM(500, "uM") == 0.5
    assert to_mM(1, "%", "NaCl") == round(10 * 1000 / 58.44, 6)      # 1 % NaCl ~ 171 mM
    assert abs(ionic_strength_from_salt("NaCl", 100) - 0.1) < 1e-9   # 1:1 salt -> I = c
    assert abs(ionic_strength_from_salt("CaCl2", 100) - 0.3) < 1e-9  # 2:1 salt -> I = 3c
    assert abs(ionic_strength_from_salt("MgCl2", 10) - 0.03) < 1e-9
    assert salinity_to_g_per_L(3.5, "%") == 35.0
    assert abs(ionic_strength_from_salinity(35.0) - SEAWATER_IONIC_STRENGTH_M) < 0.03
    assert to_minutes(2, "h") == 120.0
    assert to_minutes(30, "s") == 0.5
    assert kcat_to_per_s(60, "min(-1)") == 1.0
    assert km_to_mM(640, "uM") == 0.64
    assert parse_concentration("50 mM NaCl", "NaCl")[2] == 50.0
    assert parse_salinity("3.5 %")[0] == 35.0
    assert buffer_concentration("50 mM Tris-HCl") == 50.0
    assert plausible_ph(7.4) and not plausible_ph(19)
    assert plausible_temperature(50) and not plausible_temperature(400)
    print("standardize_units: all self-tests pass")
