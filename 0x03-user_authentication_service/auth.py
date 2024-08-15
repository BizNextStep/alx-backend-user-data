#!/usr/bin/env python3
"""
Auth module
This module provides authentication functionalities including password hashing.
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
