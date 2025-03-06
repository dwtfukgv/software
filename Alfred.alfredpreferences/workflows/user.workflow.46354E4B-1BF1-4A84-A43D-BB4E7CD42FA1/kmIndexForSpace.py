#!/usr/bin/env python
# encoding: utf-8

import os
import sys

import kmAction
from kmAction import PageItem
import utils
from utils import get_args, wf
from workflow.background import run_in_background, is_running


def key_for_record(record: PageItem):
    return f"{record.title} {record.path} {record.titlePinyin}"


def start_refresh_cache_task(space_id):
    cmd = [sys.executable, __file__, "--update", "-spaceId", f"{space_id}"]
    run_in_background(get_update_task_key(space_id), cmd)


def is_refresh_running(space_id):
    return is_running(get_update_task_key(space_id))


def update_cache(space_id):
    all_pages = kmAction.get_space_pages(space_id)
    wf().cache_data(get_cache_key(space_id), all_pages)


def get_cache_key(space_id):
    return f"km_pages_{space_id}_cached"


def get_update_task_key(space_id):
    return f"update_km_pages_{space_id}"


def main(workflow):
    query, mis, cache_hours = get_args()
    space_id = wf().args[3] if len(wf().args) > 3 else None
    if not space_id:
        space_id = kmAction.get_space_id_by_mis(mis)
    km_page_cache_seconds = int(cache_hours) * 3600
    pages_cache_key = get_cache_key(space_id)
    is_first_run = wf().cached_data_age(pages_cache_key) == 0
    if not wf().cached_data_fresh(pages_cache_key, max_age=km_page_cache_seconds):
        start_refresh_cache_task(space_id)
    if is_refresh_running(space_id):
        wf().rerun = 5
        if is_first_run:
            wf().add_item("文档索引中，加载时间视文档数量而不同", valid=False)
            wf().send_feedback()
            return
        else:
            wf().add_item("文档索引更新中...时间视文档数量而不同", valid=False)

    all_my_pages = wf().cached_data(
        pages_cache_key,
        lambda: kmAction.get_space_pages(space_id),
        max_age=0,
    )
    all_my_pages = wf().filter(
        query,
        all_my_pages,
        key_for_record,
        min_score=1,
        max_results=20,
        fold_diacritics=False,
    )
    if all_my_pages:
        for page in all_my_pages:
            modify_time = utils.from_unix_timestamp_HHMM(int(page.modifyTime) / 1000)
            wf().add_item(
                page.title,
                f"{page.path} - {modify_time}",
                page.contentId,
                valid=True,
            )
    else:
        wf().add_item("no result", "", query, valid=True)
    wf().send_feedback()


if __name__ == "__main__":
    query, mis, cache_seconds = get_args()
    # 处理更新模式
    if "--update" in sys.argv:
        if "--update" in sys.argv:
            space_id = None
            try:
                space_id_index = sys.argv.index("-spaceId")
                if space_id_index + 1 < len(sys.argv):
                    space_id = sys.argv[space_id_index + 1]
                if space_id:
                    space_id = space_id.strip()
            except ValueError:
                pass
            if not space_id:
                space_id = kmAction.get_space_id_by_mis(mis)
            update_cache(space_id)
        sys.exit(0)
    sys.exit(wf().run(main))
