""" /api/users service """
import uuid

from models import User, db


def create_user(name, email, password, address, phone_number):
    """ Create new user """
    account_number = str(uuid.uuid4())
    new_user = User(name=name, email=email, address=address, phoneNumber=phone_number, accountNumber=account_number)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return new_user
