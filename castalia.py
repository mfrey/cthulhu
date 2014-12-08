#!/usr/bin/env python2.7

import os

from subprocess import call

from os.path import normpath, basename, expanduser

import sys
import argparse

from configuration.configuration import Configuration

class Castalia(object):
    def __init__(self, configuration, input_file, castalia_installation):
        self.castalia_installation = castalia_installation
        self.binary = self.castalia_installation + "/bin/Castalia"
        self.cwd = os.getcwd()
        self.configuration = configuration
        self.input_file = input_file
        self.networks = False

        if os.path.exists(self.binary) == False:
            raise Exception("The castalia binary could not be found at " + self.binary)

        self.log_file_path = self.cwd + '/' + self.configuration + '-Log.txt'

    def run(self):
        environment = dict(os.environ)
        # probably, a bit to complicated
        file_to_split =  basename(normpath(self.input_file))
        cwd = self.input_file.split("/" + file_to_split)[0]

        if self.binary.endswith("Castalia"):
            # DEBUG: print(self.binary + " -i " + self.input_file + " -c " + self.configuration)
            with open(self.log_file_path, 'w') as logfile:
                call([self.binary, "-i", self.input_file, "-c", self.configuration], env=environment, cwd=cwd, stdout=logfile, stderr=logfile)
        else:
            # DEBUG: print(self.binary + " -i " + self.input_file + " -s \"" + self.configuration + "\" -o 2")
            with open(self.log_file_path, 'w') as logfile:
                #call([self.binary, "-i", self.input_file, "-s",  "\"", self.configuration, "\"", "-o", "2"], env=environment, cwd=cwd, stdout=logfile, stderr=logfile)
                if self.networks:
                    call([self.binary, "-i", self.input_file, "-s", self.configuration, "-n", "-o", "2"], env=environment, cwd=cwd, stdout=logfile, stderr=logfile)
                else:
                    call([self.binary, "-i", self.input_file, "-s", self.configuration, "-o", "2"], env=environment, cwd=cwd, stdout=logfile, stderr=logfile)

def main():
     parser = argparse.ArgumentParser(description='a script for running castalia simulations')
     parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='an ini file specifying the location of castalia')
     parser.add_argument('-s', dest='castalia_configuration', type=str, default="", action='store', help='a castalia configuarion to run')
     parser.add_argument('-i', dest='omnetpp_ini', type=str, default="omnetpp.ini", action='store', help='omnetpp.ini file which should be considered')

     if len(sys.argv) == 1:
         parser.print_help()
         sys.exit(1)

     arguments = parser.parse_args()
     configuration = Configuration(arguments.configuration)

     if arguments.castalia_configuration != "" and arguments.omnetpp_ini != "":
         castalia = Castalia(arguments.castalia_configuration, arguments.omnetpp_ini, configuration.settings["castalia_home"])
         castalia.run()


if __name__ == "__main__":
    main()

