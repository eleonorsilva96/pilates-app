from flask import Blueprint, jsonify, request
from sqlalchemy import select
from models import User
from extensions import db, bcrypt, AuthError
# vamos precisar do metodo de ir buscar o token
from flask_jwt_extended import jwt_required, get_jwt_identity

# Creates a blueprint that can be imported
classes_bp = Blueprint('classes_bp', __name__)

# access classes only with a valid jwt
@classes_bp.route('/classes', methods=["GET"])
@jwt_required()
def classes():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Welcome, user {current_user_id}!"}), 200
