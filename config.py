""" Config file """
import dataclasses
import os

from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


@dataclasses.dataclass
class Config:
    """ Configuration dataclass """
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'True'
    APP = os.getenv('FLASK_APP', 'app.py')
    RUN_HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
    ENV = os.getenv('FLASK_ENV', 'development')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', None)

    MAIL_SERVER = os.getenv('MAIL_SERVER', "localhost")
    MAIL_PORT = os.getenv('MAIL_PORT', "1025")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'noreply@bankingapp.com'
