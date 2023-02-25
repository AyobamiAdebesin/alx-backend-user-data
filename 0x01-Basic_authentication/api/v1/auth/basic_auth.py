#!/usr/bin/env python3
""" Basic Authentication """
import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication inherits from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the contents of the authorization header """
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if not authorization_header.startswith('Basic '):
            return
        else:
            return authorization_header.split("Basic ")[-1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Decode the credentials """
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            decoded_data = base64.b64decode(base64_authorization_header)
        except Exception:
            return
        else:
            return decoded_data.decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Extract credentials """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeError('User'):
        """ Create user object from credentials passed extracted from header """
        if user_email is None or type(user_email) or type(user_email) != str:
            return
        if user_pwd is None or type(user_pwd) != str:
            return
        if User.count() == 0:
            return
        if len(User.search({"email": user_email})) == 0:
            return None
        else:
            user = User.search({"email": user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
            else:
                return
