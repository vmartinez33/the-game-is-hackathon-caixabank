""" Flask-Mail module definition """
from flask_mail import Mail, Message

from models import UserAsset
from services.user_service import calculate_net_worth

mail = Mail()


def send_email(email, body, subject='FLASK'):
    """ send email """
    msg = Message(
        subject=subject,
        recipients=[email],
        body=body
    )
    mail.send(msg)


def send_investment_purchase_email(user, asset_symbol, quantity, amount):
    """ Send investment email to user after purchase """
    subject = "Investment Purchase Confirmation"

    user_asset = UserAsset.query.filter_by(user_id=user.id, asset_symbol=asset_symbol).first()
    current_holdings = f"{user_asset.quantity:.2f}" if user_asset else "0.00"
    total_invested = f"{user_asset.avg_purchase_price * user_asset.quantity:.2f}" if user_asset else "0.00"
    net_worth = calculate_net_worth(user)

    email_body = f"""
    Dear {user.name},

    You have successfully purchased {quantity:.2f} units of {asset_symbol} for a total amount of ${amount:.2f}.

    Current holdings of {asset_symbol}: {current_holdings} units

    Summary of current assets:
    - {asset_symbol}: {current_holdings} units purchased at ${total_invested}

    Account Balance: ${user.balance:.2f}
    Net Worth: ${net_worth:.2f}

    Thank you for using our investment services.

    Best Regards,
    Investment Management Team
    """

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=email_body
    )
    mail.send(msg)


def send_investment_sale_email(user, asset_symbol, quantity, profit_loss):
    """ Send investment email to user after purchase """
    subject = "Investment Sale Confirmation"

    user_asset = UserAsset.query.filter_by(user_id=user.id, asset_symbol=asset_symbol).first()
    current_holdings = f"{user_asset.quantity:.2f}" if user_asset else "0.00"
    total_invested = f"{user_asset.avg_purchase_price * user_asset.quantity:.2f}" if user_asset else "0.00"
    net_worth = calculate_net_worth(user)

    email_body = f"""
    Dear {user.name},

    You have successfully sold {quantity:.2f} units of {asset_symbol}.

    Total Gain/Loss: ${profit_loss:.2f}

    Remaining holdings of {asset_symbol}: {current_holdings} units

    Summary of current assets:
    - {asset_symbol}: {current_holdings} units purchased at ${total_invested}

    Account Balance: ${user.balance:.2f}
    Net Worth: ${net_worth:.2f}

    Thank you for using our investment services.

    Best Regards,
    Investment Management Team
    """

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=email_body
    )
    mail.send(msg)
