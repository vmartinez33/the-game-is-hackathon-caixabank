""" /api/user-actions routes """
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import Transaction, User, db
from utils import is_field_empty

user_action_bp = Blueprint('user-actions', __name__)


@user_action_bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    """ Creates a subscription for periodic payments. """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    pin = data.get("pin")
    amount = data.get("amount")
    interval_seconds = data.get("intervalSeconds")

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    if user.balance < float(amount):
        return jsonify("Insufficient balance"), 400

    transaction = Transaction(
        amount=float(amount),
        transaction_type="SUBSCRIPTION",
        transaction_date=datetime.now(timezone.utc),
        source_account_number=user.accountNumber,
        target_account_number=None,
        asset_symbol=None,
        asset_price_at_purchase=None,
        asset_quantity=None
    )
    db.session.add(transaction)
    db.session.commit()

    #TODO: set subscription job

    return jsonify("Subscription created successfully."), 200


@user_action_bp.route('/enable-auto-invest', methods=['POST'])
@jwt_required()
def enable_auto_invest():
    """ Enables the auto-investment feature. """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    pin = data.get("pin")

    if is_field_empty(pin):
        return jsonify("PIN cannot be null or empty"), 400

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    #TODO: enable auto invest logic

    return jsonify("Automatic investment enabled successfully."), 200
