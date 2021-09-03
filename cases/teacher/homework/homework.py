# -*- coding:utf-8 -*-
# @FileName  :one_paper.py
# @Time      :2021/8/10 11:03
# @Author    :姜楠
# @Tool      :PyCharm
from time import sleep
from selenium import webdriver
from hytest import *
from lib.HomeWork import teacher_operate, del_paper, student_Do_homework
from lib.loginTs import login, login_1
from lib.ReadExcel import read_excel_homework
from config.config import account, browser_driver, url_base


def make_ddt():
    dicts = read_excel_homework()
    ddt_list = []
    for dict1 in dicts:
        ddt_list.append({
            'name': dict1,
            "para": dicts[dict1]
        })
    return ddt_list


def suite_setup():
    INFO('发布作业用例文件初始化')
    STEP(1, '老师登录')
    login.login(account.teacher['rc']['teacher_username'], account.teacher['rc']['teacher_password'],
                url_base.rc['login_url'])
    sleep(0.5)
    STEP(2, '学生登录')
    login_1.login(account.student['rc']['student_username'], account.student['rc']['student_password'],
                  url_base.rc['login_url'])
    sleep(0.5)


def suite_teardown():
    INFO('退出登录')
    sleep(0.5)
    login.logout()
    login_1.logout()


class Teacher_operate:
    # ddt_cases 里面每个字典元素 定义一个用例的数据
    # 其中： name是该用例的名称， para是用例的参数
    ddt_cases = make_ddt()
    tags = ['冒烟测试', 'UI测试', '作业流程']

    def teststeps(self):
        mode, self.homework_name, grade_book, unite_book, book_type, paper, send_mode, vip, need_do = self.para

        STEP(1, '进入作业模块')
        INFO(teacher_operate.mode_list1[mode - 1])
        ret = teacher_operate.get_homework_page(GSTORE['driver'], mode)
        CHECK_POINT('进入作业模块成功', ret)
        sleep(0.5)

        STEP(2, '配置单个作业的类型名称等等')
        INFO(f"""
            作业名称：{self.homework_name}
            教材年级：{grade_book}
            选择单元：{unite_book}
            作业类型索引：{book_type}
        """)
        ret = teacher_operate.one_homework_pz(self.homework_name, grade_book, unite_book, book_type)
        CHECK_POINT('作业配置成功', ret)

        STEP(3, '选择试卷')
        INFO(f'试卷选择索引：{paper}')
        ret = teacher_operate.chiose_paper(book_type, paper)
        CHECK_POINT('题目选择成功', ret)

        STEP(4, '发布作业')
        teacher_operate.send_homework(send_mode, vip)

        sleep(1)

        STEP(5, '发布结果')
        driver: webdriver.Edge = GSTORE['driver']
        sleep(0.5)
        info_text = driver.find_element_by_css_selector('.message-info').text
        print(info_text, 1)
        driver.find_element_by_css_selector('#TinSoMessageBox + div span').click()
        CHECK_POINT('发布成功', '发布成功！' in info_text)

        print(need_do)
        if need_do == 1:
            try:
                STEP(6, '学生完成作业')
                ret = student_Do_homework.run(self.homework_name, GSTORE['driver1'])
                INFO(ret)
                CHECK_POINT('完成作业', True)

                STEP(7, '老师批阅作业')
                ret = teacher_operate.check_homework(self.homework_name)
                CHECK_POINT('老师批阅作业成功', ret)

                STEP(8, '学生查看批阅结果')
                ret = student_Do_homework.check_homework(self.homework_name)
                CHECK_POINT('查看批阅结果', ret == '这是一个作业批阅评语')
            except:
                pass

    def teardown(self):
        del_paper.get_homework_page(GSTORE['driver'])
        del_paper.del_homework(self.homework_name)


if __name__ == "__main__":
    print(make_ddt())
