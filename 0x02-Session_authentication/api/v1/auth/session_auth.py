#!/usr/bin/env python3
""" A Session Authentication class """
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ A session authentication model """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID given a user_id

        This session id is stored as a key in the user_id_by_session
        dict with the user_id as a value. This is because a user_id can have
        multiple session id
        """
        if type(user_id) == str:
            sess_id = str(uuid4())
            SessionAuth.user_id_by_session_id[sess_id] = user_id
            return sess_id
        else:
            return
