from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Creates a blueprint that can be imported
auth_bp = Blueprint('auth_bp', __name__)

# centralized token validator
@auth_bp.route('/check-auth', methods=["GET"])
@jwt_required()
def check_auth():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Token is valid, user: {current_user_id}"}), 200
