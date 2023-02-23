#!/usr/bin/env python3
""" Authentication Module """
from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """ Authentication class for the API """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Requires authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """ Returns current user """
        return None
