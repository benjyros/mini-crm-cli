from datetime import datetime
import contacts as contacts_module


ALLOWED_TYPES = ["Call", "E-Mail", "Meeting", "Notiz"]


def search_interactions(interactions, query):
    """Substringsuche (case-insensitive) über Datum, Typ, Betreff, Zusammenfassung."""
    results = []
    query_lower = query.lower()
    for interaction in interactions:
        text = (
            f"{interaction.get('date','')} "
            f"{interaction.get('type','')} "
            f"{interaction.get('subject','')} "
            f"{interaction.get('summary','')}"
        )
        if query_lower in text.lower():
            results.append(interaction)
    return results


def create_interaction(interactions, contacts, contact_identifier, date_str, type_str, subject, summary):
    """Erzeugt eine neue Interaktion. Gibt (interaction_dict, fehler) zurück.

    contact_identifier: E-Mail oder ID (String), um den Kontakt zu finden.
    """
    # Kontakt finden
    contact = None
    if contact_identifier.isdigit():
        contact = contacts_module.find_contact_by_id(contacts, int(contact_identifier))
    else:
        contact = contacts_module.find_contact_by_email(contacts, contact_identifier)

    if contact is None:
        return None, "Kontakt wurde nicht gefunden."

    
    if _parse_date(date_str) is None: # Datum prüfen
        return None, "Datum ist nicht gültig. Bitte im Format TT.MM.JJJJ eingeben."
    if not _is_valid_type(type_str): # Typ prüfen
        return None, "Typ ist nicht gültig. Erlaubte Werte sind: " + ", ".join(ALLOWED_TYPES) + "."

    normalized_type = _normalize_type(type_str)
    new_id = _generate_new_interaction_id(interactions)
    interaction = {
        "id": new_id,
        "contact_id": contact.get("id"),
        "date": date_str,
        "type": normalized_type,
        "subject": subject,
        "summary": summary,
        "created_at": _current_timestamp(),
    }
    return interaction, None


def delete_interaction(interactions, interaction_id):
    interaction = find_interaction_by_id(interactions, interaction_id)
    if not interaction:
        return False
    interactions.remove(interaction)
    return True


def print_interactions(interactions_list, contacts):
    """Gibt eine tabellarische Liste aller Interaktionen aus, inkl. Kontakt-E-Mail."""
    print("\nInteraktionen - Übersicht")

    if not interactions_list:
        print("Keine Interaktionen vorhanden.")
        return

    headers = ["ID", "Datum", "Typ", "Kontakt", "Betreff", "Zusammenfassung"]
    widths = [len(header) + 2 for header in headers]

    rows = []
    for interaction in interactions_list:
        contact = contacts_module.find_contact_by_id(contacts, interaction.get("contact_id"))
        if contact:
            kontakt_text = (
                f"{contact.get('firstname', '')} "
                f"{contact.get('lastname', '')} "
                f"<{contact.get('email', '')}>"
            )
        else:
            kontakt_text = f"(ID {interaction.get('contact_id')})"

        row = [
            str(interaction.get("id", "")),
            interaction.get("date", ""),
            interaction.get("type", ""),
            kontakt_text,
            interaction.get("subject", ""),
            interaction.get("summary", ""),
        ]
        rows.append(row)
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value) + 2)

    def format_row(row):
        return " ".join(f"{item:<{widths[i]}}" for i, item in enumerate(row))
    
    separator = "-".join("-" * width for width in widths)

    print(separator)
    print(format_row(headers))
    print(separator)

    for row in rows:
        print(format_row(row))

    print(separator)


def find_interaction_by_id(interactions, interaction_id):
    for interaction in interactions:
        if interaction.get("id") == interaction_id:
            return interaction
    return None


def _parse_date(date_str):
    """Versucht, ein Datum im Format TT.MM.JJJJ zu parsen. Gibt datetime oder None zurück."""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None


def _is_valid_type(type_str):
    if not type_str:
        return False
    # Wir akzeptieren verschiedene Schreibweisen, speichern aber sauber
    lower = type_str.lower()
    for allowed in ALLOWED_TYPES:
        if lower == allowed.lower():
            return True
    return False


def _normalize_type(type_str):
    """Gibt den schön formatierten Typ zurück (einer von ALLOWED_TYPES)."""
    lower = type_str.lower()
    for allowed in ALLOWED_TYPES:
        if lower == allowed.lower():
            return allowed
    # Fallback, sollte nicht passieren, wenn vorher validiert
    return type_str


def _generate_new_interaction_id(interactions):
    if not interactions:
        return 1
    return max(interaction.get("id", 0) for interaction in interactions) + 1


def _current_timestamp():
    return datetime.now().isoformat(timespec="seconds")
