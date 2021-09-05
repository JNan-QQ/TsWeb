# -*- coding:utf-8 -*-
# @FileName  :HomeWork.py
# @Time      :2021/7/22 15:03
# @Author    :姜楠
# @Tool      :PyCharm
from time import sleep
from hytest import *
from selenium import webdriver
from lib.doQuestions import student_do_homework
from lib.loginTs import login


class TeacherSendHomework:
    mode_list1 = ['单个作业', '批量作业']

    # 进入作业模块
    def getHomeworkPage(self, driver, mode=1):
        mode_list = ['newHomework', 'newMultipleHomework']
        self.driver = driver
        # 进入单个作业或批量作业页面
        self.driver.get(fr'http://teacher.waiyutong.org/Homework/{mode_list[mode - 1]}.html')

        print(f'进入模块：{self.mode_list1[mode - 1]}')
        sleep(1)
        return True

    # 单个作业模块配置
    def one_homework_pz(self, papername='', book_grade='', unit_book=None, home_type=1):
        if papername == '':
            papername = '自动化发布作业'
        if book_grade == '':
            book_grade = '七年级上'
        sleep(0.5)

        # 输入作业名称
        self.driver.find_element_by_css_selector('.homework_title').send_keys(papername)
        print(f'输入作业名称：{papername}')
        sleep(0.5)

        # 选择教材年级
        grade_list = self.driver.find_elements_by_css_selector('.book_grade_area img')
        for ii in grade_list:
            if book_grade == ii.get_attribute('title'):
                self.driver.execute_script("$(arguments[0]).click()", ii)
                break
        else:
            print('教材年级出错')

        print(f'选择教材年级：{book_grade}')
        sleep(0.5)

        # 教程单元选择
        self.driver.find_element_by_xpath(
            f'//*[@class="unit_data"]/*[@class="book_unit_cnt dib-wrap show"]/label[1]').click()
        for ii in unit_book:
            if ii == 0:
                continue
            self.driver.find_element_by_xpath(
                f'//*[@class="unit_data"]/*[@class="book_unit_cnt dib-wrap show"]/label[{ii}]').click()

        print(f'选择单元：{unit_book}')
        sleep(0.5)

        # 选择作业类型
        if int(home_type) <= 10:
            self.driver.find_element_by_css_selector(f'.type_data.auto label:nth-child({home_type})').click()
        else:
            self.driver.find_element_by_css_selector(f'.type_data.self label:nth-child({home_type - 10})').click()

        print(f'选择第{home_type}个作业类型')
        sleep(0.5)

        return True

    # 选择试卷
    def chiose_paper(self, home_type=1, home_paper=None):
        # 选择作业
        home_type = int(home_type)

        if home_type in [11, 18, 19]:
            if home_type == 11:
                self.driver.find_element_by_css_selector(f'.paper_test:nth-child({home_paper[1][0]})').click()
            else:
                checks = self.driver.find_elements_by_css_selector('.test_list_label .checked')
                for check in checks:
                    self.driver.execute_script("$(arguments[0]).click()", check)
                sleep(0.5)
                for i in home_paper[1]:
                    chil = self.driver.find_elements_by_css_selector(f'.test_list_label:nth-child({i})')
                    self.driver.execute_script("$(arguments[0]).click()", chil)

        elif home_type > 10:
            for k, v in home_paper.items():
                self.driver.find_element_by_css_selector(f'.class_unit span:nth-child({k})').click()
                for checked in self.driver.find_elements_by_css_selector('.tests_list_panel .active label .checked'):
                    self.driver.execute_script("$(arguments[0]).click()", checked)
                sleep(1)
                for iii in v:
                    if iii == 0 or home_type == 15:
                        continue
                    elif home_type == 17:
                        chil = self.driver.find_element_by_css_selector(
                            f'.word_list_label:nth-child({iii})')
                        self.driver.execute_script("$(arguments[0]).click()", chil)
                    else:
                        chil = self.driver.find_element_by_css_selector(
                            f'.tests_list_panel .active label:nth-child({iii})')
                        self.driver.execute_script("$(arguments[0]).click()", chil)
        print('试卷选择完成')
        return True

    # 发布作业
    def send_homework(self, send_mode, vip):
        # 点击发布按钮
        self.driver.find_element_by_css_selector(f'.publish_config a:nth-last-of-type({send_mode})').click()
        # 选择vip
        if vip == 1:
            self.driver.find_element_by_css_selector('#vip_homework_label').click()
        # 发布
        self.driver.find_element_by_css_selector('.ui-dialog-buttonset button:nth-child(2)').click()

        print('试卷发布成功')
        return True

    def check_homework(self, homework_name, lv=1, str_py='这是一个作业批阅评语'):
        self.driver.get(r'http://teacher.waiyutong.org/Homework/lists.html')
        sleep(0.5)
        elem = self.driver.find_element_by_css_selector('.homework_name')
        if homework_name == elem.find_element_by_css_selector('div>a').text:
            views = elem.find_elements_by_css_selector('span a.homework_list_detail')
            if views:
                views[0].click()
                piyue = self.driver.find_elements_by_css_selector('.thw_hw_mark.enabled.br_small')
                if piyue:
                    piyue[0].click()
                    sleep(0.5)
                    self.driver.find_element_by_css_selector(f'.commenttext_btn>span:nth-child({lv})').click()
                    self.driver.find_element_by_css_selector('textarea.commenttextarea').clear()
                    self.driver.find_element_by_css_selector('textarea.commenttextarea').send_keys(str_py)
                    self.driver.find_element_by_css_selector('.thw_MK_student_btn.enabled').click()
                    self.driver.find_element_by_css_selector('.ui-button-text').click()
                    return True
            else:
                pass

    def run(self, args):
        self.getHomeworkPage(int(args[0]))
        self.one_homework_pz(args[1], args[2], args[3], args[4])
        self.chiose_paper(args[4], args[5])
        self.send_homework(args[6], args[7])


teacher_operate = TeacherSendHomework()


class del_homework:

    def get_homework_page(self, driver, url='http://teacher.waiyutong.org/Homework/lists.html'):
        self.driver = driver
        self.driver.get(url)
        sleep(0.5)

    def del_homework(self, homework_name):
        self.driver.find_element_by_css_selector('.time_select_btn').click()
        sleep(0.5)
        try:
            elem = self.driver.find_element_by_css_selector('.homework_name')
            if homework_name == elem.find_element_by_css_selector('div>a').text:
                chil = self.driver.find_element_by_css_selector('.deletedHomework')
                self.driver.execute_script("$(arguments[0]).click()", chil)
                self.driver.find_element_by_css_selector('.ui-button-text').click()
                self.driver.find_element_by_css_selector('#TinSoMessageBox + div span').click()
        except:
            pass

    def del_all(self):
        while True:
            elem = self.driver.find_elements_by_css_selector('.homework_name>div>a')
            if not elem:
                break
            self.del_homework(elem[0].text)
            sleep(1)


del_paper = del_homework()


class Student_do_homework:

    def get_homework_page(self, driver):
        self.driver: webdriver.Edge = driver
        print(self.driver)
        self.driver.get(r"http://student.waiyutong.org/Homework/lists.html")
        sleep(1)
        return True

    def chose_homework(self, homework_name):
        elem_homework_list = self.driver.find_elements_by_css_selector('.homework.list_container')
        if homework_name != elem_homework_list[0].find_element_by_css_selector('.homework_title').text:
            return
        elem_homework_list[0].find_element_by_css_selector('.remain_status_btn a:nth-child(1)').click()
        sleep(2)
        return True

    def do_homework(self):
        # 等待试卷加载
        sleep(1.5)
        while True:
            try:
                self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
                self.driver.find_element_by_css_selector('button.ui-button').click()
                break
            except:
                try:
                    self.driver.find_element_by_css_selector('button.ui-button').click()
                    sleep(1)
                except:
                    pass

        ques_list = self.driver.find_elements_by_css_selector('.test_content')
        if not ques_list:
            SELENIUM_LOG_SCREEN(self.driver, width='70%')
            return '没有找到题目'
        # 题目比对结果列表【true,false】
        ques_check_list = []
        n = 1
        for ques in ques_list:
            ques_id = ques.get_attribute('data-id')
            ques_type = ques.get_attribute('data-type')
            INFO(f'进行第{n}题试题作答、判断')
            try:
                ret = student_do_homework.quesHandler(ques_id, ques_type, ques, self.driver)
                ques_check_list.append(ret)
            except:
                pass
            sleep(0.5)
            n += 1
        while True:
            time_spend = self.driver.find_element_by_css_selector(
                '.countdown_minute').text + self.driver.find_element_by_css_selector('.countdown_second').text
            if int(time_spend) >= 130:
                break
            sleep(3)
        try:
            self.driver.find_element_by_css_selector('.p_answerSubmit_btn').click()
            self.driver.find_element_by_css_selector('.ui-dialog-buttonset button:nth-child(2)').click()
            self.driver.find_element_by_css_selector('.ui-button-text').click()
            self.driver.find_element_by_css_selector('.submit_homework').click()
            self.driver.find_element_by_css_selector('.ui-button-text').click()
        except:
            SELENIUM_LOG_SCREEN(self.driver, width='70%')

        return ques_check_list

    def check_homework(self, homework_name):
        self.driver.get(r"http://student.waiyutong.org/Homework/lists.html")
        sleep(1)
        elem_homework_list = self.driver.find_elements_by_css_selector('.homework.list_container')
        if homework_name != elem_homework_list[0].find_element_by_css_selector('.homework_title').text:
            return
        elem_homework_list[0].find_element_by_css_selector('.homework_marking').click()
        py = self.driver.find_element_by_css_selector('.marking_comment').text
        return py

    def run(self, homework_name, driver):
        self.get_homework_page(driver)
        self.chose_homework(homework_name)
        ret = self.do_homework()
        return ret


student_Do_homework = Student_do_homework()

if __name__ == "__main__":
    login.open_browser('Chrome')
    login.login(username='waiyan', password='ts123456')
    student_Do_homework.get_homework_page(login.driver)
    student_Do_homework.chose_homework('自主作文')
    student_Do_homework.do_homework()
