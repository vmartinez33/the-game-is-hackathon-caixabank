""" Models file """
import uuid

from flask_sqlalchemy import SQLAlchemy

from bcrypt import bcrypt


db = SQLAlchemy()


class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    accountNumber = db.Column(
        db.String(36), unique=True, nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    def set_password(self, password):
        """ hash and set user password """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """ check hashed password """
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name}>'
