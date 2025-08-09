from flask import Blueprint, jsonify, request
from pydantic import BaseModel, field_validator, constr, ValidationError
from models import User
from extensions import db, bcrypt
import re # regular expressions module

# Creates a blueprint that can be imported
register_bp = Blueprint('register_bp', __name__)

NAME_PATTERN = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$"
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class UserSchema(BaseModel):
    fullname: constr(strip_whitespace=True)
    email: constr(strip_whitespace=True)
    password: constr(min_length=5)

    @field_validator("fullname")
    def fullname_must_be_letters(cls, v):
        if not re.match(NAME_PATTERN, v):
            raise ValueError("Only letters are allowed in the name")
        return v
    
    @field_validator("email")
    def email_must_be_valid(cls, v):
        if not re.match(EMAIL_PATTERN, v):
            raise ValueError("Please enter a valid email address.")
        return v


@register_bp.route('/register', methods=["POST"])
def register():
    try:
        user = UserSchema(**request.json) # raise ValidationError if not passed

        # hash the password
        hashed_pw = bcrypt.generate_password_hash(user.password).decode("utf-8")

        print(hashed_pw)

        new_user = User(
            name=user.fullname,
            email=user.email,
            password_hash=hashed_pw
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as e:
        # save the msg in a object and slip the text in 2 parts and show only the message
        errors = {err["loc"][0]: err["msg"].split(", ", 1)[-1] for err in e.errors()} # send only the error msg of the field
        
        error_messages = list(errors.values())
        
        return jsonify({"errors": error_messages}), 400