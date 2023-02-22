#!/usr/bin/env python3
""" Flask App """
from flask import Flask
from flask import jsonify, request, abort, redirect
from flask import make_response
from flask import url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def test_flask():
    """ Create a basic flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def register_users():
    """ Registers a user """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    else:
        return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """ Login functionality """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is True:
        get_sess_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", get_sess_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout_user():
    """ Log out a user """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def get_profile():
    """ Route to the profile page """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
