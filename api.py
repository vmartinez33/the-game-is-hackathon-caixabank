""" API route Blueprint """
from flask import Blueprint

from routes.user_routes import users_bp
from routes.dashboard_routes import dashboard_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(dashboard_bp, url_prefix='/dashboard')
