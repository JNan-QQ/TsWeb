# -*- coding:utf-8 -*-
# @FileName  :VerificationCode.py
# @Time      :2021/7/22 12:48
# @Author    :姜楠
# @Tool      :PyCharm
import datetime
import os
import time
import traceback
from hytest import *
import requests
import wmi

import random
import string

import time


def time_salt():
    unix_time = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime()), '%Y-%m-%d')))
    return str(unix_time)[0:8]


# 字符串加密
def encrypt(s):
    # 盐值用于加密钥生成
    salt_base = f"%@*{time_salt()[::-1]}*@%"

    n = int(len(s) / len(salt_base))
    # 加密钥
    salt = (n + 1) * salt_base
    encry_str = ''
    for i, j in zip(s, salt):
        ss = str(ord(i) + ord(j))
        cc = list(ss)
        for _ in range(5 - len(ss)):
            cc.insert(random.randint(0, len(cc) - 1), random.sample(string.ascii_letters, 1)[0])
        encry_str += ''.join(cc)

    return encry_str


class YZM:
    file_path = fr"{os.path.expanduser('~')}/.jiangnan/license.jn"
    host = 'www.zdhua.top'
    session = requests.Session()
    GSTORE['session'] = session

    @staticmethod
    def cipherTable():
        k = '105201314'
        str2 = ''
        str1 = str(time.time())[0:8]
        for i, j in zip(str1, k):
            if i.isalpha():
                str2 += str(ord(i) - 64 + ord(j))
            else:
                str2 += str(int(i) + int(j))
        return str2

    def login(self):
        print("""\n
                        欢迎使用线上服务系统！
            如果没有账号可以注册绑定设备（一个账号最多绑定三台设备）\n
        """)
        if not os.path.exists(self.file_path):
            os.makedirs(fr"{os.path.expanduser('~')}/.jiangnan", exist_ok=True)
            print('检查到你的系统中未绑定账号，请登录或注册！\n')
            username = input('请输入 用户名：')
            password = input('请输入 密　码：')
            mode = 1
        else:
            with open(self.file_path, 'r', encoding='utf8') as f:
                str1 = f.read()
            username = str1.split('||')[0]
            password = str1.split('||')[1]
            mode = 2

        # 发送登录请求
        res = self.session.post(f'https://{self.host}/api/sign', json={
            "username": username,
            "password": encrypt(password),
            'action': 'signin'
        })
        try:
            if res.json()['ret'] == 0:
                print('账号登录成功！\n')
                if mode == 1:
                    with open(self.file_path, 'w', encoding='utf8') as f:
                        f.write(f'{username}||{password}')
            elif res.json()['ret'] == 1:
                if mode == 2:
                    os.remove(self.file_path)
        except:
            traceback.print_exc()
            print('服务器异常！')

    def logout(self):
        # 发送登录请求
        res = self.session.post(f'https://{self.host}/api/sign', json={
            'action': 'signout'
        })
        if res.json()['ret'] == 0:
            print('退出登录成功')

    def simpleCheck(self):
        print('开始验证设备是否激活.....\n')
        res = self.session.post(f'https://{self.host}/api/pay/user', json={
            'action': 'checkActive',
        })
        if res.status_code == 200:
            res = res.json()
            local_code = self.cipherTable()
            if res['ret'] == 0:
                # if res['code'] != local_code:
                #     if int(res['code']) == int(local_code)-1:
                #         return True
                #     else:
                #         print('验证失败')
                #         print('\n或请登录以下网址进行操作：https://www.zdonghua.top\n')
                #         return False
                print('账号在服务期间')
                return True
            else:
                print(res['msg'])
                return False
        else:
            print('请求出错')
            return False

    def checkActivation(self):
        c = wmi.WMI()

        cpu = c.Win32_Processor()[0].ProcessorId.strip()
        board = c.Win32_BaseBoard()[0].SerialNumber
        # 设备编码
        machineCode = cpu[0:7] + board[0:-7] + cpu[7:] + board[-7:]

        print('开始验证设备是否可以激活.....\n')
        res = self.session.post(f'http://{self.host}/Token', json={
            'action': 'machineCode',
            'code': machineCode
        })
        # 校验码
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        activeCode = machineCode[0:2] + now_time[10:] + machineCode[2:4] + now_time[6:8] + machineCode[4:6] + \
                     now_time[0:2] + machineCode[6:9] + now_time[8:10] + machineCode[9:10] + now_time[
                                                                                             2:4] + machineCode[10:]
        activeCode = self.cipherTable()

        res = res.json()
        if res['ret'] == 0 and res['activeCode'] == activeCode:
            print(f'该账号有效期至：{res["endTime"].replace("T", " ")} ,请注意使用时间及时续费!')
            return True
        else:
            print(res['msg'])
            print('\n或请登录以下网址进行操作：https://www.zdonghua.top')
            print()


verfCode = YZM()

if __name__ == '__main__':
    verfCode.login()
    verfCode.simpleCheck()
