# Naturwissenschaften — Unterrichtsmaterial

## Was hier liegt
- Kursübersicht (`index.html`) + Lernpfad-Seiten (`lernpfade/<Reihe>/lpNN.html`) für den
  Naturwissenschaften-Kurs Klasse 5 (10 J.), Schuljahr 2026/27.
- Einzige Quelle der Wahrheit für Inhalte, Kalender und Freischalt-Daten ist `build_course.py`
  (analog zu `Informatik/SEK-I/Profilkurs/build_course.py` und `.../ITG/`). Nach jeder inhaltlichen
  Änderung `python3 build_course.py` erneut ausführen, statt die generierten HTML-Dateien direkt
  zu editieren.
- 3 Unterrichtsreihen (00 Schwimmen und Sinken, 01 Lebensmittel, 02 Fliegen), 37 Lernpfade
  (SJW 0–36), 1x 75 Minuten pro Woche.

## Konventionen
- Sprache: Deutsch.
- HTML immer als einzelne, offline lauffähige Datei — keine CDN-Abhängigkeiten (Google Fonts
  per `<link>` sind die einzige externe Ressource, wie in den beiden Informatik-Kursen).
- Zählung stets ab 0 (Einheiten, Lernpfade, SJW) — konsistent mit Profilkurs und ITG.
- Typst (.typ) für PDF-Dokumente, sobald welche dazukommen. Build-Ergebnisse (PDFs) gehören
  nach iCloud, nicht ins Repo.

## Öffentlich — Vorsicht
- Dieses Repo ist public. Keine Schüler-Klarnamen, Noten oder
  personenbezogenen Daten in Dateien oder Commit-Nachrichten.
