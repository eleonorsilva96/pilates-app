from flask_sqlalchemy import SQLAlchemy
from nanoid import generate as nanoid_generate
from flask_bcrypt import Bcrypt

# define roles
class Roles:
    USER = "user"
    ADMIN = "admin"

# generate unique opaque id for each new user created
def generate():
    return nanoid_generate()

bcrypt = Bcrypt()
db = SQLAlchemy()


