#!/usr/bin/python
# encoding: utf-8
import sys

import fsdAction
from fsdAction import query_all_release_plan_list
from utils import wf, get_args, from_unix_timestamp


def key_for_record(test_apply_item):
    return test_apply_item["name"]


def main(workflow):
    query, mis, cache_seconds = get_args()
    online_plan_list = query_all_release_plan_list()
    online_plan_list = wf().filter(
        query, online_plan_list, key_for_record, min_score=10
    )
    if online_plan_list:
        for online_plan in online_plan_list:
            wf().add_item(
                online_plan[fsdAction.FSD_FILED_NAME],
                "上线时间:{}".format(
                    from_unix_timestamp(online_plan[fsdAction.FSD_FILED_ONLINE_TIME] / 1000)
                ),
                online_plan[fsdAction.FSD_FILED_ONLINE_ID],
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
    # delete_cookies(LOG_CENTER_COOKIE_NAME)
