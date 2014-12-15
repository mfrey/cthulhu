#!/usr/bin/env python2.7

from os import path
import ConfigParser

class Configuration(object):
    def __init__(self, file_name):

        if(file_name is not None):
            self.parser = ConfigParser.ConfigParser()
            self.parser.read(file_name)

            self.settings = {
                'castalia_home': self._get_absolute_path(self._get('General', 'castalia_home')),
                'scenario_home': self._get_absolute_path(self._get('General', 'scenario_home')),
            }

        else:
            self.settings = {}

    def _get_absolute_path(self, some_path):
        return path.abspath(path.expanduser(some_path))

    def _get(self, section, option):
        return  self.parser.get(section, option)
