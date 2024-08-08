#!/usr/bin/env python3
"""
Module of Users views.
This module handles all the routes related to user operations such as creating,
retrieving, updating, and deleting user data.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Retrieves the list of all User objects.

    Returns:
        A JSON list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id
    Retrieves a User object based on the provided user_id.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        A JSON representation of the User object if found.
        404 error if the User ID does not exist or is invalid.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(401, description="Unauthorized")  # Change to 401
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id
    Deletes a User object based on the provided user_id.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        An empty JSON dictionary if the deletion was successful.
        404 error if the User ID does not exist or is invalid.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/
    Creates a new User object with the provided data.

    JSON body:
        - email (str): The user's email (mandatory).
        - password (str): The user's password (mandatory).
        - first_name (str): The user's first name (optional).
        - last_name (str): The user's last name (optional).

    Returns:
        A JSON representation of the newly created User object.
        400 error if the creation fails due to invalid data or missing fields.
    """
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get("email") is None or rj.get("email") == "":
        return jsonify({'error': "email missing"}), 400
    if rj.get("password") is None or rj.get("password") == "":
        return jsonify({'error': "password missing"}), 400
    try:
        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': "Can't create User: {}".format(e)}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/:id
    Updates a User object with the provided data.

    Args:
        user_id (str): The ID of the user to update.

    JSON body:
        - first_name (str): The user's first name (optional).
        - last_name (str): The user's last name (optional).

    Returns:
        A JSON representation of the updated User object.
        404 error if the User ID does not exist or is invalid.
        400 error if the update fails due to invalid data.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
