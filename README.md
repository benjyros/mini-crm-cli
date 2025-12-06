# Mini CRM (Console Application)

## Projektbeschreibung

Dieses Projekt ist ein einfaches, konsolenbasiertes Mini CRM.
Es ermöglicht die Verwaltung von Kontakten und deren Interaktionen (z.B. Telefonate, E-Mails, Meetings, Notizen).

Das Projekt entsteht im Rahmen des Moduls „Grundlagen Programmierung 1“ und dient dazu,
die gelernten Grundlagen (Variablen, Kontrollstrukturen, Funktionen, Listen, Dateien, Module usw.)
in einer zusammenhängenden Anwendung umzusetzen.

- Programmiersprache: Python 3
- Benutzeroberfläche: Kommandozeile (CLI)
- Datenspeicherung: JSON (Kontakte und Interaktionen)
- Export: CSV mit Semikolon als Trennzeichen

## Funktionen (geplant / umgesetzt)

- Kontakte verwalten

  - Anzeigen aller Kontakte
  - Suchen nach Kontakten (Name, E-Mail, Firma)
  - Erstellen, Bearbeiten, Löschen von Kontakten
  - Validierung der E-Mail-Adresse (Format und Eindeutigkeit)

- Interaktionen verwalten

  - Anzeigen aller Interaktionen
  - Suchen nach Interaktionen (z.B. nach Kontakt oder Stichwort)
  - Erfassen und Löschen von Interaktionen
  - Verknüpfung der Interaktion mit einem existierenden Kontakt
  - Validierung von Datum (Format: DD.MM.YYYY) und Typ

- Export
  - Export von Kontakten nach CSV
  - Export von Interaktionen nach CSV
  - Dateien heißen `export_contacts_YYYYMMDD_HHMMSS.csv` bzw. `export_interactions_YYYYMMDD_HHMMSS.csv` und liegen im automatisch erstellten Ordner `exports/`.

## Projektstruktur

```text
mini-crm-cli/
├─ src/
│  ├─ data/
│  │  ├─ exports/             # Automatisch generierte CSV-Exporte
│  │  ├─ contacts.json        # Kontaktdaten (wird bei Bedarf erstellt)
│  │  └─ interactions.json    # Interaktionen (wird bei Bedarf erstellt)
│  ├─ cli.py                  # Einstiegspunkt, Menüsteuerung
│  ├─ contacts.py             # Kontaktverwaltung (Funktionen)
│  ├─ export.py               # CSV-Export
│  ├─ interactions.py         # Interaktionsverwaltung (Funktionen)
│  └─ storage.py              # Ein-/Auslesen von JSON, Timestamps
├─ .gitignore
└─ README.md
```

- Die Ordner data/ und exports/ werden von der Anwendung erstellt, falls sie noch nicht existieren.

## Installation und Ausführung

Voraussetzungen:

- Python 3.x ist installiert.

Schritte:

1. Repository klonen:
   git clone <REPOSITORY-URL>
   cd mini-crm-cli

2. (Optional) Virtuelle Umgebung erstellen und aktivieren.

3. Anwendung starten:
   python -m src.cli

Hinweis: Je nach Umgebung kann der Befehl auch python3 -m src.cli lauten.

## Bedienung (CLI)

- Hauptmenü (Deutsch): Kontakte, Interaktionen, Export, Beenden.
- Kontakte-Menü: Suche (Substring), Aktionen (anzeigen, neuen Kontakt anlegen, bearbeiten, löschen mit Sicherheitsabfrage).
- Interaktionen-Menü: Suche, anzeigen, neue Interaktion erfassen, löschen.
- Export-Menü: Kontakte, Interaktionen oder beide als `export_*.csv` mit Zeitstempel in `exports/`.
- Alle Eingaben erfolgen per Nummernauswahl; Fehler werden mit klaren Hinweisen abgefangen.

## Team und Verantwortlichkeiten

Team:

- Oltian Kadriu
- Andrea Materazzo
- Benjamin Peterhans

Verantwortlichkeiten (Module):

- cli.py – Menüs / CLI
- contacts.py – Kontaktlogik
- export.py – Export
- interactions.py – Interaktionslogik
- storage.py – Persistenz
