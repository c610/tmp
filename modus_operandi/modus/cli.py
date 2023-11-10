#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from ctx import ECTX
from ctx import get_default_plugins_path
from analyzer import register_plugins
import sys

LINE_WITH = 80


class ListModules(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.repo:
            plugins_dir = namespace.repo
        else:
            plugins_dir = get_default_plugins_path()
        plugins = register_plugins(plugins_dir)
        for plugin_class in plugins:
            print(plugin_class.__name__)
            print(plugin_class.__doc__)
            print(" Mime types:")
            for m in plugin_class().target_mime_wildcards():
                print("\t%s" % m)
            print("\n Search description:")
            regex_dict = plugin_class().search_description()
            for k, v in regex_dict.iteritems():
                print(" TAG: %s" % k)
                print("\tRegex: %s" % v[0])
                print("\tComment: %s" % v[1])
            print("-" * LINE_WITH)
        sys.exit(0)


def stb(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_params(ctx):
    banner = '\t[--]  modus v0.7  [--]\n'

    parser = argparse.ArgumentParser(description=banner)
    parser.add_argument(
        ECTX.start_path,
        metavar="PATH",
        type=str,
        help='Source files directory.'
    )
    parser.add_argument(
        '-%s' % ECTX.wildcard[0],
        '--%s' % ECTX.wildcard,
        metavar="REGEXP",
        type=str,
        help='File name wildcard. Default value is "%s".' % ctx['filter']
    )
    parser.add_argument(
        '-%s' % ECTX.workers_num[0],
        '--%s' % ECTX.workers_num,
        metavar="NUMBER",
        type=int,
        help='Worker processes. Default value is (%d - %d). '
             'Max possible value is (%d * %d)' % (ctx['cpu'], ctx['mps'], ctx['cpu'], ctx['mpl'])
    )
    parser.add_argument(
        '-%s' % ECTX.parallelism_level[0],
        '--%s' % ECTX.parallelism_level,
        metavar="NUMBER",
        type=int,
        help='Internal worker parallelism. Default value is %d. '
             'Value in inclusive range <%d-%d>.' % (ctx['threads'], ctx['lwp'], ctx['hwp'])
    )
    parser.add_argument(
        '-%s' % ECTX.plugins_repo[0],
        '--%s' % ECTX.plugins_repo,
        metavar="PATH",
        type=str,
        help='Custom plugins dir. Default value is %s. ' % (ctx['repo'])
    )
    parser.add_argument(
        '-%s' % ECTX.strict_mime_check[0],
        '--%s' % ECTX.strict_mime_check,
        metavar="BOOL",
        type=stb,
        help='Strict mime match. WARNING! Disabling this will run all enabled analyzers '
             'against all types of files ignoring potential '
             'extension-content inconsistency Default value is %s. ' % (ctx['smc'])
    )
    parser.add_argument(
        '-l',
        '--list',
        action=ListModules,
        nargs=0,
        help="List available checks."
    )

    ctx.update(parser.parse_args().__dict__)


if __name__ == "__main__":
    pass
