# encoding: utf-8
""" Utility Class"""

import json
import os


def save_json_file(filepath, data):
    """ Saves JSON Data to File"""
    with open(filepath, 'w') as outfile:
        try:
            json.dump(data, outfile, indent=2)
        except ValueError:
            return False
        return True


def get_json_file(filepath):
    """ Get Data from cached file """
    if not os.path.exists(filepath):
        return None
    with open(filepath) as stream:
        try:
            return json.load(stream)
        except ValueError:
            return None
