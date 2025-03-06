import json
import init_path
from typing import List, Dict, Any
from dataclasses import dataclass
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import url_encode
import webUtils

LOGIN_URL = "https://raptor.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "layout"))
COOKIE_NAME = "rpt_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

SUCCESS_RESP_CODE = 10000


@dataclass
class Host:
    ip: str
    hostname: str


@dataclass
class Dashboard:
    id: str
    name: str
    desc: str
    is_core: bool
    org: str


@dataclass
class Chart:
    id: str
    name: str


@dataclass
class FrontProject:
    id: str
    domain: str


@dataclass
class Api:
    id: str
    name: str
    title: str


@dataclass
class Log:
    logId: int
    logName: str
    desc: str
    appkey: str


def query_host(keyword: str) -> List[Host]:
    url = f"https://raptor.mws.sankuai.com/raptor/s/hosts/endpoint/list?query={url_encode(keyword)}&query2=&mode=endpoint&limit=10"
    result = webUtils.get(url, login_manager)
    return [
        Host(ip=machine.get("ip", ""), hostname=machine.get("hostname", ""))
        for machine in result.get("result", {}).get("machines", [])
    ]


def get_dashboard_org(dashboard_record: Dict[str, Any]) -> str:
    bg = dashboard_record.get("bg", {}).get("name", "")
    bu = dashboard_record.get("bu", {}).get("name", "")
    org = bg
    if bu:
        org = f"{bg}/{bu}" if bg else bu
    if "contents" in dashboard_record:
        contents = dashboard_record["contents"]
        if contents:
            org += "/" + "/".join(c["name"] for c in contents)
    return org


def my_favorate_dashboard() -> List[Dashboard]:
    url = "https://raptor.mws.sankuai.com/raptor/dashboard/userFavorite"
    result = webUtils.get(url, login_manager)
    if "result" in result:
        return [
            Dashboard(
                id=r["id"],
                name=r["name"],
                desc=r["desc"],
                is_core=r["isCore"],
                org=get_dashboard_org(r),
            )
            for r in result["result"] or []
        ]
    return []


def get_charts_by_dashboard(dashboard_id: str, is_core: bool) -> List[Chart]:
    url = f"https://raptor.mws.sankuai.com/raptor/dashboard/{'core/' if is_core else ''}chartIds?dashboardId={dashboard_id}"
    result = webUtils.get(url, login_manager)
    if result["code"] == SUCCESS_RESP_CODE:
        charts = result.get("result", {}).get("charts", [])
        return [Chart(id=chart["id"], name=chart["name"]) for chart in charts]
    else:
        raise RuntimeError(result["message"])


def search_dashboard(dashboard_name: str, is_core: bool) -> List[Dashboard]:
    url = f"https://raptor.mws.sankuai.com/raptor/dashboard/{'core/' if is_core else ''}searchDashboard?name={url_encode(dashboard_name)}"
    result = webUtils.get(url, login_manager)
    if "result" in result:
        return [
            Dashboard(
                id=dashboard["id"],
                name=dashboard["name"],
                desc="",  # Assuming desc is not provided in search results
                is_core=is_core,
                org=get_dashboard_org(dashboard),
            )
            for dashboard in result["result"] or []
        ]
    return []


def get_front_project() -> List[FrontProject]:
    url = "https://raptor.mws.sankuai.com/cat/mobile/getProject"
    result = webUtils.get(url, login_manager)
    if result["code"] == SUCCESS_RESP_CODE:
        project_list = result.get("result", [])
        return [FrontProject(id=p["id"], domain=p["domain"]) for p in project_list]
    else:
        raise RuntimeError(result["message"])


def get_api_by_project(project_id: str) -> List[Api]:
    url = f"https://raptor.mws.sankuai.com/cat/mobile/getApiByProject?projectId={project_id}"
    result = webUtils.get(url, login_manager)
    if result["code"] == SUCCESS_RESP_CODE:
        result_data = result.get("result", {})
        api_list = []
        if "group" in result_data:
            group_list = result_data["group"]
            api_list.extend(
                [
                    Api(id=g["id"], name=f"API组 - {g['name']}", title=g["title"])
                    for g in group_list
                ]
            )
        if "single" in result_data:
            single_api_list = result_data["single"]
            api_list.extend(
                [
                    Api(id=api["id"], name=api["name"], title=api["title"])
                    for api in single_api_list
                ]
            )
        return api_list
    else:
        raise RuntimeError(result["message"])


def get_my_logs(offset: int = 0, limit: int = 25) -> List[Log]:
    url = "https://raptor.mws.sankuai.com/raptor/logcenter/v2/access/logs"
    data = {"offset": offset, "limit": limit}
    result = webUtils.post_json(url, login_manager, json_payload=data)
    if result.get("code","") == SUCCESS_RESP_CODE:
        logs = result.get("result", {}).get("logs", [])
        return [
            Log(
                logId=log["id"],
                logName=log["logName"],
                desc=log["desc"],
                appkey=log["appkey"],
            )
            for log in logs
        ]
    else:
        raise RuntimeError(result["message"])


def get_all_my_logs() -> List[Log]:
    all_logs = []
    offset = 0
    limit = 100  # 使用较大的limit值以减少API调用次数

    while True:
        logs = get_my_logs(offset, limit)
        all_logs.extend(logs)

        if len(logs) < limit:
            # 如果返回的日志数量小于limit，说明已经获取了所有日志
            break

        offset += limit

    return all_logs


if __name__ == "__main__":
    print(query_host("groupchat02"))

    # 测试新添加的 get_my_logs 函数
    print("Testing get_my_logs function:")
    logs = get_my_logs(offset=0, limit=5)
    for log in logs:
        print(f"Log ID: {log.logId}, Name: {log.logName}, Description: {log.desc}")

    # 测试新添加的 get_all_my_logs 函数
    print("\nTesting get_all_my_logs function:")
    all_logs = get_all_my_logs()
    print(f"Total logs retrieved: {len(all_logs)}")
    for i, log in enumerate(all_logs[:5], 1):  # 只打印前5个日志
        print(f"{i}. Log ID: {log.logId}, Name: {log.logName}, Description: {log.desc}")
    if len(all_logs) > 5:
        print("...")
