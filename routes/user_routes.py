""" /api/users routes """
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from models import User
from services.user_service import create_user
from utils import is_field_empty, validate_email, get_existing_user
from jwt_token import blocklist

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


@users_bp.route('/login', methods=['POST'])
def login_user():
    """ Logs in the user and returns a JWT token """
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    # Buscar usuario por email o account number
    user = User.query.filter((User.email == identifier) | (User.accountNumber == identifier)).first()

    if user is None:
        return jsonify(f'User not found for the given identifier: {identifier}'), 400

    if not user.check_password(password):
        return jsonify('Bad credentials'), 401

    # Generar el token JWT
    token = create_access_token(identity=user.id)

    return jsonify(token=token), 200


@users_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    """ Logs out the user and invalidates the JWT token """
    jti = get_jwt()['jti']
    blocklist.add(jti)
    return jsonify({'message': 'Logged out successfully'}), 200
