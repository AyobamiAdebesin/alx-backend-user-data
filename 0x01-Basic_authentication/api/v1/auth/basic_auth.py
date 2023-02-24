#!/usr/bin/env python3
""" Basic Authentication """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication inherits from Auth """
    super.__init__(Auth)
