# encoding: utf-8
"""
Configuration Module
"""

from src import definitions
from src import util


# noinspection PyMethodMayBeStatic
class Config(object):
    """
    Class to handle configuration file
    """

    def __init__(self):
        pass

    def get(self):
        """
        Retrieve config from file
        """
        return util.get_json_file(definitions.CONFIG_PATH)

    def save(self, config_object):
        """
        Save config to file
        """
        return util.save_json_file(definitions.CONFIG_PATH, config_object)
