from flask import Blueprint
from .register import register_bp

# Create the Blueprint object
api_bp = Blueprint('api_bp', __name__)

# Register routes inside the Blueprint object
api_bp.register_blueprint(register_bp)