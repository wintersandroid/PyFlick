# encoding: utf-8
"""
API Interface Module
"""

import json
import time
from calendar import timegm
import requests
from FlickAuth import FlickAuth
import util
import definitions


class FlickPriceApi(object):
    """ Flick Electric API Interface """

    def __init__(self, username, password, client_id, client_secret):
        self.data = None
        self.had_expired = False
        auth_instance = FlickAuth(username, password, client_id, client_secret)
        self.session = auth_instance.get_token()
        self.get_raw_data(True)

    def update(self, write_to_file=False):
        """ Pull Updates From Flick Servers"""
        self.had_expired = True
        print("getting the latest price")
        headers = {
            "Authorization": "Bearer %s" % self.session["id_token"]
        }
        req = requests.get(definitions.FLICK_PRICE_ENDPOINT, headers=headers)
        if req.status_code is not 200:
            # If we don't get a success response, we raise an exception.
            raise Exception({
                "status": req.status_code,
                "message": req.text
            })
        # A 200OK response will contain the JSON payload.
        # TODO: Create Exception Handler to catch failed json.load.
        response = json.loads(req.text)
        if write_to_file is True:
            util.save_json_file(definitions.FLICK_PRICE_DATA_STORE, response)
        self.data = response
        return response

    def price_expired(self):
        """ Checks if spot price has expired """
        now_epoch = int(time.time())
        next_epoch = self.get_next_update_time(True)
        # print "%d" % nextEpoch
        # print "%d" % nowEpoch
        return next_epoch < now_epoch

    def price_had_expired(self):
        return self.had_expired

    @staticmethod
    def get_update_time(update, is_epoch):
        """ Gets the prev/next update time """
        if is_epoch is True:
            utc_time = time.strptime(update, "%Y-%m-%dT%H:%M:%SZ")
            epoch = timegm(utc_time)
            return epoch
        return update

    def get_raw_data(self, write_to_file=False):
        """ Public method to get pricing data """
        self.data = util.get_json_file(definitions.FLICK_PRICE_DATA_STORE)
        if not self.data:
            self.data = self.update(write_to_file)
        else:
          self.had_expired = self.price_expired()
          if self.had_expired is True:
              self.data = self.update(True)
        return self.data

    def get_price_per_kwh(self):
        """ Get's the pure price per kwh as a number"""
        return self.data["needle"]["price"]

    def get_price_breakdown(self):
        """ Get the price, broken down into it's constituent parts"""
        charges = {}

        for item in self.data["needle"]["components"]:
            value = float(item["value"])
            if item["charge_method"] == "kwh":
                if value != 0:
                    charges[item["charge_setter"]] = value
            elif item["charge_method"] == "spot_price":
                charges["spot_price"] = value

        return charges

    def get_last_update_time(self, is_epoch=False):
        return self.get_update_time(self.data["needle"]["start_at"], is_epoch)

    def get_next_update_time(self, is_epoch=False):
        return self.get_update_time(self.data["needle"]["end_at"], is_epoch)
