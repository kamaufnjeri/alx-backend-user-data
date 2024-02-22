#!/usr/bin/env python3
"""Flask app for user authentication and session services
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcom() -> str:
    """GET method welcome page
    """
    return jsonify({"message": "Bienvenue"})

