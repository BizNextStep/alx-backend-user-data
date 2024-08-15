#!/usr/bin/env python3
"""
Flask application for user authentication and management.
This application allows users to register, log in, view profiles, and reset passwords.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index() -> str:
    """Return a welcome message.

    Returns:
        str: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users() -> str:
    """Register a new user.

    This endpoint allows new users to register by providing an email and password.
    If the email is already registered, an error message is returned.

    Returns:
        str: JSON response with user email and success message or an error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Register user if the user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Log in a user.

    This endpoint allows users to log in by providing their email and password.
    If the login is successful, a session ID is created and returned in a cookie.

    Returns:
        str: JSON response with user email and success message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # Create a new session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response

@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Log out a user.

    This endpoint allows users to log out by destroying their session.
    If the session is invalid, a forbidden error is returned.

    Returns:
        str: Redirect to the index page.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Get the profile of the logged-in user.

    This endpoint returns the email of the user currently logged in.
    If the user is not logged in, a forbidden error is returned.

    Returns:
        str: JSON response with user email.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Request a password reset token.

    This endpoint allows users to request a reset token by providing their email.
    If successful, the reset token is returned.

    Returns:
        str: JSON response with user email and reset token.
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)

@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update the user's password.

    This endpoint allows users to update their password using a reset token.
    If successful, a success message is returned.

    Returns:
        str: JSON response with user email and success message.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
