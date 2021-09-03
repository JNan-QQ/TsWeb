# -*- coding:utf-8 -*-
# @FileName  :CheckImgAndVideo.py
# @Time      :2021/8/16 12:58
# @Author    :姜楠
# @Tool      :PyCharm
import difflib
from hytest import INFO

"""
检测图片完整性
JPG文件结尾标识：\xff\xd9
JPEG文件结尾标识：\xff\xd9
PNG文件结尾标识：\xaeB`\x82
"""


class CheckImage(object):

    def __init__(self, img):
        with open(img, "rb") as f:
            f.seek(-2, 2)
            self.img_text = f.read()
            f.close()

    def check_jpg_jpeg(self):
        """检测jpg图片完整性，完整返回True，不完整返回False"""
        buf = self.img_text
        return buf.endswith(b'\xff\xd9')

    def check_png(self):
        """检测png图片完整性，完整返回True，不完整返回False"""

        buf = self.img_text
        return buf.endswith(b'\xaeB`\x82')


def get_equal_rate(web1, mysql1):
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
            INFO(f'web数据：{web1}\nmysql数据：{mysql1}')
            return False
    else:
        try:
            for i in range(len(web1)):
                ret = difflib.SequenceMatcher(None, web1[i], mysql1[i]).quick_ratio()
                if ret < 0.7:
                    print(web1, '\n', mysql1)
                    INFO(f'web数据：{web1}\nmysql数据：{mysql1}')
                    return False
            return True
        except:
            INFO(f'web数据：{web1}\nmysql数据：{mysql1}')
            return False


if __name__ == "__main__":
    run_code = 0
