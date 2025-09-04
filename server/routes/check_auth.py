from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from sqlalchemy import select
from models import User
import re

# Creates a blueprint that can be imported
auth_bp = Blueprint('auth_bp', __name__)

# match first letter of each word (any word character)
FIND_UPPERCASE_LETTERS = r"(?:^|\s)(\w)"

# centralized token validator
@auth_bp.route('/check-auth', methods=["GET"])
@jwt_required()
def check_auth():
    current_user_id = get_jwt_identity()
    # pass the role from cookie
    # collect user name
    name = db.session.scalars(select(User.name).where(
        User.id == current_user_id
    )).first()

    initials = re.findall(FIND_UPPERCASE_LETTERS, name)

    return jsonify({"initials": initials}), 200
