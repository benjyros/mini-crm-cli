# Mini CRM (Console Application)

## Projektbeschreibung

Dieses Projekt ist ein konsolenbasiertes Mini-CRM.
Es ermöglicht die Verwaltung von Kontakten und deren Interaktionen (z.B. Telefonate, E-Mails, Meetings, Notizen).

Das Projekt entsteht im Rahmen des Moduls „Grundlagen Programmierung 1“ und dient dazu,
die gelernten Grundlagen (Variablen, Kontrollstrukturen, Funktionen, Listen, Dateien, Module usw.)
in einer zusammenhängenden Anwendung umzusetzen.

- Programmiersprache: Python 3 (getestet mit 3.11)
- Benutzeroberfläche: Kommandozeile (CLI)
- Datenspeicherung: JSON (Kontakte und Interaktionen)
- Export: CSV mit Semikolon als Trennzeichen

## Schnellstart

1. Repository klonen und in den Projektordner wechseln.
2. (Optional) Virtuelle Umgebung erstellen (`python -m venv .venv`) und aktivieren.
3. Abhängigkeiten: Es wird nur die Python-Standardbibliothek benötigt.
4. CLI starten:

  ```bash
  python -m src.cli
  ```

5. Beim ersten Start erzeugt `storage.init_storage()` automatisch `src/data/` inkl. leerer JSON-Dateien.

> Hinweis: Unter Linux/macOS ggf. `python3` statt `python` verwenden.

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
  - `Export > Beide` erzeugt beide Dateien in einem Rutsch.

## CLI-Überblick

- Hauptmenü (Deutsch): Kontakte, Interaktionen, Export, Beenden.
- Submenüs laden vor jeder Anzeige neu von der Festplatte, was parallele CLI-Sessions robuster macht.
- `contacts.print_contacts` und `interactions.print_interactions` erzeugen tabellarische Ausgaben mit dynamischen Spaltenbreiten.
- `prompt_int` nimmt numerische Eingaben entgegen und gibt `None` zurück, wenn die Eingabe fehlschlägt – Aufrufer sollten in diesem Fall direkt zum Menü zurückkehren.
- Löschvorgänge fragen immer nach einer Sicherheitsbestätigung (`y` oder `j`). Kontakte warnen zusätzlich vor verknüpften Interaktionen und löschen diese bei Bedarf mit.

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

## Datenhaltung & Formate

- Kontakte und Interaktionen liegen als JSON-Listen unter `src/data/contacts.json` bzw. `src/data/interactions.json`.
- IDs erhöhen sich strikt monoton im Speicher (`_generate_new_*_id`). Beim Import externer Daten sollten IDs daher geprüft oder angepasst werden.
- Zeitstempel werden mit `datetime.now().isoformat(timespec="seconds")` gespeichert; CSV-Dateien nutzen `%Y%m%d_%H%M%S` im Dateinamen.
- CSV-Exporte verwenden Semikolons als Trennzeichen und werden UTF-8-kodiert mit Headerzeile geschrieben.

## Manueller Smoke-Test

1. `python -m src.cli` starten.
2. Kontakt hinzufügen (Vorname, Nachname, eindeutige E-Mail, Telefonnummer).
3. Interaktion erfassen und den Kontakt per E-Mail oder ID referenzieren.
4. `Export > Beide` ausführen und sicherstellen, dass CSV-Dateien unter `src/data/exports/` erscheinen.
5. Kontakte-Menü öffnen, Kontakt löschen, Sicherheitsabfrage bestätigen und prüfen, ob verknüpfte Interaktionen verschwinden.

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

## Häufige Fragen

- **Die Datenordner fehlen.** Einfach die CLI starten; `storage.init_storage()` erzeugt alle benötigten Dateien automatisch.
- **JSON-Datei ist defekt.** Die Anwendung zeigt eine Warnung und lädt eine leere Liste. Backup einspielen oder manuell reparieren.
- **Exports fehlen trotz erfolgreicher Meldung.** Prüfen, ob Schreibrechte für `src/data/exports/` bestehen und ob das Systemdatum korrekt gesetzt ist.
