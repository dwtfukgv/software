#!/usr/bin/env python
# encoding: utf-8
import json
import sys

from utils import url_encode

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

LOGIN_URL = "https://cellar.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "cellar_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# cluster field
ID = "id"
GROUP_NAME = "groupName"
GROUP_DESC = "groupDescription"
ROLE = "role"
CELL = "cell"
CELLAR_RD = "cellarRd"
ONLINE_STATUS = "status"

from utils import wf, get_args


def main(workflow):
    query, mis, cache_seconds = get_args()
    # key : deploy name , value : plus id
    cellar_dict = workflow.cached_data(
        "cellar_list_cache", lambda: query_all_clusters(10), max_age=int(cache_seconds)
    )
    cluster_list = list(cellar_dict.keys())
    if query:
        cluster_list = workflow.filter(query, cluster_list)

    if cluster_list:
        for cellar_appkey in cluster_list:
            workflow.add_item(cellar_appkey, arg=cellar_appkey, valid=True)
    else:
        workflow.add_item("no result", valid=False)
    workflow.send_feedback()


def query_paged_clusters(page_no, page_size):
    url = "https://cellar.mws.sankuai.com/api/v1/user/cluster/get"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {"pageNum": page_no, "pageSize": page_size}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_clusters(page_size):
    page_no = 1
    resp = query_paged_clusters(page_no, page_size)
    data = resp["data"]
    result = {}
    if data:
        for cluster in data:
            cluster_list = cluster["dsCluster"]
            remote_appkey = cluster["remoteAppkey"]
            result[remote_appkey] = [filter_cluster_fields(r) for r in cluster_list]
            while data and len(data) == page_size:
                page_no = page_no + 1
                data = query_paged_clusters(page_no)["data"]
                if not data:
                    break
                for c in data:
                    cluster_list = c["dsCluster"]
                    remote_appkey = c["remoteAppkey"]
                    result[remote_appkey] = [
                        filter_cluster_fields(r) for r in cluster_list
                    ]
    return result


def filter_cluster_fields(record):
    return {
        ID: record[ID],
        GROUP_NAME: record[GROUP_NAME],
        GROUP_DESC: record[GROUP_DESC],
        CELL: record[CELL],
        ONLINE_STATUS: record[ONLINE_STATUS],
        ROLE: record[ROLE],
        CELLAR_RD: record[CELLAR_RD],
    }


def search_server_appkey(keyword):
    url = "https://cellar.mws.sankuai.com/api/v1/info/ds/groupAppkeyAndAdmin/get"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {"q": keyword}

    try:
        resp = web.get(url, params=params, headers=headers, allow_redirects=False)
        login_manager.check_login_status(resp)
        resp.raise_for_status()
        result = resp.json()

        if result["success"]:
            # Extract only the serverAppkey from each item in the data
            return [item["serverAppkey"] for item in result["data"]]
        else:
            wf().logger.error(f"API request failed: {result}")
            return []
    except Exception as e:
        wf().logger.error(f"Error occurred while searching for server appkey: {str(e)}")
        return []


def get_cluster_details(serverAppkey):
    url = "https://cellar.mws.sankuai.com/api/v1/info/ds/areaInfoList/get"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {"serverAppkey": serverAppkey}

    try:
        resp = web.get(url, params=params, headers=headers, allow_redirects=False)
        login_manager.check_login_status(resp)
        resp.raise_for_status()
        result = resp.json()

        if result["success"]:
            area_data = result.get("data", [])
            if area_data:
                area_info = area_data[0]
                return {
                    "id": area_info.get("dataserverClusterId"),
                    "businessRd": area_info.get("businessRd"),
                    "groupName": area_info.get("groupName"),
                    "idc": area_info.get("idc"),
                    "primaryRd": area_info.get("primaryRd"),
                }
        else:
            wf().logger.error(f"API request failed: {result}")
            return None
    except Exception as e:
        wf().logger.error(f"Error occurred while getting cluster details: {str(e)}")
        return None


if __name__ == "__main__":
    sys.exit(wf().run(main))
