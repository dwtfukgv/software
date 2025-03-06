#!/usr/bin/env python
# encoding: utf-8
import sys

from onesAction import query_space, OnesProject
from utils import get_args, wf


def key_for_record(record: OnesProject):
    return f"{record.name} {record.titlePinyin}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    ones_project = query_space()
    ones_project = wf().filter(query, ones_project, key_for_record, max_results=10)
    if ones_project:
        for u in ones_project:
            wf().add_item(
                u.name,
                f"【等级{u.level}-{u.state}】 Pmis状态:{u.pmisApplicationState} - {u.category}",
                f"{u.projectId},{u.defaultPathkey}",
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
