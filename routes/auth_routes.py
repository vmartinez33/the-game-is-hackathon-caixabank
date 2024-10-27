""" /api/auth routes """
from datetime import datetime, timedelta, timezone
import uuid
from flask import Blueprint, jsonify, request
from flask_mail import Message

from models import db, OTP, User
from utils import generate_otp, validate_password
from mail import mail


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/password-reset/send-otp', methods=['POST'])
def send_otp():
    """ Sends an OTP for password reset """
    data = request.get_json()
    identifier = data.get('identifier')

    user = User.query.filter((User.email == identifier) | (User.accountNumber == identifier)).first()
    if not user:
        return jsonify(f"User not found for the given identifier: {identifier}"), 400

    otp_code = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    otp = OTP(user_id=user.id, otp_code=otp_code, expires_at=expires_at)
    db.session.add(otp)
    db.session.commit()

    msg = Message('Password Reset OTP', recipients=[user.email])
    msg.body = f"OTP:{otp_code}"
    mail.send(msg)

    return jsonify({"message": f"OTP sent successfully to: {user.email}"}), 200


@auth_bp.route('/password-reset/verify-otp', methods=['POST'])
def verify_otp():
    """ Verifies the OTP and returns a reset token """
    data = request.get_json()
    identifier = data.get('identifier')
    otp_code = data.get('otp')

    user = User.query.filter((User.email == identifier) | (User.accountNumber == identifier)).first()
    if not user:
        return jsonify(f"User not found for the given identifier: {identifier}"), 400

    otp_record = OTP.query.filter_by(user_id=user.id, otp_code=otp_code).first()

    if not otp_record or otp_record.is_expired():
        return jsonify("Invalid OTP"), 400

    password_reset_token = str(uuid.uuid4())
    user.password_reset_token = password_reset_token
    user.password_reset_token_expiration = datetime.now(timezone.utc) + timedelta(minutes=15)

    db.session.delete(otp_record)
    db.session.commit()

    return jsonify({"passwordResetToken": password_reset_token})


@auth_bp.route('/password-reset', methods=['POST'])
def password_reset():
    """ Resets the user's password """
    data = request.get_json()
    identifier = data.get('identifier')
    reset_token = data.get('resetToken')
    new_password = data.get('newPassword')

    if not identifier or not reset_token or not new_password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter((User.email == identifier) | (User.accountNumber == identifier)).first()
    if not user:
        return jsonify(f"User not found for the given identifier: {identifier}"), 400

    if user.password_reset_token is None or user.password_reset_token != reset_token or user.is_password_token_expired():
        return jsonify("Invalid reset token"), 400

    validation_error = validate_password(new_password)
    if validation_error:
        return jsonify(validation_error), 400

    user.set_password(new_password)
    user.password_reset_token = None
    user.password_reset_token_expiration = None

    db.session.commit()

    return jsonify({"message": "Password reset successfully"}), 200
