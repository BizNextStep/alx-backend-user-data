#!/usr/bin/env python3
"""
Module of Users views.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Return:
        - A list of all User objects in JSON format.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id
    Path parameter:
        - User ID or 'me' for current authenticated user.
    Return:
        - User object in JSON format if found.
        - 404 if the User ID doesn't exist or if 'me' is used and the user is not authenticated.
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id
    Path parameter:
        - User ID
    Return:
        - Empty JSON with status 200 if User is correctly deleted.
        - 404 if the User ID doesn't exist.
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
    JSON body:
        - email (mandatory)
        - password (mandatory)
        - last_name (optional)
        - first_name (optional)
    Return:
        - User object in JSON format if created successfully.
        - 400 if the creation fails due to missing or incorrect data.
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
    Path parameter:
        - User ID
    JSON body:
        - last_name (optional)
        - first_name (optional)
    Return:
        - Updated User object in JSON format if successful.
        - 404 if the User ID doesn't exist.
        - 400 if the update fails due to incorrect data.
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

