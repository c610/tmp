#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
modus.py - v0.8

small script I called modus.py from 'modus operandi'.
maybe you will find it useful.
for some reason, try to keep it private for now.
thanks.

more: code610.blogspot.com

last update(s): please see CHANGELOG file.
have fun
"""
import sys
from os.path import dirname
from os.path import abspath
import signal
from modus.cli import parse_params
from modus.ctx import ECTX
from modus.walker import SourceWalker
from modus.worker import run_worker_processes
from modus.analyzer import register_plugins


def manager_signal_handler():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def setup_analyzers(plugins_dir):
    return [A() for A in register_plugins(plugins_dir)]


def main():
    ctx = ECTX()
    parse_params(ctx)

    source_walker = SourceWalker(ctx)
    analyzers = setup_analyzers(ctx[ECTX.plugins_repo])

    try:

        run_worker_processes(
            ctx,
            source_walker,
            analyzers
        )

    finally:
        ctx.work_queue.close()
        ctx.work_queue.cancel_join_thread()


if __name__ == "__main__":
    sys.path.append(
        dirname(dirname(abspath(__file__)))
    )
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("Terminated\n")
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
