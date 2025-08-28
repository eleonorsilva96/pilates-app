
from app import app
from extensions import db
from models.users import User

with app.app_context():
    user = User(name="Maria", email="maria@gmail.com", password_hash="secretnew123")
    db.session.add(user)
    db.session.commit()
    print("User created successfully!")