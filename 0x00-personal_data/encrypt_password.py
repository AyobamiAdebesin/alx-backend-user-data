#!/usr/bin/env python3
""" Password hashing """
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password and returns a byte string
    of the hashed password
    """
    # encode the string into utf-8
    pwd = password.encode('utf-8')

    # generate salt
    salt = bcrypt.gensalt()

    # encrypt encoded string with the salt
    hashed_pwd = bcrypt.hashpw(pwd, salt)
    return hashed_pwd
