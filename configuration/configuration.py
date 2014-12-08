#!/usr/bin/env python2.7

from os import path
from configparser import ConfigParser, NoSectionError, NoOptionError

class Configuration(object):
    def __init__(self, file_name):

        if(file_name is not None):
            self.parser = ConfigParser()
            self.parser.read(file_name)

            self.settings = {
                'castalia_home': self._get_absolute_path(self._get('General', 'castalia_home')),
            }

        else:
            self.settings = {}

    def _get_absolute_path(self, some_path):
        return path.abspath(path.expanduser(some_path))
