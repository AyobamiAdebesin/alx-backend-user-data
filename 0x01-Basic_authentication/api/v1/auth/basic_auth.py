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

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeError('User'):
        """
        Create user object from credentials passed
        extracted from the header
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
        # if user_email is None or type(user_email) != str:
        #     return None
        # if user_pwd is None or type(user_pwd) != str:
        #     return None
        # if User.count() == 0:
        #     return None
        # else:
        #     try:
        #         users = User.search({"email": user_email})
        #     except Exception:
        #         return None
        #     if len(users) <= 0:
        #         return None
        #     elif users[0].is_valid_password(user_pwd):
        #         return users[0]
        #     else:
        #         return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user """
        if self.authorization_header(request):
            auth_header = self.authorization_header(request)
            base64_auth = self.extract_base64_authorization_header(
                auth_header)
            decoded_base64_auth = self.decode_base64_authorization_header(
                base64_auth)
            credentials = self.extract_user_credentials(
                decoded_base64_auth)
            user_obj = self.user_object_from_credentials(
                user_email=credentials[0],
                user_pwd=credentials[1])
            return user_obj
        else:
            return None
