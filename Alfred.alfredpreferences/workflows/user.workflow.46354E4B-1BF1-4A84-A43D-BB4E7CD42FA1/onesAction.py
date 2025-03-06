#!/usr/bin/env python
# encoding: utf-8
import datetime as dt
import getpass

import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from utils import url_encode, hanzi_to_pinyin, wf, BaseItem, DateTimeUtils
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webUtils import get

login_manager = LoginManager(
    "https://ones.sankuai.com",
    EC.presence_of_element_located((By.ID, "mainContainer")),
    "ones_cookies",
    login_check_callback=lambda l, resp: resp.json().get("status") != 401,
)

ONES_TYPE_DICT = {"REQUIREMENT": "需求", "DEVTASK": "开发任务", "DEFECT": "缺陷"}


# 定义数据结构
@dataclass
class MyOnesItem(BaseItem):
    """
    指派给我的ones
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name: str
    state: str
    onesId: int
    projectId: int
    priority: str
    onesType: str
    onesTypeDesc: str
    expectStart: str
    expectClose: str
    titlePinyin: str = ""


@dataclass
class OnesProject(BaseItem):
    """
    Ones项目
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name: str
    level: str
    projectId: str
    state: str
    category: str
    defaultPathkey: str
    pmisApplicationState: str
    createdAt: str
    titlePinyin: str = ""

    @classmethod
    def from_api_response(cls, item: Dict[str, Any]) -> "OnesProject":
        return cls(
            name=item.get("name", {}).get("value", ""),
            level=item.get("level", ""),
            projectId=item.get("id", {}).get("value", ""),
            state=item.get("state", {}).get("value", ""),
            category=item.get("category", {}).get("value", ""),
            defaultPathkey=item.get("defaultTab", {}).get("pathKey", ""),
            pmisApplicationState=item.get("pmisApplicationState", {}).get("value", ""),
            createdAt=cls.format_date(item.get("createdAt", {}).get("value")),
        )

    @staticmethod
    def format_date(timestamp):
        """将时间戳转换为可读的日期格式"""
        if timestamp:
            try:
                return DateTimeUtils.from_timestamp_date(timestamp)
            except ValueError:
                return ""
        return ""


def query_my_ones(page_no: int = 1, page_size: int = 50) -> List[MyOnesItem]:
    """
    指派给我的ones

    Args:
        page_no (int, optional): 页码. 默认是 1.
        page_size (int, optional): 每页大小. 默认是 50.

    Returns:
        List[MyOnesItem]: 操作历史列表
    """
    # reqTaskDefect=REQUIREMENT,DEVTASK,DEFECT 需求，开发任务和缺陷
    url = f"https://ones.sankuai.com/api/proxy/layout/card?type=LAYOUT_WORKBENCH&cn={page_no}&sn={page_size}&needFieldConfig=false&cardId=48853&tabName=3&reqTaskDefect=REQUIREMENT%2CDEVTASK%2CDEFECT"
    result = get(url, login_manager)
    items = result.get("data", {}).get("data", {}).get("items", [])
    return [
        MyOnesItem(
            name=item.get("name", {}).get("value", ""),
            state=item.get("state", {}).get("name", ""),
            onesId=int(item.get("id", {}).get("value", 0)),
            projectId=int(item.get("projectId", {}).get("id", 0)),
            priority=item.get("priority", {}).get("value", ""),
            onesType=item.get("type", ""),
            onesTypeDesc=ONES_TYPE_DICT.get(item.get("type", ""), ""),
            expectStart=format_date(item.get("expectStart", {}).get("value")),
            expectClose=format_date(item.get("expectClose", {}).get("value")),
        )
        for item in items
    ]


def query_space(
    page_no: int = 1, page_size: int = 30, category: str = "MY_LAST_VISIT"
) -> List[OnesProject]:
    """
    最近查看的空间列表
    Args:
        page_no (int, optional): 页码. 默认是 1.
        page_size (int, optional): 每页大小. 默认是 50.

    Returns:
        List[OnesProject]: ones空间列表
    """
    url = f"https://ones.sankuai.com/api/proxy/project/category/search/detail?isArchived=false"
    params = {"cn": page_no, "sn": page_size, "category": category}
    result = get(url, login_manager=login_manager, params=params)
    items = result.get("data", {}).get("items", [])
    return [OnesProject.from_api_response(item) for item in items]


def format_date(timestamp):
    """将时间戳转换为可读的日期格式"""
    if timestamp:
        try:
            return dt.datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")
        except ValueError:
            return ""
    return ""


if __name__ == "__main__":
    ones_items = query_my_ones()
    for item in ones_items:
        print(f"Name: {item.name}")
        print(f"State: {item.state}")
        print(f"ID: {item.onesId}")
        print(f"Project ID: {item.projectId}")
        print(f"Priority: {item.priority}")
        print(f"Type: {item.onesType}")
        print(f"Expected Start: {item.expectStart}")
        print(f"Expected Close: {item.expectClose}")
        print("---")

    ones_projects = query_space()
    for project in ones_projects:
        print(f"Name: {project.name}")
        print(f"ID: {project.id}")
        print(f"State: {project.state}")
        print(f"Category: {project.category}")
        print(f"Default Pathkey: {project.defaultPathkey}")
        print(f"PMIS Application State: {project.pmisApplicationState}")
        print(f"Created At: {project.createdAt}")
        print("---")
