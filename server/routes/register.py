from flask import Blueprint, jsonify, request
from pydantic import BaseModel, field_validator, constr, ValidationError
from models import User, Student
from extensions import db, bcrypt, EmailAlreadyExistsError, Roles
from sqlalchemy import select
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
        data = UserSchema(**request.json) # raise ValidationError if not passed

        # check for existed user student
        user = db.session.scalars(select(User).where(
            User.email == data.email,
            User.role == Roles.USER
            )).first()
        
        if user:
            raise EmailAlreadyExistsError("This email already exists")
        
        # hash the password
        hashed_pw = bcrypt.generate_password_hash(data.password).decode("utf-8")

        new_user = User(
            name=data.fullname,
            email=data.email,
            password_hash=hashed_pw
        )

        # creates a new student record and links it to the given user instance via the foreign key
        Student(user=new_user)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except ValidationError as e:
        # save the msg in a object and slip the text in 2 parts and show only the message
        errors = {err["loc"][0]: err["msg"].split(", ", 1)[-1] for err in e.errors()} # send only the error msg of the field
        
        error_messages = list(errors.values())
        
        return jsonify({"errors": error_messages}), 400
    except EmailAlreadyExistsError as e:
        # return custom error inside the same errors list
        return jsonify({"errors": [str(e)]}), 400