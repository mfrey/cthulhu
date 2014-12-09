#!/usr/bin/env python2.7

import sys
import argparse

import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class CastaliaTraceParser:
    def __init__(self):
        self.results = {}

    def read(self, filename):
        counter = 0
        rate = -1

        with open(filename, "r") as filehandle:
            for line in filehandle:
                if "packet rate is" in line:
                    counter += 1

                    if counter == 3:
                       rate = float(line.split(" ")[-1])
                       self.results[rate] = {}
                       counter = 0
                       print(".")

                else:
                    self._parse_line(line, rate)


    def _parse_line(self, line, rate):
        if "Received packet" in line:
            node = int(line.split("SN.node[")[1].split("]")[0])
            timestamp = float(line.split("SN")[0])
            seqnr = int(line.split(" ")[-4][1:])

            if node not in self.results[rate].keys():
                self.results[rate][node] = {}

            self.results[rate][node][timestamp] = seqnr


    def plot(self, flag=False, start=0, stop=0, file_name="arrival_plot-"):
        for rate in sorted(self.results.keys(), key=int):
            xlist = []
            ylist = []

            for node in self.results[rate].keys():
                xdata = []
                ydata = []

                if start == 0 and stop == 0:
                   start, stop = min(self.results[rate][node]), max(self.results[rate][node]) 

                for timestamp in sorted(self.results[rate][node], key=float): 
                    # add check for sane intervals
                    if timestamp >= start and timestamp <= stop:
                        xdata.append(timestamp)

                        if flag:
                            ydata.append(node)
                        else:
                            ydata.append(self.results[rate][node][timestamp])

                xlist.append(xdata)
                ylist.append(ydata)

            current_filename = file_name + "_" + str(rate) + ".png"
            title = "Packet Arrival Time"
            figure, axis = plt.subplots(1)

#            fig = matplotlib.pyplot.gcf()
#            fig.set_size_inches(38.5,10.5)

            for index, value in enumerate(xlist):
                if len(xlist) > 1:
                    plt.plot(value, ylist[index], linestyle=' ', marker='o', label="PAN$_"+str(index)+"$")
                    #plt.plot(value, ylist[index], drawstyle="line", lw=2.5, label="PAN$_"+str(index)+"$")
                    if flag:
                        plt.yticks([-1, 0,1,2])
                        plt.ylabel("Network")
                    else:
                        plt.ylabel("Squence Number")
                else:
                    plt.plot(value, ylist[index], drawstyle="line", lw=2.5, color="#003366")

#            plt.xticks(np.arange(min(xdata), max(xdata)+1, 0.5))
#            plt.yticks(np.arange(min(ydata)-1, max(ydata)+1, 0.5))
            #axis.set_title(title)
            #axis.set_xlabel(xlabel)
            #axis.set_ylabel(ylabel)
            plt.xlabel("Time")
            plt.legend(loc=0)
            axis.grid()
            figure.savefig(current_filename, dpi=100)
            plt.close()




def main():
    parser = argparse.ArgumentParser(description='a script for evaluating castalia trace files')
    parser.add_argument('-f', '--file', dest='trace', type=str, default="", action='store', help='a castalia trace file to evaluate')
    parser.add_argument('-t', dest='timestamps', type=str, default="", action='store', help='a beginning and ending timestamp for evaluating the trace file, e.g. 0.5,1.0')
    parser.add_argument('-r', dest='rate', type=str, default="", action='store', help='analyze only a specific rate')
    # TODO: find a better name
    parser.add_argument('-d', dest='dots', default=False, const=True, action='store_const', help='enable dots figure')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    arguments = parser.parse_args()

    if arguments.trace != "":
       trace_parser = CastaliaTraceParser()
       trace_parser.read(arguments.trace)

       if arguments.dots == True:
           file_name = "arrival-rate-dotted"
       else:
           file_name = "arrival-rate"

       # the timestamp should be in a t_0,t_1 format, e.g. 0.5,0.7
       if arguments.timestamps != '':
           start, stop = [float(timestamp) for timestamp in arguments.timestamps.split(",")]
           trace_parser.plot(arguments.dots, start, stop, file_name)
       else:
           trace_parser.plot(arguments.dots)


if __name__ == "__main__":
    main()
