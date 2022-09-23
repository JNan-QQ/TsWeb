# -*- coding:utf-8 -*-
# @FileName  :exam_paper.py
# @Time      :2021/8/17 9:34
# @Author    :姜楠
# @Tool      :PyCharm
import re
from time import sleep

from hytest import INFO, CHECK_POINT, SELENIUM_LOG_SCREEN
from selenium import webdriver
from selenium.common import exceptions as s_exceptions
from selenium.webdriver.support import expected_conditions, ui

from config.config import getCaseConfigData
from lib.doQuestions import main_handler


class StudentExam:
    mode_url = getCaseConfigData.Url['mode_url']
    mode_name = ['人机对话', '笔试考场', '外语通作业']
    driver = None

    def getExamPage(self, driver, mode):
        sleep(1)
        INFO(f'进入{self.mode_name[mode - 1]}界面')
        self.driver: webdriver.Edge = driver
        # 进入试卷列表界面
        self.driver.get(self.mode_url[self.mode_name[mode - 1]])

        sleep(0.5)
        jump_alert = expected_conditions.alert_is_present()(self.driver)
        if jump_alert:
            jump_alert.accept()

        return True

    def choseGrade(self, grade, paper_id=None):

        if paper_id or not grade:
            return True

        grades = {
            '6A': '六年级上',
            '6B': '六年级下',
            '7A': '七年级上',
            '7B': '七年级下',
            '8A': '八年级上',
            '8B': '八年级下',
            '9A': '九年级上',
            '9B': '九年级下',
            '9C': '九年级全',
            '10A': '高一第一学期',
            '10B': '高一第二学期',
            '10C': '必修第一册',
            '10D': '选择性必修第一册',
            '10E': '选修(提高类)第一册',
            '11A': '高二第一学期',
            '11B': '高二第二学期',
            '11C': '必修第二册',
            '11D': '选择性必修第二册',
            '11E': '选修(提高类)第二册',
            '12A': '高三第一学期',
            '12B': '高三第二学期',
            '12C': '必修第三册',
            '12D': '选择性必修第三册',
            '12E': '选修(提高类)第三册',
            '13D': '选择性必修第四册',

        }
        # 选择年级
        select = ui.Select(
            self.driver.find_element_by_css_selector('.book_unit_select_cnt .book_unit_select.current .book_select'))
        # 通过 Select 对象选中
        select.select_by_visible_text(grades[grade])
        sleep(0.5)

        return True

    def chosePaper(self, paper_name, mode, paper_id=None, grade_type=13, book_version=1):

        if paper_id:
            self.driver.get(getCaseConfigData.Url['exam_url'][mode - 1] % (book_version, grade_type, int(paper_id)))
            return True

        mode_paper_title = ['.rjdh_paper_title', '.bishi_paper_title', '.homework_title']

        while True:
            sleep(2)
            papers = self.driver.find_elements_by_css_selector('.list_container')
            for paper_item in papers:  # 人机对话、笔试考场、网络作业
                if paper_name == paper_item.find_element_by_css_selector(mode_paper_title[mode - 1]).text:
                    paper_item.find_element_by_css_selector('.remain_status_btn a:nth-child(1)').click()
                    return True
            else:
                btn = self.driver.find_elements_by_css_selector('a.next')
                if btn:
                    self.driver.execute_script("$(arguments[0]).click()", btn[0])
                else:
                    return False

    def doPaper(self, paper_name):
        # 等待试卷加载
        sleep(1.5)
        wait_time = 0
        while True:
            try:
                self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
                self.driver.find_element_by_css_selector('button.ui-button').click()
                break
            except s_exceptions.ElementClickInterceptedException:
                wait_time += 1
                if wait_time > 20:
                    SELENIUM_LOG_SCREEN(self.driver, width='70%')
                    CHECK_POINT(f'试卷加载 - {paper_name}', False)
                    return False
                sleep(1)
            except s_exceptions.NoSuchElementException:
                CHECK_POINT(f'试卷加载 - {paper_name}', False)
                return False

        # 判断试卷⏲是否可用
        sleep(3)
        hour = self.driver.find_element_by_css_selector('.countdown_hour').text
        minute = self.driver.find_element_by_css_selector('.countdown_minute').text
        second = self.driver.find_element_by_css_selector('.countdown_second').text
        homework_do_time = int(hour) * 3600 + int(minute) * 60 + int(second)
        if homework_do_time == 0:
            INFO('试卷⏲是不可用，可能试卷缺少资源，打开F12查看')
            return False

        # 查找题目
        ques_list = self.driver.find_elements_by_css_selector('.test_content')
        if not ques_list:
            SELENIUM_LOG_SCREEN(self.driver, width='70%')
            INFO('该试卷无题目')
            return False

        # 循环答题
        for index, ques in enumerate(ques_list):
            ques_id = ques.get_attribute('data-id')
            ques_type = ques.get_attribute('data-type')
            INFO(f'-- 进行第 {index + 1} 大题试题作答、判断\n\n')
            print(f'-- 进行第 {index + 1} 大题试题作答、判断')
            try:
                main_handler(int(ques_id), ques_type, self.driver, ques)
                INFO(f'-- 第 {index + 1} 大题试题作答、判断完成！！！\n\n')
            except Exception as e:
                INFO(f'-- 第 {index + 1} 大题试题作答、判断失败？？？\n\n')
                INFO(e)
            sleep(0.3)

        return True

    def submitHomework(self, mode):
        # 外语通作业至少需要答题90s
        if mode == 3:
            while True:
                hour = self.driver.find_element_by_css_selector('.countdown_hour').text
                minute = self.driver.find_element_by_css_selector('.countdown_minute').text
                second = self.driver.find_element_by_css_selector('.countdown_second').text
                homework_do_time = int(hour) * 3600 + int(minute) * 60 + int(second)
                homework_need_time = self.driver.find_element_by_css_selector('.p_paper_cnt').get_attribute(
                    'data-need-time')
                if 95 < int(homework_need_time) * 3600 - homework_do_time < int(homework_need_time) * 3600 - 95:
                    break
                sleep(5)

        # 点击提交按钮
        self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
        sleep(0.5)
        # 确认提交
        self.driver.find_element_by_xpath('//*[@class="ui-button-text"][text()="保存答案"]').click()
        sleep(0.5)

        # 提交后的几种状态
        submit_time = 0
        while True:
            msg_info = self.driver.find_element_by_css_selector('.message-info').text
            if msg_info == '数据计算中...':
                sleep(2)
            elif msg_info == '目前有音频未识别，请等待判分。':
                if self.driver.find_elements_by_css_selector('.zeroTips[style*="display"]'):
                    # 继续提交
                    self.driver.find_element_by_xpath('//*[@class="ui-button-text"][text()="继续提交"]').click()
            elif msg_info == '音频已全部识别完成，是否提交答案？':
                self.driver.find_element_by_xpath('//*[@class="ui-button-text"][text()="提交"]').click()
            elif msg_info == '记录保存成功':
                self.driver.find_element_by_xpath('//*[@class="ui-button-text"][text()="我知道了"]').click()
                return True
            else:
                return False
            sleep(2)

            # 提交超时
            submit_time += 2
            if submit_time > 60:
                return False

    def checkResult(self, mode):
        if mode == 3:
            web_s_score = self.driver.find_element_by_css_selector('.composition_homework_not>span').text
            web_n_score = self.driver.find_element_by_css_selector('.p_paper_cnt').get_attribute('data-tatol-score')
            right = ['外语通作业暂不判断']
            wrong = ['外语通作业暂不判断']
        else:
            right = [i.text for i in self.driver.find_elements_by_css_selector('.answer_list_right_class')]
            wrong = [i.text for i in self.driver.find_elements_by_css_selector('.answer_list_wrong_class')]
            web_score = self.driver.find_element_by_css_selector('.p_paper_nature  ul').text
            web_s_score, web_n_score = re.findall(r'得分：(\d+).*?满分：(\d+)', web_score, re.S)[0]

        INFO(f'答对的题目序号：{right}')
        INFO(f'答错的题目序号：{wrong}')
        print(f'学生实际得分：{web_s_score}，试卷实际总分：{web_n_score}')
        INFO(f'学生实际得分：{web_s_score}，试卷实际总分：{web_n_score}')

        return True


studentExam = StudentExam()
