#!/usr/bin/python
# encoding: utf-8
import sys

import craneAction
from utils import get_args, wf


def key_for_record(record):
    return "{} {} {}".format(
        record[craneAction.ITEM_TASK_NAME],
        record[craneAction.ITEM_TASK_DESCRIPTION],
        record[craneAction.ITEM_TASK_CREATOR],
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    import os

    crane_appkey = os.getenv("crane_appkey")
    records = wf().cached_data(
        "crane_appkey_tasks_{}".format(crane_appkey),
        lambda: craneAction.query_all_tasks_by_appkey(crane_appkey),
        max_age=int(cache_seconds),
    )
    records = wf().filter(query, records, key_for_record)
    if records:
        for record in records:
            wf().add_item(
                record[craneAction.ITEM_TASK_NAME],
                "[{}][{}] by {} - {}".format(
                    record[craneAction.ITEM_TASK_STATUS],
                    record[craneAction.ITEM_TASK_CRONTAB],
                    record[craneAction.ITEM_TASK_CREATOR],
                    record[craneAction.ITEM_TASK_DESCRIPTION],
                ),
                record[craneAction.ITEM_TASK_NAME],
                valid=True,
            )
    wf().add_item(query, arg=query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    # print(query_all_records())
    sys.exit(wf().run(main))
