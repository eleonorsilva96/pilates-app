from flask import Blueprint
from .check_auth import auth_bp
from .register import register_bp
from .login import login_bp, refresh_bp, logout_bp
from .dashboard import dashboard_bp
from .classes import classes_bp

# Create the Blueprint object
api_bp = Blueprint('api_bp', __name__)

# Register routes inside the Blueprint object
api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(register_bp, url_prefix='/auth')
api_bp.register_blueprint(login_bp, url_prefix='/auth')
api_bp.register_blueprint(refresh_bp, url_prefix='/auth')
api_bp.register_blueprint(logout_bp, url_prefix='/auth')
api_bp.register_blueprint(dashboard_bp)
api_bp.register_blueprint(classes_bp)