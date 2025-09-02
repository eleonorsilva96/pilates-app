from flask import Blueprint, jsonify, request
from sqlalchemy import select
from models import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Creates a blueprint that can be imported
dashboard_bp = Blueprint('dashboard_bp', __name__)

# access dashboard only with a valid jwt
@dashboard_bp.route('/dashboard', methods=["GET"])
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome, user {current_user_id}!"}), 200
