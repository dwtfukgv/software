#!/usr/bin/env python
# encoding: utf-8
import json
import sys

import utils
from utils import url_encode

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web
import utils

LOGIN_URL = "https://coe.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "onecloud-nav__wrapper"))
COOKIE_NAME = "coe_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# cluster field
INCIDENT_ID = "incident_id"
BRIEF = "brief"
CREATE_AT = "create_at"
ORG_PATH = "org_path"
OWNER = "owner"
OCCUR_TIME = "occur_time"
LEVEL = "level"
CATEGORY = "category"

from utils import wf, get_args


def key_for_record(record):
    return "{} {} {} {}".format(
        record[BRIEF], record[ORG_PATH], record[CREATE_AT], record[OWNER]
    )


def main(workflow):
    query, mis, cache_seconds = get_args()
    incidents_list = workflow.cached_data(
        "coe_favorate_incidents",
        lambda: query_all_incidents(10),
        max_age=int(cache_seconds),
    )
    incidents_list = wf().filter(query, incidents_list, key_for_record)

    if incidents_list:
        for incident in incidents_list:
            workflow.add_item(
                incident[BRIEF],
                "[{}]{} - {} ".format(
                    incident[CREATE_AT], incident[ORG_PATH], incident[OWNER]
                ),
                arg=incident[INCIDENT_ID],
                valid=True,
            )
    else:
        workflow.add_item("no result", valid=False)
    workflow.send_feedback()


def search_coe(keyword, page=1, page_size=30):
    url = "https://coe.mws.sankuai.com/api/v1.0/query/incidents"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "Content-Type": "application/json; charset=utf-8"}
    pay_loads = {
        "appkey": "",
        "finders": "",
        "create_end": "",
        "create_start": "",
        "category": [],
        "cause_todo_tags": [],
        "effectLevelDate": [],
        "level": [],
        "level_standard": [],
        "level_standard_category": [],
        "level_standard_id": [],
        "level_start": "",
        "level_end": "",
        "locators": "",
        "key": keyword,
        "orgs": [],
        "page": page,
        "page_size": page_size,
        "occur_end": utils.today_YYHHMM(),
        "occur_start": utils.days_ago_YYHHMM(30),
        "list_type": "all",
        "reason": [],
        "responsible_org_ids": [],
        "tags": [],
        "sort": "desc",
        "sort_by": "create_at",
    }
    post_json = json.dumps(pay_loads)
    wf().logger.info(post_json)
    resp = web.post(url, data=post_json, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    resp_data = resp.json()
    error_msg = resp_data["error"]
    if error_msg:
        raise RuntimeError(error_msg)
    incidents = resp_data["incidents"]
    if incidents:
        return [
            {
                INCIDENT_ID: i["_id"],
                BRIEF: i[BRIEF],
                OCCUR_TIME: i[OCCUR_TIME],
                ORG_PATH: i[ORG_PATH],
                LEVEL: i[LEVEL],
                CATEGORY: i[CATEGORY],
                OWNER: i[OWNER],
            }
            for i in incidents
        ]
    return None


def query_paged_incidents(page_no, page_size=10):
    url = "https://coe.mws.sankuai.com/api/v1.0/my/favorite/incidents"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "Content-Type": "application/json; charset=utf-8"}
    json_data = {"page": page_no, "page_size": page_size, "sort_by": "create_at"}
    resp = web.post(
        url, data=json.dumps(json_data), headers=headers, allow_redirects=False
    )
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_all_incidents(page_size):
    page_no = 1
    resp = query_paged_incidents(page_no, page_size)
    incidents = resp["incidents"]
    total_count = resp["total_count"]
    result = []
    if incidents:
        for i in incidents:
            result.append(get_incident_item(i))
            while total_count > len(result):
                page_no = page_no + 1
                incidents = query_paged_incidents(page_no)["incidents"]
                if not incidents:
                    break
                for i in incidents:
                    result.append(get_incident_item(i))
    return result


def get_incident_item(incident):
    return {
        INCIDENT_ID: incident[INCIDENT_ID],
        BRIEF: incident[BRIEF],
        CREATE_AT: incident[CREATE_AT],
        ORG_PATH: incident[ORG_PATH],
        OWNER: incident[OWNER],
    }


if __name__ == "__main__":
    sys.exit(wf().run(main))
