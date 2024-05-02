#!/usr/bin/python3
""" Manages User objects through API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
import hashlib


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves all User objects from the storage"""
    all_users = storage.all(User)
    return jsonify([user.to_dict() for user in all_users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Fetches a specific User object by its ID"""
    user = storage.get("User", user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Removes a specific User object by its ID"""
    user = storage.get("User", user_id)
    if not user:
        abort(404, description="User not found")
    user.delete()
    storage.save()
    return make_response(jsonify({"message": "User deleted"}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Adds a new User object to the storage"""
    new_user_data = request.get_json()
    if not new_user_data:
        abort(400, description="Not a valid JSON")
    if "email" not in new_user_data:
        abort(400, description="Missing email field")
    if "password" not in new_user_data:
        abort(400, description="Missing password field")

    # Encrypts the password before saving
    hashed_password = hashlib.sha256(new_user_data["password"].encode()).hexdigest()
    new_user_data["password"] = hashed_password

    user = User(**new_user_data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201, {"Location": f"/users/{user.id}"})


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Modifies a specific User object by its ID"""
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

