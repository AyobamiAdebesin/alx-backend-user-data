#!/usr/bin/env python3
""" Basic Authentication """
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
