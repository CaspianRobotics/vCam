#!/usr/bin/python
import json
import urllib2
import collections
import struct


class Connection:

    """ Driver for reading teh data from camera Qx-10 Sony """

    # construct
    def __init__(self):
        self._param = collections.OrderedDict([
                                              ("method", "getAvailableApiList"),
                                             ("params", []),
                                             ("id", 1),
                                             ("version", "1.0")])

    def int_or_str(self, v):
        if v.lower() == "false":
            return False
        if v.lower() == "true":
            return True
        try:
            return int(v)
        except ValueError:
            return v

    def get_ip_stream(self, param_list):
        self._param["method"] = param_list
        return urllib2.urlopen("http://10.0.0.1:10000/sony/camera", json.dumps(self._param)).read()
