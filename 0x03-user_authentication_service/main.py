#!/usr/bin/env python3
"""
Main module for interacting with the user authentication service.
"""

import requests

AUTH_SERVER = 'http://localhost:5000'  # Assuming authentication server is running locally


def register_user(email: str, password: str) -> None:
    """Registers a new user."""
    response = requests.post(f'{AUTH_SERVER}/register', json={'email': email, 'password': password})
    assert response.status_code == 201, f"Failed to register user: {response.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with wrong password."""
    response = requests.post(f'{AUTH_SERVER}/login', json={'email': email, 'password': password})
    assert response.status_code == 403, "Expected login to fail with wrong password"


def log_in(email: str, password: str) -> str:
    """Logs in a user and returns session ID."""
    response = requests.post(f'{AUTH_SERVER}/login', json={'email': email, 'password': password})
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    return response.json()['session_id']


def profile_unlogged() -> None:
    """Checks profile of unlogged user."""
    response = requests.get(f'{AUTH_SERVER}/profile')
    assert response.status_code == 403, "Expected profile access to fail for unlogged user"


def profile_logged(session_id: str) -> None:
    """Checks profile of logged-in user."""
    headers = {'session_id': session_id}
    response = requests.get(f'{AUTH_SERVER}/profile', headers=headers)
    assert response.status_code == 200, f"Failed to access profile: {response.text}"


def log_out(session_id: str) -> None:
    """Logs out the user."""
    headers = {'session_id': session_id}
    response = requests.delete(f'{AUTH_SERVER}/logout', headers=headers)
    assert response.status_code == 200, f"Failed to log out: {response.text}"


def reset_password_token(email: str) -> str:
    """Requests a password reset token."""
    response = requests.post(f'{AUTH_SERVER}/reset_password', json={'email': email})
    assert response.status_code == 200, f"Failed to get reset token: {response.text}"
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates password using reset token."""
    data = {'email': email, 'reset_token': reset_token, 'new_password': new_password}
    response = requests.put(f'{AUTH_SERVER}/reset_password', json=data)
    assert response.status_code == 200, f"Failed to update password: {response.text}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
