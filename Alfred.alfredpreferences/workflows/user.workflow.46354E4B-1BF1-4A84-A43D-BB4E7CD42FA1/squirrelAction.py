#!/usr/bin/env python
# encoding: utf-8
import json
import sys

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

LOGIN_URL = "https://squirrel.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "squirrel_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# cluster field
CLUSTER_NAME = "clusterName"
USED_MEM = "usedMemory"
TOTAL_MEM = "totalMemory"
TOPOLOGY = "topology"
CLUSTER_LEVEL = "clusterLevel"
DBA_ALIAS = "dbaAlias"
DBA_NAME = "dbaName"
STATUS = "status"

# cluster group field
GROUP_NAME = "groupName"
GROUP_TYPE = "groupType"
APPLICATION_LOCATION = "applicationLocation"
GROUP_DESC = "description"


def query_paged_clusters(pageNum, limit):
    url = "https://squirrel.mws.sankuai.com/v1/api/clusters/queryMine"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "env": "product"}
    params = {"offset": pageNum * limit, "limit": limit}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_clusters(limit):
    pageNum = 0
    resp = query_paged_clusters(pageNum, limit)
    data = resp["ret"]
    result = []
    if data:
        cluster_list = data["data"]
        total = data["totalCount"]
        result.extend([filter_cluster_fields(r) for r in cluster_list])
        while len(result) < total:
            pageNum = pageNum + 1
            data = query_paged_clusters(pageNum, limit)["ret"]
            total = data["totalCount"]
            cluster_list = data["data"]
            if not cluster_list:
                break
            result.extend([filter_cluster_fields(r) for r in cluster_list])
    return result


def query_paged_cluster_groups(pageNum, limit):
    url = "https://squirrel.mws.sankuai.com/v1/api/clusterGroup/queryMine"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "env": "product"}
    params = {"offset": pageNum * limit, "limit": limit}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_cluster_groups(limit):
    pageNum = 0
    resp = query_paged_cluster_groups(pageNum, limit)
    data = resp["ret"]
    result = []
    if data:
        cluster_list = data["data"]
        total = data["totalCount"]
        result.extend([filter_cluster_group_fields(r) for r in cluster_list])
        while len(result) < total:
            pageNum = pageNum + 1
            data = query_paged_cluster_groups(pageNum, limit)["ret"]
            total = data["totalCount"]
            cluster_list = data["data"]
            if not cluster_list:
                break
            result.extend([filter_cluster_group_fields(r) for r in cluster_list])
    return result


def query_all_cluster_of_group(group_name):
    url = "https://squirrel.mws.sankuai.com/v1/api/clusterGroup/{}/map/list".format(
        group_name
    )
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "env": "product"}
    params = {}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    ret = resp.json()["ret"]
    result = []
    if ret and "unitDetailList" in ret:
        unit_list = ret["unitDetailList"]
        result.extend(unit_list)
    default_cluster = ret["defaultCluster"]
    if default_cluster:
        result.append(
            {"unitName": "default", "clusterName": default_cluster["clusterName"]}
        )
    return result


def filter_cluster_fields(record):
    return {
        CLUSTER_NAME: record[CLUSTER_NAME],
        USED_MEM: record[USED_MEM],
        TOTAL_MEM: record[TOTAL_MEM],
        TOPOLOGY: record[TOPOLOGY],
        DBA_ALIAS: record[DBA_ALIAS],
    }


def filter_cluster_group_fields(record):
    return {
        GROUP_NAME: record[GROUP_NAME],
        GROUP_TYPE: record[GROUP_TYPE],
        GROUP_DESC: record[GROUP_DESC],
        APPLICATION_LOCATION: record[APPLICATION_LOCATION],
    }


def query_resource(keywords, resource_type="Cluster"):
    url = "https://squirrel.mws.sankuai.com/v1/api/commons/queryResource"
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "env": "product",
        "content-type": "application/json",
    }
    params = {"offset": 0, "limit": 20}
    data = {
        "applicationLocation": "beijing",
        "buId": "",
        "limit": 10,
        "offset": 0,
        "resourceName": keywords,
        "resourceType": resource_type,
        "sharedCluster": False,
    }
    json_data = json.dumps(data)

    resp = web.post(
        url, params=params, data=json_data, headers=headers, allow_redirects=False
    )
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    data = resp.json()["ret"]
    records = data["data"]
    return records


if __name__ == "__main__":
    # print query_all_clusters(10)
    pass
