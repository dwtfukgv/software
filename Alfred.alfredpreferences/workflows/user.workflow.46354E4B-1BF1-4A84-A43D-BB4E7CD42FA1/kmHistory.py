#!/usr/bin/env python
# encoding: utf-8
import os
import sys

import kmAction
from kmAction import UnitItem
import utils
from utils import get_args, wf, from_unix_timestamp, get_time_expression


def key_for_record(record: UnitItem):
    return f"{record.title} {record.creator} {record.titlePinyin}"


def get_operation_time(item: UnitItem):
    return item.operatorTime


def main(workflow):
    query, mis, cache_seconds = get_args()
    km_history_limit = os.getenv("km_history_limit")
    if not km_history_limit:
        km_history_limit = 200
    else:
        km_history_limit = int(os.getenv("km_history_limit"))
    units = kmAction.query_limit_operation_history(km_history_limit)
    units = wf().filter(
        query, units, key_for_record, min_score=1, fold_diacritics=False
    )
    if units:
        units.sort(key=get_operation_time, reverse=True)
        for u in units:
            operation_time = int(u.operatorTime / 1000)
            wf().add_item(
                u.title,
                f"【{get_time_expression(operation_time)}】创建人:{u.creator} - 浏览时间:{from_unix_timestamp(operation_time)}",
                u.pageId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
