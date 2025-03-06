#!/usr/bin/python
# @Time     : 2024/3/24 16:40
# @Author   : liuyulong06
# @File     : shepherdAction.py

from typing import List, Dict, Tuple, Optional
from enum import Enum
import init_path
from LoginEnvAwareManager import LoginEnvAwareManager
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webUtils import get_with_env
from utils import Environment

LOGIN_URL = "https://shepherd.mws.sankuai.com"
LOGIN_URL_TEST = "https://shepherd.mws-test.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "shepherd_cookies"
login_awared_manager = LoginEnvAwareManager(
    LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME),
    LoginManager(LOGIN_URL_TEST, WAIT_ELEMENT, COOKIE_NAME + "_TEST"),
)


class Group:
    ID = "id"
    NAME = "name"
    DESC = "description"
    PREFIX = "commonPrefix"


class API:
    ID = "id"
    NAME = "name"
    PATH = "path"
    GROUP_ID = "apiGroupId"
    GROUP_NAME = "apiGroupName"
    DESC = "description"


def key_for_group_record(record: Dict[str, str]) -> str:
    return f"{record[Group.NAME]} {record[Group.DESC]} {record[Group.PREFIX]}"


def key_for_api_record(record: Dict[str, str]) -> str:
    return f"{record[API.NAME]} {record[API.PATH]} {record[API.DESC]} {record[API.GROUP_NAME]}"


def search_shepherd(
    keyword: str = "", env: Environment = Environment.PROD
) -> Tuple[List[Dict], List[Dict]]:
    params = {'query': keyword}
    result = get_with_env("/spapi/v1/search", login_awared_manager, env, params=params)
    if result["code"] == 0:
        return result["data"]["apiGroups"], result["data"]["apis"]
    return [], []


def api_by_group(group_id: int, env: Environment = Environment.PROD) -> List[Dict]:
    relative_url = f"/spapi/v1/apis/{group_id}"
    headers = {"Accept": "application/json, text/plain"}
    return _extract_api_result(
        get_with_env(relative_url, login_awared_manager, env, headers=headers)
    )


def _extract_group_result(resp_json: Dict) -> List[Dict]:
    if "data" in resp_json:
        items = resp_json["data"]
        if items:
            return [
                {
                    Group.ID: item[Group.ID],
                    Group.NAME: item[Group.NAME],
                    Group.DESC: item.get(Group.DESC, ""),
                    Group.PREFIX: item.get(Group.PREFIX, ""),
                }
                for item in items
            ]
    return []


def _extract_api_result(resp_json: Dict) -> List[Dict]:
    if "data" in resp_json:
        items = resp_json["data"]
        if items:
            return [
                {
                    API.ID: item[API.ID],
                    API.NAME: item[API.NAME],
                    API.PATH: item[API.PATH],
                    API.GROUP_ID: item[API.GROUP_ID],
                    API.GROUP_NAME: item[API.GROUP_NAME],
                    API.DESC: item.get(API.DESC, ""),
                }
                for item in items
            ]
    return []


def groups_list(env: Environment = Environment.PROD) -> List[Dict]:
    relative_url = "/spapi/v1/groups/list"
    headers = {"Accept": "application/json, text/plain"}
    resp_json = get_with_env(relative_url, login_awared_manager, env, headers=headers)
    return _extract_group_result(resp_json)


def all_my_api_list(env: Environment = Environment.PROD) -> List[Dict]:
    api_groups = groups_list(env)
    all_my_apis = []
    for g in api_groups:
        apis = api_by_group(g[Group.ID], env)
        if apis:
            all_my_apis.extend(apis)
    return all_my_apis


def build_api_detail_url(api: Dict[str, str]) -> str:
    return (
        f"api-detail?api_group_name={api['apiGroupName']}&api_group_id={api['apiGroupId']}"
        f"&api_name={api['apiName']}&api_id={api['apiId']}&group_tab=api-manage"
    )


def build_api_group_url(api_group: Dict[str, str]) -> str:
    return f"api-group-detail?api_group_name={api_group['apiGroupName']}&api_group_id={api_group['apiGroupId']}"


if __name__ == "__main__":
    print(login_awared_manager.get_cookies(Environment.TEST))
    # print(shepherd.api_by_group(24551, Environment.TEST))
    # print(shepherd.groups_list(Environment.TEST))
    print(all_my_api_list(Environment.TEST))
    # print(shepherd.search_shepherd('phf', Environment.TEST))
