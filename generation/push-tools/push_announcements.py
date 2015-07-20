#!/usr/bin/env python

import re
import os
import datetime
import fileinput

# global variables since this is hacking
indent = 0
announce = \
'''
<ul>
{announce_body}
</ul>
'''
single_announce = \
'''
<li class="announce-container">
  <div class="announce-topic">{topic}</div>
  <div class="announce-date">{date}</div>
  <div class="announce-content">
    {content}
  </div>
</li>
'''


# C-Like Macro for typing
def IND(str, ind=1):
    str_list = str.split("\n")
    for line_num in xrange(len(str_list)):
        str_list[line_num] = "  " * ind + str_list[line_num]

    return "\n".join(str_list)


def form_str(str):
    global indent
    return IND(str, indent)


def FS(str):
    return form_str(str)


def construct_announcements(announcement_file):
    announcements = ""

    global announce, single_announce

    for line in announcement_file:
        item_set = line.strip().split("|")
        for i in xrange(len(item_set)):
            item_set[i] = item_set[i].strip()

        if item_set == ['']:
            continue

        # Always insert new announcements first
        # Assume new announcements are written on top of file
        announcements = single_announce.format(topic=item_set[0],
                                               date=item_set[1],
                                               content=IND(item_set[2])) \
            + announcements

    return announce.format(announce_body=IND(announcements))

def sub_date(filepath):
    txt = open(filepath, "r").read()
    open(filepath, "w").write(txt.replace('\\today',
                                          datetime.datetime.today().strftime(
                                              "%B %d %I:%M %p")))

if __name__ == "__main__":
    template_file = fileinput.input()
    announcement_filepath = os.path.join(
        os.path.split(os.path.abspath(__file__))[0],
        "../data/announcement.list")

    sub_date(announcement_filepath)

    for line in template_file:
        # has <!-- Announcement something, replace it with comment +
        # announcements
        if re.search("<!--", line) and re.search("Announcement", line):
            announcements = construct_announcements(open(announcement_filepath,
                                                         "r"))
            print FS("<!-- Announcements -->")
            print FS(announcements)
        else:
            print line,
            indent = len(line) - len(line.lstrip())

    template_file.close()
