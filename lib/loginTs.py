# -*- coding:utf-8 -*-
# @FileName  :loginTs.py
# @Time      :2021/7/20 9:07
# @Author    :姜楠
# @Tool      :PyCharm

from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from config.config import AccountConfig, UrlBase
from msedge.selenium_tools import Edge, EdgeOptions


class Login:
    driver: webdriver.Edge = None

    def open_browser(self, BrowserDriver):
        btype = BrowserDriver.browser_kernel
        print(btype)
        btype = btype.lower()
        self.driver = webdriver.Remote(
            command_executor=fr"http://{btype}:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver.implicitly_wait(5)
        return self.driver

    def close_browser(self):
        self.driver.quit()

    def login(self, username, password, url=UrlBase.login_url):
        # 输入网站
        self.driver.get(url)
        # 输入用户名与密码
        user_input = self.driver.find_element_by_id('username_field')
        user_input.clear()
        user_input.send_keys(username)
        pass_input = self.driver.find_element_by_id('password_field')
        pass_input.clear()
        pass_input.send_keys(password)
        # 确认登录
        self.driver.find_element_by_css_selector('.te_login').click()
        sleep(2)

    def logout(self):
        self.driver.execute_script(
            "$(arguments[0]).click()", self.driver.find_element_by_css_selector('.logout'))
        sleep(2)


login = Login()
login_1 = Login()

if __name__ == "__main__":
    pass
