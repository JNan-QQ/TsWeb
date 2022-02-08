# -*- coding:utf-8 -*-
# @FileName  :config.py
# @Time      :2021/8/10 10:35
# @Author    :姜楠
# @Tool      :PyCharm
import os
import requests
from hytest import *
from lib.VerificationCode import verfCode


def getConfig():
    verfCode.login()
    session: requests.Session = GSTORE['session']

    configDict = session.post(f'https://{verfCode.host}/api/pay/user', json={
        'action': 'listServerConfig',
    })

    return configDict.json()['userServerConfig']


config_dict = getConfig()


# url配置
class UrlBase:
    username = config_dict['UrlBase']['username']
    login_url = fr'https://{username}-www.b.waiyutong.org/'
    mode_url = [fr'http://{username}-student.b.waiyutong.org/Paper/renjiduihua.html',
                fr'http://{username}-student.b.waiyutong.org/Paper/bishi.html',
                fr'http://{username}-student.b.waiyutong.org/Practice/papers.html']
    start_url = config_dict['UrlBase']['start_url']


# 账号信息
class AccountConfig:
    # 老师账号信息
    teacher = config_dict['AccountConfig']['teacher']
    student = config_dict['AccountConfig']['student']


# 测试用例cases配置
class CasesConfig:
    # 用例编号在文件xlsx下的列数
    case_No = config_dict['CasesConfig']['case_No']
    # 测试用例结果在文件xlsx下的列数
    case_result = config_dict['CasesConfig']['case_result']
    # 测试用例文件路径，不用修改
    cases_path = config_dict['CasesConfig']['cases_path']


# 浏览器与驱动
class BrowserDriver:
    browser_kernel = config_dict['BrowserDriver']['browser_kernel']
    # 浏览器驱动路径
    driver_path = config_dict['BrowserDriver']['driver_path']
    # 浏览器路径
    browser_path = config_dict['BrowserDriver']['browser_path']


# lib配置
class LibConfig:
    mysqlAlpha = config_dict['LibConfig']['mysqlAlpha']
    mysqlBeta = config_dict['LibConfig']['mysqlBeta']


class QType:
    # 选择题
    opt = config_dict['QType']['opt']

    # 填空题
    blank = config_dict['QType']['blank']
