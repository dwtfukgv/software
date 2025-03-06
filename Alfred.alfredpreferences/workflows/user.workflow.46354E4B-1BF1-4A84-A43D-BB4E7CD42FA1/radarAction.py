#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime, timedelta, time

import utils
import webUtils
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://radar.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "layout"))
COOKIE_NAME = "radar_cookies"
login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# event field
RADAR_ID = "id"
RADAR_INCIDENT_BRIEF = "incident_brief"
RADAR_ORG = "org"
RADAR_STATUS = "status"
RADAR_LEVEL = "level"
RADAR_COMMANDER = "commander"
RADAR_CREATE_AT = "create_at"


def query_paged_events(pageNum=1, limit=100, category="all", handler="", org_id=None):
    url = "https://radar.mws.sankuai.com/api/em/display/events"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str, "env": "product"}
    today = datetime.today().date()
    seven_days_ago = today - timedelta(days=1)
    start_date = utils.unix_timestamp(seven_days_ago)
    end_date = utils.unix_timestamp(
        datetime.combine(today, time(hour=23, minute=59, second=59))
    )
    json_payload = {
        "id": [],
        "key": "",
        "level": [],
        "status": [],
        "handler": handler,
        "source": [],
        "tag": [],
        "blocked": "0",
        "org_id": org_id,
        # "start_date": utils.unix_timestamp(today) * 1000,
        # "end_date": utils.unix_timestamp(seven_days_ago) * 1000,
        "start_date": start_date * 1000,
        "end_date": end_date * 1000,
        "check_status": [],
        "current_page": pageNum,
        "page_size": limit,
        "category": "all",
    }
    resp_json = webUtils.post_json(
        url, login_manager, json_payload=json_payload, headers=headers
    )
    return extract_event(resp_json)


def extract_event(resp_json):
    if "result" in resp_json and "data" in resp_json["result"]:
        items = resp_json["result"]["data"]
        if items:
            return [
                {
                    RADAR_ID: item[RADAR_ID],
                    RADAR_INCIDENT_BRIEF: item[RADAR_INCIDENT_BRIEF],
                    RADAR_ORG: item[RADAR_ORG],
                    RADAR_STATUS: item[RADAR_STATUS],
                    RADAR_LEVEL: item[RADAR_LEVEL],
                    RADAR_COMMANDER: item[RADAR_COMMANDER],
                    RADAR_CREATE_AT: item[RADAR_CREATE_AT],
                }
                for item in items
            ]
    return []


def query_all_event(org_id):
    current_page_no = 1
    page_size = 100
    all_result = []
    result = query_paged_events(current_page_no, page_size, org_id=org_id)
    # while result:
    #     all_result.extend(result)
    #     if len(result) == page_size:
    #         current_page_no += 1
    #         result = query_paged_events(current_page_no, page_size, org_id)
    #     else:
    #         break
    return result


def query_my_event(mis):
    current_page_no = 1
    page_size = 16
    all_result = []
    result = query_paged_events(current_page_no, page_size, category="own", handler=mis)
    while result:
        all_result.extend(result)
        if len(result) == page_size:
            current_page_no += 1
            result = query_paged_events(current_page_no, page_size, mis)
        else:
            break
    return all_result


if __name__ == "__main__":
    print(query_my_event("pingxumeng"))
