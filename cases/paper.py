# -*- coding:utf-8 -*-
# @FileName  :ExamPaper.py
# @Time      :2021/8/17 9:25
# @Author    :姜楠
# @Tool      :PyCharm
from time import sleep

from hytest import *

from config.config import getCaseConfigData
from lib.ReadExcel import read_excel_paper
from lib.exam_paper import studentExam
from lib.loginTs import login_student


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
    login_student.login(getCaseConfigData.Account['student'], getCaseConfigData.Url['login_url'])
    sleep(0.5)


def suite_teardown():
    INFO('退出登录')
    sleep(0.5)
    login_student.logout()


class Test_:
    # ddt_cases 里面每个字典元素 定义一个用例的数据
    # 其中： name是该用例的名称， para是用例的参数
    ddt_cases = make_ddt()
    tags = ['paper']

    def teststeps(self):
        mode, grade, paper_id, paper_name, paper_unit = self.para

        STEP(1, f'进入{studentExam.mode_name[mode - 1]}页面')
        ret = studentExam.getExamPage(GSTORE['driver_student'], mode)
        CHECK_POINT('进入指定界面', ret)

        STEP(2, f'选择年级：{grade}|班级：{paper_unit}')
        ret = studentExam.choseGrade(grade, paper_id)
        CHECK_POINT('选择正确年级', ret)

        STEP(3, f'查找试卷 {paper_name}')
        ret = studentExam.chosePaper(paper_name, mode, paper_id)
        CHECK_POINT('试卷已查找到', ret)

        STEP(4, '学生练习试卷')
        ret = studentExam.doPaper(paper_name)
        CHECK_POINT('试卷练习完成', ret)

        STEP(5, '学生提交作业')
        ret = studentExam.submitHomework(mode)
        CHECK_POINT('提交作业成功', ret)

        STEP(6, '查看练习结果')
        ret = studentExam.checkResult(mode)
        CHECK_POINT('练习结果查看正确', ret)
