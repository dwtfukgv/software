import json
# encoding: utf-8

import json
from typing import List, Optional
from dataclasses import dataclass

from utils import url_encode, BaseItem
import webUtils
from LoginManager import LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Constants
LOGIN_URL = "https://avatar.mws.sankuai.com/"
WAIT_ELEMENT = EC.presence_of_element_located((By.ID, "app"))
COOKIE_NAME = "avatar_cookies"
API_BASE_URL = "https://avatar.mws.sankuai.com/api/v2/avatar/appkey/query"

login_manager = LoginManager(LOGIN_URL, WAIT_ELEMENT, COOKIE_NAME)

@dataclass
class ServiceItem(BaseItem):
    """Represents a service item returned by the Avatar API."""
    resourceType: str
    appkey: str
    env: str

def query_services(keyword: str) -> List[ServiceItem]:
    try:
        result = webUtils.get(API_BASE_URL, login_manager, params={"query":keyword})
        if "data" in result:
            return [
                ServiceItem(
                    resourceType=item["resourceType"],
                    appkey=item["appkey"],
                    env=item["env"]
                )
                for item in result["data"]
            ]
        return None
    except Exception as e:
        print(f"Error querying services: {e}")
        return None

if __name__ == "__main__":
    test_keywords = ["10.178.27.195", "example_appkey"]
    for keyword in test_keywords:
        print(f"Querying services for: {keyword}")
        services = query_services(keyword)
        if services:
            for service in services:
                print(f"  ResourceType: {service.resourceType}, Appkey: {service.appkey}, Env: {service.env}")
        else:
            print(f"  No services found for {keyword}")
        print()
