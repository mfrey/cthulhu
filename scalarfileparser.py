#!/usr/bin/env python2.7

import shlex

from omnetfileparser import OMNeTFileParser
from repetitiondata import RepetitionData

class ScalarFileParser(OMNeTFileParser):
    def __init__(self, file_name):
        OMNeTFileParser.__init__(self, file_name)

    def read(self):
        try:
            nodes = self._read_body()
            return RepetitionData(self.parameters, nodes)
        except IOError:
            print "Error: can\'t find file ", self.file_path, " or read it"
        finally:
            self.file_handle.close()

    def _read_body(self):
        nodes = {}
        line = self._read_next_line()
        while line:
            line = self._read_next_line()
            self._parse(line, nodes)

        return nodes

    def _parse(self, line, nodes):
        if line.startswith('scalar S'):
            node_identifier = self._get_node_identifier(line)

            if node_identifier not in nodes:
                nodes[node_identifier] = {}

            metric_name, value = shlex.split(line)[2], shlex.split(line)[3]
            nodes[node_identifier][metric_name] = float(value)
