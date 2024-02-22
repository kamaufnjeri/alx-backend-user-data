#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
authentication = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> str:
    """GET / welcome route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """ create a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        authentication.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST login user
    """
    email = request.form.get("email"),
    password = request.form.get("password")
    if not authentication.valid_login(email, password):
        abort(401)
    session_id = authentication.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"}), 200
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE logout user
    """
    session_id = request.cookies.get("session_id")
    user = authentication.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    authentication.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def user_profile() -> str:
    """GET user information
    """
    session_id = request.cookies.get("session_id")
    user = authentication.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_token_to_reset_pwd() -> str:
    """POST reset password
    """
    email = request.form.get("email")
    r_token = None
    try:
        r_token = authentication.get_reset_password_token(email)
    except ValueError:
        r_token = None
    if r_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": r_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def password_updated() -> str:
    """PUT reset password
    """
    email = request.form.get("email")
    r_token = request.form.get("reset_token")
    n_password = request.form.get("new_password")
    password_is_changed = False
    try:
        authentication.update_password(r_token, n_password)
        password_is_changed = True
    except ValueError:
        password_is_changed = False
    if not password_is_changed:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
