# -*- coding: utf-8 -*-
"""
Generator: Naturwissenschaften · Klasse 5 und 6 — Kursplan 2026/27
Erzeugt index.html (Kursübersicht) + Lernpfad-Startseiten + nutzt geteilte Assets.
Einzige Quelle der Wahrheit für Inhalte, Kalender und Freischalt-Daten.
"""
import os, html
from datetime import date, timedelta
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
LP_DIR = os.path.join(BASE, "lernpfade")
ASSET_DIR = os.path.join(BASE, "assets")
os.makedirs(LP_DIR, exist_ok=True)

# ---------------------------------------------------------------- Kalender (identisch zu Profilkurs)
START = date(2026, 8, 24)
SKIP = {date(2026,8,31),  # LP01 fiel aus, fand erst 07.09. statt -> alles ab SJW1 um 1 Woche verschoben
        date(2026,10,19), date(2026,10,26), date(2026,12,21), date(2026,12,28),
        date(2027,2,1), date(2027,3,22), date(2027,3,29)}
CAL = {}          # sjw -> (montag, freitag)
mon, sjw = START, 0
while sjw < 37:
    if mon in SKIP:
        mon += timedelta(days=7); continue
    sjw += 1
    CAL[sjw] = (mon, mon + timedelta(days=4))
    mon += timedelta(days=7)
CAL = {k - 1: v for k, v in CAL.items()}   # SJW zaehlt ab 0

def de(d):  # dd.mm.yyyy
    return d.strftime("%d.%m.%Y")
def dm(d):  # dd.mm.
    return d.strftime("%d.%m.")
def iso(d):
    return d.strftime("%Y-%m-%d")

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- Werkzeuge (URLs)
T = {
  "scratch": ("Scratch", "https://scratch.mit.edu/"),
  "makey": ("Makey Makey", "https://makeymakey.com/pages/how-to"),
  "jsfiddle": ("jsfiddle.net", "https://jsfiddle.net/"),
}

# ---------------------------------------------------------------- Vorwissen-SVGs (Icon-Raster)
CELL_W, CELL_H = 260, 190

def icon_cell(i, inner, cols):
    """Eine Rasterzelle: Rahmen, Nummernbadge oben links, zentriertes Icon (eigener Ursprung, unabhaengig vom Badge)."""
    col, row = i % cols, i // cols
    x, y = col * CELL_W, row * CELL_H
    cx, cy = CELL_W / 2.0, CELL_H / 2.0 + 18
    return (
        '<g transform="translate(%d,%d)">'
        '<rect x="6" y="6" width="%d" height="%d" rx="16" fill="none" stroke="#dfe9e2" stroke-width="2"/>'
        '<circle cx="28" cy="28" r="16" fill="#2e9e5b"/>'
        '<text x="28" y="34" text-anchor="middle" font-family="Fredoka,sans-serif" font-weight="700" font-size="17" fill="#fff">%d</text>'
        '<g transform="translate(%g,%g) scale(0.85)">%s</g>'
        '</g>'
    ) % (x, y, CELL_W - 12, CELL_H - 12, i + 1, cx, cy, inner)

def icon_grid(icons, cols):
    rows = -(-len(icons) // cols)  # ceil
    body = "".join(icon_cell(i, inner, cols) for i, inner in enumerate(icons))
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
            'font-family="Nunito,sans-serif">%s</svg>') % (CELL_W * cols, CELL_H * rows, body)

S = 'stroke="#163a2b" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
SF = 'stroke="#163a2b" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'  # ohne fill, fuer eigene Fuellfarbe

ICON_ZOLLSTOCK = ('<polyline points="-45,25 -20,-25 5,25 30,-25 55,25" %s/>'
                   '<line x1="-45" y1="25" x2="-45" y2="11" stroke="#163a2b" stroke-width="6"/>') % S
ICON_WAAGE = ('<rect x="-55" y="20" width="110" height="45" rx="10" %s/>'
              '<circle cx="0" cy="0" r="26" %s/>'
              '<line x1="0" y1="0" x2="10" y2="-14" stroke="#163a2b" stroke-width="5" stroke-linecap="round"/>') % (S, S)
ICON_STOPPUHR = ('<circle cx="0" cy="8" r="42" %s/>'
                  '<rect x="-10" y="-46" width="20" height="14" rx="4" %s/>'
                  '<line x1="22" y1="-30" x2="30" y2="-38" stroke="#163a2b" stroke-width="6" stroke-linecap="round"/>'
                  '<line x1="0" y1="8" x2="0" y2="-16" stroke="#163a2b" stroke-width="5" stroke-linecap="round"/>'
                  '<line x1="0" y1="8" x2="16" y2="8" stroke="#163a2b" stroke-width="5" stroke-linecap="round"/>') % (S, S)
ICON_MASSBAND = ('<circle cx="0" cy="0" r="40" %s/>'
                  '<rect x="30" y="-8" width="34" height="16" rx="3" fill="#163a2b"/>'
                  '<circle cx="0" cy="0" r="10" fill="#163a2b"/>') % S
ICON_THERMOMETER = ('<rect x="-11" y="-55" width="22" height="80" rx="11" %s/>'
                     '<circle cx="0" cy="34" r="20" fill="#163a2b"/>'
                     '<line x1="0" y1="-40" x2="0" y2="30" stroke="#ff6f59" stroke-width="8" stroke-linecap="round"/>') % S
ICON_FLEXBAND = ('<path d="M-50,-10 Q -20,30 10,-10 T 55,20" %s/>'
                  '<line x1="-40" y1="-2" x2="-40" y2="10" stroke="#163a2b" stroke-width="4"/>'
                  '<line x1="-10" y1="12" x2="-10" y2="24" stroke="#163a2b" stroke-width="4"/>'
                  '<line x1="30" y1="0" x2="30" y2="12" stroke="#163a2b" stroke-width="4"/>') % S

SVG_STECKBRIEF = icon_grid(
    [ICON_ZOLLSTOCK, ICON_WAAGE, ICON_STOPPUHR, ICON_MASSBAND, ICON_THERMOMETER, ICON_FLEXBAND], cols=3)

ICON_BLAUWAL = ('<path d="M-70,10 Q -40,-25 20,-12 Q 55,-8 65,5 Q 55,2 40,8 Q 10,18 -30,16 Q -55,15 -70,10 Z" %s fill="#2f8fe0" fill-opacity="0.18"/>'
                 '<path d="M20,-12 Q 35,-30 40,-10" %s/>'
                 '<circle cx="-55" cy="6" r="3" fill="#163a2b"/>') % (SF, S)
ICON_KOLIBRI = ('<ellipse cx="0" cy="5" rx="22" ry="14" %s fill="#ff8a3d" fill-opacity="0.18"/>'
                 '<path d="M-20,0 Q -45,-14 -55,-2 Q -45,4 -20,10" %s/>'
                 '<path d="M20,0 L 46,-4" %s/>'
                 '<circle cx="24" cy="-2" r="2.4" fill="#163a2b"/>') % (SF, S, S)
ICON_GIRAFFE = ('<line x1="0" y1="-55" x2="-8" y2="15" %s/>'
                 '<ellipse cx="0" cy="-58" rx="12" ry="9" %s fill="#8a5cf0" fill-opacity="0.18"/>'
                 '<path d="M-8,15 Q -30,25 -46,20 M-8,15 Q 14,25 30,18" %s/>'
                 '<circle cx="-5" cy="-64" r="2" fill="#163a2b"/><circle cx="4" cy="-64" r="2" fill="#163a2b"/>') % (S, SF, S)
ICON_KAMEL = ('<path d="M-45,20 Q -45,-18 -25,-14 Q -20,-26 -8,-14 Q 5,-22 10,-6 Q 20,-6 20,10 L 20,20" %s/>'
              '<line x1="-45" y1="20" x2="-45" y2="34" stroke="#163a2b" stroke-width="6" stroke-linecap="round"/>'
              '<line x1="18" y1="20" x2="18" y2="34" stroke="#163a2b" stroke-width="6" stroke-linecap="round"/>'
              '<circle cx="-38" cy="-16" r="2" fill="#163a2b"/>') % S

SVG_TIERPOSTER = icon_grid([ICON_BLAUWAL, ICON_KOLIBRI, ICON_GIRAFFE, ICON_KAMEL], cols=2)

# ---------------------------------------------------------------- Mini-Icons fuer Plickers-Nachholaufgaben (LP02)
ICON_ORANGE_FRUCHT = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="60" cy="58" r="34" fill="#ff8a3d" fill-opacity="0.85" stroke="#163a2b" stroke-width="5"/>'
    '<path d="M58,24 Q66,12 80,14" stroke="#2e9e5b" stroke-width="5" stroke-linecap="round" fill="none"/>'
    '<ellipse cx="57" cy="22" rx="5" ry="8" fill="#7a4a1e" transform="rotate(-20 57 22)"/>'
    '</svg>')
ICON_KOERPER_REIHE = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<g transform="translate(8,8)"><path d="M2,34 L2,14 L16,4 L40,4 L40,24 L26,34 Z" fill="#ff8a3d" fill-opacity="0.4" stroke="#163a2b" stroke-width="4" stroke-linejoin="round"/>'
    '<path d="M2,14 L26,14 L40,4 M26,14 L26,34" fill="none" stroke="#163a2b" stroke-width="4" stroke-linejoin="round"/></g>'
    '<g transform="translate(66,6)"><ellipse cx="20" cy="8" rx="18" ry="7" fill="#8a5cf0" fill-opacity="0.35" stroke="#163a2b" stroke-width="4"/>'
    '<path d="M2,8 L2,32 A18,7 0 0 0 38,32 L38,8" fill="#8a5cf0" fill-opacity="0.2" stroke="#163a2b" stroke-width="4"/></g>'
    '<g transform="translate(8,56)"><ellipse cx="20" cy="36" rx="18" ry="6" fill="#2f8fe0" fill-opacity="0.3" stroke="#163a2b" stroke-width="4"/>'
    '<path d="M20,4 L4,36 M20,4 L36,36" fill="none" stroke="#163a2b" stroke-width="4" stroke-linecap="round"/></g>'
    '<g transform="translate(66,56)"><circle cx="20" cy="20" r="18" fill="#ffc233" fill-opacity="0.4" stroke="#163a2b" stroke-width="4"/>'
    '<ellipse cx="20" cy="20" rx="18" ry="6" fill="none" stroke="#163a2b" stroke-width="2" stroke-opacity="0.5"/></g>'
    '</svg>')
ICON_KUGEL_RADIUS = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="60" cy="52" r="36" fill="none" stroke="#163a2b" stroke-width="4"/>'
    '<circle cx="60" cy="52" r="2.6" fill="#ff6f59"/>'
    '<line x1="60" y1="52" x2="94" y2="52" stroke="#2f8fe0" stroke-width="4" stroke-linecap="round"/>'
    '<text x="74" y="46" font-family="JetBrains Mono, monospace" font-size="14" font-weight="700" fill="#2f8fe0">r</text>'
    '<text x="52" y="40" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" fill="#ff6f59">M</text>'
    '</svg>')
ICON_KUGEL_UMFANG = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="60" cy="52" r="36" fill="#2f8fe0" fill-opacity="0.15" stroke="#163a2b" stroke-width="3"/>'
    '<ellipse cx="60" cy="52" rx="36" ry="12" fill="none" stroke="#ff6f59" stroke-width="4"/>'
    '<circle cx="60" cy="52" r="2.6" fill="#163a2b"/>'
    '</svg>')
ICON_KUGEL_VOLUMEN = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="38" cy="52" r="28" fill="#ffc233" fill-opacity="0.4" stroke="#163a2b" stroke-width="4"/>'
    '<line x1="38" y1="52" x2="60" y2="52" stroke="#2f8fe0" stroke-width="3" stroke-linecap="round"/>'
    '<text x="72" y="42" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="#163a2b">V=</text>'
    '<text x="70" y="60" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#163a2b">4/3πr³</text>'
    '</svg>')
ICON_BOOT_WESTE_SCHALE = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<g transform="translate(2,30)"><path d="M0,20 L34,20 L28,32 L6,32 Z" fill="#a9d6bd" fill-opacity="0.5" stroke="#163a2b" stroke-width="3.5" stroke-linejoin="round"/>'
    '<line x1="17" y1="20" x2="17" y2="2" stroke="#163a2b" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M17,4 L28,14 L17,14 Z" fill="#ff8a3d" fill-opacity="0.6" stroke="#163a2b" stroke-width="2"/></g>'
    '<g transform="translate(44,26)"><path d="M6,0 L26,0 L30,10 L26,38 L6,38 L2,10 Z" fill="#ffc233" fill-opacity="0.5" stroke="#163a2b" stroke-width="3.5" stroke-linejoin="round"/>'
    '<circle cx="16" cy="14" r="2.4" fill="#163a2b"/><circle cx="16" cy="24" r="2.4" fill="#163a2b"/></g>'
    '<g transform="translate(88,42)"><circle cx="16" cy="16" r="16" fill="#ff8a3d" fill-opacity="0.35" stroke="#163a2b" stroke-width="3.5"/>'
    '<circle cx="16" cy="16" r="10" fill="#fff7e2" stroke="#163a2b" stroke-width="2"/>'
    '<line x1="16" y1="6" x2="16" y2="26" stroke="#163a2b" stroke-width="1.5"/><line x1="6" y1="16" x2="26" y2="16" stroke="#163a2b" stroke-width="1.5"/></g>'
    '</svg>')
ICON_TOTES_MEER = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4,60 Q20,52 36,60 T68,60 T100,60 T116,60" fill="none" stroke="#2f8fe0" stroke-width="4" stroke-linecap="round"/>'
    '<path d="M4,72 Q20,64 36,72 T68,72 T100,72 T116,72" fill="none" stroke="#2f8fe0" stroke-width="4" stroke-linecap="round" stroke-opacity="0.5"/>'
    '<g transform="translate(60,50)"><ellipse cx="0" cy="0" rx="20" ry="7" fill="#ffe6b0" fill-opacity="0.7" stroke="#163a2b" stroke-width="2.5"/>'
    '<circle cx="16" cy="-2" r="5" fill="#ffe6b0" stroke="#163a2b" stroke-width="2.5"/></g>'
    '</svg>')
ICON_NORDSEE_OSTSEE = (
    '<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">'
    '<g transform="translate(6,10)"><rect x="0" y="0" width="46" height="80" rx="6" fill="none" stroke="#163a2b" stroke-width="3"/>'
    '<rect x="3" y="30" width="40" height="47" fill="#2f8fe0" fill-opacity="0.25"/>'
    '<circle cx="23" cy="26" r="10" fill="#ff8a3d" stroke="#163a2b" stroke-width="2.5"/>'
    '<circle cx="12" cy="50" r="1.6" fill="#163a2b"/><circle cx="30" cy="60" r="1.6" fill="#163a2b"/><circle cx="18" cy="68" r="1.6" fill="#163a2b"/><circle cx="34" cy="45" r="1.6" fill="#163a2b"/>'
    '<text x="23" y="94" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#163a2b">A</text></g>'
    '<g transform="translate(68,10)"><rect x="0" y="0" width="46" height="80" rx="6" fill="none" stroke="#163a2b" stroke-width="3"/>'
    '<rect x="3" y="30" width="40" height="47" fill="#2f8fe0" fill-opacity="0.25"/>'
    '<circle cx="23" cy="40" r="10" fill="#ff8a3d" stroke="#163a2b" stroke-width="2.5"/>'
    '<circle cx="16" cy="62" r="1.6" fill="#163a2b"/><circle cx="30" cy="70" r="1.6" fill="#163a2b"/>'
    '<text x="23" y="94" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" fill="#163a2b">B</text></g>'
    '</svg>')

# ---------------------------------------------------------------- LP03/LP04: Aräometer, Plickers-Karten
def word_card(lines, bold=False, grey=False, size=17):
    """Plickers-Begriffskarte als Vektor: zentrierter Text auf heller Karte."""
    n = len(lines)
    y0 = 48 - (n - 1) * size * 0.62 + size * 0.35
    txt = "".join('<text x="75" y="%.1f" text-anchor="middle" font-family="Nunito,sans-serif" '
                  'font-size="%d" font-weight="%d" fill="#163a2b">%s</text>'
                  % (y0 + i * size * 1.25, size, 800 if bold else 600, l) for i, l in enumerate(lines))
    return ('<svg viewBox="0 0 150 96" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="3" y="3" width="144" height="90" rx="10" fill="%s" stroke="#163a2b" stroke-opacity="0.18" stroke-width="2"/>%s</svg>'
            % ("#ececec" if grey else "#ffffff", txt))

def araeometer(x, y, s=1.0, labels=False):
    """Aräometer (Senkspindel): Stiel mit Skala, Luftkammer, Bleigewicht. (x,y) = Spitze oben."""
    def P(px, py):
        return "%.1f,%.1f" % (x + px * s, y + py * s)
    ticks = "".join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#163a2b" stroke-width="%.1f"/>'
                    % (x - 5 * s, y + (14 + i * 9) * s, x + (1 if i % 2 else 3) * s, y + (14 + i * 9) * s, 1.6 * s)
                    for i in range(11))
    pts = [(-7, 4), (-7, 120), (-7, 130), (-22, 135), (-22, 155), (-22, 175), (-12, 182), (-12, 194),
           (-12, 222), (-12, 230), (12, 230), (12, 222), (12, 194), (12, 182), (22, 175), (22, 155),
           (22, 135), (7, 130), (7, 120), (7, 4)]
    q = [P(*pt) for pt in pts]
    d = ("M%s L%s C%s %s %s C%s %s %s L%s C%s %s %s L%s C%s %s %s C%s %s %s L%s Z" % tuple(q))
    body = ('<path d="%s" fill="#e8f4fb" stroke="#163a2b" stroke-width="%.1f" stroke-linejoin="round"/>'
            % (d, 3 * s))
    top = '<path d="M%s A%.1f,%.1f 0 0 1 %s" fill="#e8f4fb" stroke="#163a2b" stroke-width="%.1f"/>' % (
        P(-7, 4.5), 7 * s, 7 * s, P(7, 4.5), 3 * s)
    lead = "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#8f99a3" stroke="#163a2b" stroke-width="%.1f"/>'
                   % (x + dx * s, y + dy * s, 3.2 * s, 0.8 * s)
                   for dx, dy in [(-6, 212), (0, 211), (6, 212), (-7, 219), (-1, 219), (5, 219), (-3, 225), (3, 225)])
    out = body + top + ticks + lead
    if labels:
        lab = [(40, "Skala"), (165, "Luft für Auftrieb"), (218, "Gewicht (Bleikugeln)")]
        for ly, t in lab:
            out += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2f8fe0" stroke-width="2"/>'
                    '<text x="%.1f" y="%.1f" font-family="Nunito,sans-serif" font-size="15" font-weight="700" fill="#163a2b">%s</text>'
                    % (x + 14 * s, y + ly * s, x + 40 * s, y + ly * s, x + 44 * s, y + ly * s + 5, t))
    return out

SVG_ARAEOMETER = ('<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg" role="img" '
                  'aria-label="Aräometer mit Skala, Luftkammer und Bleigewicht">%s</svg>' % araeometer(40, 8, 1.0, True))

def _tab(cols, widths, x0, y, h, head=False, fs=9):
    out, x = "", x0
    for c, w in zip(cols, widths):
        out += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#163a2b" stroke-width="1.2"/>' % (
            x, y, w, h, "#ececec" if head else "#fff")
        lines = c if isinstance(c, list) else [c]
        for i, l in enumerate(lines):
            ty = y + h / 2 + fs * 0.35 + (i - (len(lines) - 1) / 2) * fs * 1.2
            out += ('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Nunito,sans-serif" font-size="%d" '
                    'font-weight="%d" fill="#163a2b">%s</text>' % (x + w / 2, ty, fs, 800 if head else 600, l))
        x += w
    return out

_W5 = [44, 26, 92, 50, 78]
ICON_GROESSEN_KOPF = (
    '<svg viewBox="0 0 300 140" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="5" y="4" width="290" height="40" fill="#111"/>'
    '<text x="12" y="16" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">Ordne die Begriffe (Symbol der Einheit, Einheiten,</text>'
    '<text x="12" y="28" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">mögliche Messinstrumente, Symbol der Größe und</text>'
    '<text x="12" y="40" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">Größe) diesem Beispiel zu.</text>'
    '<text x="5" y="57" font-family="Nunito,sans-serif" font-size="10" font-weight="700" fill="#2f6fa8">Übersicht zu naturwissenschaftlichen Größen</text>'
    '<rect x="5" y="62" width="290" height="30" fill="#111"/>'
    + "".join('<circle cx="%.1f" cy="77" r="10" fill="%s"/><text x="%.1f" y="81" text-anchor="middle" '
              'font-family="Fredoka,sans-serif" font-size="12" font-weight="700" fill="#fff">%d</text>'
              % (5 + sum(_W5[:i]) + _W5[i] / 2, col, 5 + sum(_W5[:i]) + _W5[i] / 2, i + 1)
              for i, col in enumerate(["#2f8fe0", "#ff8a3d", "#8a5cf0", "#2e9e5b", "#ff6f59"]))
    + _tab(["Länge", "l", ["Meter, Millimeter,", "Kilometer, Zentimeter"], ["m, mm,", "km, cm"], ["Maßband, Zoll-", "stock, Lineal"]],
           _W5, 5, 92, 44, fs=8.5)
    + '</svg>')

ICON_DICHTE_ZEILE = (
    '<svg viewBox="0 0 300 140" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="5" y="4" width="200" height="40" fill="#111"/>'
    '<text x="11" y="17" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">Schlage experimentelle Bestimmungs-</text>'
    '<text x="11" y="28" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">möglichkeiten für die Dichte von</text>'
    '<text x="11" y="39" font-family="Nunito,sans-serif" font-size="9.5" font-weight="800" fill="#fff">Festkörpern vor.</text>'
    + _tab(["Dichte", ["ρ", "(Rho)"], ["Gramm pro Milliliter,", "Gramm pro Kubik-", "zentimeter"], ["g/ml,", "g/cm³"], "?"],
           [40, 30, 78, 36, 26], 5, 54, 72, fs=8.5)
    + araeometer(262, 6, 0.55)
    + '</svg>')

def fr(num, den):
    """Bruch als HTML (Zähler über Nenner)."""
    return '<span class="fr"><span>%s</span><span>%s</span></span>' % (num, den)

def step_card(title, img, alt, given, mass, steps):
    """Körper-Karte mit stufenweise aufklappbaren Hilfen: jede Hilfe steckt in der vorherigen."""
    inner = ""
    for i in range(len(steps) - 1, -1, -1):
        summary, body = steps[i]
        inner = ('<details class="step"><summary>%s</summary><div class="step-body">%s%s</div></details>'
                 % (summary, body, inner))
    return ('<article class="bc"><h3>%s</h3>'
            '<div class="bc-top"><img src="lp04-img/%s" alt="%s" loading="lazy">'
            '<div class="bc-given"><b>Gegeben (Tinkercad):</b><br>%s<br><b>Gewogene Masse:</b><br><i>m</i> = %s</div></div>'
            '%s</article>') % (title, img, alt, given, mass, inner)

def density_steps(formula, insert, volume, m, v_ml, rho, extra_tip=""):
    """Fünf Standard-Hilfen: Formel → Einsetzen → Volumen → Dichte → Ergebnis."""
    return [
        ("Hilfe 1 · Welche Volumenformel passt?",
         '<p class="m">%s</p>%s' % (formula, extra_tip)),
        ("Hilfe 2 · Maße einsetzen",
         '<p class="m">%s</p>' % insert),
        ("Hilfe 3 · Volumen ausrechnen",
         '<p class="m">%s</p><p class="tip">1 cm³ = 1 ml. Das Volumen ist höchstens 30 ml, so wie in Tinkercad gefordert. ✓</p>' % volume),
        ("Hilfe 4 · Dichte berechnen: ρ = m / V",
         '<p class="m"><i>ρ</i> = %s = %s</p>' % (fr("<i>m</i>", "<i>V</i>"), fr("%s g" % m, "%s ml" % v_ml))),
        ("Ergebnis",
         '<p class="m res"><i>ρ</i> ≈ %s %s</p><p class="tip">Die Dichte ist kleiner als die von Wasser (1 g/ml). '
         'Der Körper ist innen größtenteils hohl (ca. 15 %% Füllung) und schwimmt deshalb.</p>' % (rho, fr("g", "ml"))),
    ]

SEC_LP04_STEPS = (
    '<section class="lp-sec"><h2><span class="dot"></span>Dichtebestimmungen Schritt für Schritt</h2>'
    '<p class="vw-intro">Die Körper wurden in Tinkercad modelliert (Volumen höchstens 30 ml), im 3D-Drucker aus PLA gedruckt und gewogen. '
    'Berechne für jeden Körper zuerst das <b>Volumen</b> und danach die <b>Dichte</b>. Kommst du nicht weiter, klappe die nächste Hilfe auf, '
    'aber immer nur so viele, wie du wirklich brauchst. Hast du deinen eigenen Körper gewogen, rechne mit deiner Masse, sonst mit der Beispielmasse.</p>'
    '<h3 class="bc-group">Abb. 1 · Quader, Zylinder, Halbkugel</h3><div class="bc-list">'
    + step_card("1) Quader", "quader.svg", "Quader mit a = 2 cm, a = 2 cm, h = 1,5 cm",
                "<i>a</i> = 2 cm, <i>h</i> = 1,5 cm", "2,7 g",
                density_steps("<i>V</i> = <i>a</i> · <i>a</i> · <i>h</i>",
                              "<i>V</i> = 2 cm · 2 cm · 1,5 cm",
                              "<i>V</i> = 6 cm³ = 6 ml",
                              "2,7", "6", "0,45",
                              '<p class="tip">Grundfläche (Quadrat <i>a</i> · <i>a</i>) mal Höhe <i>h</i>.</p>'))
    + step_card("2) Zylinder", "zylinder.svg", "Zylinder mit d = 2 cm, h = 4 cm",
                "<i>d</i> = 2 cm, <i>h</i> = 4 cm", "4,8 g",
                density_steps("<i>V</i> = π · (%s)² · <i>h</i>" % fr("<i>d</i>", "2"),
                              "<i>V</i> = π · (%s)² · 4 cm = π · (1 cm)² · 4 cm" % fr("2 cm", "2"),
                              "<i>V</i> = π · 4 cm³ ≈ 12,57 cm³ = 12,57 ml",
                              "4,8", "12,57", "0,38",
                              '<p class="tip">Die Grundfläche ist ein Kreis: π · <i>r</i>², und der Radius ist der halbe Durchmesser: <i>r</i> = <i>d</i> / 2.</p>'))
    + step_card("3) Halbkugel", "halbkugel.svg", "Halbkugel mit d = 4 cm",
                "<i>d</i> = 4 cm", "6,1 g",
                density_steps("<i>V</i> = %s · π · <i>d</i>³" % fr("1", "12"),
                              "<i>V</i> = %s · π · (4 cm)³ = %s · π · 64 cm³" % (fr("1", "12"), fr("1", "12")),
                              "<i>V</i> = %s · π cm³ ≈ 16,76 cm³ = 16,76 ml" % fr("64", "12"),
                              "6,1", "16,76", "0,36",
                              '<p class="tip">Eine ganze Kugel hat <i>V</i> = %s · π · <i>d</i>³, die Halbkugel die Hälfte davon.</p>' % fr("1", "6")))
    + '</div><h3 class="bc-group">Abb. 2 · Pyramide, Kegel, Prisma</h3><div class="bc-list">'
    + step_card("4) Quadratische Pyramide", "pyramide.svg", "Quadratische Pyramide mit a = 4 cm, h = 5 cm",
                "<i>a</i> = 4 cm, <i>h</i> = 5 cm", "9,7 g",
                density_steps("<i>V</i> = %s · <i>a</i>² · <i>h</i>" % fr("1", "3"),
                              "<i>V</i> = %s · (4 cm)² · 5 cm = %s · 16 cm² · 5 cm" % (fr("1", "3"), fr("1", "3")),
                              "<i>V</i> = %s cm³ ≈ 26,67 cm³ = 26,67 ml" % fr("80", "3"),
                              "9,7", "26,67", "0,36",
                              '<p class="tip">Spitze Körper wie Pyramide und Kegel haben genau ein Drittel des Volumens einer Säule mit gleicher Grundfläche und Höhe.</p>'))
    + step_card("5) Kegel", "kegel.svg", "Kegel mit d = 4 cm, h = 6,5 cm",
                "<i>d</i> = 4 cm, <i>h</i> = 6,5 cm", "9,8 g",
                density_steps("<i>V</i> = %s · π · (%s)² · <i>h</i>" % (fr("1", "3"), fr("<i>d</i>", "2")),
                              "<i>V</i> = %s · π · (%s)² · 6,5 cm = %s · π · (2 cm)² · 6,5 cm" % (fr("1", "3"), fr("4 cm", "2"), fr("1", "3")),
                              "<i>V</i> = %s · π cm³ ≈ 27,23 cm³ = 27,23 ml" % fr("26", "3"),
                              "9,8", "27,23", "0,36",
                              '<p class="tip">Wie beim Zylinder, aber mal %s, weil der Kegel spitz zuläuft.</p>' % fr("1", "3")))
    + step_card("6) Dreieckiges Prisma", "prisma.svg", "Dreieckiges Prisma mit g = 3 cm, h_g = 2,5 cm, h_p = 7 cm",
                "<i>g</i> = 3 cm, <i>h</i><sub>g</sub> = 2,5 cm, <i>h</i><sub>p</sub> = 7 cm", "10,7 g",
                density_steps("<i>V</i> = %s · <i>g</i> · <i>h</i><sub>g</sub> · <i>h</i><sub>p</sub>" % fr("1", "2"),
                              "<i>V</i> = %s · 3 cm · 2,5 cm · 7 cm = %s · 7,5 cm² · 7 cm" % (fr("1", "2"), fr("1", "2")),
                              "<i>V</i> = 26,25 cm³ = 26,25 ml",
                              "10,7", "26,25", "0,41",
                              '<p class="tip">Dreiecksfläche (%s · <i>g</i> · <i>h</i><sub>g</sub>) mal Länge des Prismas <i>h</i><sub>p</sub>.</p>' % fr("1", "2")))
    + '</div></section>')

SEC_LP03_INFO = (
    '<section class="lp-sec"><h2><span class="dot"></span>Info: Das Aräometer</h2>'
    '<div class="info-row"><div class="fig ar-fig">%s</div><div class="info-text">'
    '<p>Das <b>Aräometer</b>, auch Senkwaage, Senkspindel, Dichtespindel oder Hydrometer genannt, ist ein Messgerät zur Bestimmung '
    'der <b>Dichte</b> (oder des spezifischen Gewichts) von Flüssigkeiten.</p>'
    '<p>Es schwimmt senkrecht: Unten sorgt ein Gewicht für einen stabilen Stand, darüber gibt eine Luftkammer Auftrieb. '
    'Wie tief es eintaucht, liest man an der Skala ab.</p>'
    '<p><b>Forschungsfrage:</b> Würde eine Orange in der Nordsee oder in der Ostsee tiefer eintauchen? '
    'Heute wird deine Orange selbst zum Aräometer.</p></div></div></section>'
) % SVG_ARAEOMETER

CSS_LP03 = """
.info-row { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 1.1rem; align-items: start; }
.ar-fig { margin: 0; padding: 0.5rem; }
.info-text p { margin: 0 0 0.7rem; }
@media (max-width: 600px) { .info-row { grid-template-columns: 1fr; } .ar-fig { max-width: 240px; } }
"""

CSS_LP04 = """
.qz-icon-fig.wide { width: 150px; height: 96px; padding: 0; background: none; border: none; }
.qz-icon-fig.xl { width: 340px; height: 160px; padding: 0.2rem; background: #fff; }
@media (max-width: 600px) {
  .qz-item-row { flex-direction: column; }
  .qz-icon-fig.xl { width: 100%; max-width: 340px; height: auto; }
  .qz-icon-fig.xl svg { height: auto; }
}
.bc-group { font-family: 'Fredoka', sans-serif; font-size: 1.05rem; color: var(--ink-soft); margin: 1.2rem 0 0.7rem; }
.bc-list { display: grid; gap: 1rem; }
.bc { background: var(--card); border: 1.5px solid var(--line); border-radius: 16px; padding: 1rem 1.1rem; }
.bc h3 { font-family: 'Fredoka', sans-serif; font-size: 1.15rem; margin: 0 0 0.6rem; color: var(--ink); }
.bc-top { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 1rem; align-items: center; }
.bc-top img { width: 100%; height: auto; display: block; border-radius: 10px; }
.bc-given { font-size: 0.95rem; line-height: 1.7; }
@media (max-width: 600px) { .bc-top { grid-template-columns: 1fr; } }
details.step { margin-top: 0.7rem; border: 1.5px solid var(--line); border-radius: 12px; background: var(--bg-2); }
details.step > summary { cursor: pointer; list-style: none; padding: 0.55rem 0.8rem; font-family: 'Fredoka', sans-serif; font-weight: 600; color: var(--primary-edge); display: flex; align-items: center; gap: 0.5rem; }
details.step > summary::-webkit-details-marker { display: none; }
details.step > summary::before { content: "▸"; display: inline-block; transition: transform 0.15s ease; }
details.step[open] > summary::before { transform: rotate(90deg); }
.step-body { padding: 0 0.8rem 0.7rem; }
.step-body > details.step { margin-left: -0.8rem; margin-right: -0.8rem; margin-bottom: -0.7rem; border-left: none; border-right: none; border-bottom: none; border-radius: 0 0 12px 12px; }
.step-body .m { font-size: 1.08rem; margin: 0.2rem 0 0.4rem; line-height: 2.4; }
.step-body .tip { font-size: 0.86rem; color: var(--ink-soft); margin: 0 0 0.5rem; }
.step-body .res { font-weight: 800; color: var(--primary-edge); }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.86em; line-height: 1.15; margin: 0 0.12em; }
.fr > span:first-child { border-bottom: 1.5px solid currentColor; padding: 0 0.2em; }
.fr > span:last-child { padding: 0 0.2em; }
.sol-fig { display: block; width: 100%; height: auto; margin: 0.6rem 0; border-radius: 10px; border: 1px solid var(--line); }
"""

# ---------------------------------------------------------------- Kursinhalt
# Jedes LP: no, sjw, title, goal, tasks[], tools[keys], fast, tags[], solution[], kind, quiz(optional), vorwissen(optional)
UNITS = [
 # =================== 00 SCHWIMMEN UND SINKEN ===================
 dict(num="00", title="Schwimmen und Sinken",
      key="#2f8fe0", key2="#1f6fb8", tint="rgba(47,143,224,0.10)",
      lps=[
        dict(no=0, sjw=0, kind="lernpfad", title="Dein Naturwissenschaftlicher Steckbrief",
             goal="Du lernst sechs wichtige physikalische Größen kennen (Länge, Gewicht, Puls, Fußlänge, Temperatur, Halsumfang) und misst sie an dir selbst mit dem passenden Messgerät.",
             tasks=["Schätze zuerst deine Körpergröße, dein Gewicht, deinen Ruhepuls, deine Fußlänge, deine Körpertemperatur und deinen Halsumfang.",
                    "Miss an sechs Stationen (Zollstock, Personenwaage, Stoppuhr, Maßband mit Schuhgrößentabelle, Fieberthermometer, flexibles Maßband) die echten Werte und trage sie mit der richtigen Einheit in dein Versuchsprotokoll ein.",
                    "Berechne den Durchschnitt der Fußlängen deines gesamten Nawikurses: Ø = Summe der Messwerte ÷ Anzahl der Messwerte."],
             tools=[],
             fast="Finde für deine gemessenen Größen jeweils ein Tier mit einer besonders großen Abweichung — wer im Kurs findet den größten Unterschied zu einem Wal, einem Kolibri oder einer Giraffe?",
             tags=["Experimentieren", "Messen & Größen"],
             vorwissen=[
               dict(cap="Bild 1 · Sechs Messstationen", svg=SVG_STECKBRIEF, quiz=[
                 dict(q="Benenne das abgebildete Messinstrument (Teil 1).",
                      done="Richtig — das ist der Zollstock.",
                      opts=[("Zollstock", True, None), ("Schere", False, "Eine Schere schneidet, sie misst nicht."),
                            ("Zickzackholz", False, "Nah dran, aber der Fachbegriff ist Zollstock."), ("Zoll", False, "Zoll ist eine Einheit, kein Gerät.")]),
                 dict(q="Benenne das abgebildete Messinstrument (Teil 2).",
                      done="Richtig — das ist die Waage.",
                      opts=[("Waage", True, None), ("Vaage", False, "Fast richtig geschrieben, aber falsch."),
                            ("Vage", False, "Das ist kein Messgerät."), ("Wage", False, "Fehlt ein Buchstabe — es heißt Waage.")]),
                 dict(q="Nenne die physikalische Größe, die Teil 3 (Stoppuhr) ermittelt.",
                      done="Richtig — Zeit.",
                      opts=[("Zeit", True, None), ("Sekunden", False, "Sekunden sind die Einheit, nicht die Größe."),
                            ("Uhr", False, "Das ist der Gerätename, nicht die Größe."), ("Stunden", False, "Stunden sind eine Einheit, keine Größe.")]),
                 dict(q="Lies den maximalen Wert ab, den das metallische Maßband (Teil 4) ermitteln kann.",
                      done="Richtig — 3 Meter.",
                      opts=[("3 Meter", True, None), ("3 Minuten", False, "Ein Maßband misst Länge, keine Zeit."),
                            ("3 Magnete", False, "Das Maßband hat nichts mit Magneten zu tun."), ("3 Maßbänder", False, "Es geht um den Skalenwert, nicht die Anzahl.")]),
                 dict(q="Nenne die physikalische Größe, die mit Teil 5 (Thermometer) ermittelt wird.",
                      done="Richtig — Temperatur.",
                      opts=[("Temperatur", True, None), ("° C", False, "Grad Celsius ist die Einheit, nicht die Größe."),
                            ("Grad Celsius", False, "Auch das ist die Einheit."), ("Fieber", False, "Fieber ist nur ein möglicher Messwert, keine Größe.")]),
                 dict(q="Benenne die Einheit des Teil 6 (flexiblen Maßbandes).",
                      done="Richtig — Zentimeter.",
                      opts=[("Zentimeter (cm)", True, None), ("Meter (m)", False, "Ein flexibles Maßband ist meist in cm skaliert."),
                            ("Millimeter (mm)", False, "Zu klein für die übliche Skala."), ("Kilometer (km)", False, "Viel zu groß für ein Maßband.")]),
               ]),
             ],
             quiz=[
               dict(q="Wähle den Messwert, der nicht zu den anderen drei passt.",
                    done="Richtig — 587 000 mg entspricht 587 g, nicht 58,7 kg.",
                    opts=[("587 000 mg", True, None), ("58,7 kg", False, "58,7 kg entsprechen 58 700 g — passt zu den anderen."),
                          ("0,0587 t", False, "0,0587 t entsprechen ebenfalls 58,7 kg."), ("58 700 g", False, "Das entspricht genau 58,7 kg.")]),
               dict(q="Wähle den Messwert, der nicht zu den anderen drei passt.",
                    done="Richtig — 0,0178 km sind 17,8 m, nicht 1,78 m.",
                    opts=[("0,0178 km", True, None), ("178 cm", False, "178 cm entsprechen 1,78 m."),
                          ("1,78 m", False, "Das ist der Ausgangswert selbst."), ("1780 mm", False, "1780 mm entsprechen ebenfalls 1,78 m.")]),
             ],
             solution=["Sechs Messgeräte → sechs physikalische Größen: Zollstock (Länge, m), Waage (Masse, kg), Stoppuhr (Puls/Zeit, bpm), Maßband (Länge, cm), Fieberthermometer (Temperatur, °C), flexibles Maßband (Umfang, cm).",
                       "Durchschnitt = Summe aller Messwerte ÷ Anzahl der Messwerte — Beispiel: Ø = (19 cm + 21 cm + 20 cm) ÷ 3 = 20 cm."]),
        dict(no=1, sjw=1, kind="lernpfad", title="Naturwissenschaftliche Größen im Tierreich",
             goal="Du rechnest Messwerte aus dem Tierreich (Gewicht, Länge, Zeit) mit dem Einheitenleiter-Algorithmus sicher in andere Einheiten um.",
             tasks=["Wende den Algorithmus „Einheitenleiter“ an: Einheit erkennen, dann Schritt für Schritt zur Ziel-Einheit gehen. Von größer zu kleiner wird mal Faktor gerechnet, von kleiner zu größer geteilt durch Faktor. Komma-Trick: ×1000 verschiebt das Komma 3 Stellen nach rechts, ÷1000 verschiebt es 3 Stellen nach links.",
                    "Rechne auf deinem Arbeitsblatt die Messwerte von sieben Tieren und einer Pflanze um: Elefanten-Gewicht (kg in g und mg), Katzen-Gewicht (kg in g und mg), Giraffen-Höhe (m in cm und km), Bambus-Wachstum (cm in m und mm), Schildkröten-Gewicht (g in kg und mg) sowie Faultier-Schlafzeit (h in min) und Kolibri-Gewicht (g in mg).",
                    "Kontrolliert eure Ergebnisse gemeinsam am Tisch, bevor ihr die Musterlösung unten aufdeckt."],
             tools=[],
             fast="Zusatzaufgabe vom Arbeitsblatt: Ein Gepard läuft 120 km/h. Rechne die Geschwindigkeit in m/s (Meter pro Sekunde) um. Dabei musst du zwei Einheiten gleichzeitig wechseln, km in m und h in s.",
             tags=["Größen & Einheiten", "Kopfrechnen"],
             companion=dict(file="lp01-groessen.html", label="interaktiven Umrechnungs-Anleitung zu allen acht Tieren"),
             vorwissen=[
               dict(cap="Bild 1 · Tiere mit besonderen Maßen", svg=SVG_TIERPOSTER, quiz=[
                 dict(q="Teil 1 kann über 30 m lang und rund 150 Tonnen schwer werden. Welches Tier ist das?",
                      done="Richtig — der Blauwal, das schwerste Tier der Erde.",
                      opts=[("Pottwal", False, "Der Pottwal ist deutlich kleiner als der Blauwal."), ("Blauwal", True, None),
                            ("Weißer Hai", False, "Haie werden nicht annähernd so schwer."), ("Elefant", False, "Elefanten leben an Land und wiegen viel weniger.")]),
                 dict(q="Teil 2 hat mit bis zu 1200 Schlägen pro Minute den schnellsten Puls im Tierreich. Welches Tier ist das?",
                      done="Richtig — der Kolibri.",
                      opts=[("Spatz", False, "Spatzen haben einen schnellen, aber deutlich niedrigeren Puls."), ("Maus", False, "Mäuse haben einen schnellen Puls, aber nicht so extrem."),
                            ("Kolibri", True, None), ("Adler", False, "Große Vögel haben einen eher langsamen Puls.")]),
                 dict(q="Teil 3 hat einen Hals von bis zu 2 m Länge. Welches Tier ist das?",
                      done="Richtig — die Giraffe.",
                      opts=[("Kamel", False, "Kamele haben einen kurzen Hals."), ("Strauß", False, "Der Straußenhals ist deutlich kürzer."),
                            ("Pferd", False, "Pferde haben einen normalen Hals."), ("Giraffe", True, None)]),
                 dict(q="Teil 4 kann seine Körpertemperatur zwischen 34 °C und 41 °C schwanken lassen, um Wasser zu sparen. Welches Tier ist das?",
                      done="Richtig — das Kamel.",
                      opts=[("Eisbär", False, "Eisbären halten ihre Temperatur sehr konstant."), ("Kamel", True, None),
                            ("Pinguin", False, "Auch Pinguine halten eine sehr konstante Temperatur."), ("Löwe", False, "Löwen schwanken nicht so stark in der Temperatur.")]),
               ]),
             ],
             catchup=[
               dict(q="Ein Elefant wiegt 3.200.000 g. Wie viel sind das in kg?",
                    done="Richtig, 3.200.000 g sind 3.200 kg.",
                    opts=[("320 kg", False, "Das wäre nur geteilt durch 10.000, teile stattdessen durch 1.000."),
                          ("200.000 kg", False, "Das passt nicht zum Ausgangswert, prüfe die Kommastellen noch einmal."),
                          ("3.200 kg", True, None),
                          ("2000 kg", False, "Rechne noch einmal nach: 3.200.000 g ÷ 1.000 = 3.200 kg.")]),
               dict(q="Eine Hauskatze wiegt 4.000 g. Wie viel sind das in kg?",
                    done="Richtig, 4.000 g sind 4 kg.",
                    opts=[("0,4 kg", False, "Das wäre geteilt durch 10.000, teile stattdessen durch 1.000."),
                          ("40 kg", False, "Von g zu kg wird geteilt, nicht multipliziert."),
                          ("4 kg", True, None),
                          ("400 kg", False, "Prüfe die Rechenrichtung noch einmal, g in kg heißt geteilt durch 1.000.")]),
               dict(q="Die Giraffe ist 550 cm groß. Wie viel sind das in m?",
                    done="Richtig, 550 cm sind 5,5 m.",
                    opts=[("5,5 m", True, None),
                          ("55 m", False, "Das Komma ist nur eine Stelle gewandert, cm in m sind aber 2 Stellen, also geteilt durch 100."),
                          ("0,55 m", False, "Das Komma ist eine Stelle zu weit gewandert."),
                          ("500 m", False, "Das passt nicht, cm in m heißt geteilt durch 100.")]),
               dict(q="Der Bambus ist an einem Tag 350 mm gewachsen. Wie viel sind das in cm?",
                    done="Richtig, 350 mm sind 35 cm.",
                    opts=[("500 cm", False, "Das passt nicht zum Ausgangswert, rechne noch einmal nach."),
                          ("35 cm", True, None),
                          ("350 cm", False, "Das ist der Wert in mm selbst, mm in cm heißt geteilt durch 10."),
                          ("3,5 cm", False, "Das Komma ist eine Stelle zu weit gewandert.")]),
               dict(q="Die Schildkröte wiegt 250.000 mg. Wie viel sind das in g?",
                    done="Richtig, 250.000 mg sind 250 g.",
                    opts=[("25 g", False, "Das wäre geteilt durch 10.000, teile stattdessen durch 1.000."),
                          ("500 g", False, "Das passt nicht zum Ausgangswert, rechne noch einmal nach."),
                          ("250 g", True, None),
                          ("2.500 g", False, "Das wäre nur geteilt durch 100, mg in g heißt geteilt durch 1.000.")]),
               dict(q="Das Faultier schläft am Tag 900 Minuten. Wie viele Stunden sind das?",
                    done="Richtig, 900 Minuten sind 15 Stunden.",
                    opts=[("1,5 h", False, "Das Komma ist eine Stelle zu weit gewandert."),
                          ("90 h", False, "Min in h heißt geteilt durch 60, nicht durch 10."),
                          ("9 h", False, "Das passt nicht zum Ausgangswert, rechne 900 min ÷ 60 noch einmal nach."),
                          ("15 h", True, None)]),
               dict(q="Der Kolibri wiegt 5.000 mg. Wie viel sind das in g?",
                    done="Richtig, 5.000 mg sind 5 g.",
                    opts=[("0,5 g", False, "Das wäre geteilt durch 10.000, teile stattdessen durch 1.000."),
                          ("50 g", False, "Prüfe die Rechenrichtung noch einmal, mg in g heißt geteilt durch 1.000."),
                          ("5 g", True, None),
                          ("500 g", False, "Das passt nicht, mg in g heißt geteilt durch 1.000, nicht durch 10.")]),
               dict(q="Ein Gepard läuft 33,3 m/s. Wie schnell ist das ungefähr in km/h?",
                    done="Richtig, 33,3 m/s sind etwa 120 km/h.",
                    opts=[("33,3 km/h", False, "Das ist nur der Zahlenwert ohne Umrechnung, m/s und km/h sind unterschiedliche Einheiten."),
                          ("12 km/h", False, "Das ist zu langsam, ein Gepard ist deutlich schneller als ein Fahrrad."),
                          ("333 km/h", False, "Das ist zu schnell, kein Landtier läuft annähernd so schnell."),
                          ("120 km/h", True, None)]),
             ],
             solution=["a) Elefant: 3.200 kg × 1.000 = 3.200.000 g, 3.200.000 g × 1.000 = 3.200.000.000 mg.",
                       "b) Hauskatze: 4 kg × 1.000 = 4.000 g, 4.000 g × 1.000 = 4.000.000 mg.",
                       "c) Giraffe: 5,5 m × 100 = 550 cm, 5,5 m × 0,001 = 0,0055 km.",
                       "d) Bambus: 35 cm × 0,01 = 0,35 m, 35 cm × 10 = 350 mm.",
                       "e) Schildkröte: 250 g × 0,001 = 0,25 kg, 250 g × 1.000 = 250.000 mg.",
                       "f) Faultier: 15 h × 60 = 900 min.",
                       "g) Kolibri: 5 g × 1.000 = 5.000 mg.",
                       "h) Gepard (Zusatzaufgabe): 120 km/h = 120.000 m ÷ 3.600 s ≈ 33,3 m/s."]),
        dict(no=2, sjw=2, kind="lernpfad", title="Die schwimmende Orange",
             goal="Du schätzt und berechnest Radius, Umfang und Volumen einer Orange und erklärst, warum sie mit Schale schwimmt, aber ohne Schale sinkt.",
             tasks=["Schätze Gewicht, Radius, Umfang und Volumen einer Orange und vergleiche mit dem Messwert.",
                    "Teste im Wasserbecken: Schwimmt die Orange mit Schale? Schwimmt sie auch ohne Schale?",
                    "Beschreibe die Gemeinsamkeit von Boot, Schwimmweste und Orangenschale: Lufteinlagerung verringert die Dichte des schwimmenden Körpers."],
             tools=[], fast="Berechne, wie viele Orangen mit Schale nötig wären, um dein eigenes Körpergewicht aus LP00 auf dem Wasser zu tragen.",
             tags=["Experimentieren", "Dichte"],
             quiz=[
               dict(q="Schätze das durchschnittliche Gewicht einer Orange.", done="Richtig — 200–500 g.",
                    opts=[("200 g – 500 g", True, None), ("1500 g – 2000 g", False, "Das wäre schwerer als eine kleine Melone."),
                          ("100 mg – 200 mg", False, "Das wäre leichter als ein Reiskorn."), ("10 g – 50 g", False, "Das wäre leichter als eine Erdbeere.")]),
               dict(q="Nenne den am besten passenden mathematischen Körper für eine Orangenform.", done="Richtig — die Kugel.",
                    opts=[("Kugel", True, None), ("Prisma", False, "Ein Prisma hat gerade Kanten."), ("Pyramide", False, "Eine Pyramide läuft spitz zu."), ("Würfel", False, "Ein Würfel hat sechs flache Seiten.")]),
               dict(q="Schätze den Radius r einer Orange.", done="Richtig — etwa 4,5 cm.",
                    opts=[("4,5 cm", True, None), ("450 mm", False, "Das wären 45 cm — viel zu groß."), ("8,5 cm", False, "Das wäre eher der Durchmesser einer sehr großen Orange."), ("0,5 cm", False, "Das wäre kleiner als eine Erbse.")]),
               dict(q="Beschreibe die Gemeinsamkeit von Boot, Schwimmweste und Orangenschale.", done="Richtig — Lufteinlagerung verringert die Dichte.",
                    opts=[("Lufteinlagerung verringert die Dichte des schwimmenden Körpers.", True, None),
                          ("Lufteinlagerung vergrößert die Dichte des schwimmenden Körpers.", False, "Luft ist sehr leicht — sie senkt die Dichte, statt sie zu erhöhen.")]),
             ],
             catchup=[
               dict(q="Schätze das durchschnittliche Gewicht einer Orange.",
                    done="Richtig, eine Orange wiegt im Schnitt 200 g bis 500 g.",
                    icon=ICON_ORANGE_FRUCHT,
                    opts=[("1500 g - 2000 g", False, "Das wäre schwerer als eine kleine Melone."),
                          ("200 g - 500 g", True, None),
                          ("100 mg - 200 mg", False, "Das wäre leichter als ein Reiskorn."),
                          ("10 g - 50 g", False, "Das wäre leichter als eine Erdbeere.")]),
               dict(q="Nenne den am besten passenden mathematischen Körper für eine Orangenform.",
                    done="Richtig, die Kugel passt am besten.",
                    icon=ICON_KOERPER_REIHE,
                    opts=[("Prisma", False, "Ein Prisma hat gerade Kanten und ebene Flächen."),
                          ("Kugel", True, None),
                          ("Pyramide", False, "Eine Pyramide läuft spitz zu."),
                          ("Würfel", False, "Ein Würfel hat sechs flache, eckige Seiten.")]),
               dict(q="Schätze den Radius r (1) einer Orange.",
                    done="Richtig, der Radius liegt bei etwa 4,5 cm.",
                    icon=ICON_KUGEL_RADIUS,
                    opts=[("450 mm", False, "450 mm sind 45 cm, das wäre viel zu groß."),
                          ("8,5 cm", False, "Das wäre eher der Durchmesser einer sehr großen Orange."),
                          ("4,5 cm", True, None),
                          ("0,5 cm", False, "Das wäre kleiner als eine Erbse.")]),
               dict(q="Schätze den Umfang (1) einer Orange.",
                    done="Richtig, der Umfang liegt bei etwa 28 cm.",
                    icon=ICON_KUGEL_UMFANG,
                    opts=[("2800 cm", False, "2800 cm wären 28 m, viel zu groß."),
                          ("2,8 cm", False, "Das wäre kleiner als der Radius allein."),
                          ("2,8 m", False, "Das wäre viel zu groß für eine Orange."),
                          ("28 cm", True, None)]),
               dict(q="Schätze das Volumen (1) (=Inhalt) einer Orange.",
                    done="Richtig, das Volumen liegt bei etwa 382 ml.",
                    icon=ICON_KUGEL_VOLUMEN,
                    opts=[("382 ml", True, None),
                          ("3,82 l", False, "Das wäre so viel wie mehrere Liter Milch, viel zu groß."),
                          ("38,2 ml", False, "Das wäre nur ein paar Löffel, viel zu wenig."),
                          ("38,2 l", False, "Das wäre ein ganzer Eimer, viel zu groß.")]),
               dict(q="Beschreibe die Gemeinsamkeit eines Boots, einer Schwimmweste und einer Orangenschale.",
                    done="Richtig, eingelagerte Luft verringert die Dichte des schwimmenden Körpers.",
                    icon=ICON_BOOT_WESTE_SCHALE,
                    opts=[("Lufteinlagerung verringert die Dichte des schwimmenden Körpers.", True, None),
                          ("Lufteinlagerung vergrößert die Dichte des schwimmenden Körpers.", False, "Luft ist sehr leicht, sie senkt die Dichte, statt sie zu erhöhen.")]),
               dict(q="Ordne die Dichte (ρ „rho“) des Wassers im abgebildeten Toten Meer (1) im Vergleich zur Dichte des Wassers in einem Süßwassersee zu.",
                    done="Richtig, das Tote Meer ist durch den hohen Salzgehalt deutlich dichter.",
                    icon=ICON_TOTES_MEER,
                    opts=[("ρ (Totes Meer) &lt; ρ (Süßwasser)", False, "Der hohe Salzgehalt macht das Wasser dichter, nicht leichter."),
                          ("ρ (Totes Meer) &gt; ρ (Süßwasser)", True, None),
                          ("ρ (Totes Meer) = ρ (Süßwasser)", False, "Der Salzgehalt im Toten Meer ist etwa zehnmal höher als im Ozean, die Dichten sind also nicht gleich.")]),
               dict(q="Würde eine Orange in der Nordsee (A) oder in der Ostsee (B) tiefer in das Wasser eintauchen?",
                    done="Richtig, in der Ostsee, wegen des geringeren Salzgehalts.",
                    icon=ICON_NORDSEE_OSTSEE,
                    opts=[("In der Ostsee (B), geringerer Salzgehalt bedeutet geringere Dichte und weniger Auftrieb.", True, None),
                          ("In der Nordsee (A), geringerer Salzgehalt bedeutet geringere Dichte und weniger Auftrieb.", False, "Die Nordsee hat den höheren, nicht den geringeren Salzgehalt.")]),
             ],
             solution=["Orange: r ≈ 4,5 cm, Umfang ≈ 28 cm (2πr), Volumen ≈ 382 ml ((4/3)πr³).",
                       "Mit Schale schwimmt die Orange (viele kleine Lufttaschen in der Schale senken die Dichte unter die von Wasser), ohne Schale sinkt sie meist (Dichte des reinen Fruchtfleischs liegt nahe oder über der von Wasser)."]),
        dict(no=3, sjw=3, kind="lernpfad", title="Das Orangen-Aräometer",
             goal="Du entwickelst aus einer Orange ein Aräometer (Senkwaage) und untersuchst im Versuch, ob sie in der Nordsee oder in der Ostsee tiefer eintauchen würde.",
             tasks=["Lies die Info zum Aräometer und notiere die Forschungsfrage: Würde eine Orange in der Nordsee oder in der Ostsee tiefer eintauchen?",
                    "Stelle eine Hypothese (begründete Vermutung) auf: In welchem Gewässer taucht die Orange tiefer ein, und warum?",
                    "Materialien: Orange, Salz, großes Gefäß für ein Wasserbad. Stelle zuerst ein Wasserbad mit wenig Salz her und miss die Eintauchtiefe der Orange, danach ein Wasserbad mit viel Salz.",
                    "Beobachtung: Notiere beide Eintauchtiefen in cm.",
                    "Auswertung: Vervollständige den Lückentext mit den Wörtern <i>unterschiedlichen Salzgehaltes, geringere Dichte, Wasserprobe mit dem geringeren Salzgehalt, tiefer, Aräometer, Dichten, geringeren Auftriebs, bestätigt/widerlegt</i>.",
                    "Ergänze in der Übersicht zu naturwissenschaftlichen Größen die Zeilen für Volumen und Dichte (Symbol, Einheiten, Messinstrument)."],
             tools=[], fast="Baue aus einem Trinkhalm und etwas Knete ein eigenes Aräometer. Markiere, wie tief es in Leitungswasser und in Salzwasser eintaucht, und vergleiche mit deiner Orange.",
             tags=["Experimentieren", "Dichte"],
             pre_sections=[SEC_LP03_INFO],
             extra_css=CSS_LP03,
             quiz=[
               dict(q="Die Hypothese konnte … werden.", done="Richtig, die Hypothese wurde bestätigt.",
                    opts=[("widerlegt", False, "Die Orange ist im weniger salzigen Wasser tatsächlich tiefer eingetaucht, so wie vermutet."),
                          ("bestätigt", True, None)]),
               dict(q="Die Orange taucht in der Wasserprobe mit dem … Salzgehalt tiefer ein.", done="Richtig, beim geringeren Salzgehalt taucht sie tiefer ein.",
                    opts=[("geringeren", True, None),
                          ("höheren", False, "Mehr gelöstes Salz macht das Wasser dichter, die Orange wird stärker nach oben gedrückt.")]),
               dict(q="Grund: Diese Wasserprobe hat eine … Dichte und erzeugt daher einen … Auftrieb.", done="Richtig, geringere Dichte bedeutet geringeren Auftrieb.",
                    opts=[("höhere … größeren", False, "Das gilt für das salzigere Wasser, in dem die Orange höher schwimmt."),
                          ("geringere … größeren", False, "Eine geringere Dichte führt zu einem geringeren, nicht zu einem größeren Auftrieb."),
                          ("geringere … geringeren", True, None)]),
               dict(q="Die Orange eignet sich also als …, wenn die genauen Dichten der Wasserproben unterschiedlichen Salzgehaltes bekannt sind.",
                    done="Richtig, als Aräometer (Senkwaage).",
                    opts=[("Waage", False, "Mit der Waage bestimmt man die Masse, nicht die Dichte einer Flüssigkeit."),
                          ("Aräometer", True, None),
                          ("Thermometer", False, "Das Thermometer misst die Temperatur."),
                          ("Messbecher", False, "Mit dem Messbecher liest man ein Volumen ab.")]),
               dict(q="Welches Symbol und welche Einheit gehören zur Größe Dichte?", done="Richtig, ρ (Rho) in g/ml oder g/cm³.",
                    opts=[("ρ (Rho), in g/ml oder g/cm³", True, None),
                          ("V, in l, ml oder cm³", False, "Das sind Symbol und Einheiten des Volumens."),
                          ("m, in kg, g oder mg", False, "Das sind Symbol und Einheiten der Masse."),
                          ("D, in kg", False, "Die Dichte hat das griechische Symbol ρ und eine zusammengesetzte Einheit.")]),
               dict(q="Wie lässt sich das Volumen (Raum) einer Flüssigkeit bestimmen?", done="Richtig, durch Ablesen an einer Skala, z. B. am Messbecher.",
                    opts=[("Mit der Waage", False, "Die Waage bestimmt die Masse."),
                          ("Mit dem Thermometer", False, "Das Thermometer misst die Temperatur."),
                          ("Mit der Uhr", False, "Mit der Uhr misst man die Zeit."),
                          ("Durch Ablesen an einer Skala", True, None)]),
             ],
             solution=["Hypothese: Die Orange würde tiefer in dem Gewässer eintauchen, das weniger gelöstes Salz enthält (Ostsee), da es eine niedrigere Dichte hat und die Orange durch den geringeren Auftrieb tiefer eintaucht.",
                       "Durchführung: Zuerst wird ein Wasserbad mit geringem Salzgehalt hergestellt und die Eintauchtiefe gemessen, anschließend ein Wasserbad mit höherem Salzgehalt, ebenfalls mit Messung der Eintauchtiefe.",
                       "Auswertung: Die Hypothese konnte <b>bestätigt</b> werden, da die <b>Wasserprobe mit dem geringeren Salzgehalt</b> aufgrund der <b>geringeren Dichte</b> und des daher <b>geringeren Auftriebs</b> die Orange <b>tiefer</b> eintauchen lässt. Die Orange eignet sich also als <b>Aräometer</b>, wenn die genauen <b>Dichten</b> der Wasserproben <b>unterschiedlichen Salzgehaltes</b> bekannt sind.",
                       "Übersicht, Volumen (Raum): Symbol V · Liter, Milliliter, Kubikzentimeter (l, ml, cm³) · Ablesen des Volumens an einer Skala.",
                       "Übersicht, Dichte: Symbol ρ (Rho) · Gramm pro Milliliter, Gramm pro Kubikzentimeter (g/ml, g/cm³) · Aräometer."]),
        dict(no=4, sjw=4, kind="lernpfad", title="Dichtebestimmungen",
             goal="Du bestimmst die Dichte von 3D-gedruckten Festkörpern: Volumen mit der passenden Formel berechnen, Masse wiegen und die Dichte mit ρ = m / V ausrechnen.",
             tasks=["Forschungsfrage: Wie lässt sich die Dichte von Festkörpern bestimmen? Stelle eine Hypothese auf und ergänze die Formel ρ = m / V (in g/ml).",
                    "Materialien: Waage, verschiedene Festkörper (Würfel, Quader, Zylinder, ggf. Pyramide, Kegel, Prisma).",
                    "Durchführung: Die Festkörper werden in Tinkercad modelliert (Volumen höchstens 30 ml), anschließend im 3D-Drucker gedruckt und gewogen.",
                    "Beobachtung: Berechne für jeden Körper zuerst das Volumen und dann die Dichte. Die aufklappbaren Hilfen unten führen dich Schritt für Schritt.",
                    "Auswertung: Konnte die Hypothese bestätigt werden? Begründe."],
             tools=[], fast="Vergleiche deine Dichten mit der Dichte von massivem PLA (1,24 g/cm³) und von Wasser (1 g/ml). Erkläre, warum die gedruckten Körper schwimmen, obwohl massives PLA sinken würde.",
             tags=["Üben & Vertiefen", "Dichte"],
             extra_css=CSS_LP04,
             sections=[SEC_LP04_STEPS],
             catchup_top=True,
             catchup_title="Einstieg: Plickers-Aufgaben",
             catchup_intro="Mit diesen Aufgaben seid ihr in die Stunde gestartet. Sie wiederholen die Übersicht zu naturwissenschaftlichen Größen. Wer gefehlt hat oder noch einmal üben möchte, kann sie hier nachholen.",
             catchup=[
               dict(q="Ordne korrekt zu: Welche Begriffe gehören zu den Spalten (1) bis (5)?",
                    done="Richtig, Größe, Symbol der Größe, Einheiten, Symbol der Einheit, mögliche Messinstrumente.",
                    icon=ICON_GROESSEN_KOPF, icon_cls="xl",
                    opts=[("Symbol der Größe (1), Größe (2), Symbol der Einheiten (3), Einheiten (4), mögliche Messinstrumente (5)", False, "„Länge“ in Spalte 1 ist die Größe selbst, ihr Symbol „l“ steht in Spalte 2."),
                          ("Größe (1), Symbol der Größe (2), Einheiten (3), Symbol der Einheit (4), mögliche Messinstrumente (5)", True, None),
                          ("Größe (1), Symbol der Größe (2), Symbol der Einheiten (3), Einheiten (4), mögliche Messinstrumente (5)", False, "In Spalte 3 stehen ausgeschriebene Wörter (Meter, Millimeter …), das sind die Einheiten. Ihre Symbole stehen in Spalte 4."),
                          ("Symbol der Größe (1), Größe (2), Einheiten (3), Symbol der Einheit (4), mögliche Messinstrumente (5)", False, "„Länge“ ist die Größe, das Symbol „l“ steht erst in Spalte 2.")]),
               dict(q="Nenne das Symbol der Größe.",
                    done="Richtig, das Symbol der Größe Masse ist m.",
                    icon=word_card(["Kilogramm, Gramm,", "Milligramm, Tonnen"], size=14), icon_cls="wide",
                    opts=[("Waage", False, "Die Waage ist das Messinstrument."),
                          ("m", True, None),
                          ("kg, g, mg, t", False, "Das sind die Symbole der Einheiten, nicht das Symbol der Größe."),
                          ("Masse", False, "Masse ist die Größe selbst, gesucht ist ihr Symbol.")]),
               dict(q="Nenne das Symbol der Einheit.",
                    done="Richtig, bpm steht für „beats per minute“, also Herzschläge pro Minute.",
                    icon=word_card(["Frequenz"], bold=True, grey=True, size=22), icon_cls="wide",
                    opts=[("f", False, "f ist das Symbol der Größe Frequenz."),
                          ("Herzschläge pro Minute", False, "Das ist die ausgeschriebene Einheit, gesucht ist ihr Symbol."),
                          ("bpm", True, None),
                          ("Uhr und Fühlen", False, "Das ist die Messmethode.")]),
               dict(q="Nenne die physikalische Größe.",
                    done="Richtig, mit dem Thermometer misst man die Temperatur.",
                    icon=word_card(["Thermometer"], size=20), icon_cls="wide",
                    opts=[("° C, K, ° F", False, "Das sind die Symbole der Einheiten."),
                          ("Grad Celsius, Kelvin, Grad Fahrenheit", False, "Das sind die Einheiten der Größe."),
                          ("T", False, "T ist das Symbol der Größe, gesucht ist die Größe selbst."),
                          ("Temperatur", True, None)]),
               dict(q="Beschreibe eine mögliche Bestimmungsmöglichkeit (Messinstrument).",
                    done="Richtig, zum Beispiel am Messbecher oder Messzylinder.",
                    icon=word_card(["Volumen", "(Raum)"], bold=True, grey=True, size=20), icon_cls="wide",
                    opts=[("V", False, "V ist das Symbol der Größe."),
                          ("Liter, Milliliter, Kubikzentimeter", False, "Das sind die Einheiten des Volumens."),
                          ("l, ml, cm³", False, "Das sind die Symbole der Einheiten."),
                          ("Ablesen des Volumens an einer Skala", True, None)]),
               dict(q="Wähle einen geeigneten Weg aus, um die Dichte von Festkörpern experimentell zu bestimmen.",
                    done="Richtig, ρ = m / V: Masse durch Volumen.",
                    icon=ICON_DICHTE_ZEILE, icon_cls="xl",
                    opts=[("Masse und Volumen bestimmen; anschließend Masse mit Volumen addieren", False, "Masse und Volumen haben unterschiedliche Einheiten, man kann sie nicht addieren."),
                          ("Masse und Volumen bestimmen; anschließend Volumen durch Masse teilen", False, "Genau umgekehrt: Die Einheit g/ml bedeutet Masse durch Volumen."),
                          ("Masse und Volumen bestimmen; anschließend Masse durch Volumen teilen", True, None),
                          ("Masse und Volumen bestimmen; anschließend Masse mit Volumen multiplizieren", False, "Die Einheit „Gramm pro Milliliter“ verrät, dass geteilt wird.")]),
             ],
             solution=["Hypothese: Die Dichte (ρ) eines Festkörpers lässt sich durch die Division der Masse (m) durch das Volumen (V) bestimmen, da ρ = m / V gilt (in g/ml).",
                       "Auswertung: Die Hypothese konnte bestätigt werden, da alle Dichten über die gegebene Formel bestimmbar waren.",
                       "Beispielergebnisse (PLA, ca. 15 % Füllung): Quader 0,45 g/ml · Zylinder 0,38 g/ml · Halbkugel 0,36 g/ml · Pyramide 0,36 g/ml · Kegel 0,36 g/ml · Prisma 0,41 g/ml. Alle liegen unter 1 g/ml, die Körper schwimmen also in Wasser.",
                       'Volumina, Abb. 1:<img class="sol-fig" src="lp04-img/volumina-1.svg" alt="Volumenberechnung für Quader, Zylinder und Halbkugel" loading="lazy">',
                       'Dichten, Abb. 1:<img class="sol-fig" src="lp04-img/dichte-1.svg" alt="Dichteberechnung für Quader, Zylinder und Halbkugel" loading="lazy">',
                       'Volumina, Abb. 2:<img class="sol-fig" src="lp04-img/volumina-2.svg" alt="Volumenberechnung für Pyramide, Kegel und Prisma" loading="lazy">',
                       'Dichten, Abb. 2:<img class="sol-fig" src="lp04-img/dichte-2.svg" alt="Dichteberechnung für Pyramide, Kegel und Prisma" loading="lazy">']),
        dict(no=5, sjw=5, kind="lernpfad", title="Schwimmen und Sinken bei Schiffen und Unterseebooten",
             goal="Du überträgst das Dichte-Prinzip auf große Gewässer: Warum trägt das Tote Meer besonders gut, und wie tauchen U-Boote gezielt auf und ab?",
             tasks=["Ordne die Dichte des Toten Meeres im Vergleich zu einem Süßwassersee zu und begründe mit dem hohen Salzgehalt.",
                    "Erkläre, warum ein Schiff aus Stahl trotzdem schwimmt, obwohl Stahl selbst eine viel höhere Dichte als Wasser hat (Hohlkörper-Prinzip).",
                    "Beschreibe, wie ein Unterseeboot mithilfe von Wasserballasttanks seine eigene Dichte verändert, um zu tauchen oder aufzutauchen."],
             tools=[], fast="Begründe, ob eine Orange in der Nordsee oder in der Ostsee tiefer eintauchen würde — die Ostsee hat deutlich weniger Salzgehalt als die Nordsee.",
             tags=["Dichte", "Alltagsbezug"],
             quiz=[
               dict(q="Ordne die Dichte (ρ) des Wassers im Toten Meer im Vergleich zu einem Süßwassersee zu.", done="Richtig — das Tote Meer ist deutlich dichter.",
                    opts=[("ρ (Totes Meer) &gt; ρ (Süßwasser)", True, None), ("ρ (Totes Meer) &lt; ρ (Süßwasser)", False, "Der extrem hohe Salzgehalt macht das Wasser dichter, nicht leichter."),
                          ("ρ (Totes Meer) = ρ (Süßwasser)", False, "Der Salzgehalt ist im Toten Meer ca. 10-mal höher als im Ozean.")]),
               dict(q="Eine Zitrone … im Salzwasser …, weil es eine höhere Dichte als reines Wasser hat.", done="Richtig — sie schwimmt höher.",
                    opts=[("schwimmt … höher", True, None), ("sinkt … tiefer", False, "Höhere Wasserdichte bedeutet mehr Auftrieb, nicht weniger.")]),
               dict(q="Im Liquidrom (Schwebebecken) wird stark salziges Wasser verwendet. Warum?", done="Richtig — Salzwasser erhöht die Dichte und damit den Auftrieb.",
                    opts=[("Es erhöht die Dichte des Wassers, damit Menschen mühelos schweben.", True, None),
                          ("Es macht das Wasser wärmer.", False, "Die Temperatur hat mit dem Schweben nichts zu tun."),
                          ("Es reinigt das Wasser besser.", False, "Es geht hier gezielt um Auftrieb, nicht um Wasserqualität.")]),
               dict(q="Würde eine Orange in der Nordsee oder in der Ostsee tiefer eintauchen?", done="Richtig — in der Ostsee, wegen des geringeren Salzgehalts.",
                    opts=[("In der Ostsee — geringerer Salzgehalt bedeutet geringere Dichte und weniger Auftrieb.", True, None),
                          ("In der Nordsee — geringerer Salzgehalt bedeutet geringere Dichte und weniger Auftrieb.", False, "Die Nordsee hat den höheren, nicht den geringeren Salzgehalt.")]),
             ],
             solution=["Totes Meer: extrem hoher Salzgehalt → hohe Dichte → starker Auftrieb, Menschen treiben fast von selbst.",
                       "Ein Schiffsrumpf verdrängt sehr viel Wasser bei relativ wenig Masse (Hohlkörper) → seine mittlere Dichte liegt unter der von Wasser.",
                       "U-Boot: Ballasttanks mit Wasser fluten → Dichte steigt → Boot sinkt; Wasser mit Druckluft herauspressen → Dichte sinkt → Boot steigt."]),
        dict(no=6, sjw=6, kind="lernpfad", title="Ölextraktion",
             goal="Du gewinnst ätherisches Öl aus Gewürznelken durch Wasserdampfdestillation und erklärst, warum es auf dem Destillat schwimmt.",
             tasks=["Baue gemeinsam einen einfachen Wasserdampfdestillations-Aufbau für Gewürznelken auf.",
                    "Beobachte, wie sich das ätherische Öl vom übrig bleibenden Destillat (überwiegend Wasser) trennt.",
                    "Begründe mit der Dichte, warum das ätherische Öl auf der Destillat-Oberfläche schwimmt."],
             tools=[], fast="Recherchiere, wofür Nelkenöl traditionell verwendet wird, und stelle einen Bezug zu seinen chemischen Eigenschaften her.",
             tags=["Experimentieren", "Trennverfahren"],
             quiz=[
               dict(q="Benenne die duftende Komponente in Nelken.", done="Richtig — ätherische Öle.",
                    opts=[("ätherische Öle", True, None), ("Pflegeöle", False, "Pflegeöle sind kosmetische Produkte, kein Fachbegriff für Duftstoffe."),
                          ("essentielle Öle", False, "Der korrekte deutsche Fachbegriff lautet ätherische Öle."), ("fettige Öle", False, "Ätherische Öle sind chemisch keine Fette.")]),
               dict(q="Benenne die Gewinnungsmethode der ätherischen Öle.", done="Richtig — Wasserdampfdestillation.",
                    opts=[("Wasserdampfdestillation", True, None), ("Destillation", False, "Genauer und richtig ist die Wasserdampfdestillation."),
                          ("Chromatographie", False, "Chromatographie trennt Stoffgemische, gewinnt aber keine Öle im großen Maßstab."), ("Hochdruckkochen", False, "Das ist kein anerkanntes Trennverfahren für ätherische Öle.")]),
               dict(q="Begründe das Schwimmen des ätherischen Öls auf der Destillat-Oberfläche.", done="Richtig — das Öl hat die geringere Dichte.",
                    opts=[("ρ (ätherisches Öl) &lt; ρ (Destillat)", True, None), ("ρ (ätherisches Öl) &gt; ρ (Destillat)", False, "Wäre die Dichte höher, würde das Öl absinken."),
                          ("ρ (ätherisches Öl) = ρ (Destillat)", False, "Bei gleicher Dichte würden sich beide vermischen, nicht trennen.")]),
             ],
             solution=["Wasserdampf löst die ätherischen Öle aus der Nelke; beim Abkühlen kondensieren Wasser und Öl gemeinsam, trennen sich aber, weil sie sich nicht mischen.",
                       "Ätherisches Nelkenöl hat eine geringere Dichte als Wasser und schwimmt deshalb sichtbar oben auf."]),
      ]),
 # =================== 01 LEBENSMITTEL ===================
 dict(num="01", title="Lebensmittel",
      key="#ff8a3d", key2="#d96a1f", tint="rgba(255,138,61,0.10)",
      lps=[
        dict(no=7, sjw=7, kind="lernpfad", title="Nahrungsmittelrallye",
             goal="Du lernst die drei Hauptnährstoffe (Fette, Proteine, Kohlenhydrate) und die Mikronährstoffe (Vitamine, Mineralstoffe) kennen und ordnest sie echten Lebensmitteln zu.",
             tasks=["Ordne an Stationen verschiedene Lebensmittel den Hauptnährstoffen zu, die in ihnen überwiegen.",
                    "Unterscheide Makronährstoffe (Fette, Proteine, Kohlenhydrate) von Mikronährstoffen (z. B. Vitamin C, Kalium, Calcium).",
                    "Vergleiche drei Erfrischungsgetränke und bewerte sie nach gesundheitlichen Gesichtspunkten (Zucker, Säure, Zusatzstoffe)."],
             tools=[], fast="Erstelle eine Woche-Speiseplan-Idee, die alle drei Hauptnährstoffe ausgewogen berücksichtigt.",
             tags=["Ernährung"],
             quiz=[
               dict(q="Welcher Begriff gehört NICHT zu den Makronährstoffen (Hauptnährstoffen)?", done="Richtig — Ballaststoffe zählen nicht zu den klassischen Makronährstoffen.",
                    opts=[("Ballaststoffe", True, None), ("Fette", False, "Fette sind einer der drei Hauptnährstoffe."), ("Eiweiße/Proteine", False, "Proteine sind einer der drei Hauptnährstoffe."), ("Kohlenhydrate/Zucker", False, "Kohlenhydrate sind einer der drei Hauptnährstoffe.")]),
               dict(q="Welcher Begriff gehört NICHT zu den Spurennährstoffen (Mikronährstoffen)?", done="Richtig — Proteine sind ein Makronährstoff.",
                    opts=[("Proteine", True, None), ("Vitamin C", False, "Vitamin C ist ein klassischer Mikronährstoff."), ("Kalium", False, "Kalium ist ein Mineralstoff (Mikronährstoff)."), ("Calcium", False, "Calcium ist ein Mineralstoff (Mikronährstoff).")]),
               dict(q="Nenne den am meisten enthaltenen Nährstoff in Kürbiskernöl.", done="Richtig — Fette.",
                    opts=[("Fette", True, None), ("Proteine", False, "Öle bestehen überwiegend aus Fett, nicht aus Eiweiß."), ("Kohlenhydrate", False, "Öle enthalten praktisch keine Kohlenhydrate."), ("Ballaststoffe", False, "Ballaststoffe stecken in Pflanzenfasern, nicht in Öl.")]),
               dict(q="Haferflocken und Linsen — welcher Nährstoff ist darin NICHT besonders stark vertreten?", done="Richtig — Fette sind hier eher gering vertreten.",
                    opts=[("Fette", True, None), ("Kohlenhydrate", False, "Beide sind reich an Kohlenhydraten."), ("Ballaststoffe", False, "Beide sind sehr ballaststoffreich."), ("Proteine", False, "Beide liefern auch nennenswert Eiweiß.")]),
               dict(q="In Öl eingelegter Thunfisch — welcher Nährstoff ist darin NICHT besonders stark vertreten?", done="Richtig — Kohlenhydrate stecken kaum in Fisch und Öl.",
                    opts=[("Kohlenhydrate", True, None), ("Fette", False, "Durch das Öl ist reichlich Fett enthalten."), ("Proteine", False, "Fisch liefert viel Eiweiß.")]),
               dict(q="Welche Aussage über Nährstoffe und Kalorien ist richtig?", done="Richtig — beide liefern etwa 4 kcal pro Gramm.",
                    opts=[("Kohlenhydrate und Proteine liefern pro Gramm etwa gleich viele Kalorien.", True, None),
                          ("Proteine sind hauptsächlich in Pflanzenölen enthalten.", False, "Pflanzenöle bestehen fast nur aus Fett."),
                          ("Fette liefern genauso viele Kalorien pro Gramm wie Kohlenhydrate.", False, "Fett liefert mit ca. 9 kcal/g mehr als doppelt so viel wie Kohlenhydrate."),
                          ("Ballaststoffe enthalten viele Kalorien.", False, "Ballaststoffe liefern kaum verwertbare Kalorien.")]),
               dict(q="Was ist ein gesundheitlich bedenklicher Aspekt vieler Erfrischungsgetränke?", done="Richtig — säurehaltige Inhaltsstoffe greifen den Zahnschmelz an.",
                    opts=[("säurehaltige Inhaltsstoffe (z. B. Zitronensäure)", True, None), ("aufsteigendes Kohlenstoffdioxidgas", False, "Die Kohlensäure-Bläschen selbst sind kaum bedenklich."), ("hoher Wasseranteil", False, "Ein hoher Wasseranteil ist eher positiv zu bewerten.")]),
             ],
             solution=["Makronährstoffe: Fette, Proteine, Kohlenhydrate — liefern Energie (Kalorien).",
                       "Mikronährstoffe: Vitamine, Mineralstoffe — liefern kaum Energie, sind aber lebensnotwendig.",
                       "Fett liefert ca. 9 kcal/g, Kohlenhydrate und Proteine je ca. 4 kcal/g."]),
        dict(no=8, sjw=8, kind="lernpfad", title="Interessantes zu Fetten",
             goal="Du unterscheidest gesunde von weniger gesunden Fetten und lernst eine chemische Nachweisprobe für Fette kennen.",
             tasks=["Ordne Fette und Öle korrekt als Makronährstoff ein und nenne Beispiele aus dem Alltag.",
                    "Führe die Fettfleckprobe an verschiedenen Lebensmittelproben durch und notiere, welche Proben Fett enthalten.",
                    "Vergleiche einen fetthaltigen Snack (z. B. Kartoffelchips, Linsenchips, Nüsse) nach Gesundheitswert."],
             tools=[], fast="Recherchiere, warum Omega-3-Fettsäuren besonders für das Gehirn wichtig sind (Stichwort: Myelin-Schutzschicht der Nervenzellen).",
             tags=["Ernährung", "Nachweisverfahren"],
             quiz=[
               dict(q="Ordne Fette und Öle dem passenden Begriff zu.", done="Richtig — Fette und Öle sind Makronährstoffe.",
                    opts=[("Makronährstoff", True, None), ("Ballaststoff", False, "Ballaststoffe sind unverdauliche Pflanzenfasern."), ("Proteine", False, "Proteine sind ein eigener Makronährstoff."), ("Mikronährstoff", False, "Mikronährstoffe liefern kaum Energie — Fett dagegen sehr viel.")]),
               dict(q="Benenne die Nachweisprobe für Lipide (Fette, Öle).", done="Richtig — die Fettfleckprobe.",
                    opts=[("Fettfleckprobe", True, None), ("Öltröpfchenprobe", False, "Das ist kein anerkannter Fachbegriff."), ("Fettreinigungsprobe", False, "Reinigung ist kein Nachweisverfahren."), ("Fettschmelzprobe", False, "Schmelzen zeigt keinen sicheren Fettnachweis.")]),
               dict(q="Wähle den gesündesten, fetthaltigen Snack aus.", done="Richtig — ungesalzene Nüsse liefern wertvolle ungesättigte Fettsäuren.",
                    opts=[("Nüsse", True, None), ("Kartoffelchips", False, "Chips enthalten meist viel gesättigtes Fett und Salz."), ("Linsenchips", False, "Auch verarbeitete Chips sind meist stark gesalzen und frittiert.")]),
               dict(q="Welche Schutzschicht der Nervenzellen profitiert besonders von gesunden Fetten (Omega-3)?", done="Richtig — das Myelin, die isolierende Schutzschicht der Nervenbahnen.",
                    opts=[("Myelin", True, None), ("Dendriten", False, "Dendriten empfangen Signale, sie sind keine Fettschicht."), ("Soma", False, "Das Soma ist der Zellkörper, keine Fettschicht."), ("Zellkern", False, "Der Zellkern steuert die Zelle, ist aber keine Fettschicht.")]),
               dict(q="Warum braucht der Körper trotzdem Fette in der Ernährung?", done="Richtig — Fette liefern Energie, schützen Organe und transportieren fettlösliche Vitamine.",
                    opts=[("Sie liefern Energie, polstern Organe und transportieren fettlösliche Vitamine (A, D, E, K).", True, None),
                          ("Sie werden im Körper überhaupt nicht benötigt.", False, "Fette sind lebensnotwendig — auf sie ganz zu verzichten wäre ungesund."),
                          ("Sie dienen nur dem Geschmack, haben aber keine Funktion.", False, "Fette erfüllen wichtige Körperfunktionen, nicht nur Geschmack.")]),
             ],
             solution=["Fettfleckprobe: Ein durchscheinender, bleibender Fleck auf Papier zeigt Fett an.",
                       "Ungesättigte Fettsäuren (z. B. in Nüssen, Fisch, Pflanzenölen) gelten als besonders gesundheitsförderlich, u. a. für Herz und Gehirn."]),
        dict(no=9, sjw=9, kind="lernpfad", title="Energiehaushalt",
             goal="Du berechnest, wie viel Energie in einer Walnuss steckt, und vergleichst sie mit der Energie, die du beim Sport verbrauchst.",
             tasks=["Verbrenne (unter Aufsicht) eine Walnusshälfte und erhitze damit eine bekannte Menge Wasser.",
                    "Berechne aus der Temperaturerhöhung des Wassers, wie viel Energie in der Walnusshälfte steckt.",
                    "Vergleiche die gewonnene Energie mit alltäglichen Bewegungen (z. B. Kniebeugen, Hampelmänner, Joggen)."],
             tools=[], fast="Rechne deinen Energiewert einer ganzen Chipstüte hoch und schätze, wie lange du dafür joggen müsstest.",
             tags=["Experimentieren", "Energie"],
             quiz=[
               dict(q="Auf wie viel Grad Celsius lassen sich 200 g Wasser (20 °C) beim Verbrennen einer Walnusshälfte etwa erwärmen?", done="Richtig — auf rund 100 °C, also fast bis zum Sieden.",
                    opts=[("ca. 100 °C", True, None), ("ca. 25 °C", False, "Das wäre eine viel zu geringe Erwärmung für die enthaltene Energie."), ("ca. 50 °C", False, "Auch das ist deutlich zu wenig."), ("ca. 75 °C", False, "Nah dran, aber die Walnuss liefert noch mehr Energie.")]),
               dict(q="Welche Energieform steckt chemisch in einer Walnuss gespeichert?", done="Richtig — chemische Energie, die beim „Verbrennen“ (Verdauen) freigesetzt wird.",
                    opts=[("chemische Energie", True, None), ("elektrische Energie", False, "In Lebensmitteln ist keine elektrische Energie gespeichert."), ("Kernenergie", False, "Kernenergie hat mit Nahrung nichts zu tun."), ("Lichtenergie", False, "Licht wird nicht in der Nuss gespeichert.")]),
               dict(q="Was passiert grundsätzlich mit der chemischen Energie einer Walnuss in deinem Körper?", done="Richtig — sie wird u. a. in Wärme- und Bewegungsenergie umgewandelt.",
                    opts=[("Sie wird in Wärme- und Bewegungsenergie umgewandelt.", True, None), ("Sie verschwindet spurlos.", False, "Energie geht nicht verloren, sie wird nur umgewandelt (Energieerhaltung)."), ("Sie bleibt für immer chemisch gespeichert.", False, "Der Körper wandelt die Energie beim Verdauen und Bewegen um.")]),
               dict(q="Warum eignet sich ein Verbrennungsversuch mit Wasser, um den Energiegehalt eines Lebensmittels zu bestimmen?", done="Richtig — die Temperaturerhöhung des Wassers zeigt direkt, wie viel Energie freigesetzt wurde.",
                    opts=[("Die Temperaturerhöhung einer bekannten Wassermenge lässt sich in eine Energiemenge umrechnen.", True, None),
                          ("Wasser verändert seine Temperatur nie, das macht die Messung einfach.", False, "Genau die Temperaturänderung ist ja die Messgröße."),
                          ("Wasser reagiert chemisch mit der Walnuss.", False, "Das Wasser nimmt nur die freiwerdende Wärme auf, es reagiert nicht mit der Nuss.")]),
             ],
             solution=["Eine Walnusshälfte (ca. 2,9 g) liefert genug Energie, um 200 g Wasser von 20 °C fast bis zum Sieden (≈100 °C) zu erwärmen.",
                       "Dieselbe Energiemenge entspricht ungefähr mehreren Dutzend Kniebeugen oder einigen hundert Metern Joggen — Nahrungsenergie und Bewegungsenergie sind direkt vergleichbar."]),
        dict(no=10, sjw=10, kind="lernpfad", title="Denaturierung von Proteinen am Beispiel von pflanzlichen Baisers",
             goal="Du stellst veganes Baiser aus Kichererbsenwasser (Aquafaba) her und erklärst, was beim Schlagen und Erhitzen mit den Proteinen passiert.",
             tasks=["Schlage Aquafaba (Kichererbsenwasser) so lange, bis ein stabiler Eischnee-ähnlicher Schaum entsteht.",
                    "Beobachte und beschreibe, wie sich Aussehen und Konsistenz beim Schlagen verändern.",
                    "Erkläre den Vorgang mit dem Fachbegriff Denaturierung: Proteine verändern durch mechanische und thermische Energie dauerhaft ihre Struktur."],
             tools=[], fast="Untersuche in der Gruppe ein weiteres Denaturierungsphänomen (z. B. Eiweiß beim Kochen, Milch mit Zitronensaft) und stelle es kurz vor.",
             tags=["Experimentieren", "Proteine"],
             quiz=[
               dict(q="Nenne das geeignetste Bohnenwasser (Aquafaba) zur Herstellung von Baisers.", done="Richtig — Kichererbsenwasser ist die klassische Aquafaba-Zutat.",
                    opts=[("Kichererbsenwasser", True, None), ("Wasser der weißen Bohnen", False, "Funktioniert schlechter als Kichererbsenwasser."), ("Wasser der schwarzen Bohnen", False, "Färbt zudem den Schaum dunkel ein."), ("Kidneybohnenwasser", False, "Auch hier ist die Schaumstabilität geringer.")]),
               dict(q="Welche Energieform bewirkt hauptsächlich das Aufschlagen des Bohnenwassers zu Schaum?", done="Richtig — mechanische Energie durchs Schlagen.",
                    opts=[("mechanische Energie (Bewegungsenergie)", True, None), ("elektrische Energie", False, "Der Handrührer nutzt zwar Strom, wirkt aber mechanisch auf das Bohnenwasser."), ("thermische Energie (Wärmeenergie)", False, "Das Aufschlagen selbst erzeugt kaum Wärme."), ("chemische Energie", False, "Beim reinen Aufschlagen findet keine chemische Reaktion statt.")]),
               dict(q="Benenne den Vorgang beim Schlagen und Erhitzen der gelösten Proteine.", done="Richtig — Denaturierung.",
                    opts=[("Denaturierung", True, None), ("Naturierung", False, "Das ist kein Fachbegriff."), ("Schmelzen", False, "Proteine schmelzen nicht wie Fett oder Eis."), ("Erhärten", False, "Erhärten beschreibt nur das äußere Ergebnis, nicht den Fachbegriff.")]),
               dict(q="Was passiert bei der Denaturierung mit der Struktur eines Proteins?", done="Richtig — die räumliche Struktur verändert sich dauerhaft, das Protein lässt sich nicht zurückverwandeln.",
                    opts=[("Die räumliche Struktur verändert sich dauerhaft und ist nicht umkehrbar.", True, None),
                          ("Das Protein wird vollständig zu Zucker.", False, "Proteine bestehen aus Aminosäuren, nicht aus Zucker."),
                          ("Das Protein verschwindet spurlos.", False, "Das Protein bleibt vorhanden, nur seine Form verändert sich.")]),
               dict(q="Welches Alltagsbeispiel zeigt ebenfalls eine Denaturierung von Proteinen?", done="Richtig — Eiweiß wird beim Kochen fest und weiß.",
                    opts=[("Eiweiß wird beim Kochen fest und undurchsichtig.", True, None), ("Zucker karamellisiert beim Erhitzen.", False, "Karamellisieren betrifft Zucker, keine Proteine."), ("Eis schmilzt in der Sonne.", False, "Schmelzen von Eis ist ein reiner Zustandswechsel des Wassers, keine Denaturierung.")]),
             ],
             solution=["Aquafaba enthält gelöste Proteine, die sich beim Schlagen (mechanische Energie) an Luftbläschen anlagern und beim Backen (thermische Energie) endgültig ihre Struktur verändern.",
                       "Denaturierung ist nicht umkehrbar — daraus lässt sich kein flüssiges Aquafaba mehr zurückgewinnen, genauso wenig wie ein gekochtes Ei wieder roh wird."]),
        dict(no=11, sjw=11, kind="lernpfad", title="Kohlenhydrate",
             goal="Du weist mit der Jodprobe Stärke in Lebensmitteln nach und lernst, welche Kohlenhydrate wann sinnvoll sind.",
             tasks=["Führe die Jodprobe (Lugol'sche Probe) an verschiedenen Lebensmitteln durch (z. B. Kartoffel, Brot, Traubenzucker).",
                    "Notiere, bei welchen Proben sich eine tiefblaue Färbung zeigt und schließe daraus auf den Stärkegehalt.",
                    "Ordne zu, welche Kohlenhydratquelle direkt vor einem Wettkampf am besten geeignet ist und warum."],
             tools=[], fast="Erhitze etwas Haushaltszucker vorsichtig mit konzentrierter Schwefelsäure (nur als Lehrkraft-Demonstration!) und erkläre, warum dabei ein schwarzer Kohlenstoff-Rückstand entsteht.",
             tags=["Experimentieren", "Nachweisverfahren"],
             quiz=[
               dict(q="Nenne eine geeignete Kohlenhydratquelle direkt vor einem Wettkampf.", done="Richtig — Traubenzucker liefert am schnellsten verfügbare Energie.",
                    opts=[("Traubenzucker", True, None), ("Reis", False, "Reis ist eine gute Energiequelle, aber zu langsam verdaulich für kurz vor dem Start."), ("Vollkornbrot", False, "Vollkornbrot wirkt eher langfristig, nicht kurzfristig vor dem Start.")]),
               dict(q="Beschreibe das Erkennungsmerkmal bei positivem Verlauf der Jodprobe (Lugol'sche Probe).", done="Richtig — eine tiefblaue Färbung zeigt Stärke an.",
                    opts=[("tiefblaue Färbung bei Anwesenheit von Stärke", True, None), ("bräunliche Färbung bei Anwesenheit von Stärke", False, "Bräunlich ist die Ausgangsfarbe der Jodlösung, nicht das positive Ergebnis."), ("tiefblaue Färbung bei Anwesenheit von Kohlenhydraten allgemein", False, "Die Jodprobe zeigt spezifisch Stärke an, nicht alle Kohlenhydrate."), ("bräunliche Färbung bei Anwesenheit von Kohlenhydraten allgemein", False, "Das ist weder die richtige Farbe noch der richtige Stoff.")]),
               dict(q="Bei welchem Naturprodukt verläuft die Jodprobe negativ?", done="Richtig — Baumwolle (Zellstoff) enthält Zellulose statt Stärke.",
                    opts=[("Baumwolle (Zellstoff)", True, None), ("Kartoffel", False, "Kartoffeln sind reich an Stärke und reagieren positiv."), ("Getreide", False, "Getreide enthält ebenfalls Stärke und reagiert positiv.")]),
               dict(q="Welcher sichtbare Bestandteil bleibt zurück, wenn Haushaltszucker mit konzentrierter Schwefelsäure reagiert?", done="Richtig — Kohle (Kohlenstoff), das „Kohle“ in „Kohlenhydrat“.",
                    opts=[("Kohle", True, None), ("Stärke", False, "Haushaltszucker (Saccharose) enthält keine Stärke."), ("Hydrat („Wasser“)", False, "Das Wasser entweicht als Dampf, sichtbar bleibt der schwarze Kohlenstoff."), ("Zucker", False, "Der Zucker wird bei der Reaktion gerade zersetzt.")]),
             ],
             solution=["Jodprobe: Iod-Kaliumiodid-Lösung färbt sich bei Stärke tiefblau-schwarz, bei reiner Zellulose (z. B. Baumwolle) bleibt die Färbung aus.",
                       "„Kohlenhydrat“ = Kohle + Hydrat: Konzentrierte Schwefelsäure entzieht dem Zucker Wasser und hinterlässt sichtbaren schwarzen Kohlenstoff."]),
      ]),
 # =================== 02 FLIEGEN ===================
 dict(num="02", title="Fliegen",
      key="#8a5cf0", key2="#6a3fcf", tint="rgba(138,92,240,0.10)",
      lps=[
        dict(no=12, sjw=12, kind="lernpfad", title="Schwimmende Steine und fliegende Teebeutel",
             goal="Du entdeckst mit zwei verblüffenden Experimenten (schwimmender Bimsstein, fliegender Teebeutel), dass Auftrieb ein Prinzip ist, das sowohl im Wasser als auch in der Luft gilt.",
             tasks=["Teste, ob ein Bimsstein in Wasser schwimmt oder sinkt, und erkläre es mit seiner extrem geringen Dichte (viele Luftbläschen).",
                    "Baue eine Teebeutel-Rakete: Entleere einen Teebeutel, stelle ihn aufrecht hin und zünde ihn oben mittig an.",
                    "Verallgemeinere: Ein Körper erfährt Auftrieb, wenn seine Dichte geringer ist als die seines umgebenden Stoffs."],
             tools=[], fast="Erkläre, warum der Teebeutel höher und schneller fliegt, wenn er genau in der Mitte angezündet wird, statt am Rand.",
             tags=["Experimentieren", "Auftrieb"],
             quiz=[
               dict(q="Verallgemeinere: Ein Körper erfährt einen Auftrieb, wenn seine Dichte … ist als sein umgebender Stoff.", done="Richtig — geringer.",
                    opts=[("geringer", True, None), ("höher", False, "Eine höhere Dichte als das Umgebende führt zum Sinken, nicht zum Auftrieb.")]),
               dict(q="Ordne die Dichte des Salzwassers im Vergleich zur Dichte eines Bimssteins zu.", done="Richtig — Bimsstein ist wegen seiner Luftbläschen leichter als Salzwasser.",
                    opts=[("ρ (Salzwasser) &gt; ρ (Bimsstein)", True, None), ("ρ (Salzwasser) &lt; ρ (Bimsstein)", False, "Bimsstein schwimmt gerade deshalb, weil er die geringere Dichte hat."), ("ρ (Salzwasser) = ρ (Bimsstein)", False, "Bei gleicher Dichte würde der Stein weder schwimmen noch sinken, sondern schweben.")]),
               dict(q="Der fliegende Teebeutel nutzt dasselbe Flugprinzip wie …", done="Richtig — der Heißluftballon.",
                    opts=[("ein Heißluftballon", True, None), ("ein Flugzeug", False, "Flugzeuge nutzen den Bernoulli-Effekt an den Tragflächen, nicht heiße Luft."), ("ein Helikopter", False, "Helikopter erzeugen Auftrieb durch rotierende Rotorblätter.")]),
               dict(q="Ordne die Dichte der heißen Luft im Teebeutel (1) im Vergleich zur kalten, umgebenden Luft (2) zu.", done="Richtig — die kalte Umgebungsluft ist dichter, deshalb steigt die heiße Luft auf.",
                    opts=[("ρ (2) &gt; ρ (1)", True, None), ("ρ (1) &gt; ρ (2)", False, "Warme Luft dehnt sich aus und wird dadurch leichter — nicht schwerer."), ("ρ (1) = ρ (2)", False, "Bei gleicher Dichte gäbe es keinen Auftrieb.")]),
               dict(q="Warum fliegt der Teebeutel höher und schneller, wenn er mittig angezündet wird?", done="Richtig — er brennt von innen nach oben durch und wirkt dabei wie ein Raketenantrieb.",
                    opts=[("Er funktioniert dann wie ein Raketenantrieb (Rückstoßprinzip).", True, None),
                          ("Es ist einfach mehr Hitze vorhanden.", False, "Nicht die Hitzemenge, sondern die Rückstoß-Wirkung des mittigen Abbrennens ist entscheidend."),
                          ("Er brennt dadurch nur schneller ab, ohne physikalischen Grund.", False, "Es steckt ein konkretes physikalisches Prinzip dahinter, kein Zufall.")]),
             ],
             solution=["Bimsstein: extrem viele eingeschlossene Luftbläschen senken seine Dichte unter die von Wasser — er schwimmt, obwohl er aus „Stein“ besteht.",
                       "Teebeutel-Rakete: heiße Luft im Inneren ist weniger dicht als die kalte Umgebungsluft (statischer Auftrieb); mittig angezündet entsteht zusätzlich ein Rückstoß-Effekt, der ihn höher fliegen lässt."]),
        dict(no=13, sjw=13, kind="lernpfad", title="Flugprinzipien",
             goal="Du lernst mit dem Bernoulli-Prinzip den zweiten großen Auftriebs-Mechanismus kennen: schnell strömende Luft erzeugt Unterdruck.",
             tasks=["Baue den klassischen Papierstreifen- oder Tischtennisball-Versuch zum Bernoulli-Effekt auf und beobachte den Effekt.",
                    "Erkläre am Modell eines Flügels, wo die Luft schneller strömt und wo dadurch Unter- bzw. Überdruck entsteht.",
                    "Recherchiere kurz, wer Daniel Bernoulli war und wofür er bekannt ist."],
             tools=[], fast="Finde heraus, ob die Flügel- bzw. Ballfläche einen Einfluss auf die Stärke des Bernoulli-Effekts hat, und begründe mit einem eigenen Mini-Versuch.",
             tags=["Experimentieren", "Bernoulli-Prinzip"],
             quiz=[
               dict(q="Nenne das Auftriebsprinzip der Teebeutelrakete aus LP12.", done="Richtig — das Rückstoßprinzip.",
                    opts=[("Rückstoßprinzip (Newton'sches Prinzip: Actio = Reactio)", True, None),
                          ("Statischer Auftrieb (Archimedisches Prinzip)", False, "Das beschreibt eher den Bimsstein, nicht das mittige Anzünden."),
                          ("Dynamischer Auftrieb (Bernoulli-Prinzip)", False, "Das mittige Anzünden wirkt wie ein Antrieb, nicht wie eine Tragfläche."),
                          ("Elektromagnetische Levitation", False, "Damit hat ein brennender Teebeutel nichts zu tun.")]),
               dict(q="Wo strömt die Luft an einer Tragfläche typischerweise am schnellsten?", done="Richtig — über der gewölbten Oberseite.",
                    opts=[("über der gewölbten Oberseite", True, None), ("unter der flachen Unterseite", False, "Dort strömt die Luft langsamer, das erzeugt den Überdruck."), ("an beiden Seiten gleich schnell", False, "Genau der Geschwindigkeitsunterschied erzeugt den Auftrieb.")]),
               dict(q="Wo entsteht an der Tragfläche der Unterdruck?", done="Richtig — dort, wo die Luft am schnellsten strömt (Oberseite).",
                    opts=[("an der Oberseite, wo die Luft schneller strömt", True, None), ("an der Unterseite, wo die Luft langsamer strömt", False, "Langsamere Strömung erzeugt Überdruck, nicht Unterdruck."), ("gar kein Unterdruck vorhanden", False, "Genau der Unterdruck erzeugt den Auftrieb nach oben.")]),
               dict(q="Hat die Fläche des Flügels (bzw. Balls) Auswirkung auf den Bernoulli-Effekt?", done="Richtig — ja, eine größere Fläche verstärkt die Auftriebswirkung.",
                    opts=[("Ja, die Fläche hat Auswirkung auf den Bernoulli-Effekt.", True, None), ("Nein, die Fläche hat keinen Einfluss.", False, "Eine größere Fläche bedeutet mehr Angriffsfläche für den Druckunterschied.")]),
               dict(q="Was war Daniel Bernoulli?", done="Richtig — Mathematiker und Physiker.",
                    opts=[("Mathematiker und Physiker", True, None), ("Ökonom und Astronom", False, "Er war kein Ökonom."), ("Biologe und Astronom", False, "Er war kein Biologe."), ("nur Astronom", False, "Astronomie war nicht sein Hauptfeld.")]),
               dict(q="Welches Flugprinzip nutzt ein Vogel hauptsächlich beim Gleitflug (ohne Flügelschlag)?", done="Richtig — das Bernoulli-Prinzip, wie bei einer Flugzeug-Tragfläche.",
                    opts=[("Bernoulli-Prinzip", True, None), ("Rückstoßprinzip", False, "Ohne Flügelschlag entsteht kein Rückstoß."), ("statischer Auftrieb", False, "Der Vogel ist dichter als Luft — er braucht dynamischen, nicht statischen Auftrieb."), ("elektromagnetische Levitation", False, "Damit hat Vogelflug nichts zu tun.")]),
             ],
             solution=["Bernoulli-Prinzip: Strömt Luft schneller, sinkt der Druck an dieser Stelle (schnelle Strömung = Unterdruck).",
                       "An einer Tragfläche strömt die Luft oben (gewölbte Seite) schneller als unten — der Druckunterschied drückt den Flügel nach oben.",
                       "Daniel Bernoulli (1700–1782): Schweizer Mathematiker und Physiker, formulierte das nach ihm benannte Strömungsprinzip."]),
        dict(no=14, sjw=14, kind="lernpfad", title="Flugexperimente",
             goal="Du baust und testest eigene Flugobjekte (Papierflieger, Fallschirm, Rotor) und wertest ihre Flugleistung systematisch aus.",
             tasks=["Baue mindestens zwei unterschiedliche Papierflieger-Modelle und miss ihre Flugweite über je drei Würfe.",
                    "Baue einen Mini-Fallschirm aus Papier/Folie und Faden und miss seine Fallzeit aus konstanter Höhe.",
                    "Stelle eine begründete Vermutung auf, welches physikalische Prinzip (Bernoulli oder Luftwiderstand/Rückstoß) bei welchem deiner Modelle überwiegt."],
             tools=[], fast="Verändere gezielt nur ein Merkmal deines besten Papierfliegers (z. B. Flügelfläche oder Nasengewicht) und miss, ob sich die Flugweite verbessert.",
             tags=["Experimentieren", "Werkstatt"],
             quiz=[
               dict(q="Warum ist es wichtig, bei einem Flugversuch mehrfach zu werfen und den Mittelwert zu bilden?", done="Richtig — einzelne Würfe streuen zufällig, der Mittelwert ist verlässlicher.",
                    opts=[("Weil einzelne Würfe zufällig streuen und der Mittelwert genauer ist.", True, None),
                          ("Weil ein einzelner Wurf immer exakt das wahre Ergebnis zeigt.", False, "Genau das Gegenteil ist der Fall — einzelne Würfe schwanken."),
                          ("Weil mehr Würfe den Flieger automatisch weiter fliegen lassen.", False, "Mehrfaches Werfen verändert nicht die Flugweite selbst, nur die Messgenauigkeit.")]),
               dict(q="Was verlangsamt vor allem den Fall eines Papier-Fallschirms?", done="Richtig — der Luftwiderstand der großen, gespannten Fläche.",
                    opts=[("der Luftwiderstand der großen Fläche", True, None), ("der Bernoulli-Effekt", False, "Ein Fallschirm hat keine typische Flügelform mit unterschiedlicher Strömungsgeschwindigkeit."), ("das Rückstoßprinzip", False, "Der Fallschirm stößt nichts aus, wie es bei einer Rakete der Fall wäre.")]),
               dict(q="Welche Veränderung verlängert typischerweise die Flugweite eines Papierfliegers?", done="Richtig — ein passend austariertes, nicht zu leichtes Nasengewicht.",
                    opts=[("ein gut austariertes Nasengewicht", True, None), ("ein möglichst schweres Heck", False, "Ein schweres Heck lässt den Flieger meist nach hinten kippen."), ("möglichst kleine Flügelflächen", False, "Zu kleine Flächen liefern zu wenig Auftrieb.")]),
               dict(q="Was ist eine Forschungsfrage, die zu einem Flugexperiment passt?", done="Richtig — eine klare, überprüfbare Frage zu genau einer veränderten Eigenschaft.",
                    opts=[("Wie verändert sich die Flugweite, wenn ich die Flügelfläche vergrößere?", True, None),
                          ("Welcher Papierflieger sieht am schönsten aus?", False, "Das ist keine messbare, naturwissenschaftliche Frage."),
                          ("Fliegt heute die Sonne?", False, "Das hat nichts mit dem Experiment zu tun.")]),
             ],
             solution=["Papierflieger nutzen überwiegend den Bernoulli-Effekt (Tragflächenform), Fallschirme überwiegend den Luftwiderstand einer großen Fläche.",
                       "Ein faires Experiment verändert immer nur eine Eigenschaft gleichzeitig (z. B. nur die Flügelfläche) und misst mehrfach, um zufällige Schwankungen auszugleichen."]),
      ]),
]

# ---------------------------------------------------------------- Hilfen
def slug(no):
    return "lp%02d" % no

UNIT_OF_LP = {}

def index_units():
    global UNIT_OF_LP
    UNIT_OF_LP = {lp["no"]: u for u in UNITS for lp in u["lps"]}

def einheit_dirname(u):
    return "%s %s" % (u["num"], u["title"])

def lp_dir_parts(no):
    u = UNIT_OF_LP[no]
    return ["lernpfade", einheit_dirname(u)]

def lp_out_dir(no):
    return os.path.join(BASE, *lp_dir_parts(no))

def lp_filename(no):
    parts = lp_dir_parts(no) + ["%s.html" % slug(no)]
    return "/".join(quote(p, safe="") for p in parts)

def companion_url(no, filename):
    parts = lp_dir_parts(no) + [filename]
    return "/".join(quote(p, safe="") for p in parts)

def kind_badge(kind):
    return {"lernpfad":"Lernpfad","projekt":"Projekt"}.get(kind,"Lernpfad")

def unlock_iso(sjw):
    return iso(CAL[sjw][1])

TOTAL_LP = sum(len(u["lps"]) for u in UNITS)

# ---------------------------------------------------------------- gemeinsame Fragmente
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Fredoka:wght@400;500;600;700&'
         'family=Nunito:wght@400;600;700;800&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

with open(os.path.join(ASSET_DIR, "theme.css"), encoding="utf-8") as f:
    THEME_CSS = f.read()
with open(os.path.join(ASSET_DIR, "theme.js"), encoding="utf-8") as f:
    THEME_JS = f.read()

def render_tags(tags):
    out = []
    for t in tags:
        cls = "tag"
        low = t.lower()
        if low.startswith("neu") or " neu" in low:
            cls = "tag neu"
        out.append('<span class="%s">%s</span>' % (cls, esc(t)))
    return "".join(out)

def render_lp_tile(lp):
    mon, fri = CAL[lp["sjw"]]
    fast = ('<div class="lp-fast"><span class="fast-badge">⚡ Schnellläufer:in</span>'
            '<span>%s</span></div>' % lp["fast"]) if lp.get("fast") else ""
    goal = lp["goal"]
    if lp.get("companion"):
        c = lp["companion"]
        goal += (' Übe vorher Schritt für Schritt an der <a href="%s">%s</a>.'
                 % (companion_url(lp["no"], c["file"]), esc(c["label"])))
    return ('<article class="lp" data-unlock="%s">\n'
            '  <div class="lp-key"><div class="lp-week">SJW %d</div>'
            '<div class="lp-no">%02d</div><div class="lp-date">%s</div></div>\n'
            '  <div class="lp-info" data-selfcheck="%s">\n'
            '    <a class="lp-name" href="%s">%s <span class="lp-badge %s">%s</span> <span class="arrow">→</span></a>\n'
            '    <p class="lp-goal"><b>Das lernst du:</b> %s</p>\n'
            '    %s\n'
            '    <p class="lp-rlp">%s</p>\n'
            '  </div>\n'
            '</article>\n') % (
        unlock_iso(lp["sjw"]), lp["sjw"], lp["no"], dm(mon), slug(lp["no"]),
        lp_filename(lp["no"]), esc(lp["title"]), lp["kind"], kind_badge(lp["kind"]),
        goal, fast, render_tags(lp.get("tags", [])))

def render_unit(u):
    weeks = [lp["sjw"] for lp in u["lps"]]
    wlabel = "SJW %d–%d" % (min(weeks), max(weeks)) if len(weeks) > 1 else "SJW %d" % weeks[0]
    tiles = "".join(render_lp_tile(lp) for lp in u["lps"])
    style = "--key:%s;--edge:%s;--tint:%s;--ktext:#fff;" % (u["key"], u["key2"], u["tint"])
    return ('<article class="unit" style="%s">\n'
            '  <div class="unit-bar"><span class="unit-chip">%s</span>'
            '<h3>%s</h3><span class="unit-weeks">%d Lernpfade<br>%s</span></div>\n'
            '  <div class="unit-body">\n%s  </div>\n'
            '</article>\n') % (style, u["num"], esc(u["title"]), len(u["lps"]), wlabel, tiles)

# ---------------------------------------------------------------- index.html
def build_index():
    index_units()
    hero = '''
<header class="hero">
  <div class="float-keys" aria-hidden="true">
    <div class="fkey fk1">🌊</div>
    <div class="fkey fk2">🍎</div>
    <div class="fkey fk3">🪁</div>
    <div class="fkey fk4">🔬</div>
    <div class="fkey fk5">🧪</div>
  </div>
  <div class="wrap">
    <span class="hero-eyebrow"><span class="blink"></span> Naturwissenschaften · Klasse 5 und 6</span>
    <h1 class="hero-title">Entdecke die <span class="pop">Natur</span> — <span class="pop2">forschen</span>, <span class="pop3">staunen</span>, verstehen</h1>
    <p class="hero-lead">
      Ein Schuljahr, drei große Fragen: Warum <b>schwimmen</b> manche Dinge und andere <b>sinken</b>? Was steckt wirklich in unseren <b>Lebensmitteln</b>? Und wie schafft es etwas, zu <b>fliegen</b>? Du experimentierst, misst, staunst — und baust am Ende jeder Reihe dein eigenes Präsentationsprojekt. Diese Seite ist deine <b>Forschungs-Landkarte</b> für das ganze Jahr.
    </p>
  </div>
</header>
'''
    why = '''
<section class="why">
  <div class="wrap why-inner">
    <p class="kicker">// warum forschen wir?</p>
    <h2>Wer <span class="u">selbst experimentiert</span>, versteht die Welt um sich herum wirklich.</h2>
    <div class="why-grid">
      <div class="why-card"><div class="ic" style="background:#2f8fe0;">🧊</div><h3>Selbst herausfinden</h3><p>Nicht nur lesen, sondern messen, wiegen, ausprobieren — du findest die Antworten in echten Experimenten selbst heraus.</p></div>
      <div class="why-card"><div class="ic" style="background:#ff8a3d;">🍽️</div><h3>Alltag verstehen</h3><p>Warum schwimmt eine Orange? Was macht Fett gesund oder ungesund? Naturwissenschaft steckt in jeder Mahlzeit und jedem Bad.</p></div>
      <div class="why-card"><div class="ic" style="background:#8a5cf0;">🪶</div><h3>Genau hinschauen</h3><p>Von der Ahornsamenschraube bis zum Flugzeugflügel — dieselben Prinzipien erklären ganz unterschiedliche Dinge.</p></div>
      <div class="why-card"><div class="ic" style="background:var(--sun);">🚀</div><h3>Für Schnellläufer:innen</h3><p>Wenn dir etwas leichtfällt, wartet die nächste Herausforderung. Zu jedem Lernpfad gibt es eine Extra-Mission.</p></div>
    </div>
  </div>
</section>
'''
    guide = '''
<section class="guide">
  <div class="wrap">
    <h2>So funktioniert diese Seite</h2>
    <p class="sub">Kurz erklärt — dann kann es losgehen.</p>
    <div class="guide-grid">
      <div class="guide-item"><div class="num">1</div><h4>Eine Woche = ein Lernpfad</h4><p>Jede Kursstunde ist ein Lernpfad. <b>SJW</b> heißt Schuljahres-Woche.</p></div>
      <div class="guide-item"><div class="num">2</div><h4>Antippen öffnet die Stunde</h4><p>Ein Klick auf einen Lernpfad öffnet Ziel, Aufgaben und Musterlösung dieser Woche.</p></div>
      <div class="guide-item"><div class="num">3</div><h4>Lösungen schalten sich frei</h4><p>Jede Musterlösung wird automatisch an ihrem Datum sichtbar — die Seite prüft das bei jedem Laden.</p></div>
      <div class="guide-item"><div class="num">4</div><h4>Die Sterne sind dein Check</h4><p>Wie sicher fühlst du dich? Tippe Sterne an — dein Stand bleibt lokal gespeichert.</p></div>
    </div>
    <div class="legend">
      <span class="lg-title">// was bedeuten die Kürzel?</span>
      <span class="lg-item"><span class="lp-badge lernpfad" style="background:#2e9e5b">Lernpfad</span> reguläre Stunde</span>
      <span class="lg-item">🔒 Lösung gesperrt · 🔓 freigeschaltet</span>
    </div>
  </div>
</section>
'''
    lp_by_unit = [len(u["lps"]) for u in UNITS]
    unit_span = []
    for u in UNITS:
        d1, d2 = CAL[u["lps"][0]["sjw"]][0], CAL[u["lps"][-1]["sjw"]][1]
        unit_span.append("%s – %s" % (dm(d1), de(d2)))
    tiles = ""
    for i, u in enumerate(UNITS):
        tiles += (
            '      <button class="sem-tile t%d%s" data-sem="u%d">\n'
            '        <div class="st-id">REIHE %s</div>\n'
            '        <div class="st-title">%s</div>\n'
            '        <div class="st-meta"><span>%d Sitzungen</span><span>%s</span></div>\n'
            '      </button>\n'
        ) % (i + 1, " active" if i == 0 else "", i, u["num"], esc(u["title"]), lp_by_unit[i], unit_span[i])
    selector = ('''
<section class="selector">
  <div class="wrap">
    <h2>Wähle deine Reihe</h2>
    <p class="sub">// drei große Fragen · {tot} feste Lernpfade</p>
    <div class="sem-grid">
''' + tiles + '''    </div>
  </div>
</section>
''').replace("{tot}", str(TOTAL_LP))

    sections = ""
    for i, u in enumerate(UNITS):
        lps = u["lps"]
        d1, d2 = CAL[lps[0]["sjw"]][0], CAL[lps[-1]["sjw"]][1]
        sections += ('<section class="sem-content%s" id="u%d-content">\n'
            '  <div class="sem-head">\n'
            '    <div class="sem-badge">%s</div>\n'
            '    <div><h2>%s</h2><p class="period">%d Lernpfade · %s – %s</p></div>\n'
            '  </div>\n%s\n'
            '</section>\n') % (
            (" active" if i == 0 else ""), i, u["num"], esc(u["title"]),
            len(lps), de(d1), de(d2), render_unit(u))

    classroom = '''
<section class="section classroom">
  <div class="wrap">
    <h2 style="text-align:center;font-family:'Fredoka',sans-serif;font-weight:600;font-size:clamp(1.5rem,3.2vw,2.1rem);margin-bottom:0.4rem;">Material im Google Classroom</h2>
    <p class="sub" style="text-align:center;">// Aufgaben, Dateien &amp; Ankündigungen zu deinem Kurs</p>
    <div class="classroom-grid">
      <a class="classroom-tile" href="https://classroom.google.com/u/0/c/NzEwNzcyMTk1NTQ2" target="_blank" rel="noopener">
        <span class="ct-id">NATURWISSENSCHAFTEN</span>
        <span class="ct-title">Zum Google Classroom <span class="ex">↗</span></span>
      </a>
    </div>
  </div>
</section>
'''

    footer = '''
<footer>
  <div class="foot-inner">
    <div>
      <b class="h">NATURWISSENSCHAFTEN · KLASSE 5 UND 6</b><br>
      Schuljahr 2026/27 · Berlin · 75 Minuten pro Woche
    </div>
    <div>
      Unterrichtsreihen:<br>
      00 Schwimmen und Sinken · 01 Lebensmittel · 02 Fliegen
    </div>
    <div>
      Aufbau:<br>
      {tot} feste Lernpfade · 3 Reihen · Übersicht + Übungs-Archiv<br>
      Lösungen mit zeitlicher Freischaltung
    </div>
  </div>
</footer>
'''.replace("{tot}", str(TOTAL_LP))

    html_doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>Naturwissenschaften · Klasse 5 und 6 — Kursübersicht 2026/27</title>\n'
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n<body>\n'
        + hero + why + guide + selector
        + sections
        + classroom
        + footer
        + '\n<script>\n' + THEME_JS + '\n</script>\n</body>\n</html>\n'
    )
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)

# ---------------------------------------------------------------- Wissens-Check (Quiz)
def render_quiz(lp):
    quiz = lp.get("quiz")
    if not quiz:
        return ""
    items = ""
    for i, q in enumerate(quiz, 1):
        opts = ""
        for text, correct, hint in q["opts"]:
            attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
            opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
        items += (
            '<div class="qz-item">'
            '<div class="qz-text"><span class="qn">%d.</span>%s</div>'
            '<div class="qz-opts">%s</div>'
            '<div class="qz-hint"></div><div class="qz-done">%s</div>'
            '</div>'
        ) % (i, q["q"], opts, q.get("done", "Richtig!"))
    return (
        '<section class="lp-sec"><h2><span class="dot"></span>Wissens-Check</h2>'
        '<div class="qz-wrap" data-qz>'
        '<div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
        '<span class="qz-bar"><span class="qz-fill"></span></span></div>'
        '%s'
        '<div class="qz-solved">✔ Stark — Wissens-Check komplett gelöst!</div>'
        '</div></section>'
    ) % (len(quiz), items)

# ---------------------------------------------------------------- Plickers-Aufgaben zum Nachholen
def render_catchup(lp):
    catchup = lp.get("catchup")
    if not catchup:
        return ""
    items = ""
    for i, q in enumerate(catchup, 1):
        opts = ""
        for text, correct, hint in q["opts"]:
            attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
            opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
        text_block = '<div class="qz-text"><span class="qn">%d.</span>%s</div>' % (i, q["q"])
        if q.get("icon"):
            cls = "qz-icon-fig" + (" " + q["icon_cls"] if q.get("icon_cls") else "")
            text_block = ('<div class="qz-item-row"><div class="%s">%s</div>%s</div>'
                          % (cls, q["icon"], text_block))
        items += (
            '<div class="qz-item">'
            '%s'
            '<div class="qz-opts">%s</div>'
            '<div class="qz-hint"></div><div class="qz-done">%s</div>'
            '</div>'
        ) % (text_block, opts, q.get("done", "Richtig!"))
    title = lp.get("catchup_title", "Plickers-Aufgaben zum Nachholen")
    intro = lp.get("catchup_intro", "Diese Aufgaben habt ihr im Unterricht mit Plickers beantwortet. Wer gefehlt hat oder noch einmal üben möchte, kann sie hier in Ruhe nachholen.")
    return (
        '<section class="lp-sec"><h2><span class="dot"></span>%s</h2>'
        '<p class="vw-intro">%s</p>'
        '<div class="qz-wrap" data-qz>'
        '<div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
        '<span class="qz-bar"><span class="qz-fill"></span></span></div>'
        '%s'
        '<div class="qz-solved">✔ Stark, alle Plickers-Aufgaben nachgeholt!</div>'
        '</div></section>'
    ) % (esc(title), intro, len(catchup), items)

# ---------------------------------------------------------------- Vorwissen (SVG-Figuren + Bild-Quiz)
def render_vorwissen(lp):
    vw = lp.get("vorwissen")
    if not vw:
        return ""
    blocks = ""
    for entry in vw:
        svg = entry["svg"]
        quiz = entry["quiz"]
        items = ""
        for i, q in enumerate(quiz, 1):
            opts = ""
            for text, correct, hint in q["opts"]:
                attr = ' data-correct="true"' if correct else (' data-hint="%s"' % esc(hint) if hint else "")
                opts += '<button class="qz-opt"%s>%s</button>' % (attr, text)
            items += (
                '<div class="qz-item">'
                '<div class="qz-text"><span class="qn">%d.</span>%s</div>'
                '<div class="qz-opts">%s</div>'
                '<div class="qz-hint"></div><div class="qz-done">%s</div>'
                '</div>'
            ) % (i, q["q"], opts, q.get("done", "Richtig!"))
        blocks += (
            '<div class="vw-block">'
            '<div class="fig">%s<div class="fig-cap">%s</div></div>'
            '<div class="qz-wrap" data-qz>'
            '<div class="qz-progress"><span class="qz-count">0 / %d richtig</span>'
            '<span class="qz-bar"><span class="qz-fill"></span></span></div>'
            '%s'
            '<div class="qz-solved">✔ Stark — %s komplett gelöst!</div>'
            '</div></div>'
        ) % (svg, esc(entry["cap"]), len(quiz), items, esc(entry["cap"].split("·")[0].strip()))
    return (
        '<section class="lp-sec"><h2><span class="dot"></span>Schau genau hin — was weißt du schon?</h2>'
        '<p class="vw-intro">Sieh dir das Bild an. Tippe die richtige Antwort an — wird sie grün, ist sie richtig. Bei rot bekommst du einen Tipp.</p>'
        '%s</section>'
    ) % blocks

# ---------------------------------------------------------------- Lernpfad-Seiten
def build_lp_page(u, lp):
    mon, fri = CAL[lp["sjw"]]
    style = "--key:%s;--edge:%s;--tint:%s;--ktext:#fff;" % (u["key"], u["key2"], u["tint"])
    tasks = "".join("<li>%s</li>" % t for t in lp["tasks"])
    tools = ""
    if lp.get("tools"):
        items = ""
        for k in lp["tools"]:
            label, url = T[k]
            items += ('<a class="tool" href="%s" target="_blank" rel="noopener">%s <span class="ex">↗</span></a>'
                      % (url, esc(label)))
        tools = ('<section class="lp-sec"><h2><span class="dot"></span>Werkzeuge</h2><div class="tool-list">%s</div></section>' % items)
    fast = ""
    if lp.get("fast"):
        fast = ('<section class="lp-sec"><div class="fast-box"><span class="fb-t">⚡ Schnellläufer:in</span>%s</div></section>'
                % lp["fast"])
    backup = ('<section class="lp-sec"><div class="backup-box"><span class="bb-t">💾 Ergebnissicherung</span>'
              'Sichere deine Ergebnisse am Stundenende gut lesbar in deinem Forschungsheft oder digital an '
              '<b>zwei Orten</b>. Achte selbstständig auf Backups.</div></section>')
    goal = lp["goal"]
    if lp.get("companion"):
        c = lp["companion"]
        goal += (' Übe vorher Schritt für Schritt an der <a href="%s" style="color:var(--primary-edge);font-weight:700;">%s</a>.'
                 % (esc(c["file"]), esc(c["label"])))
    sol = "".join("<li>%s</li>" % s for s in lp["solution"])
    solution = ('<section class="sol" id="loesung" data-unlock="%s">'
                '<h2>Musterlösung <span class="sol-status">…</span></h2>'
                '<p class="sol-countdown"></p>'
                '<div class="sol-body" hidden><ul class="sol-list">%s</ul></div>'
                '<p class="sol-hint">Die Lösung wird automatisch zum angegebenen Datum sichtbar — '
                'die Seite prüft das bei jedem Laden.</p>'
                '</section>') % (unlock_iso(lp["sjw"]), sol)

    doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>LP %02d · %s — Naturwissenschaften Klasse 5 und 6</title>\n' % (lp["no"], esc(lp["title"]))
        + FONTS + '\n<style>\n' + THEME_CSS + lp.get("extra_css", "") + '\n</style>\n</head>\n'
        '<body style="%s">\n' % style
        + '<div class="lp-page">\n'
        + '  <a class="back" href="../../index.html#u%d-content">← Zurück zur Kursübersicht</a>\n' % UNITS.index(u)
        + '  <div class="badges">\n'
        + '    <span class="b-sjw">SJW %d</span><span class="b-unit">Reihe %s · %s</span>\n' % (lp["sjw"], u["num"], esc(u["title"]))
        + '  </div>\n'
        + '  <div class="lp-hero">\n'
        + '    <div class="hero-row"><div class="keycap">%02d</div><h1>%s</h1></div>\n' % (lp["no"], esc(lp["title"]))
        + '    <p class="goal"><b>Das lernst du:</b> %s</p>\n' % goal
        + '    <p class="rlp">%s</p>\n' % render_tags(lp.get("tags", []))
        + '  </div>\n'
        + ('  %s\n' % render_vorwissen(lp) if lp.get("vorwissen") else '')
        + "".join('  %s\n' % sec for sec in lp.get("pre_sections", []))
        + ('  %s\n' % render_catchup(lp) if lp.get("catchup") and lp.get("catchup_top") else '')
        + '  <section class="lp-sec"><h2><span class="dot"></span>Aufgaben</h2><ul class="task-list">%s</ul></section>\n' % tasks
        + "".join('  %s\n' % sec for sec in lp.get("sections", []))
        + ('  %s\n' % render_quiz(lp) if lp.get("quiz") else '')
        + ('  %s\n' % render_catchup(lp) if lp.get("catchup") and not lp.get("catchup_top") else '')
        + ('  %s\n' % tools if tools else '')
        + ('  %s\n' % fast if fast else '')
        + '  %s\n' % backup
        + '  %s\n' % solution
        + '  <a class="back" href="../../index.html#u%d-content" style="margin-top:1.6rem">← zurück zur Kursübersicht</a>\n' % UNITS.index(u)
        + '</div>\n'
        + '<script>\n' + THEME_JS + '\n</script>\n</body>\n</html>\n'
    )
    out_dir = lp_out_dir(lp["no"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "%s.html" % slug(lp["no"])), "w", encoding="utf-8") as f:
        f.write(doc)

# ---------------------------------------------------------------- Lauf
index_units()
build_index()
count = 0
for u in UNITS:
    for lp in u["lps"]:
        build_lp_page(u, lp)
        count += 1

print("OK — index.html erstellt.")
print("OK — %d Lernpfad-Seiten in lernpfade/ erstellt." % count)
print("Gesamt Lernpfade laut Daten:", TOTAL_LP)
