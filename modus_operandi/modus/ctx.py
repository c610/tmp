#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing
from os import path


def get_default_plugins_path():
    return path.realpath(path.join(
        path.dirname(path.realpath(__file__)),
        "../plugins"
    ))


class ECTX(object):
    start_path = "dir"
    wildcard = "filter"
    workers_num = "proc"
    parallelism_level = "threads"
    cpu_count = "cpu"
    plugins_repo = "repo"
    min_processes_sub = "mps"
    max_processes_mul = "mpl"
    lowest_worker_parallelism = "lwp"
    highest_worker_parallelism = "hwp"
    strict_mime_check = "smc"

    def __init__(self):

        self.work_queue = multiprocessing.Queue()

        self.VALUES = {
            ECTX.cpu_count: multiprocessing.cpu_count(),
            ECTX.wildcard: '*',
            ECTX.workers_num: multiprocessing.cpu_count() - 1,
            ECTX.parallelism_level: 10,
            ECTX.min_processes_sub: 1,
            ECTX.max_processes_mul: 3,
            ECTX.lowest_worker_parallelism: 1,
            ECTX.highest_worker_parallelism: 100,
            ECTX.plugins_repo: get_default_plugins_path(),
            ECTX.strict_mime_check: True

        }

        def is_workers_num_valid(desired):
            max_workers = self[ECTX.cpu_count] \
                          * self[ECTX.max_processes_mul]
            return 0 < desired <= max_workers

        def is_parallelism_level_valid(desired):
            return self[ECTX.lowest_worker_parallelism] \
                   <= desired <= \
                   self[ECTX.highest_worker_parallelism]

        self.VALIDATION_RULES = {
            ECTX.workers_num: [
                is_workers_num_valid,
                "Worker processes number out of range."
            ],
            ECTX.parallelism_level: [
                is_parallelism_level_valid,
                "Internal worker parallelism out of range."
            ],
            ECTX.start_path: [
                lambda p: path.isdir(p),
                "Start path is not a directory."
            ]
        }

    def __getitem__(self, item):
        return self.VALUES[item]

    def __validate(self, d):
        filtered_dict = {
            k: v for k, v in d.iteritems() if
            k in self.VALIDATION_RULES.iterkeys()
        }
        for key, value in filtered_dict.iteritems():
            if not self.VALIDATION_RULES[key][0](value):
                raise ValueError(
                    '[%s=%s] %s' % (
                        key,
                        value, self.VALIDATION_RULES[key][1]
                    )
                )

    def __dropna(self, d):
        return dict((k, v) for k, v in d.iteritems() if v is not None)

    def update(self, d):
        input_params = self.__dropna(d)
        self.__validate(input_params)
        self.VALUES.update(input_params)


if __name__ == "__main__":
    pass
