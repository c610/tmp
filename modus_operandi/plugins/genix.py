#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class Genix(Analyzer):
    """
    this module was designed to spot the 'most basic'
    bugs during the source code review of Genix CMS.
    based on version 1.1.5 (described also at the blog).
    for now we have:
    -- check_xss -- check for functions with GET/POST, etc...
    -- check_sqli -- to check some basic SQLi bugs found in Genix
    """

    def target_mime_wildcards(self):
        return ["text/x-php*"]

    def search_description(self):
        return {
            "Genix:bug:SQLi": (
                "Db::result\(\"SELECT(.*?)\{\$(.*?)\}",
                "possible SQLi; wrong declaration"
            ),
            "Genix:bug:XSS": (
                "\$(.*?) = Typo::cleanX\(\$_GET\['(.*?)'",
                "it looks like we got a basic XSS bug for Genix CMS"
            ),
        }


if __name__ == "__main__":
    pass
