# -*- coding:utf-8 -*-
# @FileName  :exam_homework.py
# @Time      :2022/1/17 17:19
# @Author    :姜楠
# @Tool      :PyCharm
import re
import traceback
from time import sleep
from hytest import *
from selenium import webdriver
from lib.doQuestions import main_handler
from config.config import UrlBase
from lib.loginTs import login
from lib.VerificationCode import verfCode


class StudentExam:
    mode_url = UrlBase.mode_url
    mode_name = ['人机对话', '笔试考场', '单元测试']
    driver = None

    def chosePaper(self, driver, mode, paper_id=''):
        self.driver: webdriver.Edge = driver
        sleep(5)
        login_time = 0
        while True:
            if self.driver.find_elements_by_css_selector('.menu_for_free'):
                break
            sleep(5)
            login_time += 1
            if login_time > 10:
                return False

        if paper_id and mode == 3:
            self.driver.get(
                fr'https://{UrlBase.username}-student.b.waiyutong.org/Practice/homework.html?mode=free&hid={paper_id}')
            sleep(1)
            try:
                self.driver.switch_to.alert.accept()
            except:
                pass

            return True
        else:
            return False

    def doPaper(self, paper_name):
        # 等待试卷加载
        sleep(4)
        while True:
            try:
                self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
                self.driver.find_element_by_css_selector('button.ui-button').click()
                break
            except:
                flg_err = False
                try:
                    err_info = self.driver.find_elements_by_css_selector('.message-info')
                    if err_info:
                        if '参数有误或服务器出现异常' in err_info[0].text:
                            flg_err = True
                            INFO('参数有误或服务器出现异常，SERVER_NO:B-jiangnan')
                            SELENIUM_LOG_SCREEN(self.driver, width='70%')
                            CHECK_POINT(f'试卷加载 - {paper_name}', False)
                    self.driver.find_element_by_css_selector('button.ui-button').click()
                    sleep(1)
                except:
                    if flg_err:
                        return False
        sleep(1)
        ques_list = self.driver.find_elements_by_css_selector('.test_content')
        if not ques_list:
            SELENIUM_LOG_SCREEN(self.driver, width='70%')
            return '没有找到题目'
        n = 1
        for ques in ques_list:
            ques_id = ques.get_attribute('data-id')
            ques_type = ques.get_attribute('data-type')
            INFO(f'进行第{n}题试题作答、判断')
            print(f'进行第{n}题试题作答、判断')
            try:
                # student_do_homework.quesHandler(ques_id, ques_type, ques, self.driver)
                main_handler(ques_id, ques_type, self.driver, ques)
                print(f'第{n}题试题作答、判断完成！！！')
            except:
                # SELENIUM_LOG_SCREEN(self.driver, width='70%')
                print(f'第{n}题试题作答、判断失败？？？')
                pass
            print('\n')
            INFO('\n\n')
            sleep(0.3)
            n += 1

        # 作业提交时间限制
        while True:
            try:
                hour = self.driver.find_element_by_css_selector('.countdown_hour').text
                minute = self.driver.find_element_by_css_selector('.countdown_minute').text
                second = self.driver.find_element_by_css_selector('.countdown_second').text
                if int(hour) * 3600 + int(minute) * 60 + int(second) > 90:
                    print(int(hour) * 3600 + int(minute) * 60 + int(second))
                    break
                sleep(5)
            except:
                traceback.print_exc()
                break

        sleep(1)
        # 点击提交按钮
        self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
        sleep(0.5)
        # 确认提交
        self.driver.find_element_by_css_selector('.ui-dialog-buttonset button:nth-child(2)').click()
        sleep(0.5)

        # 判断录音是否判断完成,提交完成
        save_n = 0
        mp3_n = 0
        num_n = 0
        while True:
            try:
                msg_info = self.driver.find_element_by_css_selector('.message-info')
                if msg_info.text == '目前有音频未识别，请等待判分。':
                    mp3_n += 1
                    if mp3_n == 20:
                        CHECK_POINT('录音判分成功', False)
                        break
                elif msg_info.text == '记录保存成功':
                    for button in self.driver.find_elements_by_css_selector('.ui-button-text'):
                        if button.text == '我知道了':
                            button.click()
                            continue
                    sleep(2)
                    # try:
                    #     self.driver.find_element_by_css_selector('.submit_teacher').click()
                    #     for button in self.driver.find_elements_by_css_selector('.ui-button-text'):
                    #         if button.text == '提交':
                    #             button.click()
                    #             continue
                    # except:
                    #     traceback.print_exc()

                    break
                else:
                    save_n += 1
                    sleep(0.5)

                if save_n > 10:
                    CHECK_POINT('作业提交失败', False)
                    break
                elif self.driver.find_elements_by_css_selector('.ui-dialog .zeroTips p'):
                    for button in self.driver.find_elements_by_css_selector('.ui-button-text'):
                        if button.text == '继续提交':
                            button.click()
                            sleep(0.5)
                            continue
                    for button in self.driver.find_elements_by_css_selector('.ui-button-text'):
                        if button.text == '提交':
                            button.click()
                            continue
                sleep(0.5)
            except:
                traceback.print_exc()
                num_n += 1
                if num_n > 10:
                    SELENIUM_LOG_SCREEN(self.driver, width='70%')
                    CHECK_POINT('作业提交失败', False)
                    print('作业提交失败')
                    break
                sleep(0.5)
        print('\n\n')

        return True

    def checkResult(self):
        result_text = self.driver.find_elements_by_css_selector('.H_score')
        if result_text:
            print(f'学生实际得分：{result_text[0].text}')
            INFO(f'学生实际得分：{result_text[0].text}')

        return True


studentExam = StudentExam()

if __name__ == "__main__":
    from config.config import BrowserDriver

    verfCode.login()
    login.open_browser(BrowserDriver)
    login.login(username='waiyan', password='123456lj', url=UrlBase.login_url)
    studentExam.chosePaper(login.driver, 3, '228304')
    studentExam.doPaper('228304')
    studentExam.checkResult()
