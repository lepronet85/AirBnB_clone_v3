#!/usr/bin/python3
""" Handles CRUD operations for State objects via API """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Fetches all State objects from the storage"""
    all_states = storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a specific State object by ID"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, description="State not found")
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific State object by ID"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, description="State not found")
    state.delete()
    storage.save()
    return make_response(jsonify({"message": "State deleted"}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    new_state_data = request.get_json()
    if not new_state_data:
        abort(400, description="Not a valid JSON")
    if "name" not in new_state_data:
        abort(400, description="Missing name field")
    new_state = State(**new_state_data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201, {"Location": f"/states/{new_state.id}"})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a specific State object by ID"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, description="State not found")

    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a valid JSON")

    for key, value in updated_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
