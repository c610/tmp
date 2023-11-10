#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import imp
import re
from os import path


class PluginRegistry(ABCMeta):
    plugins = []

    def __init__(cls, name, bases, attrs):
        if name != 'Analyzer':
            PluginRegistry.plugins.append(cls)


class Analyzer(object):
    __metaclass__ = PluginRegistry
    MAX_DISPLAY_LINE_LEN = 120

    def __init__(self):
        self.description = self.search_description()

    def fit_line(self, line):
        if Analyzer.MAX_DISPLAY_LINE_LEN < len(line):
            out_str = line[:Analyzer.MAX_DISPLAY_LINE_LEN] + "...".lstrip()
        else:
            out_str = line[:-1].lstrip()
        return out_str.replace('\n', ' ').replace('\r', '')

    def scan(self, file_info):
        file_path = file_info[0]
        mime_type = file_info[1]
        results = []
        with open(file_path, 'rb') as f:
            lines = f.readlines()
            for tag, matcher in self.description.iteritems():
                regex = re.compile(matcher[0])
                for line_num, line in enumerate(lines):
                    if re.search(regex, line):
                        results.append(
                            (tag,
                             matcher[0],
                             mime_type,
                             path.realpath(file_path),
                             line_num + 1,
                             self.fit_line(line),
                             matcher[1]
                             )
                        )
            if results:
                return results

    @abstractmethod
    def search_description(self):
        pass

    @abstractmethod
    def target_mime_wildcards(self):
        pass


def register_plugins(plugins_dir):
    for filename in os.listdir(plugins_dir):
        modname, ext = os.path.splitext(filename)
        if ext == '.py':
            f, path, descr = imp.find_module(modname, [plugins_dir])
            if f:
                _ = imp.load_module(modname, f, path, descr)
    return PluginRegistry.plugins


if __name__ == "__main__":
    pass
