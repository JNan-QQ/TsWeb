# -*- coding:utf-8 -*-
# @FileName  :config.py
# @Time      :2021/8/10 10:35
# @Author    :姜楠
# @Tool      :PyCharm
from lib.Mysql_Read import sqlite3Link


class getData:

    def __init__(self):
        values = sqlite3Link.select_table('info', None, 'value')
        self.env = values[1][0]
        self.browser = values[0][0]
        self.Url = self.getUrl()
        self.Account = self.getAccount()
        self.Browser = self.getBrowser()
        self.QType = self.getQType()
        self.MysqlLinkInfo = self.getMysqlLinkInfo()

    # 链接信息
    def getUrl(self):

        if self.env == 'rc':
            host_url = 'https://www.waiyutong.org'
        elif self.env == 'beta':
            host_url = 'https://www-beta.waiyutong.org'
        else:
            username = sqlite3Link.select_table('account_info', 'user_type="branch"', 'username')[0][0]
            host_url = f'https://{username}-www.b.waiyutong.org'

        student_host = host_url.replace('www', 'student')
        # 模块链接
        mode_url = {'人机对话': f'{student_host}/Paper/renjiduihua.html', '笔试考场': f'{student_host}/Paper/bishi.html',
                    '外语通作业': f'{student_host}/Homework/lists.html'}
        # 练习界面链接
        exam_host = student_host + '/Practice'
        exam_url = [
            exam_host + '/paperPractice.html?type=ts&mode=free&version=1&grade=%s&id=%s',
            exam_host + '/paperPractice.html?type=bs&mode=free&version=1&grade=%s&id=%s',
            exam_host + '/homework.html?mode=free&grade=%s&hid=%s'
        ]

        return {'login_url': host_url, 'mode_url': mode_url, 'exam_url': exam_url}

    def getAccount(self):
        values = sqlite3Link.select_table('account_info', f'branch_type="{self.env}"')
        account = {}
        for item in values:
            account[item[3]] = [item[1], item[2]]
        return account

    def getBrowser(self):
        values = sqlite3Link.select_table('webdriver', f'browser_type="{self.browser}"')
        if not values:
            return
        else:
            return {'browser_type': values[0][1], 'browser_path': values[0][2], 'driver_path': values[0][3],
                    'default': values[0][4]}

    @staticmethod
    def getQType():
        values = sqlite3Link.select_table('topicType')
        qType = {}
        for item in values:
            qType[item[1]] = item[2].strip().split(',')
        qType['speak'] = qType['read_aloud'] + qType['situation_dialogue'] + qType['topic_brief']
        return qType

    def getMysqlLinkInfo(self):
        conf = \
            sqlite3Link.select_table('mysql_link_info', f'name="{self.env}"', 'host', 'port', 'user', 'passwd', 'db')[0]
        return conf


getCaseConfigData = getData()
