#!/usr/bin/python3
""" Manages Amenity objects through API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Fetches all Amenity objects from the storage"""
    all_amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in all_amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    amenity.delete()
    storage.save()
    return make_response(jsonify({"message": "Amenity deleted"}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    new_amenity_data = request.get_json()
    if not new_amenity_data:
        abort(400, description="Not a valid JSON")
    if "name" not in new_amenity_data:
        abort(400, description="Missing name field")
    new_amenity = Amenity(**new_amenity_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201,
                         {"Location": f"/amenities/{new_amenity.id}"})


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a specific Amenity object by ID"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")

    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a valid JSON")

    for key, value in updated_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
