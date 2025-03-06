#!/usr/bin/env python
# encoding: utf-8
import sys

from kmAction import latest_mentioned_list, MentionedItem
from utils import get_args, wf, get_time_expression, from_unix_timestamp_HHMM


def key_for_record(record: MentionedItem):
    return f"{record.title} {record.titlePinyin}"


def get_modify_time(item: MentionedItem):
    return item.recentMentionTime


def main(workflow):
    query, mis, cache_seconds = get_args()
    units = latest_mentioned_list()
    units = wf().filter(query, units, key_for_record, min_score=1, fold_diacritics=False)
    if units:
        units.sort(key=get_modify_time, reverse=True)
        for u in units:
            recent_mention_time = int(u.recentMentionTime / 1000)
            wf().add_item(
                u.title,
                f"【{get_time_expression(recent_mention_time)}】@次数:{u.mentionCount} 时间：{from_unix_timestamp_HHMM(recent_mention_time)}",
                u.contentId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
