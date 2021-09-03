# -*- coding:utf-8 -*-
# @FileName  :file2base64.py
# @Time      :2021/9/3 11:17
# @Author    :姜楠
# @Tool      :PyCharm
import os

import requests


class image:
    def check_image(self, image_path=None, image_steam=None):
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

    def download_image(self, image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            return False

    def run(self, img_url):
        ret = self.download_image(image_url=img_url)
        if ret:
            return self.check_image(image_steam=ret)
        else:
            return ret


imaGE = image()


def check_mp3():
    pass


def check_mp4():
    pass


if __name__ == "__main__":
    ret = imaGE.run('https://static.waiyutong.org/book/images/110005461_1.jpg')
    print(ret)
