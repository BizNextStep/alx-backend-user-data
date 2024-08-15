#!/usr/bin/env python3
"""
Auth module
This module provides authentication functionalities including user registration.
"""

from db import DB
from user import User
from auth import _hash_password

class Auth:
    """Auth class to interact with the authentication database.
    This class handles user registration and authentication.
    """

    def __init__(self):
        """Initialize the Auth class with a database instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user in the database.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        # Check if user already exists
        existing_user = self._db._session.query(User).filter_by(email=email).first()
        if existing_user:
            raise ValueError(f"User {email} already exists.")

        # Hash the password
        hashed_password = _hash_password(password)

        # Add user to the database
        user = self._db.add_user(email, hashed_password)
        return user
