#!/usr/bin/env python2.7

import os
from subprocess import call

import sys
import argparse

class Castalia(object):
    def __init__(self, configuration, castalia_installation = "/home/frey/Desktop/Projekte/work/sics/SemInt/Castalia-master/Castalia/", input_file="omnetpp.ini"):
        self.castalia_installation = castalia_installation
        self.binary = self.castalia_installation + '/bin/Castalia'
        self.cwd = os.getcwd()
        self.configuration = configuration
        self.input_file = input_file

        if os.path.exists(self.binary) == False:
            raise Exception("The castalia binary could not be found at " + self.binary)

        self.log_file_path = self.cwd + '/' + self.configuration + '-Log.txt'

    def run(self):
        environment = dict(os.environ)

        if self.binary.endswith("Castalia"):
            with open(self.log_file_path, 'w') as logfile:
                call([self.binary, "-i", self.input_file, "-c", self.configuration], env=environment, cwd=self.cwd, stdout=logfile, stderr=logfile)
        else:
            with open(self.log_file_path, 'w') as logfile:
                call([self.binary, "-i", self.input_file, "-s", self.configuration, "-o", "2"], env=environment, cwd=self.cwd, stdout=logfile, stderr=logfile)

def main():
     parser = argparse.ArgumentParser(description='a script for running castalia simulations')
     parser.add_argument('-r', '--run', dest='run', default=False, const=True, action='store_const', help='run simulations')
     parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a castalia configuarion to run')
     parser.add_argument('-i', dest='omnetpp_ini', type=str, default="omnetpp.ini", action='store', help='omnetpp.ini file which should be considered')

     if len(sys.argv) == 1:
         parser.print_help()
         sys.exit(1)

     arguments = parser.parse_args()

     if arguments.run == True:
         castalia = Castalia(arguments.configuration, arguments.omnetpp_ini)
         castalia.run()

if __name__ == "__main__":
    main()

