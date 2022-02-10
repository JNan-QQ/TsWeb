# -*- coding:utf-8 -*-
# @FileName  :VerificationCode.py
# @Time      :2021/7/22 12:48
# @Author    :姜楠
# @Tool      :PyCharm
import traceback
from hytest import *
import requests


class YZM:
    file_path = fr"config/account.jn"
    host = 'www.zdhua.top'
    session = requests.Session()
    GSTORE['session'] = session

    def login(self):
        print("""\n
                        欢迎使用线上服务系统！
            如果没有账号可以注册绑定设备（一个账号最多绑定三台设备）\n
        """)
        if not os.path.exists(self.file_path):
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
            "password": password,
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
            if res['ret'] == 0:
                print('账号在服务期间')
                return True
            else:
                print(res['msg'])
                return False
        else:
            print('请求出错')
            return False


verfCode = YZM()

if __name__ == '__main__':
    verfCode.login()
    verfCode.simpleCheck()
