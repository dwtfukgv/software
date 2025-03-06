#!/usr/bin/python
# encoding: utf-8
import sys

import fsdAction
from fsdAction import query_all_test_apply_list
from utils import wf, get_args, from_unix_timestamp


def key_for_test_apply(test_apply_item):
    return test_apply_item["name"]


def main(workflow):
    query, mis, cache_seconds = get_args()
    test_apply_list = query_all_test_apply_list()
    test_apply_list = wf().filter(query, test_apply_list, key_for_test_apply)
    if test_apply_list:
        for test_apply in test_apply_list:
            source = test_apply[fsdAction.FSD_FILED_SOURCE]
            med_id = test_apply[fsdAction.FSD_FILED_MED_ID]
            apply_id = test_apply[fsdAction.FSD_FILED_APPLY_ID]
            online_time = test_apply[fsdAction.FSD_FILED_ONLINE_TIME]
            online_time_desc = ""
            if online_time:
                online_time_desc = "上线时间:{}".format(
                    from_unix_timestamp(online_time / 1000)
                )
            if source == 1:
                query = "testApplyDetail/{}".format(apply_id)
            else:
                query = "deliveryDetailMed/{}".format(med_id)
            wf().add_item(
                "[{}]{}".format(
                    test_apply[fsdAction.FSD_FILED_APPLY_STATUS],
                    test_apply[fsdAction.FSD_FILED_NAME],
                ),
                online_time_desc,
                query,
                valid=True,
            )
    else:
        wf().add_item("no result", valid=False)
    wf().send_feedback()


if __name__ == "__main__":
    sys.exit(wf().run(main))
    # delete_cookies(LOG_CENTER_COOKIE_NAME)
