#!/usr/bin/python
# -*- coding: utf-8 -*-

from modus.analyzer import Analyzer


class FileAnalyzer(Analyzer):
    """
    Example modus analyzer

    User must implement two methods

    Note:
        blah blah

    Attributes:
        blah blah
    """

    def target_mime_wildcards(self):
        return ["text*"]

    def search_description(self):
        return {
            "TAG:TODO": ("#.*?TODO.*?", "comment ie. CVE?"),
        }


if __name__ == "__main__":
    pass
