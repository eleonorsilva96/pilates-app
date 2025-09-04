from flask import Flask, jsonify 
from flask_cors import CORS
from extensions import db, bcrypt, jwt, EmailAlreadyExistsError
from routes import api_bp

# Configure application
app = Flask(__name__)

# App configs
app.config.from_object('config.DevConfig')

# JWT from cookie
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900    # 15 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 604800 # 7 days

# Init extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Create database
with app.app_context():
    db.create_all()

# Register the API blueprints inside the /api prefix
app.register_blueprint(api_bp, url_prefix='/api')

# Enable cross-origin requests and cookies from Vue
CORS(
    app, 
    origins=["http://localhost:5173"],
    supports_credentials=True
)

if __name__ == "__main__":
    app.run(port=8888)