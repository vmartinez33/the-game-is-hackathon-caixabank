""" API route Blueprint """
from flask import Blueprint

from routes.user_routes import users_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp
from routes.account_routes import account_bp
from routes.user_actions_routes import user_action_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(dashboard_bp, url_prefix='/dashboard')
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(account_bp, url_prefix='/account')
api_bp.register_blueprint(user_action_bp, url_prefix='/user-actions')
