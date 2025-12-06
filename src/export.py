import csv
from datetime import datetime
import storage


def export_contacts_to_csv():
    contacts_list = storage.load_contacts()
    if not contacts_list:
        print("Keine Kontakte zum Exportieren vorhanden.")
        return None

    filename = f"export_contacts_{_timestamp_for_filename()}.csv"
    path = storage.EXPORTS_DIR / filename

    fieldnames = [
        "id",
        "email",
        "firstname",
        "lastname",
        "company",
        "phone",
        "created_at",
        "updated_at",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for contact in contacts_list:
            row = {
                "id": contact.get("id"),
                "email": contact.get("email"),
                "firstname": contact.get("firstname"),
                "lastname": contact.get("lastname"),
                "company": contact.get("company"),
                "phone": contact.get("phone"),
                "created_at": contact.get("created_at"),
                "updated_at": contact.get("updated_at"),
            }
            writer.writerow(row)

    print(f"Kontakte wurden nach {path} exportiert.")
    return path


def export_interactions_to_csv():
    interactions_list = storage.load_interactions()
    if not interactions_list:
        print("Keine Interaktionen zum Exportieren vorhanden.")
        return None

    filename = f"export_interactions_{_timestamp_for_filename()}.csv"
    path = storage.EXPORTS_DIR / filename

    fieldnames = [
        "id",
        "contact_id",
        "date",
        "type",
        "subject",
        "summary",
        "created_at",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for interaction in interactions_list:
            row = {
                "id": interaction.get("id"),
                "contact_id": interaction.get("contact_id"),
                "date": interaction.get("date"),
                "type": interaction.get("type"),
                "subject": interaction.get("subject"),
                "summary": interaction.get("summary"),
                "created_at": interaction.get("created_at"),
            }
            writer.writerow(row)

    print(f"Interaktionen wurden nach {path} exportiert.")
    return path


def export_both_to_csv():
    export_contacts_to_csv()
    export_interactions_to_csv()


def _timestamp_for_filename():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
