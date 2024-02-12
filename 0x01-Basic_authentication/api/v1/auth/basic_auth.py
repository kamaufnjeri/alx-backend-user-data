#!/usr/bin/env python3
"""A class that inherits from Auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import List


class BasicAuth(Auth):
    """Inherits from Auth"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """hat returns the Base64 part of
        the Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None

        if not type(authorization_header) == str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Return decoded data of base64"""

        if base64_authorization_header is None:
            return None

        if not type(base64_authorization_header) == str:
            return None

        try:
            decoded64 = b64decode(base64_authorization_header)
            decoded = decoded64.decode('utf-8')
        except Exception:
            return None

        return decoded

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """return email and from base64 decoded value"""

        if decoded_base64_authorization_header is None:
            return (None, None)

        if not type(decoded_base64_authorization_header) == str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        list_items = decoded_base64_authorization_header.split(":")

        return (list_items[0], list_items[1])
