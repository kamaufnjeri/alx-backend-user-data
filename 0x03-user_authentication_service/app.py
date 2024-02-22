#!/usr/bin/env python3
"""A simple Flask app with user authentication features."""
from flask import Flask, jsonify, request, abort
from auth import Auth as A

app = Flask(__name__)
AUTH = A()


@app.route('/', methods=['GET'])
def home():
    """Endpoint to welcome users"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """Endpoint to register a user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Endpoint to log in"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response, 200
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/profile', methods=['GET'])
def get_profile():
    """Endpoint to get user profile"""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Endpoint to log out"""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return jsonify({"message": "logged out"}), 200
        else:
            abort(403)
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Endpoint to get reset password token"""
    try:
        email = request.form.get('email')
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Endpoint to update password"""
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        AUTH.update_password(email, reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
