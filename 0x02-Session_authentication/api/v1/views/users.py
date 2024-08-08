#!/usr/bin/env python3
"""
Module for handling user-related routes.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieve a user by ID or the current authenticated user if 'me' is provided.

    Args:
        user_id (str): The ID of the user to retrieve or 'me' for the current user.

    Returns:
        JSON response with user data or 404 error if the user is not found.
    """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

