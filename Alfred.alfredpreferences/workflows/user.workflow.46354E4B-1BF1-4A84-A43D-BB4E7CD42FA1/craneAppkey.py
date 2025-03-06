#!/usr/bin/python
# encoding: utf-8
import sys

import craneAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {} {}".format(
        record[craneAction.ITEM_APPKEY],
        record[craneAction.ITEM_CLUSTER],
        record[craneAction.ITEM_OWT],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    records = wf().cached_data(
        "crane_appkeys", craneAction.query_all_appkey_slice, max_age=int(cache_seconds)
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record[craneAction.ITEM_APPKEY],
                "任务数:{} 业务线:{} 集群:{}".format(
                    record[craneAction.ITEM_TOTAL_TASK_COUNT],
                    record[craneAction.ITEM_OWT],
                    record[craneAction.ITEM_CLUSTER],
                ),
                record[craneAction.ITEM_APPKEY],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
