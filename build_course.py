# -*- coding: utf-8 -*-
"""
Generator: Naturwissenschaften · Klasse 5 (10 J.) — Kursplan 2026/27
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
SKIP = {date(2026,10,19), date(2026,10,26), date(2026,12,21), date(2026,12,28),
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
             tags=["Experimentieren", "Messen & Größen", "neu · Steckbrief"],
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
        dict(no=1, sjw=1, kind="lernpfad", title="Interaktiver naturwissenschaftlicher Steckbrief",
             goal="Du baust zu zweit ein Makey-Makey-Poster über ein Tier mit einer besonderen Körpermaß-Rekordleistung und programmierst es in Scratch so, dass es beim Anfassen davon erzählt.",
             tasks=["Wählt zu zweit ein Tier mit einem besonderen Maß (z. B. Blauwal-Gewicht, Kolibri-Puls, Giraffen-Halsumfang, Kamel-Körpertemperatur) und recherchiert den genauen Rekordwert.",
                    "Gestaltet ein Poster mit Bild und mindestens drei leitfähigen Stellen (z. B. aus Alufolie), die ihr später mit Makey Makey verbindet.",
                    "Programmiert in Scratch: Beim Berühren einer Stelle soll eine Sprechblase oder Tonaufnahme den passenden Messwert nennen — genau wie du dich in LP00 selbst „vorgestellt“ hast."],
             tools=["makey", "scratch"],
             fast="Baut eine vierte, versteckte Kontaktstelle ein, die eine Vergleichsfrage zu eurem eigenen Steckbrief aus LP00 stellt (z. B. „Wie oft passt dein Fuß in die Fußlänge eines Elefanten?“).",
             tags=["Physical Computing", "Team & Präsentation", "neu · Makey Makey"],
             vorwissen=[
               dict(cap="Bild 1 · Tiere mit besonderen Maßen", svg=SVG_TIERPOSTER, quiz=[
                 dict(q="Teil 1 kann über 30 m lang und rund 150 Tonnen schwer werden. Welches Tier ist das?",
                      done="Richtig — der Blauwal, das schwerste Tier der Erde.",
                      opts=[("Blauwal", True, None), ("Pottwal", False, "Der Pottwal ist deutlich kleiner als der Blauwal."),
                            ("Weißer Hai", False, "Haie werden nicht annähernd so schwer."), ("Elefant", False, "Elefanten leben an Land und wiegen viel weniger.")]),
                 dict(q="Teil 2 hat mit bis zu 1200 Schlägen pro Minute den schnellsten Puls im Tierreich. Welches Tier ist das?",
                      done="Richtig — der Kolibri.",
                      opts=[("Kolibri", True, None), ("Spatz", False, "Spatzen haben einen schnellen, aber deutlich niedrigeren Puls."),
                            ("Maus", False, "Mäuse haben einen schnellen Puls, aber nicht so extrem."), ("Adler", False, "Große Vögel haben einen eher langsamen Puls.")]),
                 dict(q="Teil 3 hat einen Hals von bis zu 2 m Länge. Welches Tier ist das?",
                      done="Richtig — die Giraffe.",
                      opts=[("Giraffe", True, None), ("Kamel", False, "Kamele haben einen kurzen Hals."),
                            ("Strauß", False, "Der Straußenhals ist deutlich kürzer."), ("Pferd", False, "Pferde haben einen normalen Hals.")]),
                 dict(q="Teil 4 kann seine Körpertemperatur zwischen 34 °C und 41 °C schwanken lassen, um Wasser zu sparen. Welches Tier ist das?",
                      done="Richtig — das Kamel.",
                      opts=[("Kamel", True, None), ("Eisbär", False, "Eisbären halten ihre Temperatur sehr konstant."),
                            ("Pinguin", False, "Auch Pinguine halten eine sehr konstante Temperatur."), ("Löwe", False, "Löwen schwanken nicht so stark in der Temperatur.")]),
               ]),
             ],
             solution=["Blauwal: bis ~150 t und ~30 m — schwerstes Tier der Erde.", "Kolibri: bis ~1200 Herzschläge/Minute — schnellster Puls im Tierreich.",
                       "Giraffe: Hals bis ~2 m lang — trotzdem nur 7 Halswirbel, genau wie beim Menschen.", "Kamel: Körpertemperatur schwankt 34–41 °C — spart dadurch Schweiß und Wasser."]),
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
             solution=["Orange: r ≈ 4,5 cm, Umfang ≈ 28 cm (2πr), Volumen ≈ 382 ml ((4/3)πr³).",
                       "Mit Schale schwimmt die Orange (viele kleine Lufttaschen in der Schale senken die Dichte unter die von Wasser), ohne Schale sinkt sie meist (Dichte des reinen Fruchtfleischs liegt nahe oder über der von Wasser)."]),
        dict(no=3, sjw=3, kind="lernpfad", title="Übungen und Dichtebestimmung mit digitalen, interaktiven Übungen",
             goal="Du festigst die Formel Dichte = Masse ÷ Volumen (ρ = m/V) an digitalen Übungsaufgaben und lernst, Dichten verschiedener Stoffe miteinander zu vergleichen.",
             tasks=["Wiederhole die Formel ρ = m/V und rechne drei einfache Beispiele im Kopf oder schriftlich durch.",
                    "Bearbeite digitale Übungsaufgaben zur Dichtebestimmung in Partnerarbeit (Zeit pro Aufgabe stoppen, Ergebnisse vergleichen).",
                    "Ordne mindestens fünf Alltagsstoffe (Kork, Eisen, Holz, Öl, Stein) nach steigender Dichte."],
             tools=[], fast="Finde einen Alltagsstoff, dessen Dichte ganz nah an der von Wasser (1 g/cm³) liegt, und begründe, warum er trotzdem manchmal schwimmt und manchmal sinkt.",
             tags=["Üben & Vertiefen", "Dichte"],
             solution=["ρ = m/V — Masse in g oder kg, Volumen in cm³ oder l, Dichte in g/cm³ oder kg/l.",
                       "Ein Stoff schwimmt in Wasser, wenn seine Dichte kleiner als 1 g/cm³ ist, und sinkt, wenn sie größer ist."]),
        dict(no=4, sjw=4, kind="lernpfad", title="Dichtebestimmung mit Orangen",
             goal="Du bestimmst experimentell die Dichte einer Orange mit und ohne Schale und vergleichst sie rechnerisch mit der Dichte von Wasser.",
             tasks=["Wiege die Orange mit und ohne Schale (Masse) und bestimme ihr Volumen per Wasserverdrängung (Eintauchen in einen Messbecher).",
                    "Berechne beide Dichten mit ρ = m/V und vergleiche sie mit der Dichte von Wasser (1 g/cm³).",
                    "Erkläre mithilfe deiner Rechnung, warum deine Beobachtung aus LP02 (schwimmt mit, sinkt ohne Schale) genau dazu passt."],
             tools=[], fast="Wiederhole den Versuch mit einer zweiten Obstsorte deiner Wahl und vergleiche die Ergebnisse mit der Orange.",
             tags=["Experimentieren", "Dichte"],
             solution=["Volumenmessung per Wasserverdrängung: Der Wasserstand steigt genau um das Volumen des eingetauchten Körpers.",
                       "Dichte mit Schale meist unter 1 g/cm³ (schwimmt), Dichte ohne Schale meist ab 1 g/cm³ (sinkt) — passt zur Beobachtung aus LP02."]),
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
        dict(no=7, sjw=7, kind="lernpfad", title="Bananen-Tattoos — Dichte im Alltag",
             goal="Du überträgst dein Dichte-Wissen auf ein alltägliches Phänomen: Warum wird eine mit einem Zahnstocher „geritzte“ Banane an genau dieser Stelle braun?",
             tasks=["Ritze mit einem stumpfen Gegenstand ein einfaches Muster oder Wort in eine unreife Bananenschale.",
                    "Beobachte über die nächsten Stunden, wie sich die geritzte Stelle im Vergleich zur restlichen Schale verändert.",
                    "Erkläre, dass an der beschädigten Stelle mehr Luft (Sauerstoff) an das Fruchtfleisch gelangt und dort schneller ein Bräunungsprozess abläuft."],
             tools=[], fast="Vergleiche die Bräunungsgeschwindigkeit bei einer angeritzten und einer nicht angeritzten Stelle mit der Stoppuhr aus LP00 über mehrere Tage.",
             tags=["Alltagsphänomen", "Experimentieren"],
             solution=["Das Ritzen verletzt Zellen der Schale; austretende Enzyme reagieren mit Sauerstoff aus der Luft (enzymatische Bräunung) — dasselbe Prinzip wie bei einem angeschnittenen Apfel.",
                       "Nach 12–24 Stunden ist das „Tattoo“ deutlich braun sichtbar, während die unversehrte Schale noch grün-gelb bleibt."]),
        dict(no=8, sjw=8, kind="lernpfad", title="Dichte an Fallbeispielen — Vertiefung",
             goal="Du wendest die Dichte-Formel auf verschiedene Fallbeispiele aus dem Alltag an und trainierst den sicheren Umgang mit Einheiten.",
             tasks=["Bearbeite in Gruppen je ein Fallbeispiel (Eisberg im Meer, Heißluftballon, Rettungsring, U-Boot) und stellt es kurz vor.",
                    "Rechnet für euer Fallbeispiel mit passenden Beispielwerten die ungefähre Dichte aus und vergleicht sie mit Wasser bzw. Luft.",
                    "Sammelt an der Tafel alle Fallbeispiele und ordnet sie nach dem Prinzip, das jeweils zum Schwimmen/Steigen führt."],
             tools=[], fast="Erkläre, warum nur etwa ein Neuntel eines Eisbergs aus dem Wasser ragt — rechne mit den Dichten von Eis (0,92 g/cm³) und Meerwasser (1,03 g/cm³).",
             tags=["Üben & Vertiefen", "Dichte"],
             solution=["Eisberg: ρ(Eis)/ρ(Meerwasser) ≈ 0,92/1,03 ≈ 0,89 — rund 89 % des Eisbergs liegen unter Wasser, nur ca. 11 % ragen heraus.",
                       "Gemeinsames Prinzip aller Fallbeispiele: Ein Körper steigt/schwimmt, wenn seine mittlere Dichte kleiner ist als die des umgebenden Mediums."]),
        dict(no=9, sjw=9, kind="lernpfad", title="Weihnachtsbound",
             goal="Du löst in kleinen Teams eine weihnachtliche Rallye aus Rätseln und Experimenten rund um Schwimmen, Sinken und Dichte.",
             tasks=["Löst als Team nacheinander mehrere Stationen mit kurzen Experimenten oder Rätseln zum bisherigen Reihen-Wissen.",
                    "Nutzt Hinweise aus richtig gelösten Stationen, um die nächste Station zu finden (Escape-Game-Prinzip).",
                    "Haltet am Ende fest, welche Station euch am meisten überrascht hat und warum."],
             tools=[], fast="Erfindet selbst eine zusätzliche Rätsel-Station zum Thema Dichte für den nächsten Jahrgang.",
             tags=["Team & Präsentation", "Wiederholung"],
             solution=["Die Bound-Stationen greifen alle bisherigen Themen der Reihe auf: Steckbrief-Größen, Orangen-Dichte, Schiffe/U-Boote, Ölextraktion.",
                       "Am Ende sollte jedes Team alle Stationen gelöst und ihre Lösungswörter zu einem gemeinsamen Weihnachts-Codewort zusammengesetzt haben."]),
        dict(no=10, sjw=10, kind="lernpfad", title="Wiederholung & Quiz-Werkstatt: Schwimmen und Sinken",
             goal="Du fasst die wichtigsten Begriffe und Zusammenhänge der Reihe zusammen und bereitest dich gezielt auf den Kurztest vor.",
             tasks=["Erstellt in Partnerarbeit eine Mindmap mit allen wichtigen Begriffen der Reihe (Dichte, Auftrieb, Volumen, Masse, Wasserverdrängung …).",
                    "Formuliert gegenseitig mindestens drei eigene Quizfragen zu bisherigen Lernpfaden und lasst sie von einem anderen Team beantworten.",
                    "Klärt in der großen Runde alle noch offenen Fragen aus der gesamten Reihe."],
             tools=[], fast="Baue aus deinen Mindmap-Begriffen eine kleine Bilderrätsel-Kette (jeder Begriff führt zum nächsten).",
             tags=["Wiederholung"],
             solution=["Zentrale Begriffe: Dichte (ρ=m/V), Auftrieb, Volumen (auch per Wasserverdrängung), Masse vs. Gewicht, Hohlkörper-Prinzip.",
                       "Wer alle Begriffe sicher erklären kann, ist gut auf den Kurztest vorbereitet."]),
        dict(no=11, sjw=11, kind="lernpfad", title="Kurztest: Schwimmen und Sinken",
             goal="Du zeigst in einem kurzen schriftlichen Test, wie sicher du die Begriffe und Rechnungen der Reihe „Schwimmen und Sinken“ beherrschst.",
             tasks=["Bearbeite den Kurztest in Einzelarbeit (ca. 30 Minuten): Begriffe erklären, Dichte berechnen, Alltagsbeispiele einordnen.",
                    "Kontrolliere am Ende deine Rechnungen noch einmal auf Einheiten und Kommastellen.",
                    "Schätze am Ende selbst ein, wie sicher du dich bei den einzelnen Aufgabenteilen gefühlt hast."],
             tools=[], fast="Formuliere zu deiner unsichersten Testaufgabe eine eigene Zusatzfrage, die du in der nächsten Stunde stellen möchtest.",
             tags=["Lernkontrolle"],
             solution=["Der Test wird von der Lehrkraft korrigiert und in der folgenden Stunde besprochen.",
                       "Nutze deine Selbsteinschätzung, um gezielt die Themen zu wiederholen, bei denen du unsicher warst."]),
        dict(no=12, sjw=12, kind="projekt", title="Präsentationsprojekt: Experimente vorbereiten",
             goal="Du planst mit deiner Gruppe ein eigenes Experiment zum Thema Schwimmen und Sinken, das ihr dem Kurs vorstellen wollt.",
             tasks=["Wählt in der Gruppe ein Experiment aus der Reihe (oder eine eigene Idee) aus, das ihr vertiefen möchtet.",
                    "Plant Materialliste, Versuchsaufbau und die genaue Erklärung, die ihr präsentieren wollt.",
                    "Übt den Versuchsaufbau mindestens einmal vollständig durch, bevor ihr präsentiert."],
             tools=[], fast="Überlegt euch eine Verständnisfrage, die ihr dem Kurs nach eurer Präsentation stellen wollt.",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Eine gute Vorbereitung enthält: klare Forschungsfrage, vollständige Materialliste, geübten Ablauf, verständliche Erklärung der Dichte-Zusammenhänge.",
                       "Zeitpuffer für Pannen einplanen — ein Experiment sollte notfalls auch ohne perfektes Ergebnis erklärt werden können."]),
        dict(no=13, sjw=13, kind="projekt", title="Präsentationsprojekt: Präsentationstag",
             goal="Du präsentierst dein Experiment zum Thema Schwimmen und Sinken vor dem Kurs und gibst deinen Mitschüler:innen faires Feedback.",
             tasks=["Führt euer Experiment vor dem Kurs vor und erklärt die dahinterliegende Dichte-Erklärung verständlich.",
                    "Beantwortet Verständnisfragen aus dem Kurs.",
                    "Gebt mindestens einer anderen Gruppe konkretes, freundliches Feedback."],
             tools=[], fast="Vergleicht euer Experiment mit einem Experiment einer anderen Gruppe: Was ist die gemeinsame Dichte-Idee dahinter?",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Am Ende der Reihe sollten alle Gruppen den Zusammenhang von Dichte, Auftrieb und Volumen an einem eigenen Beispiel erklären können.",
                       "Die Präsentationen bilden den Abschluss der Reihe „Schwimmen und Sinken“ vor den Weihnachtsferien."]),
      ]),
 # =================== 01 LEBENSMITTEL ===================
 dict(num="01", title="Lebensmittel",
      key="#ff8a3d", key2="#d96a1f", tint="rgba(255,138,61,0.10)",
      lps=[
        dict(no=14, sjw=14, kind="lernpfad", title="Nahrungsmittelrallye",
             goal="Du lernst die drei Hauptnährstoffe (Fette, Proteine, Kohlenhydrate) und die Mikronährstoffe (Vitamine, Mineralstoffe) kennen und ordnest sie echten Lebensmitteln zu.",
             tasks=["Ordne an Stationen verschiedene Lebensmittel den Hauptnährstoffen zu, die in ihnen überwiegen.",
                    "Unterscheide Makronährstoffe (Fette, Proteine, Kohlenhydrate) von Mikronährstoffen (z. B. Vitamin C, Kalium, Calcium).",
                    "Vergleiche drei Erfrischungsgetränke und bewerte sie nach gesundheitlichen Gesichtspunkten (Zucker, Säure, Zusatzstoffe)."],
             tools=[], fast="Erstelle eine Woche-Speiseplan-Idee, die alle drei Hauptnährstoffe ausgewogen berücksichtigt.",
             tags=["Ernährung", "neu · Nährstoffe"],
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
        dict(no=15, sjw=15, kind="lernpfad", title="Interessantes zu Fetten",
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
        dict(no=16, sjw=16, kind="lernpfad", title="Energiehaushalt",
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
        dict(no=17, sjw=17, kind="lernpfad", title="Denaturierung von Proteinen am Beispiel von pflanzlichen Baisers",
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
        dict(no=18, sjw=18, kind="lernpfad", title="Kohlenhydrate",
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
        dict(no=19, sjw=19, kind="lernpfad", title="Geschmackssinn & Erfrischungsgetränke im Test",
             goal="Du testest verblindet verschiedene Erfrischungsgetränke, ordnest sie nach Beliebtheit und bewertest sie zusätzlich nach Gesundheitswert.",
             tasks=["Verkoste im Blindtest drei bis vier Erfrischungsgetränke und bringt sie als Team in eine Geschmacksreihenfolge.",
                    "Vergleicht eure Geschmacksreihenfolge mit den Zutatenlisten (Zucker-, Säure-, Zusatzstoffgehalt).",
                    "Stellt begründete Vermutungen auf, wie viele unterschiedliche Geschmacksfaktoren (z. B. süß, sauer, Kohlensäure) euer Ranking beeinflusst haben."],
             tools=[], fast="Entwerft ein eigenes, möglichst gesundes Erfrischungsgetränk-Rezept und begründet eure Zutatenwahl.",
             tags=["Experimentieren", "Sinne"],
             solution=["Geschmack entsteht aus dem Zusammenspiel mehrerer Faktoren: Süße, Säure, Kohlensäure-Prickeln, Temperatur und Geruch.",
                       "Ein hoher Zucker- oder Säuregehalt sorgt oft für hohe Beliebtheit, ist aber gesundheitlich nicht automatisch die beste Wahl."]),
        dict(no=20, sjw=20, kind="lernpfad", title="Nährstoffe-Werkstatt: Ballaststoffe, Vitamine & Co.",
             goal="Du vertiefst dein Wissen über Mikronährstoffe und Ballaststoffe und erklärst, warum sie trotz kaum vorhandener Kalorien wichtig sind.",
             tasks=["Recherchiert an Stationen zu je einem Mikronährstoff (z. B. Vitamin C, Calcium, Eisen) dessen Funktion im Körper.",
                    "Ordnet Lebensmittel den jeweiligen Mikronährstoffen zu, in denen sie besonders reichlich vorkommen.",
                    "Erklärt, warum Ballaststoffe trotz kaum verwertbarer Energie wichtig für die Verdauung sind."],
             tools=[], fast="Entwerft ein Kurs-Plakat, das alle recherchierten Mikronährstoffe mit Symbol und Lebensmittel-Beispiel zeigt.",
             tags=["Ernährung", "Üben & Vertiefen"],
             solution=["Vitamine und Mineralstoffe steuern viele Körperfunktionen (z. B. Immunsystem, Knochenaufbau, Sauerstofftransport), liefern aber selbst kaum Energie.",
                       "Ballaststoffe regen die Verdauung an und sorgen für ein lang anhaltendes Sättigungsgefühl, obwohl sie kaum verdaut werden."]),
        dict(no=21, sjw=21, kind="lernpfad", title="Wiederholung & Quiz-Werkstatt: Lebensmittel",
             goal="Du fasst die wichtigsten Begriffe und Zusammenhänge der Reihe „Lebensmittel“ zusammen und bereitest dich auf den Kurztest vor.",
             tasks=["Erstellt eine gemeinsame Übersicht aller Nährstoffgruppen mit je zwei Beispiel-Lebensmitteln.",
                    "Formuliert gegenseitig eigene Quizfragen zu Fetten, Proteinen, Kohlenhydraten und Mikronährstoffen.",
                    "Klärt in der großen Runde alle noch offenen Fragen aus der gesamten Reihe."],
             tools=[], fast="Baue ein kleines Ratespiel: Beschreibe ein Lebensmittel nur über seine Nährstoffe, die anderen raten, welches es ist.",
             tags=["Wiederholung"],
             solution=["Zentrale Begriffe: Makronährstoffe (Fette, Proteine, Kohlenhydrate) vs. Mikronährstoffe (Vitamine, Mineralstoffe), Denaturierung, Jodprobe, Fettfleckprobe.",
                       "Wer alle Nachweisverfahren und Nährstoffgruppen sicher erklären kann, ist gut auf den Kurztest vorbereitet."]),
        dict(no=22, sjw=22, kind="lernpfad", title="Kurztest: Lebensmittel",
             goal="Du zeigst in einem kurzen schriftlichen Test, wie sicher du die Begriffe und Nachweisverfahren der Reihe „Lebensmittel“ beherrschst.",
             tasks=["Bearbeite den Kurztest in Einzelarbeit (ca. 30 Minuten): Nährstoffe zuordnen, Nachweisverfahren erklären, Alltagsbeispiele einordnen.",
                    "Kontrolliere am Ende deine Antworten noch einmal auf Vollständigkeit.",
                    "Schätze am Ende selbst ein, wie sicher du dich bei den einzelnen Aufgabenteilen gefühlt hast."],
             tools=[], fast="Formuliere zu deiner unsichersten Testaufgabe eine eigene Zusatzfrage, die du in der nächsten Stunde stellen möchtest.",
             tags=["Lernkontrolle"],
             solution=["Der Test wird von der Lehrkraft korrigiert und in der folgenden Stunde besprochen.",
                       "Nutze deine Selbsteinschätzung, um gezielt die Themen zu wiederholen, bei denen du unsicher warst."]),
        dict(no=23, sjw=23, kind="projekt", title="Präsentationsprojekt: Experimente vorbereiten",
             goal="Du planst mit deiner Gruppe ein eigenes Experiment zum Thema Lebensmittel, das ihr dem Kurs vorstellen wollt.",
             tasks=["Wählt in der Gruppe ein Experiment aus der Reihe (oder eine eigene Idee) aus, das ihr vertiefen möchtet.",
                    "Plant Materialliste, Versuchsaufbau und die genaue Erklärung, die ihr präsentieren wollt.",
                    "Übt den Versuchsaufbau mindestens einmal vollständig durch, bevor ihr präsentiert."],
             tools=[], fast="Überlegt euch eine Verständnisfrage, die ihr dem Kurs nach eurer Präsentation stellen wollt.",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Eine gute Vorbereitung enthält: klare Forschungsfrage, vollständige Materialliste, geübten Ablauf, verständliche Erklärung der Nährstoff-Zusammenhänge.",
                       "Zeitpuffer für Pannen einplanen — ein Experiment sollte notfalls auch ohne perfektes Ergebnis erklärt werden können."]),
        dict(no=24, sjw=24, kind="projekt", title="Präsentationsprojekt: Präsentationstag",
             goal="Du präsentierst dein Experiment zum Thema Lebensmittel vor dem Kurs und gibst deinen Mitschüler:innen faires Feedback.",
             tasks=["Führt euer Experiment vor dem Kurs vor und erklärt die dahinterliegende Nährstoff-Erklärung verständlich.",
                    "Beantwortet Verständnisfragen aus dem Kurs.",
                    "Gebt mindestens einer anderen Gruppe konkretes, freundliches Feedback."],
             tools=[], fast="Vergleicht euer Experiment mit einem Experiment einer anderen Gruppe: Welche Nährstoff-Idee steckt jeweils dahinter?",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Am Ende der Reihe sollten alle Gruppen Nährstoffe, Nachweisverfahren und Denaturierung an einem eigenen Beispiel erklären können.",
                       "Die Präsentationen bilden den Abschluss der Reihe „Lebensmittel“."]),
      ]),
 # =================== 02 FLIEGEN ===================
 dict(num="02", title="Fliegen",
      key="#8a5cf0", key2="#6a3fcf", tint="rgba(138,92,240,0.10)",
      lps=[
        dict(no=25, sjw=25, kind="lernpfad", title="Schwimmende Steine und fliegende Teebeutel",
             goal="Du entdeckst mit zwei verblüffenden Experimenten (schwimmender Bimsstein, fliegender Teebeutel), dass Auftrieb ein Prinzip ist, das sowohl im Wasser als auch in der Luft gilt.",
             tasks=["Teste, ob ein Bimsstein in Wasser schwimmt oder sinkt, und erkläre es mit seiner extrem geringen Dichte (viele Luftbläschen).",
                    "Baue eine Teebeutel-Rakete: Entleere einen Teebeutel, stelle ihn aufrecht hin und zünde ihn oben mittig an.",
                    "Verallgemeinere: Ein Körper erfährt Auftrieb, wenn seine Dichte geringer ist als die seines umgebenden Stoffs."],
             tools=[], fast="Erkläre, warum der Teebeutel höher und schneller fliegt, wenn er genau in der Mitte angezündet wird, statt am Rand.",
             tags=["Experimentieren", "Auftrieb", "neu · Fliegen"],
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
        dict(no=26, sjw=26, kind="lernpfad", title="Flugprinzipien",
             goal="Du lernst mit dem Bernoulli-Prinzip den zweiten großen Auftriebs-Mechanismus kennen: schnell strömende Luft erzeugt Unterdruck.",
             tasks=["Baue den klassischen Papierstreifen- oder Tischtennisball-Versuch zum Bernoulli-Effekt auf und beobachte den Effekt.",
                    "Erkläre am Modell eines Flügels, wo die Luft schneller strömt und wo dadurch Unter- bzw. Überdruck entsteht.",
                    "Recherchiere kurz, wer Daniel Bernoulli war und wofür er bekannt ist."],
             tools=[], fast="Finde heraus, ob die Flügel- bzw. Ballfläche einen Einfluss auf die Stärke des Bernoulli-Effekts hat, und begründe mit einem eigenen Mini-Versuch.",
             tags=["Experimentieren", "Bernoulli-Prinzip"],
             quiz=[
               dict(q="Nenne das Auftriebsprinzip der Teebeutelrakete aus LP25.", done="Richtig — das Rückstoßprinzip.",
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
        dict(no=27, sjw=27, kind="lernpfad", title="Flugexperimente",
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
        dict(no=28, sjw=28, kind="lernpfad", title="Bernoulli-Auftrieb im Flugzeug — Vertiefung",
             goal="Du überträgst das Bernoulli-Prinzip konkret auf ein startendes und landendes Flugzeug und erklärst die Funktion von Landeklappen.",
             tasks=["Skizziere den Querschnitt einer Tragfläche und markiere Luftströmung, Unterdruck- und Überdruckbereich.",
                    "Erkläre mithilfe eines Modells, warum ein Flugzeug beim Start eine hohe Geschwindigkeit erreichen muss, bevor es abheben kann.",
                    "Recherchiere, wofür Landeklappen an Tragflächen dienen und wie sie den Auftrieb bei niedrigerer Geschwindigkeit erhöhen."],
             tools=[], fast="Erkläre, warum ein beladenes Flugzeug eine längere Startbahn braucht als ein leichtes.",
             tags=["Üben & Vertiefen", "Bernoulli-Prinzip"],
             solution=["Erst ab einer bestimmten Mindestgeschwindigkeit ist der Geschwindigkeits- und damit Druckunterschied zwischen Ober- und Unterseite der Tragfläche groß genug, um das gesamte Flugzeuggewicht zu tragen.",
                       "Landeklappen vergrößern und wölben die Tragfläche zusätzlich — das erzeugt mehr Auftrieb auch bei der geringeren Geschwindigkeit während Start und Landung."]),
        dict(no=29, sjw=29, kind="lernpfad", title="Vogelflug, Ahornsamen & Co. — Flugprinzipien in der Natur",
             goal="Du entdeckst, dass die Natur alle drei Flugprinzipien (Bernoulli, Rückstoß, Luftwiderstand) auf ganz unterschiedliche Weise nutzt.",
             tasks=["Baue eine Ahornsamenschraube aus Papier nach und beobachte ihren Sinkflug im Vergleich zu einem einfachen Papierschnipsel.",
                    "Ordne Löwenzahnsamen, Schmetterlingsflug und Tornados jeweils dem passenden physikalischen Prinzip zu.",
                    "Vergleiche die Flugstrategie eines gleitenden Vogels mit der eines Kolibris (aus LP01) — wo überwiegt Segeln, wo aktives Flügelschlagen?"],
             tools=[], fast="Baue selbst eine funktionierende Ahornsamenschraube und optimiere Flügelform und -länge auf möglichst langsamen Fall.",
             tags=["Natur & Vorbild", "Bernoulli-Prinzip"],
             quiz=[
               dict(q="Warum fallen Ahornsamenschrauben langsamer als gewöhnliche Pflanzensamen?", done="Richtig — durch ihre Rotation erzeugen sie unterschiedliche Luftgeschwindigkeiten wie an einer Tragfläche.",
                    opts=[("Sie erzeugen durch Rotation unterschiedliche Luftgeschwindigkeiten (Auto-Rotation).", True, None),
                          ("Sie nutzen den Rückstoß ihrer Rotation.", False, "Es wird keine Masse ausgestoßen — das ist kein Rückstoßprinzip."),
                          ("Sie werden von Magneten in der Luft gehalten.", False, "Magnetismus spielt beim Pflanzenflug keine Rolle.")]),
               dict(q="Welches physikalische Prinzip ist bei der Windverbreitung von Löwenzahnsamen NICHT beteiligt?", done="Richtig — das Rückstoßprinzip kommt hier nicht vor.",
                    opts=[("Rückstoßprinzip", True, None), ("Bernoulli-Prinzip", False, "Die feine Schirmchen-Struktur erzeugt tatsächlich auch aerodynamischen Auftrieb."), ("Luftwiderstand", False, "Der große, leichte Schirm bremst den Fall durch Luftwiderstand."), ("Auftrieb durch Luftströmung", False, "Aufwinde können den Samen zusätzlich tragen.")]),
               dict(q="Welche Kombination von Faktoren sorgt für den effizienten Flug von Schmetterlingen?", done="Richtig — Bernoulli-Prinzip UND komplexe Luftwirbel.",
                    opts=[("Bernoulli-Prinzip UND komplexe Luftwirbel", True, None),
                          ("statischer Auftrieb UND komplexe Luftwirbel", False, "Schmetterlinge sind dichter als Luft — statischer Auftrieb reicht nicht aus."),
                          ("Rückstoßprinzip durch Flügelschlag UND Bernoulli-Prinzip", False, "Der Flügelschlag erzeugt keinen klassischen Rückstoß wie ein Raketentriebwerk.")]),
               dict(q="Ein Tornado zeigt das Bernoulli-Prinzip in extremer Form. Wie sind die Druckverhältnisse im Zentrum?", done="Richtig — im Zentrum ist der Druck deutlich niedriger als außen.",
                    opts=[("Im Zentrum ist der Druck niedriger als außen.", True, None), ("Im Zentrum ist der Druck höher als außen.", False, "Genau umgekehrt — die extrem schnelle Rotation erzeugt einen starken Unterdruck im Kern."), ("Der Druck ist überall gleich.", False, "Gerade der starke Druckunterschied macht einen Tornado so gefährlich.")]),
             ],
             solution=["Ahornsamen: Rotation erzeugt Bernoulli-Auftrieb wie ein Mini-Hubschrauber-Rotor.",
                       "Löwenzahn: Luftwiderstand und etwas aerodynamischer Auftrieb, aber kein Rückstoß.",
                       "Schmetterling: Kombination aus Bernoulli-Effekt und gezielt erzeugten Luftwirbeln an den Flügelrändern.",
                       "Tornado: extrem schnelle Rotation erzeugt nach Bernoulli einen sehr starken Unterdruck im Zentrum."]),
        dict(no=30, sjw=30, kind="lernpfad", title="Fluggeräte selbst bauen — Werkstatt",
             goal="Du konstruierst ein eigenes Fluggerät (Rotor, Drachen oder Flieger-Modell deiner Wahl) und optimierst es in mehreren Testrunden.",
             tasks=["Wähle ein Fluggerät-Modell (Papprotor, Mini-Drachen, Flugobjekt eigener Idee) und baue einen ersten Prototyp.",
                    "Teste deinen Prototyp mehrfach, miss Flugzeit oder Flugweite und notiere Verbesserungsideen.",
                    "Baue eine verbesserte zweite Version und vergleiche die Messwerte mit der ersten Version."],
             tools=[], fast="Baue eine dritte Version, die bewusst ein völlig anderes physikalisches Prinzip nutzt als deine ersten beiden, und vergleiche alle drei.",
             tags=["Werkstatt", "Experimentieren"],
             solution=["Systematisches Konstruieren bedeutet: bauen, testen, messen, gezielt eine Sache verändern, erneut testen.",
                       "Jede Verbesserung sollte auf einer konkreten physikalischen Überlegung beruhen (z. B. mehr Fläche für mehr Auftrieb, weniger Gewicht für längere Flugzeit)."]),
        dict(no=31, sjw=31, kind="lernpfad", title="Ausblick: Weltall",
             goal="Du erfährst, warum im Weltall die bisherigen Flugprinzipien (Bernoulli, Luftwiderstand) nicht mehr funktionieren und wie Raketen trotzdem fliegen.",
             tasks=["Erkläre, warum ein Flugzeugflügel im Weltall keinen Auftrieb erzeugen könnte (keine Luft vorhanden).",
                    "Beschreibe, wie eine Rakete allein durch das Rückstoßprinzip auch im Vakuum vorwärtskommt.",
                    "Vergleiche kurz die Teebeutel-Rakete aus LP25 mit einer echten Rakete: Was ist gleich, was ist anders?"],
             tools=[], fast="Recherchiere, mit welcher Geschwindigkeit eine Rakete die Erde verlassen muss (Fluchtgeschwindigkeit), um nicht wieder zurückzufallen.",
             tags=["Ausblick", "Rückstoßprinzip"],
             solution=["Ohne Luft gibt es weder Bernoulli-Auftrieb noch Luftwiderstand — im Weltraum funktioniert nur das Rückstoßprinzip (Ausstoß von Gasen nach hinten treibt die Rakete nach vorn).",
                       "Die Teebeutel-Rakete nutzt denselben Grundgedanken (Ausstoßen heißer Gase), allerdings zusätzlich unterstützt durch die im Vakuum nicht vorhandene, hier aber wirksame heiße Luft."]),
        dict(no=32, sjw=32, kind="lernpfad", title="Vibe-Coding: eigene Flug-Idee programmieren",
             goal="Du beschreibst einer KI in eigenen Worten eine kleine Flug-Simulation oder Flug-Animation und lässt sie gemeinsam mit dir Schritt für Schritt entstehen (Vibe-Coding).",
             tasks=["Formuliere eine klare Idee für eine kleine interaktive Seite zum Thema Fliegen (z. B. Papierflieger-Simulator, Ballon-Steig-Animation).",
                    "Beschreibe deine Idee in präzisen, kleinen Schritten und lass jeden Schritt einzeln umsetzen, bevor du weitermachst.",
                    "Teste deine Seite nach jedem Schritt sofort im Browser und beschreibe, was noch nicht passt."],
             tools=["jsfiddle"], fast="Baue eine kleine Interaktion ein (z. B. ein Knopf „Pusten“, der ein Objekt auf dem Bildschirm nach oben steigen lässt).",
             tags=["Programmieren", "neu · Vibe-Coding"],
             solution=["Vibe-Coding bedeutet: präzise, kleine Anweisungen formulieren, jeden Schritt sofort testen und bei Bedarf präziser nachfragen — genau wie Profilkurs-Schüler:innen es später in Klasse 9 im Detail lernen.",
                       "Auch ohne klassische Programmierkenntnisse lässt sich so eine kleine funktionierende Idee umsetzen."]),
        dict(no=33, sjw=33, kind="lernpfad", title="Wiederholung & Quiz-Werkstatt: Fliegen",
             goal="Du fasst die wichtigsten Begriffe und Zusammenhänge der Reihe „Fliegen“ zusammen und bereitest dich auf den Kurztest vor.",
             tasks=["Erstellt eine gemeinsame Übersicht der drei Flugprinzipien (statischer Auftrieb, Bernoulli-Prinzip, Rückstoßprinzip) mit je einem Beispiel.",
                    "Formuliert gegenseitig eigene Quizfragen zu Teebeutel-Rakete, Tragfläche und Naturbeispielen.",
                    "Klärt in der großen Runde alle noch offenen Fragen aus der gesamten Reihe."],
             tools=[], fast="Ordne jedem Lernpfad der Reihe „Fliegen“ das jeweils passende Hauptprinzip zu und begründe kurz.",
             tags=["Wiederholung"],
             solution=["Drei Flugprinzipien: statischer Auftrieb (Dichteunterschied, z. B. Heißluftballon), dynamischer/Bernoulli-Auftrieb (Tragfläche, Vogelflug), Rückstoßprinzip (Rakete, Teebeutel mittig gezündet).",
                       "Wer alle drei Prinzipien an einem eigenen Beispiel erklären kann, ist gut auf den Kurztest vorbereitet."]),
        dict(no=34, sjw=34, kind="lernpfad", title="Kurztest: Fliegen",
             goal="Du zeigst in einem kurzen schriftlichen Test, wie sicher du die Flugprinzipien der Reihe „Fliegen“ beherrschst.",
             tasks=["Bearbeite den Kurztest in Einzelarbeit (ca. 30 Minuten): Flugprinzipien zuordnen, Beispiele erklären, Alltagsphänomene einordnen.",
                    "Kontrolliere am Ende deine Antworten noch einmal auf Vollständigkeit.",
                    "Schätze am Ende selbst ein, wie sicher du dich bei den einzelnen Aufgabenteilen gefühlt hast."],
             tools=[], fast="Formuliere zu deiner unsichersten Testaufgabe eine eigene Zusatzfrage, die du in der nächsten Stunde stellen möchtest.",
             tags=["Lernkontrolle"],
             solution=["Der Test wird von der Lehrkraft korrigiert und in der folgenden Stunde besprochen.",
                       "Nutze deine Selbsteinschätzung, um gezielt die Themen zu wiederholen, bei denen du unsicher warst."]),
        dict(no=35, sjw=35, kind="projekt", title="Präsentationsprojekt: Experimente vorbereiten",
             goal="Du planst mit deiner Gruppe ein eigenes Experiment zum Thema Fliegen, das ihr dem Kurs vorstellen wollt.",
             tasks=["Wählt in der Gruppe ein Experiment aus der Reihe (oder eine eigene Idee) aus, das ihr vertiefen möchtet.",
                    "Plant Materialliste, Versuchsaufbau und die genaue Erklärung, die ihr präsentieren wollt.",
                    "Übt den Versuchsaufbau mindestens einmal vollständig durch, bevor ihr präsentiert."],
             tools=[], fast="Überlegt euch eine Verständnisfrage, die ihr dem Kurs nach eurer Präsentation stellen wollt.",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Eine gute Vorbereitung enthält: klare Forschungsfrage, vollständige Materialliste, geübten Ablauf, verständliche Erklärung des genutzten Flugprinzips.",
                       "Zeitpuffer für Pannen einplanen — ein Experiment sollte notfalls auch ohne perfektes Ergebnis erklärt werden können."]),
        dict(no=36, sjw=36, kind="projekt", title="Präsentationsprojekt: Präsentationstag",
             goal="Du präsentierst dein Experiment zum Thema Fliegen vor dem Kurs, blickst auf das ganze Schuljahr zurück und gibst deinen Mitschüler:innen faires Feedback.",
             tasks=["Führt euer Experiment vor dem Kurs vor und erklärt das dahinterliegende Flugprinzip verständlich.",
                    "Beantwortet Verständnisfragen aus dem Kurs.",
                    "Blickt gemeinsam zurück: Welches der drei großen Themen (Schwimmen und Sinken, Lebensmittel, Fliegen) hat euch am meisten überrascht?"],
             tools=[], fast="Schreibe dir selbst eine kurze Notiz: Was hast du in diesem Schuljahr über das Forschen selbst gelernt — nicht nur über die Inhalte?",
             tags=["Team & Präsentation", "Projekt"],
             solution=["Am Ende des Schuljahres sollten alle drei großen Prinzipien sicher erklärt werden können: Dichte/Auftrieb, Nährstoffe/Denaturierung, Flugprinzipien.",
                       "Die Präsentationen bilden den krönenden Abschluss des ersten Naturwissenschaften-Schuljahres."]),
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
        lp["goal"], fast, render_tags(lp.get("tags", [])))

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
    <span class="hero-eyebrow"><span class="blink"></span> Naturwissenschaften · Klasse 5</span>
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
      <span class="lg-item"><span class="lp-badge projekt" style="background:#2f8fe0">Projekt</span> Präsentationsprojekt</span>
      <span class="lg-item">🔒 Lösung gesperrt · 🔓 freigeschaltet</span>
      <span class="lg-item"><span class="tag neu">neu</span> neue Methode in diesem Kurs</span>
    </div>
  </div>
</section>
'''
    lp_by_unit = [len(u["lps"]) for u in UNITS]
    selector = '''
<section class="selector">
  <div class="wrap">
    <h2>Wähle deine Reihe</h2>
    <p class="sub">// drei große Fragen · ein Schuljahr · {tot} Lernpfade</p>
    <div class="sem-grid">
      <button class="sem-tile t1 active" data-sem="u0">
        <div class="st-id">REIHE 00</div>
        <div class="st-title">Schwimmen und Sinken</div>
        <div class="st-meta"><span>{n0} Sitzungen</span><span>Aug – Dez 2026</span></div>
      </button>
      <button class="sem-tile t2" data-sem="u1">
        <div class="st-id">REIHE 01</div>
        <div class="st-title">Lebensmittel</div>
        <div class="st-meta"><span>{n1} Sitzungen</span><span>Jan – Mär 2027</span></div>
      </button>
      <button class="sem-tile t3" data-sem="u2">
        <div class="st-id">REIHE 02</div>
        <div class="st-title">Fliegen</div>
        <div class="st-meta"><span>{n2} Sitzungen</span><span>Apr – Jul 2027</span></div>
      </button>
    </div>
  </div>
</section>
'''.replace("{tot}", str(TOTAL_LP)).replace("{n0}", str(lp_by_unit[0])).replace("{n1}", str(lp_by_unit[1])).replace("{n2}", str(lp_by_unit[2]))

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

    footer = '''
<footer>
  <div class="foot-inner">
    <div>
      <b class="h">NATURWISSENSCHAFTEN · KLASSE 5</b><br>
      Schuljahr 2026/27 · Berlin · 75 Minuten pro Woche
    </div>
    <div>
      Unterrichtsreihen:<br>
      00 Schwimmen und Sinken · 01 Lebensmittel · 02 Fliegen
    </div>
    <div>
      Aufbau:<br>
      {tot} Lernpfade · 3 Reihen · Übersicht + Übungs-Archiv<br>
      Lösungen mit zeitlicher Freischaltung
    </div>
  </div>
</footer>
'''.replace("{tot}", str(TOTAL_LP))

    html_doc = (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>Naturwissenschaften · Klasse 5 — Kursübersicht 2026/27</title>\n'
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n<body>\n'
        + hero + why + guide + selector
        + sections
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
        '<title>LP %02d · %s — Naturwissenschaften Klasse 5</title>\n' % (lp["no"], esc(lp["title"]))
        + FONTS + '\n<style>\n' + THEME_CSS + '\n</style>\n</head>\n'
        '<body style="%s">\n' % style
        + '<div class="lp-page">\n'
        + '  <a class="back" href="../../index.html#u%d-content">← Zurück zur Kursübersicht</a>\n' % UNITS.index(u)
        + '  <div class="badges">\n'
        + '    <span class="b-sjw">SJW %d</span><span class="b-unit">Reihe %s · %s</span>\n' % (lp["sjw"], u["num"], esc(u["title"]))
        + '  </div>\n'
        + '  <div class="lp-hero">\n'
        + '    <div class="hero-row"><div class="keycap">%02d</div><h1>%s</h1></div>\n' % (lp["no"], esc(lp["title"]))
        + '    <p class="goal"><b>Das lernst du:</b> %s</p>\n' % lp["goal"]
        + '    <p class="rlp">%s</p>\n' % render_tags(lp.get("tags", []))
        + '  </div>\n'
        + ('  %s\n' % render_vorwissen(lp) if lp.get("vorwissen") else '')
        + '  <section class="lp-sec"><h2><span class="dot"></span>Aufgaben</h2><ul class="task-list">%s</ul></section>\n' % tasks
        + ('  %s\n' % render_quiz(lp) if lp.get("quiz") else '')
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
