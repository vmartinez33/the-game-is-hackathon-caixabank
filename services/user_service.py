""" /api/users service """
import uuid

from models import User, UserAsset, db
from services.market_service import get_asset_prices


def create_user(name, email, password, address, phone_number):
    """ Create new user """
    account_number = str(uuid.uuid4())[:6]
    new_user = User(name=name, email=email, address=address, phoneNumber=phone_number, accountNumber=account_number)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def calculate_net_worth(user):
    """ Calculate the net worth of the user, including balance and asset holdings """
    assets = UserAsset.query.filter_by(user_id=user.id).all()
    assets_prices = get_asset_prices()

    total_asset_value = 0.0
    for user_asset in assets:
        current_price = assets_prices[user_asset.asset_symbol]

        if current_price:
            asset_value = user_asset.quantity * current_price
            total_asset_value += asset_value

    net_worth = user.balance + total_asset_value
    return net_worth
