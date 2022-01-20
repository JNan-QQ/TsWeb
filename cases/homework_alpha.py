# -*- coding:utf-8 -*-
# @FileName  :homework_alpha.py
# @Time      :2022/1/17 17:16
# @Author    :姜楠
# @Tool      :PyCharm
from time import sleep
from hytest import *
from lib.exam_homework import studentExam
from lib.loginTs import login_1
from lib.ReadExcel import read_excel_paper
from config.config import AccountConfig, UrlBase


def make_ddt():
    dicts = read_excel_paper()
    ddt_list = []
    for dict1 in dicts:
        ddt_list.append({
            'name': dict1,
            "para": dicts[dict1]
        })
    return ddt_list


def suite_setup():
    INFO('发布作业用例文件初始化')
    STEP(1, '学生登录')
    login_1.login(AccountConfig.student['alpha']['student_username'],
                  AccountConfig.student['alpha']['student_password'],
                  UrlBase.alpha['login_url'])
    sleep(0.5)


def suite_teardown():
    INFO('退出登录')
    sleep(0.5)
    login_1.logout()


class Test_:
    # ddt_cases 里面每个字典元素 定义一个用例的数据
    # 其中： name是该用例的名称， para是用例的参数
    ddt_cases = make_ddt()
    tags = ['homework']

    def teststeps(self):
        mode, grade, paper_id, paper_name, paper_unit = self.para

        STEP(1, f'查找进入作业 {paper_name}')
        ret = studentExam.chosePaper(GSTORE['driver1'], mode, paper_id)
        CHECK_POINT('查找到作业', ret)

        STEP(2, '学生练习作业')
        ret = studentExam.doPaper(paper_name)
        CHECK_POINT('试卷练习完成', ret)

        STEP(3, '查看练习结果')
        ret = studentExam.checkResult()
        CHECK_POINT('练习结果查看正确', ret)


if __name__ == "__main__":
    run_code = 0
