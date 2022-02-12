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
    driver = None

    def open_browser(self, BrowserDriver):
        btype = BrowserDriver.browser_kernel
        print(btype)
        btype = btype.lower()
        options = webdriver.ChromeOptions()
        # 指定浏览器分辨率
        options.add_argument('window-size=1920x3000')
        # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--disable-gpu')
        # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.add_argument('--headless')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Remote(
            command_executor=fr"http://{btype}:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options
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

