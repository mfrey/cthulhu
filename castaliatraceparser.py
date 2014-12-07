#!/usr/bin/env python2.7

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

    def plot(self, flag=True):
        for rate in sorted(self.results.keys(), key=int):
            xlist = []
            ylist = []

            for node in self.results[rate].keys():
                xdata = []
                ydata = []

                for timestamp in sorted(self.results[rate][node], key=float): 
                    xdata.append(timestamp)
                    if flag:
                        ydata.append(self.results[rate][node][timestamp])
                    else:
                        ydata.append(node + 1)

                xlist.append(xdata)
                ylist.append(ydata)

            current_filename = "arrival_plot-" + str(rate) + ".png"
            title = "Packet Arrival Time"
            figure, axis = plt.subplots(1)

            fig = matplotlib.pyplot.gcf()
            fig.set_size_inches(38.5,10.5)

            for index, value in enumerate(xlist):
                if len(xlist) > 1:
                    plt.plot(value, ylist[index], drawstyle="line", lw=2.5, label="PAN$_"+str(index)+"$")
                else:
                    plt.plot(value, ylist[index], drawstyle="line", lw=2.5, color="#003366")

#            plt.xticks(np.arange(min(xdata), max(xdata)+1, 0.5))
#            plt.yticks(np.arange(min(ydata)-1, max(ydata)+1, 0.5))
            #axis.set_title(title)
            #axis.set_xlabel(xlabel)
            #axis.set_ylabel(ylabel)
            plt.xlabel("Time")
            plt.ylabel("Squence Number")
            plt.legend(loc=0)
            axis.grid()
            figure.savefig(current_filename, dpi=100)
            plt.close()



def main():
    parser = CastaliaTraceParser()
    parser.read("/home/frey/Desktop/Projekte/work/sics/SemInt/Castalia-master/Castalia/Simulations/802154_interference/Castalia-Trace.txt")
    parser.plot()

if __name__ == "__main__":
    main()
