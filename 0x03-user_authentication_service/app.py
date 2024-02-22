#!/usr/bin/env python3
"""A Flask application for user authentication."""
from flask import Flask, jsonify, request, abort
from auth import Authenticator as Auth

app = Flask(__name__)
authentication = Auth()


@app.route('/', methods=['GET'])
def welcome():
    """Welcome message endpoint."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        authentication.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if authentication.verify_login(email, password):
            session_id = authentication.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response, 200
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/profile', methods=['GET'])
def get_profile():
    """User profile endpoint."""
    try:
        session_id = request.cookies.get('session_id')
        user = authentication.get_user_from_session(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """User logout endpoint."""
    try:
        session_id = request.cookies.get('session_id')
        user = authentication.get_user_from_session(session_id)
        if user:
            authentication.end_session(user.id)
            return jsonify({"message": "logged out"}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_token():
    """Get reset password token endpoint."""
    try:
        email = request.form.get('email')
        token = authentication.get_reset_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update password endpoint."""
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        authentication.update_password(email, reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
