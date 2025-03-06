#!/usr/bin/env python
# encoding: utf-8
import sys

import kmAction
import utils
from utils import get_args, wf


def key_for_record(record: kmAction.UnitItem):
    return f"{record.title} {record.creator} {record.titlePinyin}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    units = wf().cached_data(
        "km_collections", kmAction.query_collections, max_age=int(cache_seconds)
    )
    units = wf().filter(
        query, units, key_for_record, min_score=1, fold_diacritics=False
    )
    if units:
        for u in units:
            modify_time = utils.from_unix_timestamp(int(u.operatorTime/1000))
            wf().add_item(
                u.title,
                f"创建人:{u.creator} - 收藏时间:{modify_time}",
                u.pageId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
