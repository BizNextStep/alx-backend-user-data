#!/usr/bin/env python3
"""Auth class
This module defines the Auth class for handling user authentication, including registration,
login, session management, and password reset functionality.
"""

from db import DB
from typing import TypeVar
from user import User
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """
    _hash_password function.
    Hashes a given password using bcrypt and returns the hashed password.

    Args:
        password (str): The password to hash.
    
    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    _generate_uuid function.
    Generates a new UUID and returns it as a string.

    Returns:
        str: A newly generated UUID.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    This class provides methods for user registration, login validation,
    session management, and password reset functionality.
    """

    def __init__(self):
        """Constructor method.
        Initializes an instance of the Auth class with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user method.
        Registers a new user with the specified email and password.

        Args:
            email (str): The email address
