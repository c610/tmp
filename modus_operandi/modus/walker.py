#!/usr/bin/python
# -*- coding: utf-8 -*-

from fnmatch import fnmatch
from os import path
import magic
from modus.ctx import ECTX


class SourceWalker(object):

    def __init__(self, execution_context):
        self.ctx = execution_context
        self.m = magic.open(magic.MAGIC_MIME)
        self.m.load()

    def handle_matched_filepath(self, pattern, directory, files):

        for filename in files:
            if fnmatch(filename, pattern):
                f = path.join(directory, filename)
                if path.isfile(f) and not path.islink(f):
                    self.ctx.work_queue.put((f, self.m.file(f)))

    def run(self):
        path.walk(
            self.ctx[ECTX.start_path],
            self.handle_matched_filepath,
            self.ctx[ECTX.wildcard],
        )


if __name__ == "__main__":
    pass
