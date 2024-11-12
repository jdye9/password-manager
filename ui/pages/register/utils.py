from data_classes.credentials import Credentials
from data_classes.db import Database
from nicegui import ui
import re

db = Database("test.db")
credentials = Credentials()


def icon_fill(verified, icon):
    if verified:
        icon.props("color=green")
    else:
        icon.props("color=red")


def validate_username(username):
    try:
        users = list(map(lambda x: x["username"].lower(), db.get_users()))
        if username and username.lower() not in users:
            return True
        else:
            return False
    except:
        return False


def validate_password(password):
    """
    Validates a password based on the following criteria:
    - Minimum length of 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    try:
        if len(password) < 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            return False
        return True
    except:
        return False


def validate_input(type, input, icon):
    if type == "username":
        if validate_username(input):
            icon_fill(True, icon)
        else:
            icon_fill(False, icon)

    if type == "password":
        if validate_password(input):
            icon_fill(True, icon)
        else:
            icon_fill(False, icon)


def check_validity(username, password):
    try:
        if validate_username(username) and validate_password(password):
            registered = credentials.register(username, password)
            if registered:
                ui.navigate.to("/")
            else:
                print("Failed to register account.")
    except:
        print("Failed to register account.")
