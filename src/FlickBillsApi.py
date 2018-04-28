# encoding: utf-8
"""
API Interface Module
"""

import json
import time
from calendar import timegm
import requests
from src.FlickAuth import FlickAuth
from src import util
from src import definitions


class FlickBillsApi(object):
    """ Flick Electric API Interface """

    def __init__(self, username, password, client_id, client_secret):
        self.data = None
        auth_instance = FlickAuth(username, password, client_id, client_secret)
        self.session = auth_instance.get_token()
        self.get_raw_data(True)

    def update(self, write_to_file=False):
        """ Pull Updates From Flick Servers"""

        print("getting the latest bill")
        headers = {
            "Authorization": "Bearer %s" % self.session["id_token"]
        }
        req = requests.get(definitions.FLICK_BILLS_ENDPOINT, headers=headers)
        if req.status_code is not 200:
            # If we don't get a success response, we raise an exception.
            raise Exception({
                "status": req.status_code,
                "message": req.text
            })
        # A 200OK response will contain the JSON payload.
        # TODO: Create Exception Handler to catch failed json.load.
        response = json.loads(req.text)
        response['updatetime'] = int(time.time())
        if write_to_file is True:
            util.save_json_file(definitions.FLICK_BILLS_DATA_STORE, response)
        self.data = response
        return response

    def expired(self):
        return int(time.time()) - self.data['updatetime'] > 86400


    @staticmethod
    def convert_time(update, is_epoch):
        """ Gets the prev/next update time """
        if is_epoch is True:
            utc_time = time.strptime(update, "%Y-%m-%dT%H:%M:%SZ")
            epoch = timegm(utc_time)
            return epoch
        return update

    def get_raw_data(self, write_to_file=False):
        """ Public method to get bills data """
        self.data = util.get_json_file(definitions.FLICK_BILLS_DATA_STORE)
        if not self.data:
            self.data = self.update(write_to_file)
        expired = self.expired()
        if expired is True:
            self.data = self.update(True)
        return self.data

    def get_current_period(self):
        """ Get's the pure price per kwh as a number"""
        return self.data["current_period"]

    def get_total_savings(self):
        """ Get the price, broken down into it's constituent parts"""
        return self.data["total_savings"]

    def get_last_bill(self, is_epoch=False):
        return self.data["latest_bill"]

    def get_data(self):
        return self.data
