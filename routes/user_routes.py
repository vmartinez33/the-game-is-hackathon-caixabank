""" /api/users routes """
from flask import Blueprint, jsonify, request

from services.user_service import create_user
from utils import is_field_empty, validate_email, get_existing_user

users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['POST'])
def register_user():
    """ Registers a new user """
    data = request.get_json()

    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    address = data.get('address')
    phone_number = data.get('phoneNumber')

    if is_field_empty(name) or is_field_empty(password) or is_field_empty(email) or is_field_empty(address) or is_field_empty(phone_number):
        return jsonify('All fields are required'), 400

    if not validate_email(email):
        return jsonify('Invalid email format'), 400

    existing_user = get_existing_user(email, phone_number)
    if existing_user:
        if existing_user.email == email:
            return jsonify('Email already exists'), 400
        if existing_user.phoneNumber == phone_number:
            return jsonify('Phone number already exists'), 400

    user = create_user(name, email, password, address, phone_number)

    response = {
        'name': user.name,
        'email': user.email,
        'phoneNumber': user.phoneNumber,
        'address': user.address,
        'accountNumber': user.accountNumber,
        'hashedPassword': user.password
    }

    return jsonify(response), 200
