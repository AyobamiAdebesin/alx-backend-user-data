#!/usr/bin/env python3
""" Encrypting a password with an hash function """
from bcrypt import hashpw, gensalt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hashing a password with bcrypt """
    # Encode password before hashing
    pwd_bytes = password.encode('utf-8')
    # Generate salt for hashing
    salt = gensalt()
    # return hashed password
    return hashpw(pwd_bytes, salt)


class Auth:
    """ Auth class to interact with the authentication database """
    def __init__(self):
        """ Initializes the database """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user in the database """
        # Check if user exists in the database
        get_user = self._db.find_user_by(email=email, password=password)
        if get_user is not None:
            raise ValueError(f"User {email} already exists")
        else:
            # Hash the password
            user_hashed_pwd = _hash_password(password=password)
        # Add the user into the database 
        user = self._db.add_user(email=email, hashed_password=user_hashed_pwd)
        return user
