#!/usr/bin/env python

import re
import os
import datetime
import fileinput

# global variables since this is hacking
indent = 0
head = \
'''
<table>
    <thead>
      <tr>
        <th>Date</th>
        <th>Lecture</th>
      </tr>
    </thead>
    <tbody>
{tablebody}
    </tbody>
</table>
'''
row_lecture = \
'''
<tr class="lecture-row">
  <td>{date}</td>
  <td>{lecturename}</td>
</tr>
'''
row_part = \
'''
<tr class="part-row">
  <th colspan="2">{topicname}</th>
</tr>
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


def construct_table(table_file):
    table = ""
    lecture_date = datetime.date(2015, 8, 31)

    global head, row_lecture, row_part

    table_list = []
    last_concat = False

    for line in table_file:
        this_concat = last_concat
        line = line.strip()
        if line == '':
            continue
        if line[0] == '#':
            continue
        if line.endswith('\\'):
            if line == '\\':
                continue
            if line.endswith('\\\\'):
                line = line.rstrip('\\\\') + '<br/>'
            else:
                line = line.rstrip('\\')
            last_concat = True
        else:
            last_concat = False

        if this_concat:
            table_list[-1] += line
        else:
            table_list.append(line)

    for line in table_list:
        item_set = line.strip().split("|")
        for i in xrange(len(item_set)):
            item_set[i] = item_set[i].strip()

        if item_set == ['']:
            continue

        if re.search("part", item_set[0]):
            table += row_part.format(topicname=item_set[1])

        if re.search("lecture", item_set[0]):
            table += row_lecture.format(lecturename=item_set[1],
                                        date=lecture_date.strftime("%m/%d"))
            lecture_date += datetime.timedelta(days=7)

    return head.format(tablebody=IND(table))


if __name__ == "__main__":
    template_file = fileinput.input()
    schedule_filepath = os.path.join(
        os.path.split(os.path.abspath(__file__))[0],
        "../data/schedule.table")

    for line in template_file:
        # has <!-- Schedule something, replace it with comment + table
        if re.search("<!--", line) and re.search("Schedule", line):
            table = construct_table(open(schedule_filepath, "r"))
            print FS("<!-- Schedule -->")
            print FS(table)
        else:
            print line,
            indent = len(line) - len(line.lstrip())

    template_file.close()
