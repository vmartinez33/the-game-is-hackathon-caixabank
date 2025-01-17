""" Models file """
import uuid
from datetime import datetime, timezone

import pytz
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    accountNumber = db.Column(
        db.String(36), unique=True, nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    balance = db.Column(db.Float, nullable=False, default=0.0)
    password_reset_token = db.Column(db.String(256), nullable=True)
    password_reset_token_expiration = db.Column(db.DateTime, nullable=True)
    pin = db.Column(db.String(4), nullable=True)

    # transactions = db.relationship("Transaction", back_populates="user")
    # assets = db.relationship("UserAsset", back_populates="user")

    def set_password(self, password):
        """ hash and set user password """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """ check hashed password """
        return bcrypt.check_password_hash(self.password, password)

    def is_password_token_expired(self):
        """ Check if password token is expired """
        return datetime.now(timezone.utc) > pytz.UTC.localize(self.password_reset_token_expiration)

    def __repr__(self):
        return f'<User {self.name}>'


class OTP(db.Model):
    """ OTP model """
    __tablename__ = 'otp_codes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        """ Check if OTP code is expired """
        return datetime.now(timezone.utc) > pytz.UTC.localize(self.expires_at)


class Transaction(db.Model):
    """ Transaction model """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    transaction_date = db.Column(db.TIMESTAMP, nullable=False)
    source_account_number = db.Column(db.String(36), nullable=False)
    target_account_number = db.Column(db.String(36), nullable=True)
    asset_symbol = db.Column(db.String(256), nullable=True)
    asset_price_at_purchase = db.Column(db.Float, nullable=True)
    asset_quantity = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, transaction_type='{self.transaction_type}', \
            transaction_date='{self.transaction_date}', \
            source_account_number='{self.source_account_number}', target_account_number='{self.target_account_number}')>"


class UserAsset(db.Model):
    """ UserAsset model """
    __tablename__ = "user_assets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    asset_symbol = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Float, default=0)
    avg_purchase_price = db.Column(db.Float, default=0)
