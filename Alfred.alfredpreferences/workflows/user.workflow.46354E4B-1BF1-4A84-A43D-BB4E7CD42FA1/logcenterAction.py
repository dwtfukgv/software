#!/usr/bin/python
# encoding: utf-8
from LoginEnvAwareManager import LoginEnvAwareManager
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import Environment, logger
import requests as web

LOGIN_URL = "http://logcenter.data.sankuai.com"
LOGIN_URL_TEST = "http://logcenter.test.data.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "fullpage"))
COOKIE_NAME = "log_center_cookies"

login_manager_prod = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)
login_manager_test = LoginManager(LOGIN_URL_TEST, WAIT_ELEMENT, COOKIE_NAME + "_TEST")
login_manager = LoginEnvAwareManager(login_manager_prod, login_manager_test)
LOG_NAME = "log_name"
DESC = "description"


def query_paged_log(url, env: Environment = Environment.PROD):
    cookies_str = login_manager.get_cookies(env)
    url = login_manager.get_url(url, env)
    headers = {"Cookie": cookies_str}
    resp = web.get(url, headers=headers, allow_redirects=False)
    login_manager.check_login_status(resp, env)
    resp.raise_for_status()
    return resp.json()


def query_logs(select_dep_name,env: Environment = Environment.PROD):
    logs = query_paged_log(
        "/logcenter/rest/logs/?format=json&offset=0&limit=25"
        "&select_dep_name={}".format(select_dep_name),
        env,
    )
    next_url = logs["next"]
    logs_result = [
        {LOG_NAME: log[LOG_NAME], DESC: log[DESC]} for log in logs["results"]
    ]
    while next_url:
        logs = query_paged_log(next_url, env)
        next_url = logs["next"]
        logs_result.extend(
            [{LOG_NAME: log[LOG_NAME], DESC: log[DESC]} for log in logs["results"]]
        )
    return logs_result


def query_my_logs(env: Environment = Environment.PROD):
    return query_logs("lc_operators", env)


def query_all_logs(env: Environment = Environment.PROD):
    return query_logs("all", env)


def key_for_log(log):
    return "{} {}".format(log[LOG_NAME], log[DESC])


if __name__ == "__main__":
    print(query_my_logs())
