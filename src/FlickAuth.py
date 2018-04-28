# encoding: utf-8
"""
Authentication Module
"""

import json
import time
import requests
from src import definitions
from src.exceptionHandler import AuthException
from src import util


class FlickAuth(object):
    """
    Class to handle authentication/token generation
    """

    def __init__(self, username, password, client_id, client_secret):
        """
        Initialize and get an authentication token
        """
        token = self.check_active_session()
        if not token:
            self.token = self.authenticated_flick(username, password, client_id, client_secret)
        else:
            self.token = token

    # noinspection PyMethodMayBeStatic
    def check_active_session(self):
        """
        Check for an active session and return it if it exists
        """
        token = util.get_json_file(definitions.AUTH_FILE_PATH)
        if not token:
            return False
        now = int(time.time())
        if now < token["expires_at"]:
            return token

    # noinspection PyMethodMayBeStatic
    def save_access_token_file(self, data):
        """
        Save the access token to file
        """
        data["authenticated_at"] = int(time.time())
        # FYI: Tokens appear to expire in 2 months/60 days
        data["expires_at"] = data["authenticated_at"] + data["expires_in"]
        return util.save_json_file(definitions.AUTH_FILE_PATH, data)

    def authenticated_flick(self, username, password, client_id, client_secret):
        """
        HTTPS Auth method
        """
        payload = {
            "grant_type": "password",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        req = requests.post(definitions.FLICK_OAUTH_ENDPOINT, data=payload, headers=headers)
        if req.status_code is not 200:
            # If we don't get a success response, we raise an exception.
            raise AuthException({
                "status": req.status_code,
                "message": req.text
            })
        # A 200OK response will contain the JSON payload.
        response = json.loads(req.text)
        self.save_access_token_file(response)
        return response

    def get_token(self):
        """ Returns the token"""
        return self.token
