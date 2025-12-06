import storage
import contacts
import interactions
import export as export_module


def prompt_int(message):
    """Fragt eine Ganzzahl ab. Gibt None zurück, wenn keine gültige Zahl eingegeben wurde."""
    value = input(message).strip()
    if not value:
        return None
    if not value.isdigit():
        print("Bitte eine Zahl eingeben.")
        return None
    return int(value)


def contacts_submenu():
    # Beim Einstieg: alle Kontakte anzeigen
    all_contacts = storage.load_contacts()
    contacts.print_contacts(all_contacts)

    while True:
        print("\nKontakte - Menü")
        print("----------------")
        print("1) Suche")
        print("2) Aktion auswählen")
        print("3) Zurück zur Übersicht")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            # Suche: nur Treffer zeigen, danach direkt zurück ins Menü
            all_contacts = storage.load_contacts()
            query = input("Suchbegriff eingeben: ").strip()
            if not query:
                print("Suchbegriff darf nicht leer sein.")
            else:
                results = contacts.search_contacts(all_contacts, query)
                print("\nSuchergebnisse")
                contacts.print_contacts(results)

        elif choice == "2":
            # Vor einer Aktion die aktuelle Liste zeigen, damit man die ID sieht
            all_contacts = storage.load_contacts()
            print("\nAktuelle Kontakte")
            contacts.print_contacts(all_contacts)

            print("\nAktionen:")
            print("1) Kontakt anzeigen")
            print("2) Kontakt bearbeiten")
            print("3) Kontakt löschen")
            print("4) Neuer Kontakt")

            action = input("Aktion wählen (1-4): ").strip()

            if action == "4":
                # Neuer Kontakt ohne vorherige ID
                create_contact_flow()
                # Danach aktualisierte Liste zeigen
                all_contacts = storage.load_contacts()
                print("\nAktualisierte Kontaktübersicht")
                contacts.print_contacts(all_contacts)
                continue

            contact_id = prompt_int("Kontakt-ID eingeben: ")
            if contact_id is None:
                continue

            if action == "1":
                show_contact_details(contact_id)
            elif action == "2":
                edit_contact_flow(contact_id)
            elif action == "3":
                delete_contact_flow(contact_id)
            else:
                print("Ungültige Aktion.")

            # Nach einer Aktion erneut die aktualisierte Liste anzeigen
            all_contacts = storage.load_contacts()
            print("\nAktualisierte Kontaktübersicht")
            contacts.print_contacts(all_contacts)

        elif choice == "3":
            # Zurück ins Hauptmenü
            break
        else:
            print("Ungültige Auswahl. Bitte 1-3 eingeben.")


def interactions_submenu():
    # Beim Einstieg: alle Interaktionen anzeigen
    all_contacts = storage.load_contacts()
    all_interactions = storage.load_interactions()
    interactions.print_interactions(all_interactions, all_contacts)

    while True:
        print("\nInteraktionen - Menü")
        print("---------------------")
        print("1) Suche")
        print("2) Aktion auswählen")
        print("3) Zurück zur Übersicht")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            # Suche: nur Treffer zeigen, danach direkt zurück ins Menü
            all_contacts = storage.load_contacts()
            all_interactions = storage.load_interactions()
            query = input("Suchbegriff eingeben: ").strip()
            if not query:
                print("Suchbegriff darf nicht leer sein.")
            else:
                results = interactions.search_interactions(all_interactions, query)
                print("\nSuchergebnisse")
                interactions.print_interactions(results, all_contacts)

        elif choice == "2":
            # Vor einer Aktion die aktuelle Liste zeigen
            all_contacts = storage.load_contacts()
            all_interactions = storage.load_interactions()
            print("\nAktuelle Interaktionen")
            interactions.print_interactions(all_interactions, all_contacts)

            print("\nAktionen:")
            print("1) Interaktion anzeigen")
            print("2) Interaktion löschen")
            print("3) Neue Interaktion")

            action = input("Aktion wählen (1-3): ").strip()

            if action == "3":
                create_interaction_flow()
                # Danach aktualisierte Liste zeigen
                all_contacts = storage.load_contacts()
                all_interactions = storage.load_interactions()
                print("\nAktualisierte Interaktionsübersicht")
                interactions.print_interactions(all_interactions, all_contacts)
                continue

            interaction_id = prompt_int("Interaktions-ID eingeben: ")
            if interaction_id is None:
                continue

            if action == "1":
                show_interaction_details(interaction_id)
            elif action == "2":
                delete_interaction_flow(interaction_id)
            else:
                print("Ungültige Aktion.")

            # Nach Aktion erneut aktualisierte Liste anzeigen
            all_contacts = storage.load_contacts()
            all_interactions = storage.load_interactions()
            print("\nAktualisierte Interaktionsübersicht")
            interactions.print_interactions(all_interactions, all_contacts)

        elif choice == "3":
            # Zurück ins Hauptmenü
            break
        else:
            print("Ungültige Auswahl. Bitte 1-3 eingeben.")


def export_submenu():
    while True:
        print("\nExport - Menü")
        print("--------------")
        print("1) Kontakte")
        print("2) Interaktionen")
        print("3) Beide")
        print("4) Zurück zum Hauptmenü")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            export_module.export_contacts_to_csv()
        elif choice == "2":
            export_module.export_interactions_to_csv()
        elif choice == "3":
            export_module.export_both_to_csv()
        elif choice == "4":
            break
        else:
            print("Ungültige Auswahl. Bitte 1-4 eingeben.")


def create_contact_flow():
    all_contacts = storage.load_contacts()
    print("\nNeuer Kontakt")
    print("--------------")
    firstname = input("Vorname: ").strip()
    lastname = input("Nachname: ").strip()
    email = input("E-Mail: ").strip()
    company = input("Firma (optional): ").strip()
    phone = input("Telefon: ").strip()

    contact, error = contacts.create_contact(all_contacts, firstname, lastname, email, company, phone)
    if error:
        print("Fehler:", error)
        return

    all_contacts.append(contact)
    storage.save_contacts(all_contacts)
    print("Kontakt wurde gespeichert.")


def show_contact_details(contact_id):
    all_contacts = storage.load_contacts()
    contact = contacts.find_contact_by_id(all_contacts, contact_id)
    if contact is None:
        print("Kontakt nicht gefunden.")
        return

    print("\nKontaktdetails")
    print("---------------")
    print(f"ID: {contact.get('id')}")
    print(f"Vorname: {contact.get('firstname')}")
    print(f"Nachname: {contact.get('lastname')}")
    print(f"E-Mail: {contact.get('email')}")
    print(f"Firma: {contact.get('company') or '-'}")
    print(f"Telefon: {contact.get('phone')}")
    print(f"Erstellt am: {contact.get('created_at')}")
    print(f"Aktualisiert am: {contact.get('updated_at')}")


def edit_contact_flow(contact_id):
    all_contacts = storage.load_contacts()
    contact = contacts.find_contact_by_id(all_contacts, contact_id)
    if contact is None:
        print("Kontakt nicht gefunden.")
        return

    print("\nKontakt bearbeiten (Enter = Wert beibehalten)")
    print("-----------------------------------------------")
    
    firstname = contact.get("firstname")
    print(f"Aktueller Vorname: {firstname}")
    new_firstname = input("Neuer Vorname: ").strip()
    if new_firstname:
        firstname = new_firstname
        
    lastname = contact.get("lastname")
    print(f"Aktueller Nachname: {lastname}")
    new_lastname = input("Neuer Nachname: ").strip()
    if new_lastname:
        lastname = new_lastname
        
    email = contact.get("email")
    print(f"Aktuelle E-Mail: {email}")
    new_email = input("Neue E-Mail: ").strip()
    if new_email:
        email = new_email

    company = contact.get("company")
    print(f"Aktueller Firma: {company or '-'}")
    new_company = input("Neue Firma (leer = keine): ").strip()
    if new_company:
        company = new_company
    else:
        company = ""

    phone = contact.get("phone")
    print(f"Aktuelle Telefonnummer: {phone}")
    new_phone = input("Neue Telefonnummer: ").strip()
    if new_phone:
        phone = new_phone
        
    _, error = contacts.update_contact(
        contact,
        all_contacts,
        firstname,
        lastname,
        email,
        company,
        phone,
    )
    if error:
        print("Fehler:", error)
        return

    storage.save_contacts(all_contacts)
    print("Kontakt wurde aktualisiert.")


def delete_contact_flow(contact_id):
    all_contacts = storage.load_contacts()
    all_interactions = storage.load_interactions()
    uses = [interaction for interaction in all_interactions if interaction.get("contact_id") == contact_id]

    contact = contacts.find_contact_by_id(all_contacts, contact_id)
    if contact is None:
        print("Kontakt nicht gefunden.")
        return

    print("Kontakt:")
    print(contacts.format_contact_short(contact))
    if uses:
        print(f"Achtung: Es existieren {len(uses)} Interaktionen für diesen Kontakt.")
        print("Die Interaktionen werden auch gelöscht.")
    confirm = input(f"Diesen Kontakt {'und deren Interaktionen ' if uses else ''}wirklich löschen? (y/n): ").strip().lower()
    if confirm not in ("y", "j"):
        print("Löschen abgebrochen.")
        return

    success = contacts.delete_contact(all_contacts, contact_id) and [interactions.delete_interaction(all_interactions, interaction.get("id")) for interaction in all_interactions]
    if success:
        storage.save_contacts(all_contacts)
        storage.save_interactions(all_interactions)
        print(f"Kontakt {'und deren Interaktionen wurden' if uses else 'wurde'} gelöscht.")
    else:
        print(f"Kontakt {'und deren Interaktionen konnten' if uses else 'konnte'} nicht gelöscht werden.")


def create_interaction_flow():
    all_contacts = storage.load_contacts()
    all_interactions = storage.load_interactions()

    print("\nNeue Interaktion")
    print("-----------------")
    print("Kontakt auswählen (E-Mail oder ID):")
    contact_identifier = input("> ").strip()

    date_str = input("Datum (TT.MM.JJJJ): ").strip()

    print("Typ (Call, E-Mail, Meeting, Notiz):")
    type_str = input("> ").strip()

    subject = input("Betreff (optional): ").strip()
    summary = input("Zusammenfassung: ").strip()

    interaction, error = interactions.create_interaction(
        all_interactions,
        all_contacts,
        contact_identifier,
        date_str,
        type_str,
        subject,
        summary,
    )
    if error:
        print("Fehler:", error)
        return

    all_interactions.append(interaction)
    storage.save_interactions(all_interactions)
    print("Interaktion wurde gespeichert.")


def show_interaction_details(interaction_id):
    all_contacts = storage.load_contacts()
    all_interactions = storage.load_interactions()
    interaction = interactions.find_interaction_by_id(all_interactions, interaction_id)
    if interaction is None:
        print("Interaktion nicht gefunden.")
        return

    contact = contacts.find_contact_by_id(all_contacts, interaction.get("contact_id"))

    print("\nInteraktionsdetails")
    print("--------------------")
    print(f"ID: {interaction.get('id')}")
    print(f"Datum: {interaction.get('date')}")
    print(f"Typ: {interaction.get('type')}")
    if contact:
        print(f"Kontakt: {contacts.format_contact_short(contact)}")
    else:
        print(f"Kontakt: (unbekannt, ID {interaction.get('contact_id')})")
    print(f"Betreff: {interaction.get('subject') or '-'}")
    print(f"Zusammenfassung: {interaction.get('summary')}")
    print(f"Erstellt am: {interaction.get('created_at')}")


def delete_interaction_flow(interaction_id):
    all_interactions = storage.load_interactions()
    interaction = interactions.find_interaction_by_id(all_interactions, interaction_id)
    if interaction is None:
        print("Interaktion nicht gefunden.")
        return

    confirm = input("Diese Interaktion wirklich löschen? (y/n): ").strip().lower()
    if confirm not in ("y", "j"):
        print("Löschen abgebrochen.")
        return

    success = interactions.delete_interaction(all_interactions, interaction_id)
    if success:
        storage.save_interactions(all_interactions)
        print("Interaktion wurde gelöscht.")
    else:
        print("Interaktion konnte nicht gelöscht werden.")


def run():
    storage.init_storage()
    while True:
        print("\nMiniCRM - Hauptmenü")
        print("====================")
        print("1) Kontakte")
        print("2) Interaktionen")
        print("3) Export")
        print("4) Beenden")
        choice = input("Auswahl: ").strip()

        if choice == "1":
            contacts_submenu()
        elif choice == "2":
            interactions_submenu()
        elif choice == "3":
            export_submenu()
        elif choice == "4":
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte 1-4 eingeben.")


if __name__ == "__main__":
    run()
