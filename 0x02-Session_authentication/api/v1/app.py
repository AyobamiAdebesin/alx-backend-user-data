#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Any
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE', auth)
if auth_type == 'auth':
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized error """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ User forbidden error """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter_request() -> Any:
    """
    Filter the request to retrive the
    authentication details.

    This function will be triggered before each request
    """
    if auth is None:
        pass
    else:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
            ]
        if auth.require_auth(request.path, excluded_paths):
            pass
            if auth.authorization_header(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
            else:
                request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)