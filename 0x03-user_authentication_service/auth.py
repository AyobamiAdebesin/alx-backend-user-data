#!/usr/bin/env python3
""" Encrypting a password with an hash function """
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashing a password with bcrypt """
    # Encode password before hashing
    pwd_bytes = password.encode('utf-8')
    # Generate salt for hashing
    salt = gensalt()
    # return hashed password
    return hashpw(pwd_bytes, salt)


def _generate_uuid() -> str:
    """
    Generating a unique ID and returns a string
    representation of the ID
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database """
    def __init__(self):
        """ Initializes the database """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user in the database """
        # Check if user exists in the database with their email
        # email suffices to check if a user exists or not
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            # Hash the password
            user_hashed_pwd = _hash_password(password=password)
            # Add the user into the database
            user = self._db.add_user(email, user_hashed_pwd)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate credentials of a user before log in """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return (checkpw(password.encode('utf-8'), user.hashed_password))
