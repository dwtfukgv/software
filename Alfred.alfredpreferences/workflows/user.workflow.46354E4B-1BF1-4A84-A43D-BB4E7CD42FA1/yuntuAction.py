#!/usr/bin/env python
# encoding: utf-8

import webUtils

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://yuntu.sankuai.com/v3/online/team"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "yuntu_cookies"


def check_login_status(l_manager, resp):
    if resp.status_code == 200:
        result = resp.json()
        if "status" in result:
            return result.get("status") != 401
    return True


login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME, check_login_status)

DASHBOARD_KEY = "dashboardKey"
DASHBOARD_NAME = "dashboardName"
DASHBOARD_OWNER = "owner"
DASHBOARD_CREATOR = "resourceCreator"
DASHBOARD_CREATE_TIME = "createTime"
DASHBOARD_UPDATE_TIME = "updateTime"
DASHBOARD_FAVORITE = "favorite"
DASHBOARD_LATEST_TIME = "lastestViewTime"

RESOURCE_KEY = "resourceKey"
RESOURCE_NAME = "resourceName"
RESOURCE_TYPE = "resourceType"


def query_paged_favorites_dashboard(page_num=1, page_size=16):
    url = "https://yuntu.sankuai.com/api/proxy/atlas/space/favorites/query"
    params = {"cn": page_num, "sn": page_size}
    pay_load = {
        "favoriteFilter": {
            "resourceCreator": "",
            "resourceName": "",
            "resourceType": "",
        }
    }
    resp = webUtils.post_json(url, login_manager, pay_load, params=params)
    return extract_favorites(resp)


def extract_record(resp):
    if "data" in resp and "items" in resp["data"]:
        items = resp["data"]["items"]
        return [
            {
                DASHBOARD_KEY: item[DASHBOARD_KEY],
                DASHBOARD_NAME: item[DASHBOARD_NAME],
                DASHBOARD_OWNER: item[DASHBOARD_OWNER],
                DASHBOARD_CREATE_TIME: item[DASHBOARD_CREATE_TIME],
                DASHBOARD_UPDATE_TIME: item[DASHBOARD_UPDATE_TIME],
                DASHBOARD_FAVORITE: item[DASHBOARD_FAVORITE],
                DASHBOARD_LATEST_TIME: item[DASHBOARD_LATEST_TIME],
            }
            for item in items
        ]


def extract_favorites(resp):
    if "data" in resp and "items" in resp["data"]:
        items = resp["data"]["items"]
        return [
            {
                DASHBOARD_KEY: item[RESOURCE_KEY],
                DASHBOARD_NAME: item[RESOURCE_NAME],
                DASHBOARD_OWNER: item[DASHBOARD_OWNER],
                DASHBOARD_CREATOR: item[DASHBOARD_CREATOR],
                DASHBOARD_CREATE_TIME: item[DASHBOARD_CREATE_TIME],
                DASHBOARD_UPDATE_TIME: item[DASHBOARD_UPDATE_TIME],
                RESOURCE_TYPE: item[RESOURCE_TYPE],
            }
            for item in items
        ]


def query_paged_recently_view(page_num=1, page_size=16):
    url = "https://yuntu.sankuai.com/api/proxy/atlas/space/dashboards/recentlyView?cn={}&sn={}&filterString=&orderBy=&order=".format(
        page_num, page_size
    )
    resp = webUtils.get(url, login_manager)
    return extract_record(resp)


def query_all_favorite_dashboards():
    current_page_no = 1
    page_size = 16
    all_result = []
    result = query_paged_favorites_dashboard(current_page_no, page_size)
    while result:
        all_result.extend(result)
        if len(result) == page_size:
            current_page_no += 1
            result = query_paged_favorites_dashboard(current_page_no, page_size)
        else:
            break
    return all_result


def query_all_recently_view_dashboards():
    current_page_no = 1
    page_size = 16
    all_result = []
    result = query_paged_recently_view(current_page_no, page_size)
    while result:
        all_result.extend(result)
        if len(result) == page_size:
            current_page_no += 1
            result = query_paged_recently_view(current_page_no, page_size)
        else:
            break
    return all_result


if __name__ == "__main__":
    print(len(query_all_recently_view_dashboards()))
    print(len(query_all_favorite_dashboards()))
