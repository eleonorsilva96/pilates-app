from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import select
from pydantic import BaseModel, constr
from models import User
from extensions import db, bcrypt, AuthError
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
import re # regular expressions module

# Creates a blueprint that can be imported
login_bp = Blueprint('login_bp', __name__)
refresh_bp = Blueprint('refresh_bp', __name__)
logout_bp = Blueprint('logout_bp', __name__)

class UserSchema(BaseModel):
    email: constr(strip_whitespace=True)
    password: constr(strip_whitespace=True)


@login_bp.route('/login', methods=["POST"])
def login():
    try:
        data = UserSchema(**request.json)
        
        user = db.session.scalars(select(User).where(User.email == data.email)).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data.password):
            raise AuthError("Invalid e-mail or password")

        # create JWT tokens
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        refresh_token = create_refresh_token(identity=user.id, additional_claims={"role": user.role})

        response = make_response(jsonify({
             "message": "Login successful"
        }), 200)

        # store tokens in an HTTP-only cookie so it is sent automatically with requests to the backend
        # store refresh token to be able to get a new access token without requiring the user to log in again
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response
    except AuthError as e:
            return jsonify({"errors": [str(e)]}), 401
    

@refresh_bp.route('/refresh', methods=["GET"])
@jwt_required(refresh=True) # reads the refresh token on the HTTP-only cookie
def refresh():
    current_user = get_jwt_identity()
    data = get_jwt()
    role = data.get("role")

    access_token = create_access_token(identity=current_user, additional_claims={"role": role})
    response = jsonify({"message": "Token refreshed"})
    set_access_cookies(response, access_token)
    return response

@logout_bp.route('/logout', methods=["GET", "POST"])
def logout():
    response = jsonify({"message": "Access token removed"})
    unset_jwt_cookies(response)  # removes access (and refresh) cookies
    return response, 200
