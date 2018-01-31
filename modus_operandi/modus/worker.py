#!/usr/bin/python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process
from ctx import ECTX
import re
import os
from sys import stdout
import csv
from multiprocessing import Lock

lock = Lock()
csv_writer = csv.writer(stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


class PoisonPill(StopIteration):
    pass


def write_csv_line(data):
    with lock:
        csv_writer.writerow(data)
        stdout.flush()


def prepare_mime_matcher(target_mime):
    def mime_matcher(a):
        for wc in a.target_mime_wildcards():
            pattern = re.compile(wc)
            if re.search(pattern, target_mime):
                return True
        return False

    return mime_matcher


def __perform_scan_task(file_info, analyzers, strict=False):
    if strict:
        mime_filter = prepare_mime_matcher(file_info[1])
        analyzers = filter(mime_filter, analyzers)
    for a in analyzers:
        s_info = a.scan(file_info)
        if s_info:
            for row in s_info:
                write_csv_line(row)


def __consume_from(queue):
    while True:
        val = queue.get()
        if PoisonPill is not type(val):
            yield val
        else:
            return


def __worker(threads_num, work_queue, analyzers, strict=True):
    try:
        pool = ThreadPoolExecutor(threads_num)
        for file_info in __consume_from(work_queue):
            pool.submit(
                __perform_scan_task,
                file_info,
                analyzers,
                strict
            )
    except KeyboardInterrupt:
        pass
    finally:
        pool.shutdown(wait=False)


def run_worker_processes(ctx, source_walker, analyzers):
    processes = []
    processes.extend([Process(
        target=__worker,
        args=(
            ctx[ECTX.parallelism_level],
            ctx.work_queue,
            analyzers,
            ctx[ECTX.strict_mime_check]
        ))
        for _ in xrange(0, ctx[ECTX.workers_num])
    ])
    for p in processes:
        p.start()

    write_csv_line([
        'tag',
        'pattern',
        "mime-type",
        "file_path",
        "line number",
        "line_part",
        "comment"
    ])
    source_walker.run()
    for _ in processes:
        ctx.work_queue.put(PoisonPill())

    for p in processes:
        p.join()


if __name__ == "__main__":
    pass
