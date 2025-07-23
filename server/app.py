from flask import Flask, jsonify 
from flask_cors import CORS
from extensions import db
from models import User
from routes import api_bp

# Configure application
app = Flask(__name__)

# App configs
app.config.from_object('config.DevConfig')

# Init SQLAlchemy extension
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()

# Register the API blueprint with the /api prefix
app.register_blueprint(api_bp, url_prefix='/api')

# Enable cross-origin requests to talk with Vue
CORS(app, origins=["http://localhost:5173"])

if __name__ == "__main__":
    app.run(port=8888)