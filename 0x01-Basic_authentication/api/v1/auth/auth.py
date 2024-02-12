#!/usr/bin/env python3
"""Auth class created"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage api authentications"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
