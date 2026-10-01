import re


def validate_registration(data):
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password") or ""
    if not name:
        raise ValueError("Name is required")
    if len(name) > 120:
        raise ValueError("Name must be 120 characters or fewer")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(email) > 254:
        raise ValueError("Enter a valid email address")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > 128:
        raise ValueError("Password must be 128 characters or fewer")
    return {"name": name, "email": email, "password": password}


def validate_login(data):
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        raise ValueError("Email and password are required")
    return {"email": email, "password": password}


def validate_profile_update(data):
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    if not name or len(name) > 120:
        raise ValueError("Name is required and must be 120 characters or fewer")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(email) > 254:
        raise ValueError("Enter a valid email address")
    return {"name": name, "email": email}


def validate_password_update(data):
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""
    if not current_password:
        raise ValueError("Enter your current password")
    if len(new_password) < 8:
        raise ValueError("New password must be at least 8 characters")
    if len(new_password) > 128:
        raise ValueError("New password must be 128 characters or fewer")
    return {"current_password": current_password, "new_password": new_password}
