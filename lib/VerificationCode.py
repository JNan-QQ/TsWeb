# -*- coding:utf-8 -*-
# @FileName  :VerificationCode.py
# @Time      :2021/7/22 12:48
# @Author    :姜楠
# @Tool      :PyCharm
import os
import requests
from config.config import LibConfig

class YZM:
    file_path = fr"{os.path.expanduser('~')}/.jiangnan/license.jn"
    host = LibConfig.verificationHost

    # 激活系统
    def activation(self):
        name = input('请输入激活分配用户名：')
        tokens = input('请输入分配激活码：')
        with open(self.file_path, 'w', encoding='utf8') as f:
            f.write(f'{name}||{tokens}')

        response = requests.get(fr'{self.host}/tokens?action=check&name={name}&token={tokens}')
        res = response.json()
        if res['ret'] == 0:
            print('激活成功')
            return True
        else:
            print('激活失败')
            return False

    def license(self):
        if not os.path.exists(self.file_path):
            os.makedirs(fr"{os.path.expanduser('~')}/.jiangnan", exist_ok=True)
            return self.activation()
        with open(self.file_path, 'r', encoding='utf8') as f:
            str1 = f.read()
        name = str1.split('||')[0]
        token = str1.split('||')[1]
        response = requests.get(fr'{self.host}/tokens?action=check&name={name}&token={token}')
        res = response.json()
        if res['ret'] == 0:
            print('验证成功')
            return True
        else:
            print('验证失败', res)
            return False

    def addLicense(self, name, tokens, type1):
        response = requests.post(fr'{self.host}/tokens', json={
            'action': 'add',
            'name': name,
            'token': tokens,
            'type': type1
        })
        res = response.json()
        return res


verfCode = YZM()
