""" utils functions """
import random
import re

from models import User


def validate_email(email):
    """ Validate email with regex """
    # Expresión regular para validar el formato del email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def is_field_empty(field):
    """ Check if field is empty """
    return field is None or field.strip() == ""


def get_existing_user(email, phone_number):
    """ Get user with same email or phone_number """
    existing_user = User.query.filter((User.email == email) | (User.phoneNumber == phone_number)).first()
    return existing_user


def generate_otp():
    """ Generate 6 digit OTP code """
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def validate_password(password):
    """ Validate password """
    if re.search(r'\s', password):
        return "Password cannot contain whitespace"

    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter"

    if not re.search(r'\d', password):
        return "Password must contain at least one digit and one special character"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character"

    if len(password) < 8:
        return "Password must be at least 8 characters long"

    if len(password) >= 128:
        return "Password must be less than 128 characters long"

    return None


def is_asset_valid(asset_symbol):
    """ Checks if an asset symbol is valid """
    valid_assets = ("AAPL", "GOOGL", "TSLA", "AMZN", "MSFT", "NFLX", "FB", "BTC", "ETH", "XRP", "GOLD", "SILVER")
    if asset_symbol in valid_assets:
        return True
    return False
