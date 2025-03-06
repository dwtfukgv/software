#!/usr/bin/env python
# encoding: utf-8
import sys

from kmAction import ReceivedItem, latest_received_list
from utils import get_args, wf, get_time_expression, from_unix_timestamp_HHMM


def key_for_record(record: ReceivedItem):
    return f"{record.title} {record.sender} {record.titlePinyin}"


def get_modify_time(item: ReceivedItem):
    return item.recentReceivedTime


def main(workflow):
    query, mis, cache_seconds = get_args()
    units = latest_received_list()
    units = wf().filter(query, units, key_for_record, min_score=1, fold_diacritics=False)
    if units:
        units.sort(key=get_modify_time, reverse=True)
        for u in units:
            recent_received_time = int(u.recentReceivedTime / 1000)
            wf().add_item(
                u.title,
                f"【{get_time_expression(recent_received_time)}】发送人:{u.sender} 时间：{from_unix_timestamp_HHMM(recent_received_time)}",
                u.contentId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
