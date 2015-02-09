#!/usr/bin/env python2.7


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

class Plot:
    def __init__(self, files = ["prr0.dat", "prr1.dat"]):
        self.xdata = []
        self.ydata = []

        for file_name in files:
            with open(file_name, "r") as file_handle:
                data = []
                # line looks likes this:
                #    scalar SN.node[0].Application arrival:count     10160
                for line in file_handle:
                   arrival_count = int(line.split(" ")[-1])
                   data.append(arrival_count)

                self.ydata.append(data)
                size = len(data)
                offset = np.arange(0, 0.25, 0.0001)

                if len(offset) != size:
                    print("mismatch in x data set size. we've made " +
                        str(len(offset)) + " but it is actually " + str(size))

                self.xdata.append(offset)


    def plot(self, filename):
        figure = plt.figure()
        axis = figure.add_subplot(111)
        labels = ['CSMA','CSMA']

        for index, value in enumerate(self.xdata):
            if len(self.xdata) > 1:
                plt.plot(value, self.ydata[index], drawstyle="line", lw=2.5, label=labels[index])
            else:
                plt.plot(value, self.ydata[index], drawstyle="line", lw=2.5, color="#003366")

        title = "Packets Received vs. Beacon Offset (CSMA/CSMA)"
        xlabel = "Beacon Offset"
        ylabel = "Received Packets"

        plt.title(title)
        plt.legend(loc=0)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        plt.grid()

        figure.savefig(filename)
        plt.close()



def main():
    plot = Plot(["prr0.dat","prr1.dat"])
    plot.plot("meh.png")


if __name__ == "__main__":
    main()
