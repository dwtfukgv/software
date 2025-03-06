#!/usr/bin/python
# encoding: utf-8
import init_path
from LoginEnvAwareManager import LoginEnvAwareManager
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web
from utils import Environment
from webUtils import get_with_env

# cluster field
ID = "id"
CLUSTER_ID = "clusterId"
LEVEL = "level"
NODE_NUM = "node_num"
DATABASE_ID = "id"
DATABASE_NAME = "dbName"
NAME = "name"
DESC = "description"
APPKEY = "appKey"
DBAUSER = "dbaUser"

# login manager
COOKIE_NAME = "rds_cookies"
LOGIN_URL = "https://rds.mws.sankuai.com"
LOGIN_URL_TEST = "https://rds.mws-test.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.CLASS_NAME, "rds-db-list"))

login_manager_prod = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)
login_manager_test = LoginManager(LOGIN_URL_TEST, WAIT_ELEMENT, COOKIE_NAME + "_TEST")
login_awared_manager = LoginEnvAwareManager(login_manager_prod, login_manager_test)


def query_paged_clusters(page_no, env: Environment = Environment.PROD):
    params = {"current": page_no, "page_size": 10, "with_node_num": "true"}
    return get_with_env(
        "/api/v3/resource/clusters", login_awared_manager, env, params=params
    )


def query_all_clusters(env: Environment = Environment.PROD):
    page_no = 1
    resp = query_paged_clusters(page_no, env)
    data = resp["data"]
    result = []
    if data:
        data_list = data["data"]
        total = data["total"]
        result.extend([filter_cluster_fields(r) for r in data_list])
        while len(result) < total:
            page_no = page_no + 1
            data = query_paged_clusters(page_no, env)["data"]
            total = data["total"]
            data_list = data["data"]
            if not data_list:
                break
            result.extend([filter_cluster_fields(r) for r in data_list])
    return result


def query_paged_database(
    cluster_id=None,
    keyword=None,
    page_size=20,
    page_no=None,
    env: Environment = Environment.PROD,
):
    params = {"access_only": "false"}
    if cluster_id:
        params["cluster_id"] = cluster_id
    if keyword:
        params["keyword"] = keyword
    params["current"] = 1 if not page_no else page_no
    params["page_size"] = 20 if not page_size else page_size
    resp = get_with_env(
        "/api/v3/resource/databases", login_awared_manager, env, params=params
    )
    data = resp.get("data", {}).get("data", [])
    return [filter_db_fields(r) for r in data]


def query_databases_by_cluster_id(cluster_id, env: Environment = Environment.PROD):
    return query_paged_database(cluster_id, env=env)


def filter_cluster_fields(record):
    return {
        ID: record[ID],
        NAME: record[NAME],
        DESC: record[DESC],
        APPKEY: record[APPKEY],
        DBAUSER: record[DBAUSER],
        LEVEL: record[LEVEL],
        NODE_NUM: record[NODE_NUM],
    }


def filter_db_fields(record):
    return {
        DATABASE_ID: record[DATABASE_ID],
        DATABASE_NAME: record[DATABASE_NAME] if DATABASE_NAME in record else "",
        DESC: record[DESC],
        CLUSTER_ID: record["serviceGroupId"],
    }


if __name__ == "__main__":
    # print(query_all_clusters())
    print(query_paged_database(199224))
