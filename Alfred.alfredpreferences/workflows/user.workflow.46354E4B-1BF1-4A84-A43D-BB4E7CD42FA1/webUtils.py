import json
import init_path
import requests as web
import LoginManager
import LoginEnvAwareManager
from utils import Environment, wf


def get(url, login_manager: LoginManager = None, params=None, headers=None):
    req_headers = {}
    if login_manager:
        cookies_str = login_manager.get_cookies()
        req_headers = {
            "Cookie": cookies_str,
        }
    if headers:
        req_headers.update(headers)
    resp = web.get(url, params=params, headers=req_headers, allow_redirects=False)
    return get_json_result(resp, login_manager)


def get_with_env(
    url,
    loginEnvAwareManager: LoginEnvAwareManager,
    env: Environment = Environment.PROD,
    params=None,
    headers=None,
):
    req_headers = {}
    if loginEnvAwareManager:
        cookies_str = loginEnvAwareManager.get_cookies(env)
        req_headers = {
            "Cookie": cookies_str,
        }
        url = loginEnvAwareManager.get_url(url, env)
    if headers:
        req_headers.update(headers)

    resp = web.get(url, params=params, headers=req_headers, allow_redirects=False)
    return get_json_result_env(resp, loginEnvAwareManager, env)


def post_json(
    url,
    login_manager: LoginManager = None,
    json_payload=None,
    params=None,
    headers=None,
):
    req_headers = {}
    if login_manager:
        cookies_str = login_manager.get_cookies()
        req_headers = {
            "Cookie": cookies_str,
        }
    if headers:
        req_headers.update(headers)
    resp = web.post(
        url,
        params=params,
        json=json_payload,
        headers=req_headers,
        allow_redirects=False,
    )
    return get_json_result(resp, login_manager)


def post_form(
    url, login_manager: LoginManager = None, data=None, params=None, headers=None
):
    req_headers = {}
    if login_manager:
        cookies_str = login_manager.get_cookies()
        req_headers = {
            "Cookie": cookies_str,
        }
    if headers:
        req_headers.update(headers)
    resp = web.post(
        url, params=params, data=data, headers=req_headers, allow_redirects=False
    )
    return get_json_result(resp, login_manager)


def get_json_result(resp, login_manager=None):
    try:
        if resp.status_code >= 300:
            wf().logger.error(f"请求异常，状态码: {resp.status_code}")
        if login_manager:
            login_manager.check_login_status(resp)
        resp.raise_for_status()
        return resp.json()
    except json.JSONDecodeError:
        wf().logger.error("无法解析 JSON 响应")
        return None
    except web.RequestException as e:
        wf().logger.error(f"请求异常: {str(e)}")
        return None


def get_json_result_env(
    resp,
    login_awared_manger=None,
    env: Environment = Environment.PROD,
):
    try:
        if resp.status_code >= 300:
            wf().logger.error(f"请求异常，状态码: {resp.status_code}")
        if login_awared_manger:
            login_awared_manger.check_login_status(resp, env)
        resp.raise_for_status()
        return resp.json()
    except json.JSONDecodeError:
        wf().logger.error("无法解析 JSON 响应")
        return None
    except web.RequestException as e:
        wf().logger.error(f"请求异常: {str(e)}")
        return None


def post_json_with_env(
    url,
    loginEnvAwareManager: LoginEnvAwareManager,
    env: Environment = Environment.PROD,
    json_payload=None,
    params=None,
    headers=None,
):
    req_headers = {}
    if loginEnvAwareManager:
        cookies_str = loginEnvAwareManager.get_cookies(env)
        req_headers = {
            "Cookie": cookies_str,
        }
        url = loginEnvAwareManager.get_url(url, env)
    if headers:
        req_headers.update(headers)

    resp = web.post(
        url,
        params=params,
        json=json_payload,
        headers=req_headers,
        allow_redirects=False,
    )
    return get_json_result_env(resp, loginEnvAwareManager, env)


def post_form_with_env(
    url,
    loginEnvAwareManager: LoginEnvAwareManager,
    env: Environment = Environment.PROD,
    data=None,
    params=None,
    headers=None,
):
    req_headers = {}
    if loginEnvAwareManager:
        cookies_str = loginEnvAwareManager.get_cookies(env)
        req_headers = {
            "Cookie": cookies_str,
        }
        url = loginEnvAwareManager.get_url(url, env)
    if headers:
        req_headers.update(headers)

    resp = web.post(
        url,
        params=params,
        data=data,
        headers=req_headers,
        allow_redirects=False,
    )
    return get_json_result_env(resp, loginEnvAwareManager, env)
