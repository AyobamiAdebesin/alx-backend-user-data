#!/usr/bin/env python3

""" Main file """

from auth import Auth

auth = Auth()

print(auth.get_user_from_session(session_id="6fd008b8-40bb-4cb8-b69d-796e107ac6c7"))