#!/usr/bin/env python2.7

class OMNeTFileParser:
    def __init__(self, file_path):
        try:
            self.file_path = file_path
            self.current_line_nr = 0
            self.file_handle = open(self.file_path, "r")
            self.parameters = self._read_preamble()
        except IOError:
            print "Error: can\'t find file ", self.file_path, " or read it"
        except:
            self.file_handle.close()

    def _read_preamble(self):
        return {'version': self._parse_key_value("version"),
                'run': self._parse_key_value("run"),
                'configname': self._parse_attribute("configname"),
                'datetime': self._parse_attribute("datetime"),
                'experiment': self._parse_attribute("experiment"),
                'inifile': self._parse_attribute("inifile"),
                'iterationvars': self._parse_attribute("iterationvars"),
                'iterationvars2': self._parse_attribute("iterationvars2"),
                'measurement': self._parse_attribute("measurement"),
                'network': self._parse_attribute("network"),
                'offset': self._parse_attribute("offset"),
                'payload': self._parse_attribute("payload"),
                'processid': self._parse_attribute("processid"),
                'rate': self._parse_attribute("rate"),
                'repetition': self._parse_attribute("repetition"),
                'replication': self._parse_attribute("replication"),
                'resultdir': self._parse_attribute("resultdir"),
                'runnumber': self._parse_attribute("runnumber"),
                'sd': self._parse_attribute("sd"),
                'seedset': self._parse_attribute("seedset")}

    def _parse_key_value(self, key):
        words = self.file_handle.readline().split(' ')
        if len(words) != 2:
            print "Could not parse key value line %d from %s because there are %d words" % (self.current_line_nr, self.file_path, len(words))
            raise

        if words[0] != key:
            print "Error while parsing key value line: Expected %s but got %s" % (key, words[0])
            raise

        return words[1].strip()

    def _parse_attribute(self, name):
        words = self._read_next_line().split(' ')

#        if len(words) != 3:
#            print "Could not parse attribute line %d from %s because there are %d words" % (self.current_line_nr, self.file_path, len(words))
#            raise

        if words[0] != 'attr' or words[1] != name:
            print "Could not parse line %d from %s for attribute %s" % (self.current_line_nr, self.file_path, name)
            raise

        return words[2].strip()

    def _read_next_line(self):
        self.current_line_nr += 1
        return self.file_handle.readline()

    def _get_node_identifier(self, line):
        # TODO: fix that (that's quite aweful)
        #return line.split(' ')[1].split('.')[1].split('[')[1].split(']')[0]
        return line.split('[')[1].split(']')[0]
