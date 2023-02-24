#!/usr/bin/env python3
""" Basic Authentication """
import base64
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
            return
        if not isinstance(decoded_base64_authorization_header, str):
            return
        if ":" not in decoded_base64_authorization_header:
            return
        return tuple(decoded_base64_authorization_header.split(":"))
