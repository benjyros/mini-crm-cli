import json
from pathlib import Path

# Verzeichnis, in dem die JSON-Dateien liegen
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = DATA_DIR / "exports"

CONTACTS_FILE = DATA_DIR / "contacts.json"
INTERACTIONS_FILE = DATA_DIR / "interactions.json"


def init_storage():
    """Stellt sicher, dass die Verzeichnisse und JSON-Dateien existieren."""
    DATA_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)

    if not CONTACTS_FILE.exists():
        _save_json(CONTACTS_FILE, [])
    if not INTERACTIONS_FILE.exists():
        _save_json(INTERACTIONS_FILE, [])


def load_contacts():
    return _load_json(CONTACTS_FILE, [])


def save_contacts(contacts):
    _save_json(CONTACTS_FILE, contacts)


def load_interactions():
    return _load_json(INTERACTIONS_FILE, [])


def save_interactions(interactions):
    _save_json(INTERACTIONS_FILE, interactions)


def _load_json(path, default):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print("Warnung: Datei", path.name, "ist beschädigt. Starte mit leerer Liste.")
        return default


def _save_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
