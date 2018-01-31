#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class Piwigo(Analyzer):
    """
    this module was designed to spot the 'most basic'
    bugs during the source code review of Piwigo 2.9.2.
    For now we have:
    -- check_xss -- testing for basic XSS
    -- check_sqli_pwg_realesc -- checking for wrong sanitization
       when pwg_db_real_escape_string is used in query
    """

    def target_mime_wildcards(self):
        return ["text/x-php*"]

    def __prepare_check_sqli_pwg_realesc_definitions(self, methods):
        traversal_dict = {}
        for m in methods:
            regexes = [
                "pwg_db_real_escape_string(.*?)\$_" + m + "\['(.*?)'",
                "WHERE(.*?)" + m + "\['(.*?)'"
            ]
            for r in regexes:
                tag = "bug:SQLI:Piwigo:%s-%s" % (r[:4], m)
                traversal_dict[tag] = (
                    r, "possible path traversal"

                )

        return traversal_dict

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
        desc_dict = self.__prepare_check_sqli_pwg_realesc_definitions(methods)
        desc_dict['bug:XSS:Piwigo'] = (
            "span class=(.*?){/if}>{\$(.*?)}",
            "it looks like we got a basic XSS for Piwigo"
        )
        return desc_dict


if __name__ == "__main__":
    pass
