#!/usr/bin/env python
# encoding: utf-8
import sys

from onesAction import query_my_ones, MyOnesItem
from utils import get_args, wf


def key_for_record(record: MyOnesItem):
    return f"{record.name} {record.onesTypeDesc} {record.titlePinyin}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    ones_list = query_my_ones()
    ones_list = wf().filter(query, ones_list, key_for_record, max_results=10)
    if ones_list:
        for u in ones_list:
            wf().add_item(
                u.name,
                f"【{u.onesTypeDesc}】优先级:{u.priority} - 状态:{u.state}",
                f"{u.projectId},{u.onesId},{u.onesType}",
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
