#!/usr/bin/env python3
""" A Session Authentication class """
from .auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if type(session_id) == str:
            for k in self.user_id_by_session_id:
                if k == session_id:
                    return self.user_id_by_session_id.get(k)
        else:
            return

    def current_user(self, request=None) -> User:
        """ Returns current user after authentication """
        if request:
            get_session_id_from_cookie = self.session_cookie(request)
            if get_session_id_from_cookie is not None and \
                    get_session_id_from_cookie in SessionAuth().user_id_by_session_id:
                get_user_id = self.user_id_by_session_id(
                    get_session_id_from_cookie)
                user = User.get(get_user_id)
                return user
            else:
                return
        return
