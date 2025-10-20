from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from sqlalchemy import select
from models import User
import re

# Creates a blueprint that can be imported
auth_bp = Blueprint('auth_bp', __name__)

# match first letter of each word (any word character)
FIND_UPPERCASE_LETTERS = r'\b[A-Z]'

#TODO: pass the role from cookie

# centralized token validator
@auth_bp.route('/check-auth', methods=["GET"])
@jwt_required()
def check_auth():
    current_user_id = get_jwt_identity()
     
    # collect user name
    name = db.session.scalar(select(User.name).where(
        User.id == current_user_id
    ))

    if not name:
        return jsonify({"error": "User not found"}), 404

    initials = re.findall(FIND_UPPERCASE_LETTERS, name)

    return jsonify({"initials": initials}), 200
