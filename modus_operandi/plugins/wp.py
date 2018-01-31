#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class Wordrpess(Analyzer):
    """
    this module was designed to spot the 'most basic'
    bugs during the source code review of Wordpress 4.x.
    for now we have:
    -- check_xss_methods
    -- check_sqli_declar
    -- check_fileinc
    """

    def __prepare_rce_definitions(self, methods):
        dict = {}
        functions = [
            'call_user_func', 'call_user_func ',
            'function_exists', 'function_exists '
        ]
        for m in methods:
            for f in functions:
                tag = "bug:RCE:%s-%s" % (f.rstrip(), m)
                dict[tag] = (
                    f + "(.*?)\\$_" + m + "\['(.*?)'\]",
                    "possible path traversal",
                    'it looks like we got a basic "Wordpress-related" RCE bug'
                )

        return dict

    def __prepare_file_inc_definitions(self, methods):
        dict = {}
        functions = [
            'include', 'include ',
            'include_once', 'include_once ',
            'require', 'require ',
            'require_once ', 'require_once '
        ]
        for m in methods:
            for f in functions:
                tag = "bug:INCLUDE:%s-%s" % (f.rstrip(), m)
                dict[tag] = (
                    f + "(.*?)\\$_" + m + "\['(.*?)'\]",
                    'it looks like we got a basic "Wordpress-related" include-bug...'
                )
        return dict

    def __prepare_sqli_definitions(self, methods):
        dict = {}
        for m in methods:
            tag = "bug:SQLi:Wordpress:%s" % m
            dict[tag] = (
                "\$wpdb->get_results\('SELECT(.*?)WHERE (.*?)=(.*?)\$_" + m + "\[(.*?)\]\);",
                "possible umsafe unserialize"
            )

        return dict

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
        desc_dict = self.__prepare_rce_definitions(methods)
        desc_dict.update(
            self.__prepare_file_inc_definitions(methods)
        )
        desc_dict.update(
            self.__prepare_sqli_definitions(methods)
        )
        return desc_dict


if __name__ == "__main__":
    pass
