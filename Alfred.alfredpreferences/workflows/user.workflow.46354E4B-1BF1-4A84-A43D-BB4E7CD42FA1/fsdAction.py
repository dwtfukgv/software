#!/usr/bin/python
# encoding: utf-8

from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests as web
import socket

# login manager
LOGIN_URL = "https://fsd.sankuai.com/workbench"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, "fsd_cookies")
TIMEOUT = 5

FSD_FILED_ONLINE_ID = "onlineProgramId"
FSD_FILED_APPLY_ID = "applyProgramId"
FSD_FILED_MED_ID = "medId"
FSD_FILED_NAME = "name"
FSD_FILED_SOURCE = "source"
# 0-未开始   10-上线中  20-已上线
FSD_FILED_ONLINE_STATUS = "status"
FSD_ONLINE_STATUS_DIC = {0: "未开始", 10: "上线中", 20: "已上线"}
FSD_FILED_APPLY_STATUS = "status"
FSD_FILED_ONLINE_TIME = "projectOnlineTime"
FSD_APPLY_STATUS_DIC = {
    0: "开发中",
    20: "交付QA",
    30: "测试中",
    50: "测试完成",
    55: "待上线",
    60: "已上线",
}


def query_release_plan_paged_list(url, page_no, page_size):
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "M-Appkey": "fe_com.sankuai.waimaiqafsd.qafe",
        "Dnt": "1",
    }
    params = {"pageNum": page_no, "pageSize": page_size}
    try:
        resp = web.get(
            url, params=params, headers=headers, allow_redirects=False, timeout=TIMEOUT
        )
        login_manager.check_login_status(resp)
        resp.raise_for_status()
        return resp.json()
    except socket.timeout:
        login_manager.re_login()
        # ed token过期后，接口会超时。。
        raise RuntimeError("fsd timeout，please login again")


def query_all_release_plan_list():
    page_no = 1
    resp = query_release_plan_paged_list(
        "https://fsd.sankuai.com/api/qa/v1/onlinePlan/getOnlinePlanList?relatedMe=true&planType=&orgId=&status=",
        page_no=page_no,
        page_size=15,
    )
    online_plan_data = resp["data"]
    result_online_list = []
    if online_plan_data:
        test_apply_list = online_plan_data["list"]
        count = online_plan_data["count"]
        result_online_list.extend(
            [
                {
                    FSD_FILED_ONLINE_ID: record[FSD_FILED_ONLINE_ID],
                    FSD_FILED_NAME: record[FSD_FILED_NAME],
                    FSD_FILED_ONLINE_TIME: record[FSD_FILED_ONLINE_TIME],
                    FSD_FILED_ONLINE_STATUS: FSD_ONLINE_STATUS_DIC[
                        record[FSD_FILED_ONLINE_STATUS]
                    ],
                }
                for record in test_apply_list
            ]
        )
    return result_online_list


def query_test_apply_paged_list(url, page_no, page_size):
    cookies_str = login_manager.get_cookies()
    headers = {
        "Cookie": cookies_str,
        "M-Appkey": "fe_com.sankuai.waimaiqafsd.qafe",
        "Dnt": "1",
    }
    params = {"pageNum": page_no, "pageSize": page_size}
    try:
        resp = web.get(
            url, params=params, headers=headers, allow_redirects=False, timeout=TIMEOUT
        )
        login_manager.check_login_status(resp)
        resp.raise_for_status()
        return resp.json()
    except socket.timeout:
        login_manager.re_login()
        # ed token过期后，接口会超时。。。
        raise RuntimeError("fsd timeout，please login again")


def query_all_test_apply_list():
    page_no = 1
    resp = query_test_apply_paged_list(
        "https://fsd.sankuai.com/api/qa/v1/delivery/getDeliveryPlanList?relatedMe=true&orgId=&env=&jobName=&source=0,1,2",
        page_no=page_no,
        page_size=15,
    )
    test_apply_data = resp["data"]
    result_apply_list = []
    if test_apply_data:
        test_apply_list = test_apply_data["list"]
        count = test_apply_data["count"]
        if test_apply_list:
            for l in test_apply_list:
                status = l[FSD_FILED_APPLY_STATUS]
                if status in FSD_APPLY_STATUS_DIC:
                    status_desc = FSD_APPLY_STATUS_DIC[status]
                else:
                    status_desc = "unknown"
                result_apply_list.append(
                    {
                        FSD_FILED_APPLY_ID: l[FSD_FILED_APPLY_ID],
                        FSD_FILED_MED_ID: l[FSD_FILED_MED_ID],
                        FSD_FILED_NAME: l[FSD_FILED_NAME],
                        FSD_FILED_APPLY_STATUS: status_desc,
                        FSD_FILED_SOURCE: l[FSD_FILED_SOURCE],
                        FSD_FILED_ONLINE_TIME: l[FSD_FILED_ONLINE_TIME],
                    }
                )
        while len(result_apply_list) < count:
            page_no = page_no + 1
            resp = query_test_apply_paged_list(
                "https://fsd.sankuai.com/api/qa/v1/delivery/getDeliveryPlanList?pageNum={}&pageSize={}&relatedMe=true&orgId=&env=&jobName=&source=0,1,2",
                page_no=page_no,
                page_size=15,
            )
            test_apply_data = resp["data"]
            count = test_apply_data["count"]
            test_apply_list = test_apply_data["list"]
            if not test_apply_list:
                break
            for l in test_apply_list:
                status = l[FSD_FILED_APPLY_STATUS]
                if status in FSD_APPLY_STATUS_DIC:
                    status_desc = FSD_APPLY_STATUS_DIC[status]
                else:
                    status_desc = "unknown"
                result_apply_list.append(
                    {
                        FSD_FILED_APPLY_ID: l[FSD_FILED_APPLY_ID],
                        FSD_FILED_MED_ID: l[FSD_FILED_MED_ID],
                        FSD_FILED_NAME: l[FSD_FILED_NAME],
                        FSD_FILED_APPLY_STATUS: status_desc,
                        FSD_FILED_SOURCE: l[FSD_FILED_SOURCE],
                        FSD_FILED_ONLINE_TIME: l[FSD_FILED_ONLINE_TIME],
                    }
                )
    return result_apply_list


if __name__ == "__main__":
    print(query_all_test_apply_list())
