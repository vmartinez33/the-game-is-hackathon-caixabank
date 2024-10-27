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
