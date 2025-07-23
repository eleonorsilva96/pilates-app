from flask import Blueprint, jsonify

# Creates a blueprint that can be imported
hello_bp = Blueprint('hello_bp', __name__)

@hello_bp.route('/hello', methods=["GET"])
def hello():
    return jsonify(message="Hello from Flask again!")