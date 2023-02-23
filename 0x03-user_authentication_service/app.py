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
def users():
    """
    Registers a user and add the user to the database
    and return a message to the client if the operation
    was successful or not.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    else:
        return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Login functionality

    This end point authenticates a user with AUTH.valid_login().

    If true, we create a session id token for that user with
    AUTH.create_session() and update the user profile in the database
    with the session_id. The server now sends this session_id token
    back to the client in form of a cookie.

    If false, we return a 401 status code(unauthorized request)
    """
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
def logout():
    """Logout functionality

    This endpoint receives a session_id token from the request
    in form of a token and search for the user in the database
    using this token with AUTH.get_user_from_session_id(session_id).

    If such user exists, we destroy the session with
    AUTH.destroy_session(user_id) byupdating the session_id attribute
    of that user to None in the database. Then we redirect the user
    to the homepage.

    Else, we abort and return a 403 status code.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """
    Route to the profile page

    This endpoint gets the session_id token of a user
    from the client request in form of a token and uses this
    token to get the corresponding user from the database with
    AUTH.get_user_from_session_id(session_id) and returns a
    json payload containing the user email.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """
    Reset password

    This endpoint receives an email of a user and calls
    the AUTH.get_reset_password_token(email) to generate a
    password reset token. This token is returned to the client
    in a json payload
    """
    email = request.form.get('email')
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
    Update a user's password

    This endpoint receives the email, reset_token that was returned
    by the reset_password(POST) endpoint, and the new password of the
    user. It then uses the AUTH.update_password(reset_token, new_password)
    to update the user's password in the database and returns the email
    and new password in a json payload to the client.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
