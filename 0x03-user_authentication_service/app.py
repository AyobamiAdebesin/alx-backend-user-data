#!/usr/bin/env python3
""" Flask App """
from flask import Flask
from flask import jsonify, request, abort, redirect
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
