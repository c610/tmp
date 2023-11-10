#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class BasicXssAnalyzer(Analyzer):
    """
    this module was designed to spot the 'most basic'
    XSS bugs during the source code review of Dlink router.
    Based on version dir300. For now we have:

        redefined basic modules for v0.7:
       -- check_xss --
    """

    def target_mime_wildcards(self):
        return ["text/x-php*"]

    def search_description(self):
        return {
            # TODO one below hangs on 192k php-font file
            # "TAG:def": ("(.*?)echo \$_POST\[\"(.*?)\"", "it looks like we got a basic SQLi bug."),
            "bug:XSS:Dlink[GET]": ("input (.*?)echo \$_GET\[\"(.*?)\"", "it looks like we got a basic XSS bug."),
            "bug:XSS:Dlink[POST]": ("echo \$_POST\[\".*?\"", "it looks like we got a basic XSS bug."),
        }


if __name__ == "__main__":
    pass
