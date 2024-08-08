#!/usr/bin/env python3
"""
Definition of the SessionAuth class.
This class provides the foundation for session-based authentication.
"""

from .auth import Auth
from models.user import User
from uuid import uuid4  # Importing uuid4


class SessionAuth(Auth):
    """ Implements Session Authentication protocol methods. """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user with the provided user_id.

        Args:
            user_id (str): The ID of the user to create a session for.

        Returns:
            str: A session ID if user_id is valid, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on the provided session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID, or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance associated with the session ID from the request.

        Args:
            request: The Flask request object containing the session cookie.

        Returns:
            User: The user instance associated with the session, or None if not found.
        """
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the session associated with the provided request.

        Args:
            request: The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully deleted, otherwise False.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        if session_cookie not in self.user_id_by_session_id:
            return False  # Check if the session exists
        del self.user_id_by_session_id[session_cookie]
        return True
