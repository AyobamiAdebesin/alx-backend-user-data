#!/usr/bin/env python3
""" Encrypting a password with an hash function """
from bcrypt import hashpw,gensalt


def _hash_password(password: str) -> bytes:
    """ Hashing a password with bcrypt """
    #Encode password before hashing
    pwd_bytes = password.encode('utf-8')
    salt = gensalt()
    return hashpw(pwd_bytes, salt)
