#!/usr/bin/env python3
""" Authentication Module """
from flask import Flask, request
from typing import List, TypeVar
import re


class Auth:
    """ Authentication class for the API """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks which routes don't need authentication

        Returns True if path is None,
        Returns True if excluded_paths is None or empty
        Returns False if path is in excluded_paths

        excluded_paths contains string path always ending by a "/"
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True
        # slash_tolerant = "/"
        # if path is None or excluded_paths is None or\
        # len(excluded_paths) == 0:
        #     return True
        # if path:
        #     if path.endswith("/"):
        #         if path in excluded_paths:
        #             return False
        #         elif path not in excluded_paths:
        #             return True
        #     else:
        #         path_slash = path+slash_tolerant
        #         if path in excluded_paths or path_slash in excluded_paths:
        #             return False
        #         elif path not in excluded_paths:
        #             return True
        # else:
        #     return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header key in the request
        If the Authorization header key does not exist, return None
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """ Returns current user for a request """
        return None
