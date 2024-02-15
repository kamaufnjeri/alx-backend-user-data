#!/usr/bin/env python3
"""new view for session_auth login"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def auth_session_login():
    """post method to retrieve email and password to login user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})

    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)

            SESSION_NAME = os.getenv("SESSION_NAME")
            resp = jsonify(user.to_json())

            resp.set_cookie(SESSION_NAME, session_id)

            return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    "/auth_session/logout",
    methods=["DELETE"],
    strict_slashes=False
)
def logout_user():
    """logout user route"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)

    if destroy is False:
        abort(404)

    return jsonify({}), 200
