#!/usr/bin/env python3
"""
Module for encrypting passwords using bcrypt.
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the salted, hashed password as a byte string.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

