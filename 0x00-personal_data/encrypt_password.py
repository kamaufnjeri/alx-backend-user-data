#!/usr/bin/env python3
"""Module for password encryption."""
import bcrypt


def encrypt_password(password: str) -> bytes:
    """Encrypts a password using a randomly generated salt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid_password(hashed_password: bytes, password: str) -> bool:
    """Checks if a hashed password matches the provided password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
