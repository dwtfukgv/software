#!/usr/bin/env python
# encoding: utf-8
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import url_encode
import requests as web

LOGIN_URL = "https://digger.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "digger_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)


def query_dashboard(keyword):
    url = "https://digger.sankuai.com/metric/dashboard/list?name={}&create_user=&last_update_user=&org_id=&data_status=1&audit_status=1&page_size=15&page_num=1".format(
        url_encode(keyword)
    )
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    resp = web.get(url, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    result = resp.json()
    if "datas" in result:
        dashboard_list = [d["dashboard"] for d in result["datas"]]
        return [{"id": d["dashboard_id"], "name": d["name"]} for d in dashboard_list]
    return None


def get_favourite():
    url = "https://digger.sankuai.com/metric/favourite/get_favourite"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    resp = web.get(url, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    result = resp.json()
    if "data" in result:
        data = result["data"]
        for k, v in data.items():
            return [{"id": d["business_id"], "name": d["alias_name"]} for d in v]
    return None


if __name__ == "__main__":
    # print query_dashboard('商家')
    pass
