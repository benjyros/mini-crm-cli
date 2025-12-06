from datetime import datetime
import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_contact(contacts, firstname, lastname, email, company, phone):
    """Erzeugt einen neuen Kontakt-Datensatz. Gibt (kontakt_dict, fehler) zurück."""
    error = _validate_contact_data(contacts, firstname, lastname, email, phone)
    if error:
        return None, error

    new_id = _generate_new_contact_id(contacts)
    now = _current_timestamp()
    contact = {
        "id": new_id,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "company": company,
        "phone": phone,
        "created_at": now,
        "updated_at": now,
    }
    return contact, None


def update_contact(contact, contacts, firstname, lastname, email, company, phone):
    """Aktualisiert einen vorhandenen Kontakt. Gibt (kontakt_dict, fehler) zurück."""
    contact_id = contact.get("id")
    error = _validate_contact_data(contacts, firstname, lastname, email, phone, contact_id)
    if error:
        return None, error

    contact["firstname"] = firstname
    contact["lastname"] = lastname
    contact["email"] = email
    contact["company"] = company
    contact["phone"] = phone
    contact["updated_at"] = _current_timestamp()
    return contact, None


def delete_contact(contacts, contact_id):
    """Löscht einen Kontakt aus der Liste. Gibt True bei Erfolg, False wenn nicht gefunden."""
    contact = find_contact_by_id(contacts, contact_id)
    if not contact:
        return False
    contacts.remove(contact)
    return True


def search_contacts(contacts, query):
    """Einfache Substring-Suche (case-insensitive) über mehrere Felder."""
    results = []
    query_lower = query.lower()
    for contact in contacts:
        text = (
            f"{contact.get('firstname','')} {contact.get('lastname','')} "
            f"{contact.get('email','')} {contact.get('phone','')} {contact.get('company','')}"
        )
        if query_lower in text.lower():
            results.append(contact)
    return results


def print_contacts(contacts_list):
    """Gibt eine tabellarische Liste aller Kontakte aus."""
    print("\nKontakte - Übersicht")

    if not contacts_list:
        print("Keine Kontakte vorhanden.")
        return

    headers = ["ID", "Vorname", "Nachname", "E-Mail", "Firma", "Telefon"]
    widhts = [len(header) + 2 for header in headers]

    rows = []
    for contact in contacts_list:
        row = [
            str(contact.get("id", "")),
            contact.get("firstname", ""),
            contact.get("lastname", ""),
            contact.get("email", ""),
            contact.get("company", ""),
            contact.get("phone", ""),
        ]
        rows.append(row)
        for index, value in enumerate(row):
            widhts[index] = max(widhts[index], len(value) + 2)

    def format_row(row):
        return " ".join(f"{item:<{widhts[i]}}" for i, item in enumerate(row))
    
    separator = "-".join("-" * widht for widht in widhts)

    print(separator)
    print(format_row(headers))
    print(separator)

    for row in rows:
        print(format_row(row))

    print(separator)


def find_contact_by_id(contacts, contact_id):
    for contact in contacts:
        if contact.get("id") == contact_id:
            return contact
    return None


def find_contact_by_email(contacts, email):
    for contact in contacts:
        if contact.get("email") == email:
            return contact
    return None


def format_contact_short(contact):
    """Kurze Darstellung eines Kontakts für Listen."""
    return f"{contact.get('id')} - {contact.get('firstname')} {contact.get('lastname')} <{contact.get('email')}>"


def _validate_contact_data(contacts, firstname, lastname, email, phone, ignore_contact_id=None):
    """Validiert die Kontaktdaten. Gibt None bei Erfolg oder eine Fehlermeldung als String zurück."""
    if not firstname:
        return "Vorname darf nicht leer sein."
    if not lastname:
        return "Nachname darf nicht leer sein."
    if not email:
        return "E-Mail darf nicht leer sein."
    if not _is_valid_email(email):
        return "E-Mail-Adresse ist nicht gültig."
    if not _is_email_unique(contacts, email, ignore_contact_id):
        return "Es existiert bereits ein Kontakt mit dieser E-Mail-Adresse."
    # Firma ist optional, Telefon prüfen wir nur auf Leerheit sonst zu kompliziert pro Land
    if not phone:
        return "Telefonnummer darf nicht leer sein."
    return None


def _generate_new_contact_id(contacts):
    """Erzeugt eine neue ID auf Basis der vorhandenen Kontakte."""
    if not contacts:
        return 1
    return max(contact.get("id", 0) for contact in contacts) + 1


def _is_valid_email(email):
    """Einfache E-Mail-Validierung mit Regex."""
    if not email:
        return False
    return EMAIL_PATTERN.match(email) is not None


def _is_email_unique(contacts, email, ignore_contact_id=None):
    """Prüft, ob die E-Mail-Adresse noch nicht verwendet wird."""
    for contact in contacts:
        if contact.get("email") == email:
            if ignore_contact_id is not None and contact.get("id") == ignore_contact_id:
                # Eigener Kontakt bei Bearbeitung
                continue
            return False
    return True


def _current_timestamp():
    """Gibt einen Zeitstempel als String zurück."""
    return datetime.now().isoformat(timespec="seconds")
