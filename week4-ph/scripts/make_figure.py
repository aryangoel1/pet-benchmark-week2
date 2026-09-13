"""
Render the planned pH figure for the paper, straight from the shipped benchmark.

    python3 scripts/make_figure.py

Writes figures/figure_ph.svg -- four panels, standard library only, no plotting
dependency. The design rationale and the caption live in docs/FIGURE_PLAN.md; this
script is the executable version of that plan, so the figure can never describe a
dataset other than the one in data/ph_benchmark_v1.csv.

Panels
    A  distribution of reported pH optima, coloured by enzyme class
    B  measured outcome (residual / relative activity) against assay pH, with the
       direction of the effect -- the axis Luke's schema cannot currently hold
    C  joint pH x temperature coverage, showing where the benchmark can test both axes
    D  the audit funnel: 105 candidates -> 38 removed by rule -> 67 shipped
"""
import csv
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
FIGS = os.path.join(HERE, "figures")

W, H = 1180, 820
PAL = ["#2f6f9f", "#c2603d", "#4e8f5b", "#8a6bab", "#b8912f", "#5f9ea0",
       "#a8577a", "#7a7a7a"]
INK, MUTED, GRID = "#1c1c1c", "#666666", "#dcdcdc"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


class Canvas:
    def __init__(self):
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=11, fill=INK, anchor="start", weight="normal",
             style="normal", rotate=None):
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica,Arial,sans-serif"'
                 f' font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
                 f' font-weight="{weight}" font-style="{style}"{tr}>{esc(s)}</text>')

    def line(self, x1, y1, x2, y2, stroke=INK, w=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
                 f' stroke="{stroke}" stroke-width="{w}"{d}/>')

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, opacity=1.0, rx=0):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}"'
                 f' height="{max(h,0):.1f}" fill="{fill}" stroke="{stroke}"'
                 f' stroke-width="{sw}" opacity="{opacity}" rx="{rx}"/>')

    def circle(self, cx, cy, r, fill, stroke="#ffffff", sw=0.8, opacity=1.0):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"'
                 f' stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')

    def tri(self, cx, cy, r, fill, up=True, stroke="#ffffff", sw=0.8):
        s = -1 if up else 1
        pts = f"{cx:.1f},{cy + s * r:.1f} {cx - r:.1f},{cy - s * r * 0.8:.1f} " \
              f"{cx + r:.1f},{cy - s * r * 0.8:.1f}"
        self.add(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}"'
                 f' stroke-width="{sw}"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" '
                f'fill="#ffffff"/>\n' + "\n".join(self.parts) + "\n</svg>\n")


def panel_frame(c, x, y, w, h, letter, title):
    c.text(x - 26, y - 14, letter, size=15, weight="bold")
    c.text(x, y - 14, title, size=12, weight="bold")
    c.line(x, y + h, x + w, y + h, INK, 1.1)
    c.line(x, y, x, y + h, INK, 1.1)


def main():
    with open(os.path.join(DATA, "ph_benchmark_v1.csv"),
              encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    stats = json.load(open(os.path.join(DATA, "ph_stats.json"), encoding="utf-8"))

    c = Canvas()
    c.text(40, 34, "The Week-4 pH benchmark for plastic-degrading enzymes",
           size=17, weight="bold")
    c.text(40, 54,
           f"{stats['shipped']} curated measurements - {stats['distinct_papers_shipped']}"
           f" open-access articles - every value read against its source sentence",
           size=11.5, fill=MUTED)

    # ---------------- Panel A : pH optimum distribution ----------------------
    px, py, pw, ph = 78, 106, 470, 210
    opt = [r for r in rows if r["measurement_type"] == "pH optimum" and num(r["pH"])]
    classes = [k for k, _ in Counter(r["enzyme_class"] or "unclassified"
                                     for r in opt).most_common()]
    colour = {k: PAL[i % len(PAL)] for i, k in enumerate(classes)}
    panel_frame(c, px, py, pw, ph, "A",
                f"Reported pH optima  (n = {len(opt)})")

    lo, hi, step = 3.0, 9.5, 0.5
    nb = int(round((hi - lo) / step))
    bins = [defaultdict(int) for _ in range(nb)]
    for r in opt:
        v = num(r["pH"])
        b = min(nb - 1, max(0, int((v - lo) / step)))
        bins[b][r["enzyme_class"] or "unclassified"] += 1
    peak = max((sum(b.values()) for b in bins), default=1)
    bw = pw / nb

    for k in range(0, peak + 1, max(1, peak // 4)):
        yy = py + ph - (k / peak) * ph
        c.line(px, yy, px + pw, yy, GRID, 0.8)
        c.text(px - 7, yy + 3.5, str(k), size=9.5, fill=MUTED, anchor="end")
    for i in range(nb):
        acc = 0
        for cl in classes:
            n = bins[i][cl]
            if not n:
                continue
            hgt = (n / peak) * ph
            c.rect(px + i * bw + 1.5, py + ph - acc - hgt, bw - 3, hgt,
                   fill=colour[cl], opacity=0.92)
            acc += hgt
    for i in range(nb + 1):
        v = lo + i * step
        if abs(v - round(v)) < 1e-9:
            c.line(px + i * bw, py + ph, px + i * bw, py + ph + 4, INK, 1)
            c.text(px + i * bw, py + ph + 17, f"{v:.0f}", size=9.5, anchor="middle")
    c.text(px + pw / 2, py + ph + 36, "pH optimum", size=11, anchor="middle")
    c.text(px - 40, py + ph / 2, "measurements", size=10.5, anchor="middle",
           fill=INK, rotate=-90)

    ly = py + 6
    for cl in classes:
        c.rect(px + pw - 150, ly - 8, 9, 9, fill=colour[cl])
        c.text(px + pw - 136, ly, cl[:24], size=9, fill=INK)
        ly += 13

    # ---------------- Panel B : outcome vs pH -------------------------------
    qx, qy, qw, qh = 660, 106, 440, 210
    out = [r for r in rows if num(r["relative_activity_pct"]) is not None
           and num(r["pH"]) is not None]
    panel_frame(c, qx, qy, qw, qh, "B",
                f"Activity retained at pH  (n = {len(out)})")
    xlo, xhi = 3.0, 12.5
    for k in (0, 25, 50, 75, 100):
        yy = qy + qh - (k / 105.0) * qh
        c.line(qx, yy, qx + qw, yy, GRID, 0.8)
        c.text(qx - 7, yy + 3.5, str(k), size=9.5, fill=MUTED, anchor="end")
    yy50 = qy + qh - (50 / 105.0) * qh
    c.line(qx, yy50, qx + qw, yy50, "#c2603d", 1.0, dash="4,3")
    c.text(qx + qw - 3, yy50 - 5, "50% retained", size=8.5, fill="#c2603d", anchor="end")
    for v in range(3, 13):
        xx = qx + (v - xlo) / (xhi - xlo) * qw
        c.line(xx, qy + qh, xx, qy + qh + 4, INK, 1)
        c.text(xx, qy + qh + 17, str(v), size=9.5, anchor="middle")
    for r in out:
        v, a = num(r["pH"]), num(r["relative_activity_pct"])
        xx = qx + (v - xlo) / (xhi - xlo) * qw
        yy = qy + qh - (min(a, 105) / 105.0) * qh
        d = r["direction"]
        col = {"stabilising": "#4e8f5b", "destabilising": "#c2603d"}.get(d, "#7a7a7a")
        if d == "stabilising":
            c.tri(xx, yy, 5.2, col, up=True)
        elif d == "destabilising":
            c.tri(xx, yy, 5.2, col, up=False)
        else:
            c.circle(xx, yy, 4.2, col)
    c.text(qx + qw / 2, qy + qh + 36, "assay pH", size=11, anchor="middle")
    for i, (lbl, col, up) in enumerate([("retained", "#4e8f5b", True),
                                        ("lost", "#c2603d", False)]):
        c.tri(qx + 14, qy + 14 + i * 15, 5.2, col, up=up)
        c.text(qx + 26, qy + 18 + i * 15, lbl, size=9.5)
    c.text(qx + qw - 3, qy + 14, "% of maximal / initial activity",
           size=9, fill=MUTED, anchor="end")

    # ---------------- Panel C : pH x temperature coverage -------------------
    rx, ry, rw, rh = 78, 420, 470, 210
    both = [r for r in rows if num(r["pH"]) is not None
            and num(r["temperature_c"]) is not None]
    panel_frame(c, rx, ry, rw, rh, "C",
                f"Joint pH x temperature coverage  (n = {len(both)})")
    xlo, xhi, tlo, thi = 3.0, 12.5, 0.0, 80.0
    for t in range(0, 81, 20):
        yy = ry + rh - (t - tlo) / (thi - tlo) * rh
        c.line(rx, yy, rx + rw, yy, GRID, 0.8)
        c.text(rx - 7, yy + 3.5, str(t), size=9.5, fill=MUTED, anchor="end")
    for v in range(3, 13):
        xx = rx + (v - xlo) / (xhi - xlo) * rw
        c.line(xx, ry + rh, xx, ry + rh + 4, INK, 1)
        c.text(xx, ry + rh + 17, str(v), size=9.5, anchor="middle")
    jitter = Counter()
    for r in both:
        v, t = num(r["pH"]), num(r["temperature_c"])
        key = (round(v, 1), round(t))
        off = jitter[key] * 3.4
        jitter[key] += 1
        xx = rx + (v - xlo) / (xhi - xlo) * rw + off
        yy = ry + rh - (t - tlo) / (thi - tlo) * rh
        cl = r["enzyme_class"] or "unclassified"
        c.circle(xx, yy, 4.6, colour.get(cl, "#7a7a7a"), opacity=0.88)
    c.text(rx + rw / 2, ry + rh + 36, "pH", size=11, anchor="middle")
    c.text(rx + 8, ry + 16, "temperature (°C)", size=10, fill=MUTED)

    # ---------------- Panel D : audit funnel --------------------------------
    fx, fy, fw = 660, 420, 440
    c.text(fx - 26, fy - 14, "D", size=15, weight="bold")
    c.text(fx, fy - 14, "What the audit removed, and why", size=12, weight="bold")

    rule_names = {
        "PH-X1": "methods / protocol sentence",
        "PH-X2": "range endpoint read as optimum",
        "PH-X3": "wrong enzyme attributed",
        "PH-X4": "ambiguous - several enzymes",
        "PH-X5": "model-predicted value",
        "PH-X6": "off-target enzyme class",
        "PH-X7": "secondhand / review sentence",
        "PH-X8": "analytical-method pH",
        "PH-X9": "no measurement of that type",
        "PH-X10": "duplicate measurement",
        "PH-X11": "garbled table cell",
        "PH-X12": "no outcome at that pH",
    }
    counts = stats["exclusion_rule_counts"]
    order = sorted(counts.items(), key=lambda kv: -kv[1])
    bar_max = max(counts.values())
    bh, gap = 15.5, 4.0
    yy = fy + 6
    c.text(fx, yy, f"{stats['candidates']} candidate rows inherited from Week 2",
           size=10.5, fill=MUTED)
    yy += 16
    for code, n in order:
        wpx = (n / bar_max) * 150
        c.rect(fx + 172, yy - bh + 4, wpx, bh - 4, fill="#c2603d", opacity=0.82, rx=1.5)
        c.text(fx, yy, f"{code}  {rule_names.get(code, code)}"[:34], size=9.3)
        c.text(fx + 176 + wpx, yy, str(n), size=9.3, fill=INK)
        yy += bh + gap - 3
    yy += 6
    c.line(fx, yy, fx + fw - 20, yy, GRID, 1)
    yy += 16
    c.text(fx, yy, f"{stats['excluded']} rows removed "
                   f"({stats['exclusion_rate_pct']}% of candidates)", size=10.5)
    yy += 16
    c.text(fx, yy, f"{stats['shipped']} rows shipped - "
                   f"{stats['scored_condition_axis']} scoreable on the pH axis, "
                   f"{stats['scored_sequence_model']} by a sequence model",
           size=10.5, weight="bold")
    yy += 16
    c.text(fx, yy, f"{stats['rows_with_outcome_pct']} rows carry a recovered outcome "
                   f"(% activity) at their pH", size=10.5, fill=MUTED)

    c.text(40, H - 18,
           "Rows counted once per exclusion rule; a row can fire more than one rule. "
           "Generated by scripts/make_figure.py from data/ph_benchmark_v1.csv.",
           size=9, fill=MUTED)

    os.makedirs(FIGS, exist_ok=True)
    path = os.path.join(FIGS, "figure_ph.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(c.svg())
    print(f"wrote {path}")
    print(f"  panel A: {len(opt)} pH optima")
    print(f"  panel B: {len(out)} rows with a recovered outcome")
    print(f"  panel C: {len(both)} rows with pH and temperature")
    print(f"  panel D: {stats['excluded']} exclusions across "
          f"{len(counts)} rules")


if __name__ == "__main__":
    main()
