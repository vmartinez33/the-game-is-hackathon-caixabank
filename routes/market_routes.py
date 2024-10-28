""" /market routes """
from flask import Blueprint, jsonify

from services.market_service import get_asset_prices

market_bp = Blueprint('market', __name__)


@market_bp.route('/prices', methods=['GET'])
def get_prices():
    """ Retrieves current market prices for all assets """
    asset_prices = get_asset_prices()

    if asset_prices is None:
        return jsonify({"error": "Error fetching asset prices"}), 500

    return jsonify(asset_prices), 200


@market_bp.route('/prices/<string:symbol>', methods=['GET'])
def get_asset_price(symbol):
    """ Retrieves the current market price for a specific asset """
    asset_price = get_asset_prices(asset_symbol=symbol)

    if asset_price is None:
        return jsonify({"error": f"Asset '{symbol}' not found or error fetching price"}), 500

    return jsonify(asset_price), 200
