# -*- coding:utf-8 -*-
# @FileName  :exam_paper.py
# @Time      :2021/8/17 9:34
# @Author    :姜楠
# @Tool      :PyCharm
from time import sleep
from hytest import *
from selenium import webdriver
from lib.doQuestions import student_do_homework
from selenium.webdriver.support.ui import Select
from config.config import url_base
from lib.loginTs import login


class Student_exam:
    mode_url = url_base.rc['mode_url']
    mode_name = ['人机对话', '笔试考场']
    driver = None

    def get_exam_paper(self, driver, mode=1, url=None):
        sleep(1)
        INFO(f'进入{self.mode_name[mode - 1]}界面')
        self.driver: webdriver.Edge = driver
        if url:
            self.driver.get(url)
        else:
            self.driver.get(self.mode_url[mode - 1])

        try:
            self.driver.switch_to.alert.accept()
            sleep(1)
        except:
            sleep(1)
        return True

    def choise_grade(self, grade):
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
            '11A': '高二第一学期',
            '11B': '高二第二学期',
            '11C': '必修第二册',
            '12A': '高三第一学期',
            '12B': '高三第二学期',
            '12C': '必修第三册',
        }
        select = Select(
            self.driver.find_element_by_css_selector('.book_unit_select_cnt .book_unit_select.current .book_select'))
        # 通过 Select 对象选中
        # print(grades[grade])
        select.select_by_visible_text(grades[grade])
        sleep(0.5)

        return True

    def chose_paper(self, paper_name, mode):
        list1 = ['.rjdh_paper_title', '.bishi_paper_title']
        while True:
            flg = False
            papers = self.driver.find_elements_by_css_selector('.list_container')
            for i in papers:
                if paper_name == i.find_element_by_css_selector(list1[mode - 1]).text:
                    i.find_element_by_css_selector('.remain_status_btn a:nth-child(1)').click()
                    flg = True
                    break
            if flg:
                break
            else:
                btn = self.driver.find_element_by_css_selector('a.next')
                self.driver.execute_script("$(arguments[0]).click()", btn)
                sleep(3)

        return True

    def do_paper(self, paper_name):
        # 等待试卷加载
        sleep(1.5)
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
        ques_list = self.driver.find_elements_by_css_selector('.test_content')
        if not ques_list:
            SELENIUM_LOG_SCREEN(self.driver, width='70%')
            return '没有找到题目'
        n = 1
        for ques in ques_list:
            ques_id = ques.get_attribute('data-id')
            ques_type = ques.get_attribute('data-type')
            INFO(f'进行第{n}题试题作答、判断')
            try:
                student_do_homework.ques_handler(ques_id, ques_type, ques, self.driver)
                print(f'第{n}题试题作答、判断完成！！！')
            except:
                # SELENIUM_LOG_SCREEN(self.driver, width='70%')
                pass
            sleep(0.5)
            n += 1

        # 等待音频播放完毕
        # while True:
        #     try:
        #         mp3s = self.driver.find_element_by_css_selector('.test_ctrl_info_area').get_attribute('style')
        #         if mp3s != 'display: block;':
        #             break
        #     except:
        #         sleep(5)

        self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
        sleep(1)
        self.driver.find_element_by_css_selector('.ui-dialog-buttonset button:nth-child(2)').click()
        sleep(0.5)
        n = 0
        while True:
            if self.driver.find_element_by_css_selector('.message-info').text == '记录保存成功':
                self.driver.find_element_by_css_selector('.ui-button-text').click()
                break
            else:
                sleep(1)
                if n == 10:
                    #
                    break
                n += 1

        return True

    def check_result(self):
        right = [i.text for i in self.driver.find_elements_by_css_selector('.answer_list_right_class')]
        wrong = [i.text for i in self.driver.find_elements_by_css_selector('.answer_list_wrong_class')]
        INFO(f'答对的题目序号：{right}')
        INFO(f'答错的题目序号：{wrong}')

        return True


student_exam = Student_exam()

if __name__ == "__main__":
    from config.config import browser_driver

    login.open_browser(browser_driver.student_browser)
    login.login(username='waiyan', password='123456lj', url=url_base.rc['login_url'])
    student_exam.get_exam_paper(login.driver)
    student_exam.choise_grade('9A')
    student_exam.chose_paper('江苏省9AU01人机对话单元卷01', 1)
    student_exam.do_paper('江苏省9AU01人机对话单元卷01')
