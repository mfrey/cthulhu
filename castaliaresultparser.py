#!/usr/bin/env python2.7

import sys
import numpy as np

import argparse
import itertools

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import os
from subprocess import call

from castalia import Castalia

from os.path import normpath, basename

class CastaliaResultParser:
    def __init__(self):
        self.results = {} 
        self.nodes = [] 
        self.files = []

    def _parse_line(self, line):
        # let's split the line by '|'
        data = line.split('|')
        # well, it's actual data and not a header
        if len(data) > 1:
            # let's filter empty elements and newlines from the list
            data = [element for element in data if len(element) > 0 and element != '\n']

            if data[0] != ' ':
                # let's check if we have multiple parameters
                parameters = data.pop(0).strip().split(',')
                # get the keys
                parameters = [parameter.split('=')[1] for parameter in parameters]
                # our future dict key
                key = ','.join(parameters)

                if key not in self.results.keys():
                    self.results[key] = []

                for value in data:
                    self.results[key].append(float(value))


    def read_breakdown_packets(self, filename):
        self.results = {}
        self.nodes = [] 

        with open(filename, "r") as filehandle:
            for line in filehandle:
                self._parse_line(line)

    def _get_bins(self, bins):
        result = [element[1:-1].split(',') for element in bins]
        result = itertools.chain(*result) 
        result = [int(element) for element in result if element != "inf"]
        result = sorted(list(set(result)), key=int)
        return result

    def plot_histogram(self):
        data = self.prepare_data()
        bins = self._get_bins(self.nodes)

        print("Generating histograms for application latency: ")

        for payload in data.keys():
            for node in data[payload].keys():
                for rate in sorted(data[payload][node],key=int):
                    sys.stdout.write('.')
                    title = "Application Latency (#Nodes: " + node + " Payload: " + payload + " Bytes, Rate: " + rate + ")" 
                    current_filename = "application_latency-" + payload + "_" + node + "_" + rate + ".png"
                    hist_data = [float(element) for element in data[payload][node][rate]]
                    figure, axis = plt.subplots(1)
                    plt.hist(hist_data, bins, color='#003366')
                    plt.title(title)
                    self.files.append(current_filename)
                    figure.savefig(current_filename)
                    plt.close()


    def prepare_data(self):
        data = {}

        for key in self.results.keys():
            payload, rate, node = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      
                   
            if node not in data[payload].keys():
                data[payload][node] = {}

            if rate not in data[payload][node].keys():
                data[payload][node][rate] = []

            data[payload][node][rate] = self.results[key]

        return data

    def plot_breakdown_packets(self):
        data = self.prepare_data()
        print("Generating bar plots for packet breakdown: ")
        # let's generate plots
        for payload in data.keys():
            for node in data[payload].keys():
                rates = [] 
                failed = []
                success = []

                for rate in sorted(data[payload][node],key=int):
                    rates.append(float(rate))
                    failed.append(data[payload][node][rate][0])
                    success.append(data[payload][node][rate][3])

                sys.stdout.write('.')
                title = "Packet Breakdown (#Nodes: " + node + " Payload: " + payload + " Bytes)" 
                self.generate_bar_plot("packets_breakdown_" + payload + "_" + node + ".png", title, rates, [failed, success], "rate", "packets", ['failed','success'])
        print("\n")

    def read_multiple_columns(self, filename):
        self.results = {}
        self.nodes = [] 

        with open(filename, "r") as filehandle:
            for line in filehandle:
                preamble = line.split('|')

                if len(preamble) > 1:
                    if preamble[0] == ' ':
                       preamble.pop(0)
                       self.nodes = [element.split('=')[-1].strip() for element in preamble]

                self._parse_line(line)


    def plot(self, title, filename, xlabel, ylabel):
        data = self.prepare_data()
        nr_of_nodes = -1

        print("Generating line plots for " + title + ": ")

        for payload in data.keys():
            for node in data[payload].keys():
                rates = [] 
                average = []
                minimum = []
                maximum = [] 

                for rate in sorted(data[payload][node],key=int):
                    rates.append(float(rate))
                    average.append(data[payload][node][rate][0])
                    minimum.append(data[payload][node][rate][1])
                    maximum.append(data[payload][node][rate][2])

                sys.stdout.write('.')
                title = "Average Latency (#Nodes: " + node + " Payload: " + payload + " Bytes)" 
                current_filename = filename + "-" + payload + "-" + node + ".png"
                figure, axis = plt.subplots(1)
                axis.plot(rates, average, lw=2, label=title, color='#003366')
                #axis.fill_between(rates, [i + j for i, j in zip(average, maximum)], [i - j for i, j in zip(average, minimum)], facecolor='#003366', alpha=0.5)
                axis.fill_between(rates, maximum, minimum, facecolor='#003366', alpha=0.5)
                axis.set_title(title)
                axis.set_xlabel(xlabel)
                axis.set_ylabel(ylabel)
                axis.grid()
                figure.savefig(current_filename)
                self.files.append(current_filename)
                plt.close()
                print("\n")

    def plot_ext(self, title, filename, xlabel, ylabel):
        data = {} 
        nr_of_nodes = -1

        for key in self.results.keys():
            payload, rate = key.split(',')

            if payload not in data.keys():
                data[payload] = {}      

            if rate not in data[payload].keys():
                data[payload][rate] = {}

            data[payload][rate] = self.results[key]
            # store the number of nodes
            nr_of_nodes = len(self.results[key])

        print("Generating line plots for " + title + ": ")
        # let's generate plots
        for payload in data.keys():
            # we create a new plot for each #nodes 
            for current_node in range(nr_of_nodes):
                rates = []  
                reception_rate = []
                sys.stdout.write('.')
                for rate in sorted(data[payload], key=int):
                    rates.append(rate)
                    reception_rate.append(float(data[payload][rate][current_node]))

                # create the title of the figure
                current_title = title + "(#Nodes = " + self.nodes[current_node] + ", Payload = " + payload + ")" 
                current_filename = filename + "-" + payload + "-" + self.nodes[current_node] + ".png"
                # finally let's plot the reception rate 
                self.generate_line_plot(current_filename, current_title, [rates], [reception_rate], xlabel, ylabel, [])


    def generate_line_plot(self, filename, title, xlist, ylist, xlabel, ylabel, labels): 
        figure = plt.figure()
        axis = figure.add_subplot(111)
        markers = ['s','^','v','2','*','3','d']

        for index, value in enumerate(xlist):
            if len(xlist) > 1:
                plt.plot(value, ylist[index], drawstyle="line", lw=2.5, label=labels[index])
            else:
                plt.plot(value, ylist[index], drawstyle="line", lw=2.5, color="#003366")

        plt.title(title)
        plt.legend()
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        plt.grid()
        plt.savefig(filename)
        self.files.append(filename)

    def generate_line_plot_ext(self, filename, title, xlist, mu, sigma, xlabel, ylabel): 
        figure, axis = plt.subplots(1)
        axis.plot(xlist, mu, lw=2, label=title, color='#003366')
        axis.fill_between(xlist, [i + j for i, j in zip(mu, sigma)], [i - j for i, j in zip(mu, sigma)], facecolor='#003366', alpha=0.5)
        axis.set_title(title)
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.grid()
        figure.savefig(filename)
        self.files.append(filename)

    def write_result_file(self, pattern, input_file, output_file, networks):
        castalia = Castalia(pattern, input_file)
        castalia.binary += "Results"
        castalia.networks = networks
        file_to_split =  basename(normpath(input_file))
        cwd = input_file.split("/" + file_to_split)[0]
        castalia.log_file_path = cwd + "/" + output_file
        castalia.run()
    
    def generate_bar_plot(self, filename, title, xdata, ydata, xlabel, ylabel, labels): 
        figure, axis = plt.subplots()

        index = np.array(xdata)
        width = 1.0

        bar_widths = -1

        if bar_widths > 0:
            axis.bar(index, ydata, bar_widths)
        else:
            print len(index)
            print len(ydata[1])
            print len(ydata[0])
            axis.bar(index, ydata[1], width, color="#990000")
            axis.bar(index+width, ydata[0], width, color="#003366")

        axis.set_ylabel(ylabel)
        axis.set_xlabel(xlabel)

        #axis.set_xticks(index + width)

        axis.set_title(title)
        #axis.legend((ydata[0][0], ydata[1][0]), (labels[0], labels[1]) )
        axis.grid(axis="y")

        plt.savefig(filename)
        self.files.append(filename)
        plt.close()

    def prepare_line_plot(self, filename, title, xlabel, ylabel, data):
        xlist = [] 
        std = [] 
        mean = [] 

        for key in sorted(data):
            xlist.append(key)
            mean.append(float(np.mean(data[key])))
            std.append(float(np.std(data[key])))

        self.generate_line_plot(filename, title, xlist, mean, std, xlabel, ylabel) 


 
    def _flat_data(self, nodes):
        result = {}

        for key in self.results.keys():
            rate = key.split(',')[0]

            if rate not in result.keys():
                result[rate] = {}

                for node in xrange(0, nodes):
                    result[rate][node] = []

            data = self.results[key]
            node = data.index(max(data))

            result[rate][node].append(self.results[key][node])

        self.results = result


    def generate_packet_reception_rate_plot(self, nodes, network):
        xdata = []
        ydata = []
        label = []

        # remove sender from result data
        self._flat_data(nodes)

        for node in xrange(0, nodes):
            xlist = []
            ylist = []

            for rate in sorted(self.results.keys(), key=int):
                xlist.append(rate)
                ylist.append(self.results[rate][node])

            xdata.append(xlist)
            ydata.append(ylist) 

            if network:
                label.append("PAN$_{" + str(node) + "}$")
            else:
               if node == 0:
                   label.append("1 Node")
               else:
                   label.append(str(node+1) + " Nodes")

        self.generate_line_plot("packet_reception_rate.png", "Packet Reception Rate", xdata, ydata, "Packet Rate", "Packet Reception Rate", label)


class ReportGenerator:
    def __init__(self):
        self.scenarios = {} 

    def _get_header(self):
        header =  '<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        header += '<html xmlns="http://www.w3.org/1999/xhtml">'
        header += '  <head>'
        header += '    <title>Results</title>'
        header += '    <link rel="stylesheet" href="style.css" type="text/css">'
        header += '  </head>'
        header += '  <body>'
        return header

    def _get_footer(self):
        footer = '  </body>'
        footer += '</html>'
        return footer

    def write(self, filename):
        with open(filename, "w") as output:
          output.write(self._get_header())

          for scenario in self.scenarios:
             output.write(self._get_scenario(scenario))

          output.write(self._get_footer())

    def _get_scenario(self, scenario):
        result = '<h3>' + scenario + '</h3>'
        counter = 0

        for entry in self.scenarios[scenario]:
           result += '<a href="' + entry +'"><img src="' + entry + '"width=250 height=250></a>'

           if counter < 5:
               counter += 1
           else:
               counter = 0
               result += '</br></br>'

        return result


def main():
     parser = argparse.ArgumentParser(description='a script for evaluating castalia simulations')
     parser.add_argument('-c', dest='configuration', type=str, default="", action='store', help='a castalia configuarion to evaluate')

     if len(sys.argv) == 1:
         parser.print_help()
         sys.exit(1)

     arguments = parser.parse_args()

     if arguments.configuration != "":
         results = CastaliaResultParser()
         results.write_result_file("application level", arguments.configuration, "application.txt")
         results.read_multiple_columns("application.txt")
         results.plot_histogram()

         results.write_result_file("average latency", arguments.configuration, "latency.txt")
         results.read_multiple_columns("latency.txt")
         results.plot("Average Latency", "average_latency", "rate", "latency")

         results.write_result_file("Packets received", arguments.configuration, "received.txt")
         results.read_multiple_columns("received.txt")
         results.plot_ext("Received Packets", "received_packets", "rate", "packets")
    
         results.write_result_file("Packets reception rate", arguments.configuration, "reception.txt")
         results.read_multiple_columns("reception.txt")
         results.plot_ext("Packet Reception Rate", "packet_reception_rate", "rate", "packet reception rate")

         results.write_result_file("Packet breakdown", arguments.configuration, "breakdown.txt")
         results.read_breakdown_packets("breakdown.txt")
         results.plot_breakdown_packets()

         report = ReportGenerator()
         report.scenarios['Test'] = results.files
         report.write('test.html')

if __name__ == "__main__":
    main()

