#!/usr/bin/env python3
"""
API initialization module.
"""

from flask import Flask, jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

auth = BasicAuth()

@app.before_request
def before_request():
    """
    Method to handle actions before each request.
    Assigns the current authenticated user to request.current_user.
    """
    request.current_user = auth.current_user(request)

@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors.
    Returns:
        JSON response with error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

