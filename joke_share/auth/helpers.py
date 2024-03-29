import re


def is_valid_email(email: str):
    """Checks whether the email is valid or not"""

    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if re.search(email_regex, email):
        return True
    else:
        return False


def is_valid_username(username: str):
    """Checks whether the username is valid or not"""

    username_regex = r"^[a-zA-Z0-9_-]{6,28}$"
    if re.search(username_regex, username):
        return True
    else:
        return False


def is_valid_passowrd(password: str):
    """Checks whether the password is valid or not"""

    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[~!@#$%^&*()_+\-=/<>:;'\\]", password):
        return False
    
    return True

