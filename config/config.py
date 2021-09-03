# -*- coding:utf-8 -*-
# @FileName  :config.py
# @Time      :2021/8/10 10:35
# @Author    :姜楠
# @Tool      :PyCharm
import os


class account:
    # 老师账号信息
    teacher = {
        'alpha': {
            'teacher_username': 'wym老师1',
            'teacher_password': '123456'
        },
        'beta': {
            'teacher_username': 'wym老师1',
            'teacher_password': '123456'
        },
        'rc': {
            'teacher_username': 'wym老师1',
            'teacher_password': '123456'
        }

    }

    # 学生账号信息
    student = {
        'alpha': {
            'student_username': 'jn0002',
            'student_password': 'ts123456'
        },
        'beta': {
            'student_username': 'waiyan',
            'student_password': '123456lj'
        },
        'rc': {
            'student_username': 'waiyan',
            'student_password': '123456lj'
        }

    }
    # student_username = 'waiyan'
    # student_password = '123456lj'
    # student_username = 'jn0002'
    # student_password = 'ts123456'


# 测试用例cases配置
class cases_config:
    # 用例编号在文件xlsx下的列数
    case_No = 1
    # 测试用例结果在文件xlsx下的列数
    case_result = 5
    # 测试用例文件路径，不用修改
    cases_path = os.getcwd() + r'\config\cases.xlsx'


class browser_driver:
    # 浏览器驱动路径
    teacher_browser = {
        'browser_kernel': 'Chrome',
        # 浏览器驱动路径
        'driver_path': r'C:\PythonTool\chromedriver.exe',
        # 浏览器路径
        'browser_path': r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    }
    # student_browser = {
    #     # 浏览器内核
    #     'browser_kernel': 'Edge',
    #     # 浏览器驱动路径
    #     'driver_path': r'C:\PythonTool\msedgedriver.exe',
    #     # 浏览器路径
    #     'browser_path': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    # }

    student_browser = {
        # 浏览器内核
        'browser_kernel': 'Chrome',
        # 浏览器驱动路径
        'driver_path': r'C:\PythonTool\chromedriver_360.exe',
        # 浏览器路径
        'browser_path': r'C:\Users\Administrator\AppData\Local\360Chrome\Chrome\Application\360chrome.exe'
    }


class url_base:
    alpha = {
        'login_url': r'https://jiangnan-www.b.waiyutong.org/',
        'mode_url': [r'http://jiangnan-student.b.waiyutong.org/Paper/renjiduihua.html',
                     r'http://jiangnan-student.b.waiyutong.org/Paper/bishi.html']
    }
    beta = {
        'login_url': r'https://www-beta.waiyutong.org/',
        'mode_url': [r'http://student-beta.waiyutong.org/Paper/renjiduihua.html',
                     r'http://student-beta.waiyutong.org/Paper/bishi.html']
    }
    rc = {
        'login_url': r'https://www.waiyutong.org/',
        'mode_url': [r'http://student.waiyutong.org/Paper/renjiduihua.html',
                     r'http://student.waiyutong.org/Paper/bishi.html']
    }


if __name__ == "__main__":
    print(cases_config.cases_path)
