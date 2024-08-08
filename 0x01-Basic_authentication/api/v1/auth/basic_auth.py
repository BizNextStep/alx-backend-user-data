#!/usr/bin/env python3
"""
BasicAuth module for handling Basic Authentication.
"""

import re
import base64
import binascii
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User

class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth for managing Basic Authentication.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 encoded part of the Authorization header if valid, otherwise None.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The base64-encoded authorization header.

        Returns:
            str: The decoded value of the Base64 part of the Authorization header if valid, otherwise None.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user credentials from a base64-decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 part of the Authorization header.

        Returns:
            Tuple[str, str]: The user's email and password as a tuple, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) == 2:
            return credentials[0], credentials[1]
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a user based on the user's authentication credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User object if authentication is successful, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users or not users[0].is_valid_password(user_pwd):
                return None
            return users[0]
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the user from a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated user, or None if authentication fails.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)

