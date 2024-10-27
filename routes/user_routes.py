""" /api/users routes """
from flask import Blueprint, jsonify

users_bp = Blueprint('users', __name__)


@users_bp.route('/register', methods=['POST'])
def register_user():
    """ User register endpoint """
    return jsonify({'message': "User registered"}), 200
