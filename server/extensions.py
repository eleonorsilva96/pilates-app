from flask_sqlalchemy import SQLAlchemy
from nanoid import generate as nanoid_generate

# define roles
class Roles:
    USER = "user"
    ADMIN = "admin"

# generate unique opaque id for each new user created
def generate():
    return nanoid_generate()

db = SQLAlchemy()

