""" Service to fetch market prices in real time """
import requests

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
