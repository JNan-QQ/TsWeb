# -*- coding:utf-8 -*-
# @FileName  :doQuestions.py
# @Time      :2021/8/12 10:47
# @Author    :姜楠
# @Tool      :PyCharm
import re
from hytest import *
from selenium import webdriver
# 导入Select类
from selenium.webdriver.support.ui import Select
from lib.CheckImgAndVideo import getEqualRate
from lib.Mysql_Read import mysql_read_alpha
from lib.CheckImgAndVideo import imageCheck, videoCheck
from config.config import QType

try:
    import xml.etree.cElementTree as eT
except ImportError:
    import xml.etree.ElementTree as eT


# 短文
def xml_text(p):
    cc = ''
    if p.text:
        cc = p.text
    for i in p.iter():
        if i.tail:
            cc += i.tail
    cc = cc.rstrip()

    return cc


# 选项
def xml_text1(p):
    cc = ''
    for i in p.itertext():
        if i and not i.isspace():
            cc += i
    cc = cc.rstrip()
    return cc


def replace_xml(p):
    x = ['B', 'U', 'I', 'br/']
    for i in x:
        p = p.replace(f'<{i}>', '').replace(f'</{i}>', '')
    return p


def mysql_content_format(xml_str):
    xml_str = f'<tml>{xml_str}</tml>'
    xml_str = replace_xml(xml_str)
    root = eT.fromstring(xml_str)
    # print(root)

    # 提取图片 - web: tag = img
    image = [i.text for i in root.findall('.//img')]

    # 提取短文 - web: class = idx
    idx_text = [xml_text(i) for i in root.findall('.//p/Idx/..') if xml_text(i)]

    # 题目短文2
    idx_text2 = [xml_text(i) for i in root.findall('./T/p') if not i.findall('.//Idx') and xml_text(i)]

    idx_text2 += [i.text for i in root.findall('./Led/p') if not i.findall('.//Idx') and i.text]

    # 提取标题类型 - web: class=Mid
    mid_text = [i.text for i in root.findall('./T/p/Mid') if i.text]

    # 提取小题 - web: class = question_content
    qs = root.findall('./Qs')

    question = []
    for q_q in qs:
        # 格式化答案
        answer = [i for i in q_q.attrib['As'].replace('#', '').split('*') if i]

        # 提取小题题目 - web: class = question_p
        ques = [xml_text(i) for i in q_q.findall('./T/p') if not i.findall('./Idx')]
        # print(ques)
        # 提取小题选项 - web: class = label
        opt = [xml_text1(i) for i in q_q.findall('./Opt/T')]
        opt = [i for i in opt if '.jpg' not in i]
        ques += opt
        ques = [i for i in ques if i and i != ' ']

        question.append([ques, answer])

    mp3 = [i.text for i in root.findall('La')]

    # class = china_q
    sh_q = [i.text for i in root.findall('Sh/p')]

    sa = root.findall('Sa')
    if sa:
        sa_q = re.findall(r'\((.*?\.mp3)\)\(\d+\)\(\d+\)', sa[0].text, re.S)
        sa_q = [i for i in sa_q if i not in ['1.mp3', '0.mp3']]
    else:
        sa_q = []

    mysql_dict = {
        '图片': image,
        '题目短文标题': mid_text,
        '题目短文': idx_text,
        '题目短文2': idx_text2,
        '题目问题、选项、答案': question,
        '题目音频': mp3,
        '情景问答': [sh_q, sa_q]
    }
    # print(mysql_dict)
    return mysql_dict


def web_check(elem: webdriver.Chrome, driver: webdriver.Chrome, mysql_connect, ques_type):
    if mysql_connect['图片']:
        # print('开始比对图片')
        images_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
        CHECK_POINT('----对比题目中的图片名字相同', imageCheck.check_name(images_web, mysql_connect['图片']))

        # img_request = [imageCheck.run(i) for i in images_web]
        # CHECK_POINT('----各图片链接访问是否成功,图片是否完整', False not in img_request)

        # print('--比对图片完成！！！')

    if mysql_connect['题目短文标题']:
        # print('开始比对短文标题')
        mid_web = [i.text for i in elem.find_elements_by_css_selector('.Mid') if i.text]
        CHECK_POINT('----对比题目标题是否相同', getEqualRate(mid_web, mysql_connect['题目短文标题']))

        # print('--比对短文标题完成！！！')

    if mysql_connect['题目短文']:
        # print('开始比对短文')
        idx_web = [i.text for i in elem.find_elements_by_css_selector('p.idx') if i.text]
        if idx_web:
            CHECK_POINT('----对比题目短文是否相同', getEqualRate(idx_web, mysql_connect['题目短文']))

        # print('--比对短文完成！！！')

    if mysql_connect['题目短文2']:
        # print('开始比对短文2')
        idx_web2 = [re.sub(r'\(\d+\)', '()', i.text) for i in
                    elem.find_elements_by_css_selector('.text_content p:not(.idx , .Mid), .test_empty_content>p') if
                    i.text]
        idx_web2 = [re.sub(r'__\d+__', '____', i) for i in idx_web2 if not i.isspace()]
        CHECK_POINT('----对比题目短文2是否相同', getEqualRate(idx_web2, mysql_connect['题目短文2']))

        # print('--比对短文2完成！！！')

    if mysql_connect['题目音频']:
        # print('开始比对短文音频')
        mp3_web = []
        mp3_url = []
        for web_ss in elem.find_elements_by_css_selector('.p_Laudio'):
            mp3_web.append(
                f'({web_ss.get_attribute("data-mp3")})({web_ss.get_attribute("data-starttime")})({web_ss.get_attribute("data-endtime")})')
            mp3_url.append(web_ss.get_attribute("data-mp3"))

        CHECK_POINT('----对比音频', getEqualRate(mp3_web, mysql_connect['题目音频']))

        mp3_request_result = videoCheck(mp3_url)
        CHECK_POINT('----访问音频链接', True in mp3_request_result)

        play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
        driver.execute_script("$(arguments[0]).click()", play_btn)

        # print('--比对音频完成！！！')

    if mysql_connect['情景问答']:

        if mysql_connect['情景问答'] != [[], []]:
            # print('开始比对音频2')

            web_sh = [i.get_attribute('innerText') for i in
                      elem.find_elements_by_css_selector('.china_question')]
            web_sh = [re.sub(r'^[0-9]\.', '', i) for i in web_sh]

            web_sa = [i.get_attribute('data-mp3') for i in
                      elem.find_elements_by_css_selector('.speak_sentence')]
            INFO(mysql_connect['情景问答'])
            INFO([web_sh, web_sa])
            if mysql_connect['情景问答'] != [web_sh, web_sa]:
                if web_sh != mysql_connect['情景问答'][0]:
                    print(web_sh, mysql_connect['情景问答'][0])
                    CHECK_POINT('----比对问答题目音频 - 题目', False)
                if web_sa == [] or mysql_connect['情景问答'][1] == []:
                    CHECK_POINT('----未找到mysql/web音频数据', False)
                else:
                    for web_sa_i in web_sa:
                        if web_sa_i not in mysql_connect['情景问答'][1]:
                            CHECK_POINT('----比对问答题目音频 - 音频', False)
                            break
            else:
                CHECK_POINT('----比对问答题目音频', True)

            play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
            driver.execute_script("$(arguments[0]).click()", play_btn)

        # print('--比对音频2问答完成！！！')

    if mysql_connect['题目问题、选项、答案']:
        # print('开始完成小题 题目问题、选项、答案')
        ques_mysql_list = mysql_connect['题目问题、选项、答案']
        ques_web_list = elem.find_elements_by_css_selector('.question_content')
        CHECK_POINT(f'----小题数量对比 web:{len(ques_web_list)},mysql:{len(ques_mysql_list)}',
                    len(ques_web_list) == len(ques_mysql_list))

        for ii in range(len(ques_web_list)):
            INFO(f'------开始对比该大题的第 {ii + 1} 小问')

            # 题目选项
            if ques_mysql_list[ii][0]:
                # print('----进入小题题目对比')
                ques = [i.text for i in ques_web_list[ii].find_elements_by_css_selector('.question_p') if i.text]
                ques += [re.sub(r'[A-D]\. |[A-D]\.', '', i.text) for i in
                         ques_web_list[ii].find_elements_by_css_selector('label') if i.text]
                ques = [i.split('\n')[0] for i in ques if i]
                INFO(ques)
                INFO(ques_mysql_list[ii][0])
                CHECK_POINT('------对比该小问问题内容', getEqualRate(ques, ques_mysql_list[ii][0]))

            # 答案
            if ques_mysql_list[ii][1]:
                # print('----进入小题答案完成')
                # 单项选择类型
                if ques_type in QType.opt:
                    opt_btn = ques_web_list[ii].find_element_by_css_selector(
                        f'label:nth-of-type({ques_mysql_list[ii][1][0]}) input')
                    driver.execute_script("$(arguments[0]).click()", opt_btn)

                # 填空
                elif ques_type in QType.blank:
                    sends_input = ques_web_list[ii].find_elements_by_css_selector('input')
                    for iii in range(len(ques_mysql_list[ii][1])):
                        sends_input[iii].send_keys(ques_mysql_list[ii][1][iii])

                elif ques_type in ['1700', '3000']:
                    select = Select(ques_web_list[ii].find_element_by_css_selector("select"))
                    select.select_by_index(ques_mysql_list[ii][1][0])

            INFO('------该小问作答完成')
        # print('--小题作答完成！！！')

    elif ques_type in ['2700']:
        elem.find_element_by_css_selector('textarea').send_keys('[cs] [jiangnan] [zdh]')

    return True


def main_handler(ques_id, ques_type, driver, elem):
    content = mysql_read_alpha(f"""select question_content from ts_test where id={ques_id}""")[0]
    INFO(f'----试题id是{ques_id}')

    # 格式化数据库代码
    driver.implicitly_wait(1)
    mysql_connect = mysql_content_format(content)
    web_check(elem, driver, mysql_connect, ques_type)
    # print('\n')
    driver.implicitly_wait(5)

    # print(content, '\n')
    # print(mysql_connect)


if __name__ == "__main__":
    q_isd = 1
    c = mysql_read_alpha(f"""select question_content from ts_test where id={q_isd}""")[0]
    a = mysql_content_format(c)
    print(c, '\n')
    print(a)
    pass
