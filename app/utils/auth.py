from functools import wraps
from flask import request, jsonify
from app.models import User

def requires_master_role(f):
    """
    A decorator to restrict access to users with the 'master' role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Retrieve user from the request header or your authentication system.
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"error": "Unauthorized - User ID missing"}), 401

        # Query the user in the database.
        user = User.query.get(user_id)
        if not user or user.role != "master":
            return jsonify({"error": "Forbidden - Master access required"}), 403

        # Proceed to the endpoint if the user is authorized.
        return f(*args, **kwargs)
    return decorated_function
