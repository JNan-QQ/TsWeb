# -*- coding:utf-8 -*-
# @FileName  :__st__.py
# @Time      :2021/7/23 15:04
# @Author    :姜楠
# @Tool      :PyCharm
from hytest import *
from lib.loginTs import login_1
from lib.VerificationCode import ver_code
from config.config import browser_driver


def suite_setup():
    INFO('套件目录初始化')
    STEP(1, '系统验证')
    ver_code.license()
    STEP(2, '打开浏览器')
    print('PAPER1')
    GSTORE['driver1'] = login_1.open_browser(browser_driver.student_browser)


def suite_teardown():
    INFO('套件目录清除')
    STEP(1, '关闭浏览器')
    login_1.close_browser()

