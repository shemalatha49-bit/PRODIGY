"""
Simple Contact Management System
A command-line application for managing contacts with persistent storage.
"""

import json
import os
import re
from typing import List, Dict, Optional


# File path for storing contacts
CONTACTS_FILE = "contacts.json"


def load_contacts() -> List[Dict[str, str]]:
    """
    Load contacts from the JSON file.
    
    Returns:
        List of contact dictionaries. Returns empty list if file doesn't exist.
    """
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Warning: Contacts file is corrupted. Starting with empty contact list.")
            return []
    return []


def save_contacts(contacts: List[Dict[str, str]]) -> None:
    """
    Save contacts to the JSON file.
    
    Args:
        contacts: List of contact dictionaries to save
    """
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)
    print("✓ Contacts saved successfully.")


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid, False otherwise
    """
    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number (accepts digits, spaces, hyphens, parentheses, and plus sign).
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if phone contains at least some digits, False otherwise
    """
    # Remove common formatting characters
    digits_only = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Check if it contains at least 7 digits
    return digits_only.isdigit() and len(digits_only) >= 7


def contact_exists(contacts: List[Dict[str, str]], name: str) -> bool:
    """
    Check if a contact with the given name already exists.
    
    Args:
        contacts: List of existing contacts
        name: Name to check
        
    Returns:
        True if contact exists, False otherwise
    """
    return any(contact['name'].lower() == name.lower() for contact in contacts)


def find_contact_index(contacts: List[Dict[str, str]], name: str) -> Optional[int]:
    """
    Find the index of a contact by name (case-insensitive).
    
    Args:
        contacts: List of contacts
        name: Name to search for
        
    Returns:
        Index of the contact if found, None otherwise
    """
    for i, contact in enumerate(contacts):
        if contact['name'].lower() == name.lower():
            return i
    return None


def add_contact(contacts: List[Dict[str, str]]) -> None:
    """
    Add a new contact to the contact list.
    
    Args:
        contacts: List of existing contacts
    """
    print("\n--- Add New Contact ---")
    
    # Get and validate name
    while True:
        name = input("Enter name: ").strip()
        if not name:
            print("❌ Name cannot be empty. Please try again.")
            continue
        if contact_exists(contacts, name):
            print(f"❌ A contact with the name '{name}' already exists.")
            choice = input("Do you want to enter a different name? (y/n): ").strip().lower()
            if choice != 'y':
                print("Operation cancelled.")
                return
            continue
        break
    
    # Get and validate phone number
    while True:
        phone = input("Enter phone number: ").strip()
        if not phone:
            print("❌ Phone number cannot be empty. Please try again.")
            continue
        if not validate_phone(phone):
            print("❌ Invalid phone number format. Please enter at least 7 digits.")
            continue
        break
    
    # Get and validate email
    while True:
        email = input("Enter email address: ").strip()
        if not email:
            print("❌ Email cannot be empty. Please try again.")
            continue
        if not validate_email(email):
            print("❌ Invalid email format. Please enter a valid email (e.g., user@example.com).")
            continue
        break
    
    # Create and add the new contact
    new_contact = {
        'name': name,
        'phone': phone,
        'email': email
    }
    
    contacts.append(new_contact)
    save_contacts(contacts)
    print(f"\n✓ Contact '{name}' added successfully!")


def view_all_contacts(contacts: List[Dict[str, str]]) -> None:
    """
    Display all contacts in a formatted manner.
    
    Args:
        contacts: List of contacts to display
    """
    print("\n--- All Contacts ---")
    
    if not contacts:
        print("No contacts found. The contact list is empty.")
        return
    
    print(f"\nTotal contacts: {len(contacts)}\n")
    
    # Print contacts with formatting
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")
        print("-" * 50)


def search_contact(contacts: List[Dict[str, str]]) -> None:
    """
    Search for a contact by name (case-insensitive, partial match).
    
    Args:
        contacts: List of contacts to search
    """
    print("\n--- Search Contact ---")
    
    if not contacts:
        print("No contacts available to search.")
        return
    
    search_term = input("Enter name to search: ").strip().lower()
    
    if not search_term:
        print("❌ Search term cannot be empty.")
        return
    
    # Find all matching contacts (partial match)
    matches = [c for c in contacts if search_term in c['name'].lower()]
    
    if not matches:
        print(f"No contacts found matching '{search_term}'.")
        return
    
    print(f"\nFound {len(matches)} contact(s):\n")
    for i, contact in enumerate(matches, 1):
        print(f"{i}. {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")
        print("-" * 50)


def edit_contact(contacts: List[Dict[str, str]]) -> None:
    """
    Edit an existing contact's information.
    
    Args:
        contacts: List of contacts
    """
    print("\n--- Edit Contact ---")
    
    if not contacts:
        print("No contacts available to edit.")
        return
    
    name = input("Enter the name of the contact to edit: ").strip()
    
    if not name:
        print("❌ Name cannot be empty.")
        return
    
    index = find_contact_index(contacts, name)
    
    if index is None:
        print(f"❌ Contact '{name}' not found.")
        return
    
    contact = contacts[index]
    print(f"\nEditing contact: {contact['name']}")
    print(f"Current Phone: {contact['phone']}")
    print(f"Current Email: {contact['email']}\n")
    
    print("Leave blank to keep current value.")
    
    # Edit name
    new_name = input(f"Enter new name [{contact['name']}]: ").strip()
    if new_name:
        # Check if new name already exists (and is different from current)
        if new_name.lower() != contact['name'].lower() and contact_exists(contacts, new_name):
            print(f"❌ A contact with the name '{new_name}' already exists. Name not changed.")
            new_name = contact['name']
    else:
        new_name = contact['name']
    
    # Edit phone
    while True:
        new_phone = input(f"Enter new phone [{contact['phone']}]: ").strip()
        if not new_phone:
            new_phone = contact['phone']
            break
        if validate_phone(new_phone):
            break
        print("❌ Invalid phone number format. Please try again or leave blank to keep current.")
    
    # Edit email
    while True:
        new_email = input(f"Enter new email [{contact['email']}]: ").strip()
        if not new_email:
            new_email = contact['email']
            break
        if validate_email(new_email):
            break
        print("❌ Invalid email format. Please try again or leave blank to keep current.")
    
    # Update contact
    contacts[index] = {
        'name': new_name,
        'phone': new_phone,
        'email': new_email
    }
    
    save_contacts(contacts)
    print(f"\n✓ Contact updated successfully!")


def delete_contact(contacts: List[Dict[str, str]]) -> None:
    """
    Delete a contact from the contact list.
    
    Args:
        contacts: List of contacts
    """
    print("\n--- Delete Contact ---")
    
    if not contacts:
        print("No contacts available to delete.")
        return
    
    name = input("Enter the name of the contact to delete: ").strip()
    
    if not name:
        print("❌ Name cannot be empty.")
        return
    
    index = find_contact_index(contacts, name)
    
    if index is None:
        print(f"❌ Contact '{name}' not found.")
        return
    
    contact = contacts[index]
    
    # Confirmation before deletion
    print(f"\nContact to delete:")
    print(f"Name: {contact['name']}")
    print(f"Phone: {contact['phone']}")
    print(f"Email: {contact['email']}\n")
    
    confirm = input("Are you sure you want to delete this contact? (y/n): ").strip().lower()
    
    if confirm == 'y':
        contacts.pop(index)
        save_contacts(contacts)
        print(f"\n✓ Contact '{name}' deleted successfully!")
    else:
        print("Deletion cancelled.")


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("       CONTACT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add a new contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Edit an existing contact")
    print("5. Delete a contact")
    print("6. Exit")
    print("=" * 50)


def get_menu_choice() -> str:
    """
    Get and validate menu choice from user.
    
    Returns:
        User's menu choice as a string
    """
    choice = input("Enter your choice (1-6): ").strip()
    return choice


def main():
    """Main function to run the contact management system."""
    # Load existing contacts
    contacts = load_contacts()
    
    print("\n🌟 Welcome to the Contact Management System! 🌟")
    
    # Main program loop
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_all_contacts(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            edit_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            print("\n👋 Thank you for using the Contact Management System!")
            print("Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
