import json
import init_path
from typing import List, Dict, Any
from dataclasses import dataclass
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import url_encode
import webUtils

LOGIN_URL = "https://es.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "eagle_cookies"

login_manager = LoginManager(
    LOGIN_URL,
    WAIT_ELEMENT,
    COOKIE_NAME,
    login_check_callback=lambda l, resp: resp.json().get("code") != -1,
)

@dataclass
class ESCluster:
    clusterId: int
    clusterName: str
    clusterGroupName: str
    desc: str
    owt: str
    esStatus: str
    appkey: str
    sla: str
    createTime: str


@dataclass
class ESClusterGroup:
    clusterGroupId: int
    groupName: str
    clusterGroupAppkey: str


def parse_cluster_group(group_data: Dict[str, Any]) -> ESClusterGroup:
    return ESClusterGroup(
        clusterGroupId=group_data["id"],
        groupName=group_data["clusterGroupName"],
        clusterGroupAppkey=group_data["clusterGroupAppkey"],
    )


def parse_cluster(log_data: Dict[str, Any]) -> ESCluster:
    return ESCluster(
        clusterId=log_data["id"],
        clusterName=log_data["clusterName"],
        clusterGroupName=log_data["clusterGroupName"],
        desc=log_data["desc"],
        owt=log_data["owt"],
        esStatus=log_data["esStatus"],
        appkey=log_data["appkey"],
        sla=log_data["sla"],
        createTime=(
            log_data["createTime"].split("T")[0] if log_data.get("createTime") else ""
        ),
    )


def get_clusters_by_type(type: str, page_no=0, page_size=20) -> List[ESCluster]:
    """
    根据指定的类型获取日志列表。

    Args:
        type (str): 日志类型，例如 "mine" 表示获取当前用户的日志， "all"代表全部
        page_no (int, optional): 页码，默认为0。
        page_size (int, optional): 每页显示的日志数量，默认为20。

    Returns:
        List[Log]: 返回包含Log对象的列表。

    Raises:
        可能会抛出网络请求相关的异常，如连接错误、超时等。
    """
    url = f"{LOGIN_URL}/webapi/cluster/list?clusterName=&owt=&version=&coreVersion=&status=&order=ASC"
    params = {"type": type, "pageNumber": page_no, "pageSize": page_size}
    result = webUtils.get(url, login_manager, params=params)
    rows = result.get("data", {}).get("rows", [])
    return [parse_cluster(r) for r in rows]


def get_all_clusters_by_type(type: str) -> List[ESCluster]:
    all_logs = []
    page_no = 0
    while True:
        logs = get_clusters_by_type(type, page_no)
        if not logs:
            break
        all_logs.extend(logs)
        page_no += 1
    return all_logs


def get_cluster_groups(
    my_cluster_group: bool = False, page_no: int = 0, page_size: int = 10
) -> List[ESClusterGroup]:
    url = f"{LOGIN_URL}/webapi/clusterGroup/list"
    params = {
        "myClusterGroup": str(my_cluster_group).lower(),
        "clusterGroupName": "",
        "pageNumber": page_no,
        "pageSize": page_size,
        "order": "ASC",
        "sort": "",
    }
    result = webUtils.get(url, login_manager, params=params)
    rows = result.get("data", {}).get("rows", [])
    return [parse_cluster_group(r) for r in rows]


def get_all_cluster_groups(my_cluster_group: bool = True) -> List[ESClusterGroup]:
    all_groups = []
    page_no = 0
    while True:
        groups = get_cluster_groups(my_cluster_group, page_no)
        if not groups:
            break
        all_groups.extend(groups)
        page_no += 1
    return all_groups


if __name__ == "__main__":
    logs = get_all_clusters_by_type("all")
    if logs:
        print(f"获取到 {len(logs)} 条日志")
        print("第一条日志信息：")
        print(f"日志ID: {logs[0].clusterId}")
        print(f"集群名称: {logs[0].clusterName}")
        print(f"集群组名称: {logs[0].clusterGroupName}")
        print(f"描述: {logs[0].desc}")
        print(f"OWT: {logs[0].owt}")
        print(f"ES状态: {logs[0].esStatus}")
        print(f"Appkey: {logs[0].appkey}")
        print(f"SLA: {logs[0].sla}")
        print(f"创建时间: {logs[0].createTime}")
    else:
        print("未获取到日志信息")
