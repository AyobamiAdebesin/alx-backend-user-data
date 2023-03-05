#!/usr/bin/env python3
""" Session Expiration Authentication """
import os
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Adding expiration to Session Authentication """

    def __init__(self):
        """ Overloads and initializes attributes """
        if getenv('SESSION_DURATION') is not None:
            session_duration = int(getenv('SESSION_DURATION'))
        else:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ Creates a session """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ Overloads this method for the SessionAuth class """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get('created_at')
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")
