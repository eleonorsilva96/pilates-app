from flask import Blueprint
from .hello import hello_bp

# Create the Blueprint object
api_bp = Blueprint('api_bp', __name__)

# Register routes inside the Blueprint object
api_bp.register_blueprint(hello_bp)