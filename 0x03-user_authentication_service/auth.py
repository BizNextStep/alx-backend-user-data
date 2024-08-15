#!/usr/bin/env python3
"""
Auth module
This module provides authentication functionalities including user registration,
session management, and password reset.
"""

from db import DB
from user import User
import uuid

class Auth:
    """Auth class to interact with the authentication database."""

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
        existing_user = self._db._session.query(User).filter_by(email=email).first()
        if existing_user:
            raise ValueError(f"User {email} already exists.")

        hashed_password = self._hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def _hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password.
        """
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from the session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User: The corresponding User object or None if not found.
        """
        if session_id is None:
            return None
        return self._db._session.query(User).filter_by(session_id=session_id).first()

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for a user.

        Args:
            user_id (int): The ID of the user whose session will be destroyed.
        """
        user = self._db._session.query(User).filter_by(id=user_id).first()
        if user:
            user.session_id = None
            self._db._session.commit()

    def create_session(self, email: str) -> str:
        """Create a session for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            session_id = str(uuid.uuid4())
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If the user does not exist.
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if not user:
            raise ValueError("User does not exist.")
        
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db._session.commit()
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update the user's password using a reset token.

        Args:
            reset_token (str): The reset token.
            new_password (str): The new password.
        """
        user = self._db._session.query(User).filter_by(reset_token=reset_token).first()
        if user:
            user.hashed_password = self._hash_password(new_password)
            user.reset_token = None  # Clear the reset token
            self._db._session.commit()
        else:
            raise ValueError("Invalid reset token.")
