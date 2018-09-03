#!/usr/bin/env python
# encoding: utf-8
"""
Main Module
"""

from FlickPriceApi import FlickPriceApi
from FlickBillsApi import FlickBillsApi
from config import Config


def main():
    """ Main, nuff said """
    config = Config().get()
    api = FlickPriceApi(config["username"], config["password"], config["client_id"], config["client_secret"])
    # Returns Price Per KwH
    print api.get_price_per_kwh()
    # Returns dict with Charges and price
    print api.get_price_breakdown()
    # Get last updated timestamp
    print api.get_last_update_time()
    # Get last updated timestamp as seconds since epoch
    print api.get_last_update_time(True)
    # Get next update timestamp
    print api.get_next_update_time()
    # Get next update timestamp as seconds since epoch
    print api.get_next_update_time(True)

    api = FlickBillsApi(config["username"], config["password"], config["client_id"], config["client_secret"])
    print("Bills data", api.get_data())

if __name__ == "__main__":
    main()
