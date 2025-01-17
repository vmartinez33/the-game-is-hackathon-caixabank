""" /api/account routes """
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from mail import send_investment_purchase_email, send_investment_sale_email
from models import Transaction, User, UserAsset, db
from services.market_service import get_asset_prices, update_user_asset
from services.user_service import calculate_net_worth
from utils import is_asset_valid

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


@account_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit_money():
    """ Deposits a specific amount into the user's account """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    pin = data.get("pin")
    amount = float(data.get("amount"))

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    user.balance += amount
    db.session.commit()

    transaction = Transaction(amount=amount, transaction_type="CASH_DEPOSIT",
                              transaction_date=datetime.now(timezone.utc),
                              source_account_number=user.accountNumber,
                              target_account_number="N/A")
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Cash deposited successfully"}), 200


@account_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw_money():
    """ Withdraws a specific amount from the user's account """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    amount = float(data.get("amount"))
    pin = data.get("pin")

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    if user.balance < amount:
        return jsonify("Insufficient balance"), 400

    user.balance -= amount
    db.session.commit()

    transaction = Transaction(amount=amount, transaction_type="CASH_WITHDRAWAL",
                              transaction_date=datetime.now(timezone.utc),
                              source_account_number=user.accountNumber,
                              target_account_number="N/A")
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Cash withdrawn successfully"}), 200


@account_bp.route('/fund-transfer', methods=['POST'])
@jwt_required()
def fund_transfer():
    """ Transfers funds to another account """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    amount = float(data.get("amount"))
    pin = data.get("pin")
    target_account_number = data.get("targetAccountNumber")

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    if user.balance < amount:
        return jsonify("Insufficient balance"), 400

    target_user = User.query.filter_by(accountNumber=target_account_number).first()
    if not target_user:
        return jsonify({"msg": "Target account not found"}), 404

    user.balance -= amount
    target_user.balance += amount
    db.session.commit()

    transaction = Transaction(amount=amount, transaction_type="CASH_TRANSFER",
                              transaction_date=datetime.now(timezone.utc),
                              source_account_number=user.accountNumber,
                              target_account_number=target_account_number)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Fund transferred successfully"}), 200


@account_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transaction_history():
    """ Retrieves the user's transaction history """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    transactions = Transaction.query.filter(
        (Transaction.source_account_number == user.accountNumber) |
        (Transaction.target_account_number == user.accountNumber)
    ).all()

    transaction_list = [{
        "id": transaction.id,
        "amount": transaction.amount,
        "transactionType": transaction.transaction_type,
        "transactionDate": int(transaction.transaction_date.timestamp() * 1000),
        "sourceAccountNumber": transaction.source_account_number,
        "targetAccountNumber": transaction.target_account_number
    } for transaction in transactions]

    return jsonify(transaction_list), 200


@account_bp.route('/buy-asset', methods=['POST'])
@jwt_required()
def buy_asset():
    """ Buys a specified asset for the user """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    asset_symbol = data.get("assetSymbol")
    amount = data.get("amount")
    pin = data.get("pin")

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    if not is_asset_valid(asset_symbol):
        return jsonify("Asset not valid"), 400

    asset_price = get_asset_prices(asset_symbol)
    if not asset_price or user.balance < amount:
        return jsonify("Internal error occurred while purchasing the asset."), 500

    quantity = amount / asset_price

    user.balance -= amount
    transaction = Transaction(
        source_account_number=user.accountNumber,
        amount=amount,
        transaction_type="ASSET_PURCHASE",
        asset_symbol=asset_symbol,
        asset_price_at_purchase=asset_price,
        asset_quantity=quantity,
        transaction_date=datetime.now(timezone.utc)
    )
    db.session.add(transaction)
    db.session.commit()

    update_user_asset(user, asset_symbol, quantity, asset_price)
    send_investment_purchase_email(user, asset_symbol, quantity, amount)

    return jsonify("Asset purchase successful."), 200


@account_bp.route('/sell-asset', methods=['POST'])
@jwt_required()
def sell_asset():
    """ Sells a specified asset for the user """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.json
    asset_symbol = data.get("assetSymbol")
    quantity = data.get("quantity")
    pin = data.get("pin")

    if user.pin != pin:
        return jsonify("Invalid PIN"), 403

    if not is_asset_valid(asset_symbol):
        return jsonify("Asset not valid"), 400

    current_price = get_asset_prices(asset_symbol)
    user_asset = UserAsset.query.filter_by(user_id=user.id, asset_symbol=asset_symbol).first()
    if not current_price or not user_asset or user_asset.quantity < quantity:
        return jsonify("Internal error occurred while selling the asset."), 500

    sale_amount = quantity * current_price
    profit_loss = sale_amount - (user_asset.avg_purchase_price * quantity)
    user.balance += sale_amount
    user_asset.quantity -= quantity

    if user_asset.quantity == 0:
        db.session.delete(user_asset)

    transaction = Transaction(
        source_account_number=user.accountNumber,
        amount=sale_amount,
        transaction_type="ASSET_SELL",
        asset_symbol=asset_symbol,
        asset_price_at_purchase=current_price,
        asset_quantity=quantity,
        transaction_date=datetime.now(timezone.utc)
    )
    db.session.add(transaction)
    db.session.commit()

    send_investment_sale_email(user, asset_symbol, quantity, profit_loss)

    return jsonify("Asset sale successful."), 200


@account_bp.route('/assets', methods=['GET'])
@jwt_required()
def get_user_assets():
    """ User asset informational endpoint """


@account_bp.route('/net-worth', methods=['GET'])
@jwt_required()
def net_worth():
    """ Provide users with an overview of their net worth """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = calculate_net_worth(user)

    return jsonify(data), 200
