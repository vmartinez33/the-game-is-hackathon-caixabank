""" /api/dashboard routes """
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import User

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/user', methods=['GET'])
@jwt_required()
def user_info():
    """ Retrieves the logged-in user's details """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        return jsonify('User not found'), 404

    return jsonify({
        'name': user.name,
        'email': user.email,
        'phoneNumber': user.phoneNumber,
        'address': user.address,
        'accountNumber': user.accountNumber,
        'hashedPassword': user.password
    }), 200


@dashboard_bp.route('/account', methods=['GET'])
@jwt_required()
def account_info():
    """ Retrieves account information, including balance """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        return jsonify('User not found'), 404

    return jsonify({
        'accountNumber': user.accountNumber,
        'balance': user.balance
    }), 200
