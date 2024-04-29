#!/usr/bin/python3
"""
This script defines the index for the application, including routes
for status and statistics.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Endpoint to check the application's status, returning a JSON response.
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Endpoint to retrieve the count of each instance type,
    returning a JSON response.
    """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
