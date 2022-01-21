# -*- coding:utf-8 -*-
# @FileName  :config.py
# @Time      :2021/8/10 10:35
# @Author    :姜楠
# @Tool      :PyCharm
import os


# 账号信息
class AccountConfig:
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
        # 'alpha': {
        #     'student_username': 'waiyan',
        #     'student_password': '123456lj'
        # },
        'alpha': {
            'student_username': 'studentReceiver',
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


# 测试用例cases配置
class CasesConfig:
    # 用例编号在文件xlsx下的列数
    case_No = 1
    # 测试用例结果在文件xlsx下的列数
    case_result = 7
    # 测试用例文件路径，不用修改
    cases_path = os.getcwd() + r'\config\cases.xlsx'


# 浏览器与驱动
class BrowserDriver:
    # 浏览器驱动路径
    student_browser = {
        'browser_kernel': 'Chrome',
        # 浏览器驱动路径
        'driver_path': r'C:\PythonTool\chromedriver.exe',
        # 浏览器路径
        'browser_path': r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    }
    teacher_browser = {
        # 浏览器内核
        'browser_kernel': 'Edge',
        # 浏览器驱动路径
        'driver_path': r'C:\PythonTool\msedgedriver.exe',
        # 浏览器路径
        'browser_path': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    }

    # student_browser = {
    #     # 浏览器内核
    #     'browser_kernel': 'Chrome',
    #     # 浏览器驱动路径
    #     'driver_path': r'C:\PythonTool\chromedriver_360.exe',
    #     # 浏览器路径
    #     'browser_path': r'C:\Users\Administrator\AppData\Local\360Chrome\Chrome\Application\360chrome.exe'
    # }


# url配置
class UrlBase:
    username = 'jiangnan'
    alpha = {
        'login_url': fr'https://{username}-www.b.waiyutong.org/',
        'mode_url': [fr'http://{username}-student.b.waiyutong.org/Paper/renjiduihua.html',
                     fr'http://{username}-student.b.waiyutong.org/Paper/bishi.html',
                     fr'http://{username}-student.b.waiyutong.org/Practice/papers.html'],
        'start_url': '',
    }
    beta = {
        'login_url': r'https://www-beta.waiyutong.org/',
        'mode_url': [r'http://student-beta.waiyutong.org/Paper/renjiduihua.html',
                     r'http://student-beta.waiyutong.org/Paper/bishi.html',
                     r'http://student-beta.waiyutong.org/Practice/papers.html']
    }
    rc = {
        'login_url': r'https://www.waiyutong.org/',
        'mode_url': [r'http://student.waiyutong.org/Paper/renjiduihua.html',
                     r'http://student.waiyutong.org/Paper/bishi.html',
                     r'http://student.waiyutong.org/Practice/papers.html']
    }


# lib配置
class LibConfig:
    verificationHost = r'104.41.177.149'
    mysqlAplha = ['192.168.1.186', 'ts_waiyutong', 'Ts*#!@#123WYT']
    mysqlBeta = ['121.41.116.146', 'waiyutong_read', 'Ts123456']


class QType:
    # 选择题
    opt = ['1100', '1200', '2200', '2800', '2900', '13600', '12900', '12800']

    # 填空题
    blank = ['1300', '1600', '2100', '2500', '2600', '7300', '12600']


if __name__ == "__main__":
    print(CasesConfig.cases_path)
