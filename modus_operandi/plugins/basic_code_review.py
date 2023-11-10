#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class CodeReview(Analyzer):
    """
    This module was designed to spot the 'most basic'
    bugs during the source code review. for now we have:
    -- basic_xss
    -- basic_unserialize
    -- basic_path_traversal

    """

    def __prepare_xss_definitions(self, methods):
        xss_dict = {}

        functions = ['echo ', 'return ', 'print ']
        for m in methods:
            for f in functions:
                tag = "XSS:%s-%s" % (f.rstrip(), m)
                xss_dict[tag] = (f + "(.*?)\$_" + m + "\[(.*?)\]", "possible xss")
        return xss_dict

    def __prepare_taversal_definitions(self, methods):
        traversal_dict = {}
        functions = [
            'readfile', 'readfile ',
            'fopen', 'fopen ',
            'is_readable', 'is_readable ',
            'glob', 'glob '
        ]
        for m in methods:
            for f in functions:
                tag = "PATH-TRAVERSAL:%s-%s" % (f.rstrip(), m)
                traversal_dict[tag] = (f + "(.*?)\\$_" + m + "\['(.*?)'\]", "possible path traversal")

        return traversal_dict

    def __prepare_unserialize_definitions(self, methods):
        unserialize_dict = {}

        functions = [
            'unserialize',
            'unserialize '
        ]
        for m in methods:
            for f in functions:
                tag = "SERIALIZATION:%s-%s" % (f.rstrip(), m)
                unserialize_dict[tag] = (f + "(.*?)\\$_" + m + "\['(.*?)'\]", "possible umsafe unserialize")

        return unserialize_dict

    def target_mime_wildcards(self):
        return ["text/x-php*"]

    def search_description(self):
        methods = [
            'GET',
            'POST',
            'REQUEST',
            'FILES',
            'COOKIE',
            'SERVER',
            'SESSION',
            'ENV',
            'COOKIE'
        ]
        desc_dict = self.__prepare_xss_definitions(methods)
        desc_dict.update(
            self.__prepare_taversal_definitions(methods)
        )
        desc_dict.update(
            self.__prepare_unserialize_definitions(methods)
        )
        return desc_dict


if __name__ == "__main__":
    pass
