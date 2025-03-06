#!/usr/bin/env python
# encoding: utf-8

import webUtils
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://domain.mws.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "navbar"))
COOKIE_NAME = "domain_cookies"
login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

# event field
DOMAIN_ID = "id"
DOMAIN_FULLNAME = "fullname"
DOMAIN_DESC = "description"
DOMAIN_ENV = "env"
DOMAIN_NET = "net"
# 等级
DOMAIN_RANK = "rank"
# 类别 NG/MGW
DOMAIN_KIND = "kind"
# 负责人
DOMAIN_OWNER = "owner"
# 用途
DOMAIN_USAGE = "usage"

DOMAIN_TECHTEAM = "techteam"
# 认证状态
DOMAIN_AUTHED = "authed"


def query_paged_domains(page_num, page_size, scope="all", keyword=None):
    url = "https://domain.mws.sankuai.com/api/entries"
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}
    params = {
        "order": "match",
        "scope": scope,
        "page": page_num,
        "page_size": page_size,
        "type": "all",
    }
    if keyword:
        params["search"] = keyword
    resp_json = webUtils.get(url, login_manager, params=params, headers=headers)
    return extract_event(resp_json)


def extract_event(resp_json):
    if "entries" in resp_json:
        items = resp_json["entries"]
        if items:
            return [
                {
                    DOMAIN_ID: item[DOMAIN_ID],
                    DOMAIN_FULLNAME: item[DOMAIN_FULLNAME],
                    DOMAIN_DESC: item[DOMAIN_DESC],
                    DOMAIN_ENV: "线上" if "prod" == item[DOMAIN_ENV] else "线下",
                    DOMAIN_NET: "外网" if "external" == item[DOMAIN_NET] else "内网",
                    DOMAIN_RANK: "核心" if "external" == item[DOMAIN_NET] else "内网",
                    DOMAIN_USAGE: item[DOMAIN_USAGE],
                    DOMAIN_TECHTEAM: item[DOMAIN_TECHTEAM],
                    DOMAIN_AUTHED: item[DOMAIN_AUTHED],
                    DOMAIN_OWNER: item[DOMAIN_OWNER],
                    DOMAIN_KIND: item[DOMAIN_KIND],
                }
                for item in items
            ]
    return []


def query_domain(scope="all", keyword=None):
    current_page_no = 1
    page_size = 20
    all_result = []
    result = query_paged_domains(current_page_no, page_size, scope, keyword)
    while result:
        all_result.extend(result)
        if len(result) == page_size:
            current_page_no += 1
            result = query_paged_domains(current_page_no, page_size, scope, keyword)
        else:
            break
    return all_result


def query_my_domain():
    return query_domain("mine")


if __name__ == "__main__":
    print(query_paged_domains(1, 20, "all", "open"))
