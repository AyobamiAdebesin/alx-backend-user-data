#!/usr/bin/env python3
""" Views for handling Session authentication routes """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from typing import Any


@app_views.route("/auth_session/login", strict_slashes=False, methods=['POST'])
def login() -> Any:
    """ Login functionality """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if user_password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": user_email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    elif len(user) > 0 and users[0].is_valid_password(user_password) is False:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        sess_id = auth.create_session()
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), sess_id)
        return response
