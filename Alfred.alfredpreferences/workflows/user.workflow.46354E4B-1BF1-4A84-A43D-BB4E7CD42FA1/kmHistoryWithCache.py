#!/usr/bin/env python
# encoding: utf-8
import os
import sys

import kmAction
from kmAction import UnitItem
import utils
from utils import get_args, wf
from workflow.background import run_in_background, is_running

KM_CACHE_HISTORY_LIST = "km_history_list"
KM_REFRESH_HISTORY_PROCESS = "update_km_history_list"


def key_for_record(record: UnitItem):
    return f"{record.title} {record.creator} {record.titlePinyin}"


def get_operation_time(item: UnitItem):
    return item.operatorTime


def start_refresh_cache_task():
    cmd = [
        sys.executable,
        __file__,
        "--update",
    ]
    run_in_background(KM_REFRESH_HISTORY_PROCESS, cmd)


def is_refresh_running():
    return is_running(KM_REFRESH_HISTORY_PROCESS)


def update_cache():
    km_history_limit = os.getenv("km_history_limit", "200")
    km_history_limit = int(km_history_limit)
    wf().cache_data(KM_CACHE_HISTORY_LIST, kmAction.query_limit_operation_history(km_history_limit))


def main(workflow):
    query, mis, cache_seconds = get_args()
    km_history_limit = int(os.getenv("km_history_limit", "200"))
    
    units = wf().cached_data(KM_CACHE_HISTORY_LIST, lambda: kmAction.query_limit_operation_history(km_history_limit), max_age=int(cache_seconds))
    
    if not wf().cached_data_fresh(KM_CACHE_HISTORY_LIST, max_age=int(cache_seconds)):
        start_refresh_cache_task()
    if is_refresh_running():
        wf().rerun = 1

    units = wf().filter(query, units, key_for_record, min_score=1, fold_diacritics=False)
    if units:
        units.sort(key=get_operation_time, reverse=True)
        for u in units:
            operation_time = utils.from_unix_timestamp(
                int(u.operatorTime) / 1000 if u.operatorTime else 0
            )
            wf().add_item(
                u.title,
                f"创建人:{u.creator} - 浏览时间:{operation_time}",
                u.pageId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    if "--update" in sys.argv:
        update_cache()
        sys.exit(0)
    sys.exit(wf().run(main))
