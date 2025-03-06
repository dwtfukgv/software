#!/usr/bin/env python
# encoding: utf-8
import re
import utils
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web

LOGIN_URL = "https://dev.sankuai.com/cargo/stack"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "cargo_cookies"


def check_dev_login_status(l_manager, resp):
    if resp.status_code == 200:
        json_resp = resp.json()
        if "errorMsg" in json_resp:
            error_msg = json_resp["errorMsg"]
            return  not "userid or username is empty" == error_msg
    return True

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME, check_dev_login_status)

# cargo field
STACK_UUID = "stackuuid"
NAME = "name"
SWIMLANE = "swimlane"
SERVICE_COUNT = "service_count"
MACHINE_ENV = "machine-env"

# git repo field
GIT_APP_KEY = "appkey"
SERVICE_ALIAS = "serviceAlias"
REPO = "repo"
SERVICE_TYPE = "serviceType"

REPO_PATTERN = re.compile("ssh://git@git\\.sankuai\\.com(.*)\\.git")


def query_paged_cargos(pageNum, page_size, stack_filter="own"):
    url = "https://dev.sankuai.com/api/cargo/stack"
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "Referer": "https://dev.sankuai.com/cargo/stack",
        "web-type": "devtools",
    }
    params = {
        "page": pageNum,
        "page_size": page_size,
        "stack_filter": stack_filter,
        "type": "user_stacks_by_page",
    }
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_my_pr_list():
    url = "https://dev.sankuai.com/rest/api/2.0/pull-requests"
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "Referer": "https://dev.sankuai.com/code/home",
        "web-type": "devtools",
    }
    params = {
        "role": "reviewer",
        "start": 0,
        "limit": 100,
        "withAttributes": True,
        "state": "OPEN",
        "order": "create_date_desc",
        "mode": "1",
        "withIssues": "true",
        "mustWithComment": "false",
    }
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    result = resp.json()["result"]["values"]
    if result:
        return [filter_pull_request_fields(r) for r in result]
    return []


def search_cargos(keywords, type="swimlane"):
    url = "https://dev.sankuai.com/api/cargo/search"
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "Referer": "https://dev.sankuai.com/cargo/stack",
        "web-type": "devtools",
    }
    params = {"type": type, "query": keywords}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    result = resp.json()["data"]
    if result:
        result = result["stack"]
        if result:
            return [filter_cargo_search_fields(r) for r in result]
    return []


def query_my_all_cargos(limit):
    pageNum = 0
    resp = query_paged_cargos(pageNum, limit)
    cargo_list = resp["data"]
    total = resp["total"]
    result = []
    if cargo_list:
        result.extend([filter_cargo_fields(r) for r in cargo_list])
        while len(result) < total:
            pageNum = pageNum + 1
            resp = query_paged_cargos(pageNum, limit)
            cargo_list = resp["data"]
            total = resp["total"]
            if not cargo_list:
                break
            result.extend([filter_cargo_fields(r) for r in cargo_list])
    return result


def filter_cargo_fields(record):
    return {
        STACK_UUID: record[STACK_UUID],
        NAME: record[NAME],
        SWIMLANE: record[SWIMLANE],
        SERVICE_COUNT: record[SERVICE_COUNT],
        MACHINE_ENV: record[MACHINE_ENV],
    }


def filter_cargo_search_fields(record):
    return {
        STACK_UUID: record["stack_uuid"],
        NAME: record[NAME],
        SWIMLANE: record[SWIMLANE],
        SERVICE_COUNT: record[SERVICE_COUNT],
        MACHINE_ENV: record[MACHINE_ENV],
    }


def filter_pull_request_fields(record):
    author = record["author"]["user"]["displayName"]
    title = record["title"]
    id = record["id"]
    reviewers_status = []
    to_ref = record["toRef"]
    from_branch = record["fromRef"]["displayId"]
    to_branch = to_ref["displayId"]
    project_key = to_ref["repository"]["project"]["key"]
    name = to_ref["repository"]["name"]
    reviewers = record["reviewers"]
    for r in reviewers:
        approved = r["approved"]
        reviewer = r["user"]["displayName"]
        reviewer_status = reviewer
        if approved:
            reviewer_status += "|Y"
        else:
            reviewer_status += "|N"
        reviewers_status.append(reviewer_status)
    approve_status_by_reviewer = ",".join(reviewers_status)
    return {
        "author": author,
        "title": title,
        "id": id,
        "name": name,
        "key": project_key,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "reviewers": approve_status_by_reviewer,
    }


# code git


def query_paged_code_repo(pageNum, page_size, keyword=""):
    url = "https://dev.sankuai.com/setting/api/service-list"
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "Referer": "https://dev.sankuai.com/",
        "web-type": "devtools",
    }
    params = {"cn": pageNum, "sn": page_size, "type": "all", "keyword": keyword}
    resp = web.get(url, params=params, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp)
    resp.raise_for_status()
    return resp.json()


def query_my_all_code_repos(limit):
    page_no = 1
    resp = query_paged_code_repo(page_no, limit)
    data = resp["data"]
    total = data["tn"]
    result = []
    if data:
        repo_list = data["data"]
        result.extend([filter_repos_fields(r) for r in repo_list])
        while len(result) < total:
            page_no = page_no + 1
            resp = query_paged_code_repo(page_no, limit)
            data = resp["data"]
            total = data["tn"]
            repo_list = data["data"]
            if not repo_list:
                break
            result.extend([filter_repos_fields(r) for r in repo_list])
    return result


def filter_repos_fields(record):
    return {
        GIT_APP_KEY: record[GIT_APP_KEY],
        SERVICE_ALIAS: record[SERVICE_ALIAS],
        REPO: extra_repo_name(record[REPO]),
        # REPO: record[REPO],
        SERVICE_TYPE: record[SERVICE_TYPE],
    }


def extra_repo_name(repo_url):
    try:
        match_result = REPO_PATTERN.match(repo_url)
        return match_result.group(1)
    except:
        return "error when parse repo address"


if __name__ == "__main__":
    repo = "ssh://git@git.sankuai.com/wm/waimai_kv_group_b_bizauth.git"
    extra_repo_name(repo)
    print(query_my_pr_list())
