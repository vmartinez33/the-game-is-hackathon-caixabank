""" /api/account routes """
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from models import User, db

account_bp = Blueprint('account', __name__)


@account_bp.route('/pin/create', methods=['POST'])
@jwt_required()
def create_pin():
    """ Creates pin for user """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.get_json()
    pin = data.get('pin')
    password = data.get('password')

    if not pin or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if not user.check_password(password):
        return jsonify("Bad credentials"), 401

    user.pin = pin
    db.session.commit()

    return jsonify({"msg": "PIN created successfully"}), 200


@account_bp.route('/pin/update', methods=['POST'])
@jwt_required()
def update_pin():
    """ Updates pin for user """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.get_json()
    old_pin = data.get('oldPin')
    password = data.get('password')
    new_pin = data.get('newPin')

    if not old_pin or not password or not new_pin:
        return jsonify({"msg": "Missing required fields"}), 400

    if not user.check_password(password):
        return jsonify("Bad credentials"), 401

    if user.pin != old_pin:
        return jsonify({"msg": "Invalid old PIN"}), 401

    user.pin = new_pin
    db.session.commit()

    return jsonify({"msg": "PIN updated successfully"}), 200
