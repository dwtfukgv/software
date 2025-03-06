#!/usr/bin/python
# encoding: utf-8

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

# cluster field
ID = "id"
NAME = "site_name"
APPKEY = "myAppkey"

# login manager
COOKIE_NAME = "oceanus_cookies"
LOGIN_URL = "https://oceanus.mws.sankuai.com/my_site"
WAIT_ELEMENT = EC.presence_of_element_located((By.CLASS_NAME, "my-site"))

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)


def query_paged_sites(page_no):
    url = "https://oceanus.mws.sankuai.com/api/v2/sites/my"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    page_size = 20
    params = {
        "currentPage": page_no,
        "limit": page_size,
        "offset": (page_no - 1) * page_size,
    }
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_sites():
    page_no = 1
    resp = query_paged_sites(page_no)
    data = resp["result"]
    result = []
    if data:
        data_list = data["items"]
        total = data["total"]
        result.extend([filter_site_fields(r) for r in data_list])
        while len(result) < total:
            page_no = page_no + 1
            data = query_paged_sites(page_no)["result"]
            total = data["total"]
            data_list = data["items"]
            if not data_list:
                break
            result.extend([filter_site_fields(r) for r in data_list])
    return result


def filter_site_fields(record):
    return {ID: record[ID], NAME: record[NAME], APPKEY: record[APPKEY]}


if __name__ == "__main__":
    print(query_all_sites())
