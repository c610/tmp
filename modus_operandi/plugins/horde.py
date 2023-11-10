#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class Horde(Analyzer):
    """
    this module was designed to spot the 'most basic'
    bugs during the source code review of Horde 5.2.x.
    based on version 5.2.21-22 (described also at the blog).
    for now we have:
    -- check_xss_setget -- check for functions with GET/POST, etc...
    -- check_xss_setdef -- check for functinos declared as setDefault
    """

    def target_mime_wildcards(self):
        return ["text/x-php*"]

    def search_description(self):
        return {
            "bug:XSS:Horde:setdef": (
                "-\>setDefault\(\$vars->get\('(.*?)'",
                "possible XSS (setDefault) for Horde based on: CVE-2017-1690[6-8]"
            ),
            "bug:XSS:Horde:set-get": (
                "\$vars->set\('(.*?)',(.*?)->get\('(.*?)'",
                "possible XSS (set/get) for Horde"
            ),

        }


if __name__ == "__main__":
    pass
