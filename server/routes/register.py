from flask import Blueprint, jsonify, request

# Creates a blueprint that can be imported
register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.json.get("fullname")
        email = request.json.get("email")
        password = request.json.get("password")

        if not fullname and not email and not password:
            return jsonify(code=404)

        print(f"fullname: {fullname}")
        print(f"email: {email}")
        print(f"password: {password}")

        return jsonify(code=200)
