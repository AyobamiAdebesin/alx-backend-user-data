#!/usr/bin/env python3
""" Encrypting a password with an hash function """
from bcrypt import hashpw,gensalt


def _hash_password(self, password: str) -> bytes:
    """ Hashing a password with bcrypt """
    salt = gensalt()
    return hashpw(password, salt)
