#!/usr/bin/python
# encoding: utf-8

import os
import getpass
from typing import Optional, Callable, Dict, Tuple, Union
import init_path
from utils import wf
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from workflow import PasswordNotFound
from pycookiecheat import chrome_cookies
import webbrowser

CHROME_PATH = "open -a /Applications/Google\\ Chrome.app %s"
DEFAULT_CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"


class LoginManager:
    def __init__(
        self,
        login_url: str,
        wait_element: Callable,
        cookie_name: str,
        login_check_callback=None,
    ):
        """
        初始化LoginManager对象。

        Args:
            login_url (str): 登录页面的URL。
            wait_element (Callable): 用于等待特定元素出现的回调函数。
            cookie_name (str): 用于存储cookie的名称。
            login_check_callback 用于检查登录状态的回调函数,返回false登录不通过，唤起浏览器登录，默认为None，默认检查resp响应的httpstatus（301,302,401）
        """

        self.login_url = login_url
        self.wait_element = wait_element
        self.cookie_name = cookie_name
        self.login_type = os.getenv("login_type") or "from_local_cookie"
        # self.login_type = login_type
        self.login_check_callback = login_check_callback
        self.cookie_file = self._get_cookie_file()

    def _get_cookie_file(self) -> Optional[str]:
        chrome_cookie_dir = os.getenv("chrome_cookie_dir")
        return os.path.expanduser(chrome_cookie_dir) if chrome_cookie_dir else None

    def __login(self, chrome_driver_path: str = DEFAULT_CHROME_DRIVER_PATH) -> None:
        browser = self._get_browser(chrome_driver_path)
        try:
            self._perform_login(browser)
        except TimeoutException:
            wf().logger.warning("Login timeout!")
            raise RuntimeError("Login timeout!")
        except Exception as e:
            wf().logger.error(f"Login failure: {str(e)}")
            raise RuntimeError("Login failure!") from e
        finally:
            browser.quit()

    def _get_browser(
        self, chrome_driver_path: str
    ) -> Union[webdriver.Chrome, webdriver.Safari]:

        if os.path.exists(DEFAULT_CHROME_DRIVER_PATH):
            options = Options()
            options.add_argument(
                f"user-data-dir={os.path.expanduser('~/Library/Application Support/Google/Chrome/Default')}"
            )
            service = Service(executable_path=DEFAULT_CHROME_DRIVER_PATH)
            return webdriver.Chrome(service=service, options=options)
        else:
            print(
                f"ChromeDriver not found at {self.chrome_driver_path}. Falling back to Safari."
            )
            return webdriver.Safari()

    def _perform_login(self, browser: WebDriver) -> None:
        browser.get(self.login_url)
        try:
            WebDriverWait(browser, 60).until(self.wait_element)
        except Exception as e:
            print(f"Error waiting for element: {str(e)}")
            raise

        cookies = {c.get("name"): c.get("value") for c in browser.get_cookies()}
        cookie_str = ";".join(["{0}={1}".format(k, v) for k, v in cookies.items()])
        wf().logger.info("login success !")
        self.save_cookies(cookie_str)
        return cookies

    def check_login_status(self, resp) -> None:
        if self.login_check_callback:
            if not self.login_check_callback(self, resp):
                self.re_login()
                raise RuntimeError(
                    "Login timeout, please login first, then retry after one minute."
                )
        if resp.status_code in (301, 302, 401):
            self.re_login()
            raise RuntimeError(
                "Login timeout, please login first, then retry after one minute."
            )

    def get_cookies(self) -> str:
        if self.login_type == "selenium":
            try:
                return wf().get_password(self.cookie_name)
            except PasswordNotFound:
                self.re_login()
                raise RuntimeError("Please login first, then retry")
        else:
            cookies = chrome_cookies(self.login_url, cookie_file=self.cookie_file)
            return ";".join(f"{k}={v}" for k, v in cookies.items())

    def save_cookies(self, value: str) -> None:
        wf().save_password(self.cookie_name, value)

    def delete_cookies(self) -> None:
        try:
            wf().delete_password(self.cookie_name)
        except PasswordNotFound:
            pass

    def re_login(self) -> None:
        if self.login_type == "selenium":
            self.delete_cookies()
            self.__login()
        else:
            webbrowser.get(CHROME_PATH).open(self.login_url)
