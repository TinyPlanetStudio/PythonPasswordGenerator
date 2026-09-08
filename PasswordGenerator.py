import random
from pathlib import Path


path_file = Path(__file__).with_name("path.ini")
if path_file.exists():
    save_path = Path(path_file.read_text(encoding="utf-8").strip())
else:
    save_path = Path(input("Please enter the file path where you want your passwords to be saved: ").strip())
    path_file.write_text(str(save_path), encoding="utf-8")

if save_path.is_dir():
    save_path /= "password.password"

print("What is this password for?")
password_usage = input().strip()
print("Is there already a password? y/n")
existing_password_response = input().strip().lower()
if existing_password_response == "y":
    print("Please enter the existing password")
    password = input()
else:
    print("Enter the desired password length")
    password_length = int(input())
    characters = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()"
    )
    password = "".join(random.choice(characters) for _ in range(password_length))
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
