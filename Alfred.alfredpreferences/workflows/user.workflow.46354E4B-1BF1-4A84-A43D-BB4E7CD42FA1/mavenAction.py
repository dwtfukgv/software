# -*- coding: utf-8 -*-
# @Time     : 2024/3/29 19:13
# @Author   : liuyulong06
# @File     : mavenAction.py


from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import webUtils

LOGIN_URL = "https://maven.sankuai.com"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "page"))
COOKIE_NAME = "maven_cookies"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)


def search_maven(keyword):
    """ """
    url = "https://maven.sankuai.com/api/search/component/fulltext"
    params = {"q": keyword, "page": 0, "size": 10}
    result = webUtils.get(url, login_manager=login_manager, params=params)
    return result["aggregatedComponents"]


def search_maven_detail(group_id, artifact_id):
    url = "https://maven.sankuai.com/api/search/component"
    params = {
        "groupId": group_id,
        "artifactId": artifact_id,
        "page": 0,
        "size": 100,
        "needDetail": True,
    }
    result = webUtils.get(url, login_manager=login_manager, params=params)
    return result["aggregatedComponents"]
