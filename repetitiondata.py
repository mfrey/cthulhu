#!/usr/bin/env python2.7

class RepetitionData:
    def __init__(self, parameters, nodes):
        self.parameters = parameters
        self.nodes = nodes

    def get_parameter(self, parameter_name):
        try:
            return self.parameters[parameter_name]
        except KeyError:
            print "Unknown parameter " + parameter_name

    def get_node_results(self):
        return self.nodes
