#!/usr/bin/env python3
"""
Definition of the Auth class.
This module provides methods for handling API authentication,
including path checking, header extraction, and session management.
"""

import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication.

        Args:
            path (str): The URL path to be checked.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path or path.startswith(excluded_path.rstrip('/')):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request object.

        Args:
            request: The Flask request object.

        Returns:
            str: The authorization header if present, None otherwise.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request object.
        (This method should be overridden in a subclass for specific authentication.)

        Args:
            request: The Flask request object.

        Returns:
            User: The user instance associated with the request, or None.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request object.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not present.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)

