#!/usr/bin/python3
"""
Script that initializes a Flask application and integrates a Blueprint.
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
from flasgger import Swagger

# Initialize the Flask application
app = Flask(__name__)
# Register the Blueprint for the application views
app.register_blueprint(app_views)
# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# Configure Swagger for API documentation
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'HBNB REST API',
            "route": '/v1/views',
        }
    ]
}
# Initialize Swagger with the Flask app
swagger = Swagger(app)

@app.teardown_appcontext
def teardown_session(exception):
    """
    Closes the storage session after each request.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handles 404 errors by returning a JSON response with a 404 status code.
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    # Retrieve environment variables for the API host and port
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    # Set default values for the host and port if not specified
    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    # Run the Flask application
    app.run(host=host, port=port, threaded=True)

