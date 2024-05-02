#!/usr/bin/python3
""" Manages City objects through API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_for_state(state_id):
    """Fetches all City objects associated with a specific State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, description="State not found")
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a specific City object by ID"""
    city = storage.get("City", city_id)
    if not city:
        abort(404, description="City not found")
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a specific City object by ID"""
    city = storage.get("City", city_id)
    if not city:
        abort(404, description="City not found")
    city.delete()
    storage.save()
    return make_response(jsonify({"message": "City deleted"}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_for_state(state_id):
    """Creates a new City object associated with a specific State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, description="State not found")
    new_city_data = request.get_json()
    if not new_city_data:
        abort(400, description="Not a valid JSON")
    if "name" not in new_city_data:
        abort(400, description="Missing name field")
    new_city = City(**new_city_data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201,
                         {"Location": f"/cities/{new_city.id}"})


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a specific City object by ID"""
    city = storage.get("City", city_id)
    if not city:
        abort(404, description="City not found")

    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a valid JSON")

    for key, value in updated_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
