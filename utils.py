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
