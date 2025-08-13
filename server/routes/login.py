from flask import Blueprint, jsonify, request
from sqlalchemy import select
from pydantic import BaseModel, field_validator, constr, ValidationError
from models import Users
from extensions import db, bcrypt, AuthError
from flask_jwt_extended import JWTManager, create_access_token
import re # regular expressions module

# Creates a blueprint that can be imported
login_bp = Blueprint('login_bp', __name__)

class UsersSchema(BaseModel):
    email: constr(strip_whitespace=True)
    password: constr(strip_whitespace=True)


@login_bp.route('/login', methods=["POST"])
def login():
    try:
        data = UsersSchema(**request.json)
        
        user = db.session.scalars(select(Users).where(Users.email == data.email)).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data.password):
            raise AuthError("Invalid e-mail or password")

        # create JWT token
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})

        print(f"token: ${access_token}")

        return jsonify({
            "access_token": access_token,
            "message": "Login successful"}), 200
    except AuthError as e:
            return jsonify({"errors": [str(e)]}), 401
