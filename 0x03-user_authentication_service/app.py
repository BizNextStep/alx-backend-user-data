#!/usr/bin/env python3
"""Flask class
This module sets up a Flask web application for user authentication and management.
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """GET /
    Returns a welcome message.
    
    Return:
        - JSON response with a welcome message and HTTP status 200.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """POST /users
    Registers a new user with the provided email and password.
    
    Return:
        - JSON response indicating the email and a success message if user is created.
        - JSON response with an error message if the email is already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Logs in a user by validating their email and password.
    
    Return:
        - JSON response indicating the email and a success message if login is successful.
        - HTTP 401 error if login credentials are invalid.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Logs out a user by destroying their session.
    
    Return:
        - Redirects to the welcome page if logout is successful.
        - HTTP 403 error if the session is invalid or does not exist.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Retrieves the profile information of the logged-in user.
    
    Return:
        - JSON response with the user's email if the session is valid.
        - HTTP 403 error if the user is not logged in.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Generates a reset password token for the user identified by their email.
    
    Return:
        - JSON response with the user's email and the reset token if successful.
        - HTTP 403 error if the user is not found.
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Updates the user's password using the provided reset token.
    
    Return:
        - JSON response with the user's email and a success message if the password is updated.
        - HTTP 403 error if the reset token is invalid or other errors occur.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}", "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
