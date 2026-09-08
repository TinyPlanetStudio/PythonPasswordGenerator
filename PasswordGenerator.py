import random
from pathlib import Path

CHARACTER_GROUPS = {
    "numbers": "0123456789",
    "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "lowercase": "abcdefghijklmnopqrstuvwxyz",
    "symbols": "!@#$%^&*()",
}


def generate_password():
    print("Enter the desired password length")
    password_length = int(input())

    while True:
        print("Enter requirements separated by commas: numbers, uppercase, lowercase, symbols, or none")
        requirements_input = input().strip().casefold()
        if requirements_input in ("", "none", "no requirements"):
            return "".join(
                random.choice("".join(CHARACTER_GROUPS.values()))
                for _ in range(password_length)
            )

        requirements = {
            requirement.strip()
            for requirement in requirements_input.split(",")
            if requirement.strip()
        }
        invalid_requirements = requirements - CHARACTER_GROUPS.keys()
        if invalid_requirements:
            print("Invalid requirements. Please use the listed options.")
            continue
        break

    all_characters = "".join(CHARACTER_GROUPS.values())
    while True:
        password = "".join(
            random.choice(all_characters) for _ in range(password_length)
        )
        if all(
            any(character in CHARACTER_GROUPS[requirement] for character in password)
            for requirement in requirements
        ):
            return password


def read_passwords(file_path):
    if not file_path.exists():
        return []

    passwords = []
    current_password = None
    for line in file_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            if current_password is not None:
                passwords.append(current_password)
            current_password = {"usage": line[1:-1]}
        elif current_password is not None and ": " in line:
            field, value = line.split(": ", 1)
            current_password[field.lower()] = value

    if current_password is not None:
        passwords.append(current_password)
    return passwords


def write_passwords(file_path, passwords):
    with file_path.open("w", encoding="utf-8") as file:
        for password in passwords:
            file.write(f"[{password['usage']}]\n")
            if password.get("website"):
                file.write(f"Website: {password['website']}\n")
            if password.get("username"):
                file.write(f"Username: {password['username']}\n")
            file.write(f"Password: {password.get('password', '')}\n\n")


def manage_passwords(file_path):
    passwords = read_passwords(file_path)
    if not passwords:
        print("No passwords have been saved yet.")
        return

    print("What password do you want to manage? Type 'list' to see all passwords.")
    password_usage = input().strip()
    if password_usage.casefold() == "list":
        print("Saved passwords:")
        for saved_password in passwords:
            print(f"- {saved_password['usage']}")
        print("What password do you want to manage?")
        password_usage = input().strip()

    matching_passwords = [
        password
        for password in passwords
        if password["usage"].casefold() == password_usage.casefold()
    ]
    if not matching_passwords:
        print("No password found with that name.")
        return

    password = matching_passwords[0]
    print("Would you like to change username, change password, change website, or delete all information?")
    action = input().strip().casefold()

    if action == "change username":
        password["username"] = input("Enter the new username: ").strip()
    elif action == "change password":
        print("Would you like to enter a password or generate one randomly?")
        password_method = input().strip().casefold()
        if password_method in ("generate", "random", "generate one randomly"):
            password["password"] = generate_password()
            print(f"New password: {password['password']}")
        elif password_method in ("enter", "manual", "enter a password"):
            password["password"] = input("Enter the new password: ")
        else:
            print("That is not a valid option.")
            return
    elif action == "change website":
        password["website"] = input("Enter the new website URL: ").strip()
    elif action == "delete all information":
        passwords.remove(password)
    else:
        print("That is not a valid option.")
        return

    write_passwords(file_path, passwords)
    print("Password information updated successfully.")


path_file = Path(__file__).with_name("path.ini")
if path_file.exists():
    save_path = Path(path_file.read_text(encoding="utf-8").strip())
else:
    save_path = Path(input("Please enter the file path where you want your passwords to be saved: ").strip())
    path_file.write_text(str(save_path), encoding="utf-8")

if save_path.is_dir():
    save_path /= "password.password"

print("Would you like to add or manage passwords?")
mode = input().strip().casefold()
if mode == "manage":
    manage_passwords(save_path)
    raise SystemExit

print("What is this password for?")
password_usage = input().strip()
print("Is there already a password? y/n")
existing_password_response = input().strip().lower()
if existing_password_response == "y":
    print("Please enter the existing password")
    password = input()
else:
    password = generate_password()
    print(password)

print("Is there a username associated with this password? y/n")
username_response = input().strip().lower()
username = ""
if username_response == "y":
    print("Please enter the username")
    username = input().strip()

print("Is there a website associated with this password? y/n")
website_response = input().strip().lower()
website = ""
if website_response == "y":
    print("Please enter the website URL")
    website = input().strip()

with save_path.open("a", encoding="utf-8") as file:
    file.write(f"[{password_usage}]\n")
    if website_response == "y":
        file.write(f"Website: {website}\n")
    if username_response == "y":
        file.write(f"Username: {username}\n")
    file.write(f"Password: {password}\n")
    file.write("\n")

print("Password saved successfully.")
