#!/usr/bin/python3
""" Manages User objects through API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
import hashlib


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Fetches all User objects from the storage"""
    all_users = storage.all(User)
    return jsonify([user.to_dict() for user in all_users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a specific User object by ID"""
    user = storage.get("User", user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific User object by ID"""
    user = storage.get("User", user_id)
    if not user:
        abort(404, description="User not found")
    user.delete()
    storage.save()
    return make_response(jsonify({"message": "User deleted"}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object"""
    new_user_data = request.get_json()
    if not new_user_data:
        abort(400, description="Not a valid JSON")
    if "email" not in new_user_data:
        abort(400, description="Missing email field")
    if "password" not in new_user_data:
        abort(400, description="Missing password field")

    # Hashing the password for security
    hashed_password = hashlib.sha256(
        new_user_data["password"].encode()
    ).hexdigest()

    user = User(email=new_user_data["email"], password=hashed_password)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201,
                         {"Location": f"/users/{user.id}"})


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a specific User object by ID"""
    user = storage.get("User", user_id)
    if not user:
        abort(404, description="User not found")

    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a valid JSON")

    for key, value in updated_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
