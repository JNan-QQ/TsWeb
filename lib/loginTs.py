# -*- coding:utf-8 -*-
# @FileName  :loginTs.py
# @Time      :2021/7/20 9:07
# @Author    :姜楠
# @Tool      :PyCharm

from time import sleep

from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver


class Login:
    driver: webdriver.Edge = None

    def open_browser(self, BrowserDriver):
        # 未指定浏览器，默认打开谷歌浏览器
        if not BrowserDriver:
            print('使用默认谷歌浏览器')
            self.driver = webdriver.Chrome()
        else:
            # 浏览器类型
            browser_btype = BrowserDriver['browser_type']
            # Edge
            if browser_btype == 'Edge':
                if BrowserDriver['default']:
                    print('使用edge浏览器默认配置')
                    self.driver = webdriver.Edge()
                else:
                    options = EdgeOptions()
                    options.use_chromium = True
                    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
                    options.binary_location = BrowserDriver['browser_path']
                    self.driver = Edge(BrowserDriver['driver_path'], options=options)
            elif browser_btype == 'Chrome':
                if BrowserDriver['default']:
                    print('使用chrome浏览器默认配置')
                    self.driver = webdriver.Chrome()
                else:
                    options = webdriver.ChromeOptions()
                    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
                    options.binary_location = BrowserDriver['browser_path']
                    self.driver = webdriver.Chrome(BrowserDriver['driver_path'], options=options)
            else:
                print('目前仅支持 谷歌、Edge 浏览器！')
                return None

        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def close_browser(self):
        self.driver.quit()

    def login(self, user=('waiyan', '123456lj'), url='https://jiangnan-www.b.waiyutong.org/'):
        # 输入网站
        self.driver.get(url)
        # 输入用户名与密码
        if isinstance(user, (list, tuple)):
            username = user[0]
            password = user[1]
        elif isinstance(user, dict):
            username = user['username']
            password = user['password']
        else:
            print('账号信息有误！！！')
            return
        user_input = self.driver.find_element_by_id('username_field')
        user_input.clear()
        user_input.send_keys(username)
        pass_input = self.driver.find_element_by_id('password_field')
        pass_input.clear()
        pass_input.send_keys(password)
        # 确认登录
        self.driver.find_element_by_css_selector('.te_login').click()
        # 等待登录成功
        while not self.driver.find_elements_by_css_selector('.uname'):
            sleep(2)

    def logout(self):
        self.driver.execute_script("$(arguments[0]).click()", self.driver.find_element_by_css_selector('.logout'))
        sleep(2)


# login_teacher = Login()
login_student = Login()

if __name__ == "__main__":
    pass
