#!/usr/bin/env python
# encoding: utf-8

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

LOGIN_URL = "https://mafka.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "mafka_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# topic field
ID = "id"
NAME = "name"
APP_KEY = "appkey"
REMARK = "remark"

# consumer field
TOPIC_NAME = "topicName"


def query_paged_topics(pageNum, limit, content=""):
    url = "https://mafka.mws.sankuai.com/mafka/restful/topic/list"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {
        "pageNum": pageNum,
        "limit": limit,
        "type": 1,
        "auth": -1,
        "content": content,
    }
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_topics(limit):
    pageNum = 1
    resp = query_paged_topics(pageNum, limit)
    data = resp["data"]
    result = []
    if data:
        cluster_list = data["list"]
        total = data["total"]
        result.extend([filter_topic_fields(r) for r in cluster_list])
        while len(result) < total:
            pageNum = pageNum + 1
            data = query_paged_topics(pageNum, limit)["data"]
            total = data["total"]
            cluster_list = data["list"]
            if not cluster_list:
                break
            result.extend([filter_topic_fields(r) for r in cluster_list])
    return result


def filter_topic_fields(record):
    return {
        ID: record[ID],
        NAME: record[NAME],
        APP_KEY: record[APP_KEY],
        REMARK: record[REMARK],
    }


def query_paged_consume_group(pageNum, limit, content=""):
    url = "https://mafka.mws.sankuai.com/mafka/restful/consumer/list"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {
        "pageNum": pageNum,
        "limit": limit,
        "type": 3,
        "auth": -1,
        "content": content,
    }
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_consume_groups(limit):
    pageNum = 1
    resp = query_paged_consume_group(pageNum, limit)
    data = resp["data"]
    result = []
    if data:
        cluster_list = data["list"]
        total = data["total"]
        result.extend([filter_consume_fields(r) for r in cluster_list])
        while len(result) < total:
            pageNum = pageNum + 1
            data = query_paged_consume_group(pageNum, limit)["data"]
            total = data["total"]
            cluster_list = data["list"]
            if not cluster_list:
                break
            result.extend([filter_consume_fields(r) for r in cluster_list])
    return result


def filter_consume_fields(record):
    return {
        ID: record[ID],
        NAME: record[NAME],
        APP_KEY: record[APP_KEY],
        REMARK: record[REMARK],
        TOPIC_NAME: record[TOPIC_NAME],
    }
