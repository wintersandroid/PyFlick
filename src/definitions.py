# encoding: utf-8
"""
Global Constant Definition Module
"""

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
AUTH_FILE_PATH = os.path.join(ROOT_DIR, 'auth.json')

FLICK_OAUTH_ENDPOINT = "https://api.flick.energy/identity/oauth/token"
FLICK_PRICE_ENDPOINT = "https://api.flick.energy/customer/mobile_provider/price"
FLICK_BILLS_ENDPOINT = "https://api.flick.energy/customer/mobile_provider/bills"
FLICK_PRICE_DATA_STORE = os.path.join(ROOT_DIR, 'pricing.json')
FLICK_BILLS_DATA_STORE = os.path.join(ROOT_DIR, 'bills.json')
