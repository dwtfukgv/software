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


def start_refresh_cache_task(page_id):
    cmd = [sys.executable, __file__, "--update", "-pageId", page_id]
    run_in_background(get_update_task_key(page_id), cmd)


def is_refresh_running(page_id):
    return is_running(get_update_task_key(page_id))


def update_cache(page_id):
    all_pages = kmAction.get_all_sub_pages(page_id)
    wf().cache_data(get_pages_cache_key(page_id), all_pages)


def get_pages_cache_key(page_id):
    return f"km_pages_{page_id}_cached"


def get_update_task_key(page_id):
    return f"update_km_pages_{page_id}"


def main(workflow):
    query, mis, cache_hours = get_args()
    page_id = wf().args[3] if len(wf().args) > 3 else None
    km_page_cache_seconds = int(cache_hours) * 3600
    cache_key = get_pages_cache_key(page_id)
    is_first_run = wf().cached_data_age(cache_key) == 0
    if not wf().cached_data_fresh(cache_key, max_age=km_page_cache_seconds):
        # 如果已过期，后台任务刷新
        start_refresh_cache_task(page_id)
    if is_refresh_running(page_id):
        # 如果正在运行，添加刷新提示
        wf().rerun = 5
        if is_first_run:
            wf().add_item("文档索引中，加载时间视文档数量而不同", valid=False)
            wf().send_feedback()
            return
        else:
            wf().add_item("文档索引更新中...时间视文档数量而不同", valid=False)
    # 无视缓存时间，取上次已缓存的结果
    all_my_pages = wf().cached_data(
        cache_key,
        lambda: kmAction.get_all_sub_pages(page_id),
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
    wf().add_item("打开根目录文档", "", page_id, valid=True)
    if all_my_pages:
        for page in all_my_pages:
            modify_time = utils.from_unix_timestamp_HHMM(int(page.modifyTime) / 1000)
            wf().add_item(
                page.title,
                f"{page.path} - {modify_time}",
                page.contentId,
                valid=True,
            )
    wf().send_feedback()


if __name__ == "__main__":
    # 处理更新模式
    if "--update" in sys.argv:
        page_id = None
        try:
            page_id_index = sys.argv.index("-pageId")
            if page_id_index + 1 < len(sys.argv):
                page_id = sys.argv[page_id_index + 1]
                if page_id:
                    page_id = page_id.strip()
                    update_cache(page_id)
        except ValueError:
            pass
        sys.exit(0)
    sys.exit(wf().run(main))
