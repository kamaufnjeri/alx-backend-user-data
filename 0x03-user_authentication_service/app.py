#!/usr/bin/env python3
"""A Flask application for user authentication."""
from flask import Flask, jsonify, request, abort
from auth import Authenticator as Auth

app = Flask(__name__)
authentication = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """Endpoint to display a welcome message"""
    return jsonify({"message": "Bienvenue"})
