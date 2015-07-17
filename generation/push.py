#!/usr/bin/env python

import sys
import commands


def push_announce():
    return "./push-tools/push_announcements.py -"


def push_table():
    return "./push-tools/push_table.py -"


def push_all():
    return push_table() + " | " + \
        push_announce()


func_map = {"all": push_all, "announce": push_announce,
            "an": push_announce,
            "table": push_table, "t": push_table}

if __name__ == "__main__":
    run_cmd = "cat ./data/index.html.tep"

    if len(sys.argv) == 1:
        run_cmd += " | " + push_all()
    else:
        for cmd in sys.argv[1:]:
            if cmd not in func_map:
                print cmd, "not found, add in func_map in push (or typo?)"
            else:
                run_cmd += " | " + func_map[cmd]()

    print run_cmd
    open("../site/index.html", "w").write(commands.getoutput(run_cmd))
