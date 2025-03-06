#!/usr/bin/env python
# encoding: utf-8
import sys

import kmAction
from kmAction import UnitItem
import os
from utils import get_args, wf, from_unix_timestamp
from workflow.background import run_in_background, is_running

KM_CACHE_EDIT_LATEST_LIST = "km_latest_edit_list"
KM_REFRESH_EDIT_LIST_PROCESS = "update_km_latest_edit_list"


def key_for_record(record: UnitItem):
    return f"{record.title} {record.creator} {record.titlePinyin}"


def get_modify_time(item: UnitItem):
    return item.modifyTime


def start_refresh_cache_task():
    cmd = [
        sys.executable,
        __file__,
        "--update",
    ]
    run_in_background(KM_REFRESH_EDIT_LIST_PROCESS, cmd)


def is_refresh_running():
    return is_running(KM_REFRESH_EDIT_LIST_PROCESS)


def update_cache():
    wf().cache_data(KM_CACHE_EDIT_LATEST_LIST, kmAction.latest_edit_list())


def main(workflow):
    query, mis, cache_seconds = get_args()
    km_edit_history = wf().cached_data(KM_CACHE_EDIT_LATEST_LIST, kmAction.latest_edit_list, 0)
    if not wf().cached_data_fresh(KM_CACHE_EDIT_LATEST_LIST, max_age=5):
        start_refresh_cache_task()
    if is_refresh_running():
        wf().rerun = 1

    km_edit_history = wf().filter(query, km_edit_history, key_for_record, min_score=1, fold_diacritics=False)
    if km_edit_history:
        km_edit_history.sort(key=get_modify_time, reverse=True)
        for u in km_edit_history:
            modify_time = from_unix_timestamp(int(u.modifyTime) / 1000)
            wf().add_item(
                u.title,
                f"创建人:{u.creator} - 更新时间:{modify_time}",
                u.pageId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    # 处理更新模式
    if "--update" in sys.argv:
        update_cache()
        sys.exit(0)
    sys.exit(wf().run(main))
