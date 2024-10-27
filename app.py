""" app.py """
from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def hello_world():
    """ hello_world() """
    return "<p>Hello, World!</p>"
