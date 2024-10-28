""" Service to fetch market prices in real time """
import requests

from models import db, UserAsset

API_URL = "https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-e0f31110-7521-4cb9-86a2-645f66eefb63/default/market-prices-simulator"


def get_asset_prices(asset_symbol=None):
    """ Get real time asset prices """
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        asset_prices = response.json()

        if asset_symbol:
            return asset_prices.get(asset_symbol.upper())

        return asset_prices

    except requests.RequestException as e:
        print(f"Error al obtener precios de assets: {e}")
        return None


def update_user_asset(user, asset_symbol, quantity, asset_price):
    """ Updates the user asset info """
    user_asset = UserAsset.query.filter_by(user_id=user.id, asset_symbol=asset_symbol).first()

    if user_asset:
        total_cost = user_asset.avg_purchase_price * user_asset.quantity + asset_price * quantity
        new_quantity = user_asset.quantity + quantity
        user_asset.avg_purchase_price = total_cost / new_quantity
        user_asset.quantity = new_quantity
    else:
        user_asset = UserAsset(
            user_id=user.id,
            asset_symbol=asset_symbol,
            quantity=quantity,
            avg_purchase_price=asset_price
        )
        db.session.add(user_asset)

    db.session.commit()
