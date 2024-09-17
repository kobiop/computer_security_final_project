from flask import json
import os
import hmac
import hashlib
from flask_mail import Message
from .. import mail

with open("backend/config/password_config.json") as config_file:
    password_config = json.load(config_file)


def is_password_common(password):
    # Path to the common passwords file
    file_path = "backend/config/common_passwords.txt"

    try:
        # Open and read the file
        with open(file_path, "r") as file:
            # Read all lines and strip newline characters
            common_passwords = {line.strip() for line in file}

        # Check if the entered password is in the set of common passwords
        return password in common_passwords

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return False


def validate_password(password):
    config = password_config["password_requirements"]
    if len(password) < config["password_len"]:
        return False
    if sum(c.isupper() for c in password) < config["uppercase"]:
        return False
    if sum(c.isdigit() for c in password) < config["numbers"]:
        return False
    if sum(not c.isalnum() for c in password) < config["special_char"]:
        return False
    if sum(c.islower() for c in password) < config["lowercase"]:
        return False
    return True


def generate_salt(length):
    random_bytes = os.urandom(length)
    sha1_hash = hashlib.sha1(random_bytes).digest()
    return sha1_hash


def hash_password(password, salt):

    return hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()


def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
