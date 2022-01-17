# -*- coding:utf-8 -*-
# @FileName  :exam_homework.py
# @Time      :2022/1/17 17:19
# @Author    :姜楠
# @Tool      :PyCharm
import re
from time import sleep
from hytest import *
from selenium import webdriver
from lib.doQuestions import main_handler
from selenium.webdriver.support.ui import Select
from config.config import UrlBase
from lib.loginTs import login
from lib.VerificationCode import verfCode


class StudentExam:
    mode_url = UrlBase.alpha['mode_url']
    mode_name = ['人机对话', '笔试考场', '单元测试']
    driver = None

    def chosePaper(self, mode, paper_id=''):
        if paper_id and mode == 3:
            self.driver.get(
                fr'https://{UrlBase.username}-student.b.waiyutong.org/Practice/homework.html?mode=free&hid={paper_id}')
            return True
        else:
            return False


if __name__ == "__main__":
    run_code = 0
