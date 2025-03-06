#!/usr/bin/env python
# encoding: utf-8
import datetime as dt
import getpass

import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from utils import url_encode, hanzi_to_pinyin, wf, BaseItem
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import logging
import uuid
import webUtils

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 常量定义
LOGIN_URL = "https://km.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "km_cookies"

# 初始化登录管理器
login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)


# 定义数据结构
@dataclass
class CollectionItem(BaseItem):
    """
    收藏列表项
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    contentKey: str
    contentType: str
    title: str
    contentCreator: str
    contentModTime: str
    titlePinyin: str = ""


@dataclass
class UnitItem(BaseItem):
    """
    收藏列表项
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pageId: str
    title: str
    creator: str
    modifyTime: str
    operatorTime: str = ""
    titlePinyin: str = ""


@dataclass
class MentionedItem(BaseItem):
    """
    AT ME, 提到我
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    contentId: int
    title: str
    recentMentionTime: int
    mentionCount: int
    titlePinyin: str = ""


@dataclass
class ReceivedItem(BaseItem):
    """
    大象收到的
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    contentId: str
    title: str
    sender: str
    recentReceivedTime: int
    titlePinyin: str = ""


@dataclass
class CommentedItem(BaseItem):
    """
    我评论的
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    contentId: str
    title: str
    recentCommentTime: int
    commentCount: int
    titlePinyin: str = ""


@dataclass
class PageItem(BaseItem):
    """
    个人空间文档项
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    contentId: str
    title: str
    childCount: int
    modifyTime: str
    modifier: str
    path: str = ""
    titlePinyin: str = ""


def api_request(url: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
    """
    通用 API 请求函数

    Args:
        url (str): API 端点 URL
        method (str, optional): HTTP 方法. 默认是 "GET".
        data (Optional[Dict], optional): POST 请求的数据. 默认是 None.

    Returns:
        Dict: API 响应的 JSON 数据

    Raises:
        ValueError: 如果 HTTP 方法不支持
        requests.RequestException: 如果 API 请求失败
    """
    cookies_str = login_manager.get_cookies()
    headers = {"Cookie": cookies_str}

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, allow_redirects=False)
        elif method.upper() == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(
                url, headers=headers, json=data, allow_redirects=False
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        login_manager.check_login_status(response)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise


def query_users(keyword: str) -> List[str]:
    """
    查询用户

    Args:
        keyword (str): 搜索关键词

    Returns:
        Optional[List[str]]: 匹配的用户列表，如果没有匹配则返回 None
    """
    url = f"https://km.sankuai.com/api/users/neixin/search?input={url_encode(keyword)}&pageSize=10&pageNo=0"
    result = api_request(url)
    users = result.get("data", {}).get("users", [])
    return [v for user in users for (_, v) in user.items()] if users else []


def search_history() -> List[Dict]:
    """
    获取搜索历史

    Returns:
        List[Dict]: 搜索历史列表
    """
    url = "https://km.sankuai.com/api/citadelsearch/content/history"
    result = api_request(url)
    return result.get("data", [])


def query_dxuid(mis: str) -> Dict:
    """
    查询 DXUID

    Args:
        mis (str): MIS 号

    Returns:
        Dict: DXUID 信息
    """
    url = "https://km.sankuai.com/dxuid"
    result = webUtils.post_json(url, login_manager, json_payload=[mis])
    uid = result.get("data", [])
    wf().logger.info(f"uid:{uid}")
    if uid:
        return uid[0]
    else:
        return None


def suggest(query: str) -> List[str]:
    """
    获取搜索建议

    Args:
        query (str): 搜索查询

    Returns:
        List[str]: 搜索建议列表
    """
    url = f"https://km.sankuai.com/api/citadelsearch/content/sug?keyword={url_encode(query)}"
    result = api_request(url)
    sug_list = result.get("data", {}).get("sugList", [])
    return [sug["sug"] for sug in sug_list]


def operation_history(
    operation_types: int = 3, page_no: int = 1, page_size: int = 50
) -> List[UnitItem]:
    """
    获取操作历史

    Args:
        operation_types (int, optional): 操作类型. 默认是 3.
        page_no (int, optional): 页码. 默认是 1.
        page_size (int, optional): 每页大小. 默认是 50.

    Returns:
        List[UnitItem]: 操作历史列表
    """
    url = f"https://km.sankuai.com/api/operationHistory?pageNo={page_no}&pageSize={page_size}&operationTypes={operation_types}"
    result = api_request(url)
    units = result.get("data", {}).get("units", [])
    return [UnitItem(**u) for u in units] if units else []


def query_limit_operation_history(km_history_limit: int = 300) -> List[UnitItem]:
    """
    查询限制数量的操作历史

    Args:
        km_history_limit (int, optional): 历史记录数量限制. 默认是 300.

    Returns:
        List[UnitItem]: 操作历史列表
    """
    page_no, page_size = 1, 50
    result_limit = []
    while len(result_limit) < km_history_limit:
        history_record = operation_history(page_no=page_no, page_size=page_size)
        if not history_record:
            break
        result_limit.extend(history_record)
        page_no += 1
    return result_limit[:km_history_limit]


def latest_edit_list(offset: int = 0, limit: int = 300) -> List[UnitItem]:
    """
    获取最近编辑

    Args:
        offset (int, optional): 偏移量. 默认是 0.
        limit (int, optional): 限制数量. 默认是 300.

    Returns:
        List[UnitItem]: 最近编辑列表
    """
    url = f"https://km.sankuai.com/api/pages/latestEdit?offSet={offset}&limit={limit}"
    result = api_request(url)
    units = result.get("data", {}).get("units", [])
    return [UnitItem(**u) for u in units]


def latest_mentioned_list(offset: int = 0, limit: int = 90) -> List[MentionedItem]:
    """
    获取最近被提及列表

    Args:
        offset (int, optional): 偏移量. 默认是 0.
        limit (int, optional): 限制数量. 默认是 30.

    Returns:
        List[UMentionedItemnitItem]: 最近被提及列表
    """
    url = f"https://km.sankuai.com/api/data/userRelated/mentioned?offset={offset}&limit={limit}"
    result = api_request(url)
    units = result.get("data", {}).get("units", [])
    return [MentionedItem(**u) for u in units]


def latest_commented_list(offset: int = 0, limit: int = 90) -> List[CommentedItem]:
    """
    最近评论的文档列表

    Args:
        offset (int, optional): 偏移量. 默认是 0.
        limit (int, optional): 限制数量. 默认是 30.

    Returns:
        List[CommentedItem]: 最近评论的文档列表
    """
    url = f"https://km.sankuai.com/api/data/userRelated/commented?offset={offset}&limit={limit}"
    result = api_request(url)
    units = result.get("data", {}).get("units", [])
    return [CommentedItem(**u) for u in units]


def latest_received_list(offset: int = 0, limit: int = 30) -> List[ReceivedItem]:
    """
    最近评论的文档列表

    Args:
        offset (int, optional): 偏移量. 默认是 0.
        limit (int, optional): 限制数量. 默认是 30.

    Returns:
        List[ReceivedItem]: 最近评论的文档列表
    """
    url = f"https://km.sankuai.com/api/data/userRelated/received?offset={offset}&limit={limit}&queryId={uuid.uuid4()}"
    result = api_request(url)
    units = result.get("data", {}).get("units", [])
    return [ReceivedItem(**u) for u in units]


def quick_access_list(
    collection_type: str, content_types: str = "0,2"
) -> List[CollectionItem]:
    """
    获取快速访问列表

    Args:
        collection_type (int): 收藏类型
        content_types (str, optional): 内容类型. 默认是 "0,2".

    Returns:
        List[ContentItem]: 快速访问列表
    """
    url = f"https://km.sankuai.com/api/collection/collection?collectionType={collection_type}&contentTypes={content_types}"
    result = api_request(url)
    content_list = result.get("data", {}).get("contentVOList", [])
    return [CollectionItem(**c) for c in content_list]


def query_collections() -> List[UnitItem]:
    """
    查询收藏文档列表

    Returns:
        List[UnitItem]: 收藏文档列表
    """
    all_collections = []
    offset, limit = 0, 30
    while True:
        url = (
            f"https://km.sankuai.com/api/collection/list?offset={offset}&limit={limit}"
        )
        result = api_request(url)
        units = result.get("data", {}).get("units", [])
        if not units:
            break
        all_collections.extend([UnitItem(**c) for c in units])
        if len(units) < limit:
            break
        offset += limit
    return all_collections


def get_space_id_by_mis(mis: str) -> Dict:
    """
    通过 MIS 获取空间 ID

    Args:
        mis (str): MIS 号

    Returns:
        Dict: 空间 ID 信息
    """
    url = f"https://km.sankuai.com/api/spaces/person?mis={mis}"
    return api_request(url).get("data", {})


def get_pages_by_space_id(space_id: str) -> List[PageItem]:
    """
    通过空间 ID 获取页面

    Args:
        space_id (str): 空间 ID

    Returns:
        List[PageItem]: 页面列表
    """
    url = f"https://km.sankuai.com/api/spaces/child/{space_id}"
    result = api_request(url)
    return get_space_page_list(result)


def get_child_pages_by_id(space_id: str, page_id: str) -> List[PageItem]:
    """
    获取子页面

    Args:
        space_id (str): 空间 ID
        page_id (str): 页面 ID

    Returns:
        List[PageItem]: 子页面列表
    """
    url = f"https://km.sankuai.com/api/pages/child/{space_id}/{page_id}"
    result = api_request(url)
    return get_space_page_list(result)


def get_space_page_list(result: Dict) -> List[PageItem]:
    """
    获取空间页面列表

    Args:
        result (Dict): API 响应结果

    Returns:
        List[PageItem]: 页面列表
    """
    page_list = result.get("data", {}).get("list", [])
    return [PageItem(**p) for p in page_list]


def get_space_pages(space_id: str) -> List[PageItem]:
    """
    获取空间所有页面

    Args:
        space_id (str): 空间 ID

    Returns:
        List[PageItem]: 所有页面列表
    """
    # 获取直接子页面
    pages = get_pages_by_space_id(space_id)
    all_pages = []
    current_path = ""
    return get_all_pages(all_pages, space_id, current_path, pages)


def get_all_pages(
    all_pages: List[PageItem], space_id: str, current_path: str, pages: List[PageItem]
) -> List[PageItem]:
    """
    递归获取所有页面

    Args:
        all_pages (List[PageItem]): 所有页面列表
        space_id (str): 空间 ID
        current_path (str): 当前路径
        pages (List[PageItem]): 当前页面列表

    Returns:
        List[PageItem]: 更新后的所有页面列表
    """
    for p in pages:
        all_pages.append(p)
        if p.childCount:
            sub_pages = get_child_pages_by_id(space_id, p.contentId)
            if sub_pages:
                get_all_pages(
                    all_pages, space_id, f"{current_path}/{p.title}", sub_pages
                )
        p.path = current_path
    return all_pages


def get_all_sub_pages(content_id: str) -> List[PageItem]:
    """
    获取一个文档下所有的子文档

    Args:
        content_id: 学城文档id
    Returns:
        List[PageItem]: 所有页面列表
    """
    space_id = get_space_id_by_page(content_id)
    pages = get_child_pages_by_id(space_id, content_id)
    all_pages = []
    current_path = ""
    return get_all_pages(all_pages, space_id, current_path, pages)


def get_space_id_by_page(content_id: str) -> str:
    url = f"https://km.sankuai.com/api/permission/content/{content_id}/getContentInfo"
    return api_request(url).get("data", {}).get("spaceId")


if __name__ == "__main__":
    uid = query_dxuid("tangxuejun")
    print(uid)
    edit_list = quick_access_list(1)
    for e in edit_list:
        print(e)
    # result = wf().filter("im", edit_list, lambda item: item.titlePinyin)
    # print(result)
