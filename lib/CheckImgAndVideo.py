# -*- coding:utf-8 -*-
# @FileName  :CheckImgAndVideo.py
# @Time      :2021/8/16 12:58
# @Author    :姜楠
# @Tool      :PyCharm
import difflib
from hytest import INFO
import os
import requests

"""
检测图片完整性
JPG文件结尾标识：\xff\xd9
JPEG文件结尾标识：\xff\xd9
PNG文件结尾标识：\xaeB`\x82
"""


class ImageCheck:
    def checkImage(self, image_path=None, image_steam=None):
        type_dict = {
            'jpg': [b'\xff\xd8', b'\xff\xd9'],
            'png': [b'\x89PNG', b'\xaeB`\x82'],
            'jpeg': [b'\xff\xd8', b'\xff\xd9'],
        }
        if image_path:
            file_type = image_path.split('.')[-1].lower()

            with open(image_path, 'rb') as image:
                data = image.read()
            if file_type in ['jpeg', 'jpg']:
                return [data[:2], data[-2:]] == type_dict[file_type]
            elif file_type == 'png':
                return [data[:4], data[-4:]] == type_dict[file_type]

        if image_steam:
            data = image_steam
            flg = False
            if [data[:2], data[-2:]] == type_dict['jpg']:
                flg = True
            elif [data[:4], data[-4:]] == type_dict['png']:
                flg = True
            return flg

    def DownloadImage(self, image_url):
        print(image_url)
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            return False

    def run(self, img_url):
        ret = self.DownloadImage(image_url=img_url)
        if ret:
            return self.checkImage(image_steam=ret)
        else:
            return ret

    def check_name(self, web_img, mysql_img):
        web_img = [i.split('/')[-1] for i in web_img]
        for i in mysql_img:
            if i not in web_img:
                return False
        return True


imageCheck = ImageCheck()


def videoCheck(mp3_url):
    flg = []
    for i in mp3_url:
        response = requests.get(f'https://static.waiyutong.org/book/mp3/{i}')
        if response.status_code == 200:
            flg.append(True)
        else:
            flg.append(False)
    return flg


def getEqualRate(web1, mysql1):
    """
    比较两个字符串的相似程度
    Args:
        web1:第一个字符串
        mysql1:第二个字符串
    Returns:
        返回两个字符串的相似程度（0~1）
    """
    if isinstance(web1, str):
        ret = difflib.SequenceMatcher(None, web1, mysql1).quick_ratio()
        if ret > 0.7:
            return True
        else:
            print(web1, '\n', mysql1)
            INFO(f'----web数据：{web1}\nmysql数据：{mysql1}')
            return False
    else:
        try:
            if len(web1) == 0 or len(mysql1) == 0:
                return False
            for i in range(len(web1)):
                if web1[i] in ['—', '— ']:
                    continue
                ret = difflib.SequenceMatcher(None, web1[i], mysql1[i]).quick_ratio()
                if ret < 0.7:
                    print(web1, '\n', mysql1)
                    INFO(f'----web数据：{web1}\nmysql数据：{mysql1}')
                    return False
            return True
        except:
            print(web1, '\n', mysql1)
            INFO(f'----web数据：{web1}\nmysql数据：{mysql1}')
            return False


if __name__ == "__main__":
    run_code = 0
