#!/usr/bin/env python
# encoding: utf-8
import sys

import kmAction
from kmAction import CollectionItem
import utils
from utils import get_args, wf,get_time_expression,from_unix_timestamp


def key_for_record(record: CollectionItem):
    return f"{record.title} {record.contentCreator} {record.titlePinyin}"


def main(workflow):
    query, mis, cache_seconds = get_args()
    collection_type = wf().args[3]
    units = kmAction.quick_access_list(collection_type)
    units = wf().filter(query, units, key_for_record, min_score=1, fold_diacritics=False)
    if units:
        for u in units:
            modify_time = int(u.contentModTime / 1000)
            wf().add_item(
                u.title,
                f"创建人:{u.contentCreator} - 更新时间:{from_unix_timestamp(modify_time)}",
                u.contentKey,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
