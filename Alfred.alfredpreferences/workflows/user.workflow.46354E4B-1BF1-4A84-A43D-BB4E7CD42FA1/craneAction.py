#!/usr/bin/env python
# encoding: utf-8
import json
from utils import url_encode

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

LOGIN_URL = "https://crane.mws.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "crane-app"))
COOKIE_NAME = "crane_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

ITEM_APPKEY = "appKey"
ITEM_TOTAL_TASK_COUNT = "totalTaskCount"
ITEM_CLUSTER = "cluster"
ITEM_OWT = "owt"
ITEM_PDL = "pdl"

ITEM_TASK_ID = "taskid"
ITEM_TASK_NAME = "name"
ITEM_TASK_CREATOR = "creator"
ITEM_TASK_CRONTAB = "crontab"
ITEM_TASK_STATUS = "status"
ITEM_TASK_DESCRIPTION = "description"


def query_appkey_slice(page_num=1, page_size=10, keyword=""):
    url = "https://crane.mws.sankuai.com/appKey/getAppKeySlice?pageNum={}&pageSize={}&appKey={}".format(
        page_num, page_size, url_encode(keyword)
    )
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    resp = web.get(url, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    result = resp.json()
    if "result" in result and "items" in result["result"]:
        items = result["result"]["items"]
        return [
            {
                ITEM_APPKEY: item[ITEM_APPKEY],
                ITEM_TOTAL_TASK_COUNT: item[ITEM_TOTAL_TASK_COUNT],
                ITEM_CLUSTER: item[ITEM_CLUSTER],
                ITEM_OWT: item[ITEM_OWT],
                ITEM_PDL: item[ITEM_PDL],
            }
            for item in items
            if item[ITEM_TOTAL_TASK_COUNT] > 0
        ]
    return []


def query_all_appkey_slice():
    current_page_no = 1
    page_size = 10
    all_result = []
    result = query_appkey_slice(current_page_no, page_size)
    while result:
        all_result.extend(result)
        current_page_no += 1
        result = query_appkey_slice(current_page_no, page_size)
    return all_result


def query_task_slice(page_num=1, page_size=10, appkey=""):
    url = "https://crane.mws.sankuai.com/task/getTaskSlice?pageNum={}&pageSize={}&appKey={}".format(
        page_num, page_size, appkey
    )
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    resp = web.get(url, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_tasks_by_appkey(appkey):
    current_page_no = 1
    page_size = 50
    all_result = []
    resp = query_task_slice(current_page_no, page_size, appkey)
    total = get_total(resp)
    if total > 0:
        add_item_to_result(resp, all_result)
        while len(all_result) < total:
            current_page_no += 1
            resp = query_task_slice(current_page_no, page_size, appkey)
            add_item_to_result(resp, all_result)
    return all_result


def get_status_desc(task_stauts):
    if 1 == task_stauts:
        return "运行"
    elif 2 == task_stauts:
        return "暂停"
    return "unknown"


def add_item_to_result(resp, result_list):
    status = resp["status"]
    if "success" == status and "result" in resp:
        result = resp["result"]
        if "items" in result:
            items = result["items"]
            if items:
                result_list.extend(
                    [
                        {
                            ITEM_TASK_ID: item[ITEM_TASK_ID],
                            ITEM_TASK_NAME: item[ITEM_TASK_NAME],
                            ITEM_TASK_CREATOR: item[ITEM_TASK_CREATOR],
                            ITEM_TASK_CRONTAB: item[ITEM_TASK_CRONTAB],
                            ITEM_TASK_STATUS: get_status_desc(item[ITEM_TASK_STATUS]),
                            ITEM_TASK_DESCRIPTION: item[ITEM_TASK_DESCRIPTION],
                        }
                        for item in items
                    ]
                )


def get_total(resp):
    if "result" in resp and "total" in resp["result"]:
        return resp["result"]["total"]
    return 0


if __name__ == "__main__":
    # print search_history()
    print(query_all_tasks_by_appkey("com.sankuai.waimai.e.task"))
