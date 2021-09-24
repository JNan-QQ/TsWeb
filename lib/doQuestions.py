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
from lib.CheckImgAndVideo import imageCheck


class DoTest:
    options = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    driver = None

    def quesHandler(self, ques_id, ques_type, elem, driver):
        self.driver: webdriver.Edge = driver
        row = mysql_read_alpha(f"""select answer_num,question_content from ts_test where id={ques_id}""")
        # print(row)
        INFO(f'该作业试题id是{ques_id}')

        if ques_type == '1100':
            return self.type_1100(row, elem)
        elif ques_type == '1200':
            return self.type_1200(row, elem)
        elif ques_type == '1300':
            return self.type_1300(row, elem)
        elif ques_type == '1400':
            return self.type_1400(row, elem)
        elif ques_type == '1500':
            return self.type_1500(row, elem)
        elif ques_type == '1600':
            return self.type_1600(row, elem)
        elif ques_type == '1700':
            return self.type_1700(row, elem)
        elif ques_type == '2100':
            return self.type_2100(row, elem)
        elif ques_type == '2200':
            return self.type_2200(row, elem)
        elif ques_type == '2300':
            return self.type_2300(row, elem)
        elif ques_type == '2400':
            return self.type_2400(row, elem)
        elif ques_type == '2500':
            return self.type_2500(row, elem)
        elif ques_type == '2600':
            return self.type_2600(row, elem)
        elif ques_type == '2700':
            return self.type_2700(row, elem)
        elif ques_type == '2800':
            return self.type_2800(row, elem)
        elif ques_type == '2900':
            return self.type_2900(row, elem)
        elif ques_type == '3000':
            return self.type_3000(row, elem)
        elif ques_type == '7300':
            return self.type_7300(row, elem)

        # 高中题型
        elif ques_type == '13600':
            return self.type_1200(row, elem)
        elif ques_type == '13700':
            return self.type_1600(row, elem)
        elif ques_type in ['14100', '14600', '14200']:
            return self.type_1400(row, elem)
        elif ques_type in ['14300']:
            return self.type_14300(row, elem)
        elif ques_type in ['14400']:
            return self.type_14400(row, elem)
        elif ques_type == '13800':
            return self.type_13800(row, elem)
        elif ques_type == '14500':
            return self.type_14500(row, elem)
        else:
            # print(row)
            INFO(f'无题目类型：{ques_type},id:{ques_id}')
            # CHECK_POINT('', False)
            return row

    # 听录音选图片
    def type_1100(self, content, elem):
        ques = content[1]
        # 题目(不一定有)
        ques_mysql = re.findall(r'<Qs(.*?)</Qs>', ques, re.S)[0]
        questions_mysql = [i for i in re.findall(r'<p>(.*?)</p>', ques_mysql, re.S) if i]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p') if i.text]
        check_question = getEqualRate(ques_web, questions_mysql)
        CHECK_POINT('问题比对', check_question)

        # 选项图片（一定有）
        image_mysql = re.findall(r'<img>(.*?)</img>', ques_mysql, re.S)
        image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]

        print([imageCheck.run(i) for i in image_web])

        for i in range(len(image_mysql)):
            if image_mysql[i] in image_web[i]:
                flg = True
            else:
                flg = False
            CHECK_POINT(f'{self.options[i]}选项图片比对', flg)

        # 题目音频
        mp3_mysql = re.findall(r'<La>\((.*?)\).*?</La>', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')]
        check_mp3 = getEqualRate(mp3_web, mp3_mysql)
        CHECK_POINT('比对音频', check_mp3)

        # 题目答案
        right_answer = re.findall(r'As="(.*?)"', ques, re.S)[0]
        opt_btn = elem.find_element_by_css_selector(f'label:nth-of-type({right_answer}) input')
        self.driver.execute_script("$(arguments[0]).click()", opt_btn)

        play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", play_btn)

    # 录音单选
    def type_1200(self, content, elem):
        ques = content[1]

        # 题目、选项
        ques_mysql = [i for i in re.findall(r'<p>(.*?)</p>', ques, re.S) if ((i != ' ') and i)]
        ques_web = []
        for topic in elem.find_elements_by_css_selector('.question_content'):
            ques_web += [i.text for i in topic.find_elements_by_css_selector('.question_p') if i.text]
            ques_web += [re.sub(r'[A-Z]\. ', '', i.text) for i in topic.find_elements_by_css_selector('label')]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('对比题目、选项', ret)

        # 音频
        mp3_mysql = re.findall(r'<La>.*?\((1[23][06]0.*?\.mp3)\).*?</La>', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')]
        for mp3 in mp3_web:
            if mp3 not in mp3_mysql:
                CHECK_POINT('比对音频', False)
                break
        else:
            CHECK_POINT('比对音频', True)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_content')
        for i in range(len(sends_input)):
            opt_btn = sends_input[i].find_element_by_css_selector(f'label:nth-of-type({right_answer[i]}) input')
            self.driver.execute_script("$(arguments[0]).click()", opt_btn)

        play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", play_btn)

    # 看图听一篇短文，请根据内容从A、B、C三个选项中选择正确的选项，完成信息记录表。
    def type_1300(self, content, elem):
        ques = content[1]
        # 题目图片
        image_mysql = re.findall('<img>(.*?)</img>', ques, re.S)[0]
        image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')][0]
        CHECK_POINT('比对图片', image_mysql in image_web)

        # 选项
        option_mysql = re.findall('<Opt><T><p>(.*?)</p></T></Opt>', ques, re.S)
        option_web = [re.sub(r'[A-Z]\. ', '', i.text) for i in elem.find_elements_by_css_selector('label')]
        ret = getEqualRate(option_web, option_mysql)
        CHECK_POINT('题目选项比对', ret)

        # 题目音频
        mp3_mysql = re.findall(r'<La>\((.*?)\).*?</La>', ques, re.S)[0]
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')][0]
        CHECK_POINT('比对音频', mp3_web == mp3_mysql)

        # 答案
        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_content')
        for i in range(len(sends_input)):
            opt_btn = sends_input[i].find_element_by_css_selector(f'label:nth-of-type({right_answer[i]}) input')
            self.driver.execute_script("$(arguments[0]).click()", opt_btn)

    # 朗读短文
    def type_1400(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i.replace('<Idx></Idx>', '').replace('<Mid>', '').replace('</Mid>', '') for i
                      in re.findall(r'<p>(.*?)</p>', ques, re.S) if i]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_content p') if
                    ((i.text != ' ') and i.text)]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('比对题目原文', ret)

        # 音频
        mp3_mysql = re.findall(r'\((14[0126].*?\.mp3)\)', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.question_content p span')]
        flg = True
        for i in mp3_web:
            if i not in mp3_mysql:
                flg = False
                break
        CHECK_POINT('音频比对', flg)

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)

    # 情景问答
    def type_1500(self, content, elem):
        ques = content[1]

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)

        # 题目
        sh_mysql = re.findall(r'<Sh>.*?</Sh>', ques, re.S)[0]
        ques_mysql = [i for i in re.findall(r'<p>(.*?)</p>', sh_mysql, re.S) if i]
        if ques_mysql:
            ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_content') if
                        i.text]
            ques_web = [re.sub(r'[0-9]\.  ', '', i) for i in ques_web[0].split('\n')]
            # print(ques_web)
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('图片比对', image_mysql[0] in image_web[0])

        # 音频
        mp3_mysql = re.findall(r'\((15.*?\.mp3)\)', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.question_li div')]
        flg = True
        for i in mp3_web:
            if i not in mp3_mysql:
                flg = False
                print(mp3_mysql, mp3_web)
                break
        CHECK_POINT('对比音频', flg)

    # 话题简述
    def type_1600(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i.replace('\r\n', '') for i in re.findall(r'<p>(.*?)</p>', ques, re.S) if
                      (('<img>' not in i) and ('<Blk>' not in i))]
        if ques_mysql:
            ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_content p') if
                        i.text]

            # //////////////////////////////////
            # if elem.find_element_by_css_selector('span>p').text.startswith('II．'):
            #     ques_web.insert(0, elem.find_element_by_css_selector('span>p').text)
            # /////////////////////////////////
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('图片比对', image_mysql[0] in image_web[0])

        # 音频
        mp3_mysql = re.findall(r'\((1[6,37].*?\.mp3)\)', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in
                   elem.find_elements_by_css_selector('.question_division_line span')]
        flg = True
        for i in mp3_web:
            if i not in mp3_mysql:
                flg = False
                print(mp3_mysql, mp3_web)
                break
        CHECK_POINT('对比音频', flg)

        answer = [i.replace('#', '') for i in re.findall(r'As="(.*?)"', ques, re.S) if i]
        if answer:
            INFO('写入答案')
            sends_input = elem.find_elements_by_css_selector('input')
            for i in range(len(answer)):
                sends_input[i].send_keys(answer[i])

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)

    # 选相天空
    def type_1700(self, content, elem):
        ques = content[1]
        # 前文
        first_text_web = [i.text for i in elem.find_elements_by_css_selector('.first_text .question_text p') if i.text]
        if first_text_web:
            first_text_mysql = re.findall(r'<p>(.*?)</p>', ques, re.S)
            ret = getEqualRate(first_text_web, first_text_mysql)
            CHECK_POINT('对比前文', ret)

        # 选项题目
        ques_mysql = [i for i in re.findall(r'<Qs>*?<p>(.*?)<Cob.*?></Cob></p></T></Qs>', ques, re.S) if i]
        if ques_mysql:
            ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p') if i.text]
            CHECK_POINT('对比单题目', ques_web == ques_mysql)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            flg = True
            for i in range(len(image_mysql)):
                if image_mysql[i] not in image_web[i]:
                    flg = False
                    break
            CHECK_POINT(f'选项图片比对', flg)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_p')
        for i in range(len(right_answer)):
            # 创建Select对象
            select = Select(sends_input[i].find_element_by_tag_name('select'))

            # 通过 Select 对象选中
            select.select_by_index(right_answer[i])

        # 音频
        mp3_mysql = re.findall(r'<La>\((17.*?\.mp3)\)', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')]
        flg = True
        for i in mp3_web:
            if i not in mp3_mysql:
                flg = False
                print(mp3_mysql, mp3_web)
                break
        CHECK_POINT('对比音频', flg)

        play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", play_btn)

    # 填空
    def type_2100(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i) for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S) if '<img>' not in i]
        ques_mysql = [i for i in ques_mysql if (i != '') and (not u'\u4e00' <= i[0] <= u'\u9fa5')]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p')]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('对比题目', ret)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        if len(right_answer) == 1:
            right_answer = right_answer[0].replace('#', '').split('*')
        else:
            a = right_answer
            right_answer = []
            for i in a:
                c = i.replace('#', '').split("*")
                right_answer.extend(c)
        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

    # 单项选择
    def type_2200(self, content, elem):
        # answer_num = content[0]
        ques = content[1]
        # 题目
        ques_mysql = [i.replace('<Blk></Blk>', '').replace('<I>', '').replace('</I>', '') for i
                      in re.findall(r'<p>(.*?)</p>', ques, re.S) if '<img>' not in i]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p') if i]
        ques_web += [re.sub(r'[A-Z]\. ', '', i.text) for i in elem.find_elements_by_css_selector('.space_space_option')
                     if i.text]
        ques_web = [i for i in ques_web if i != '']
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('对比题目、选项', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)[0]
        chil = elem.find_element_by_css_selector(f'label:nth-of-type({right_answer})')
        self.driver.execute_script("$(arguments[0]).click()", chil)

    # 短文填词
    def type_2300(self, content, elem):
        ques = content[1]
        right_answer = [i.replace('#', '') for i in re.findall(r'As="(.*?)"', ques, re.S)]
        ques_mysql = [i.replace('<Num></Num>', '').replace(' ', '') for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S)]
        # print(ques_mysql)
        ques_web = [re.sub(r'_(\d+)_', '', i.text).replace(' ', '') for i in
                    elem.find_elements_by_css_selector('.text_content p')]

        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

    # 改写
    def type_2400(self, content, elem):
        ques = content[1]

        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i).replace('<U>', '').replace('</U>', '') for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S)]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p')]
        ret = getEqualRate(ques_web, ques_mysql)
        # print(ques_web,ques_mysql)
        CHECK_POINT('对比题目', ret)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)[0].replace('#', '').split('*')
        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

    # 翻译句子
    def type_2500(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i) for i in re.findall(r'<p>(.*?)</p>', ques, re.S)]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.question_p')]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('对比题目', ret)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)[0].replace('#', '').split('*')
        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

    # 任务型阅读
    def type_2600(self, content, elem):
        ques = content[1]
        right_answer = [i.replace('#', '') for i in re.findall(r'As="(.*?)"', ques, re.S)]
        ques_mysql = [i.replace(' ', '') for i in re.findall(r'<p><Idx></Idx>(.*?)</p>', ques, re.S)]
        # print(ques_mysql)
        ques_web = [i.text.replace(' ', '') for i in elem.find_elements_by_css_selector('.text_content p.idx')]

        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

    # 作文
    def type_2700(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = re.findall(r'<p><Idx></Idx>(.*?)</p>', ques, re.S)
        ques_web = [i.text for i in elem.find_elements_by_css_selector('p.idx')]
        ret = getEqualRate(ques_web, ques_mysql)
        # print(ques_web, ques_mysql)
        CHECK_POINT('比对作文题目', ret)

        # 图片
        image_mysql = re.findall('<img>(.*?)</img>', ques, re.S)
        image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
        flg = True
        for i in range(len(image_mysql)):
            if image_mysql[i] not in image_web[i]:
                flg = False
                break
        CHECK_POINT('作文图片比对', flg)

        elem.find_element_by_css_selector('textarea').send_keys('[cs][jiangnan] this a cs zw')

    # 完型填空
    def type_2800(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i.replace('<Num></Num>', '') for i in re.findall(r'<p><Idx></Idx>(.*?)</p>', ques, re.S)]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('text_content p.idx')]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('比对题目短文内容', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        # 选项
        options_mysql = re.findall(r'<Opt><T>(.*?)</T></Opt>', ques, re.S)
        options_web = [re.sub(r'[A-Z]\. ', '', i.text) for i in
                       elem.find_elements_by_css_selector('label .space_space_option')]
        ret = getEqualRate(options_web, options_mysql)
        CHECK_POINT('检查选项内容', ret)

        # 答案
        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_content')
        for i in range(len(sends_input)):
            chil = sends_input[i].find_element_by_css_selector(f'label:nth-of-type({right_answer[i]})')
            self.driver.execute_script("$(arguments[0]).click()", chil)

    # 阅读理解
    def type_2900(self, content, elem):
        ques = content[1]
        # 阅读短文原文
        txt_mysql = [i.replace('<B>', '').replace('</B>', '') for i in
                     re.findall(r'<p><Idx></Idx>(.*?)</p>', ques, re.S)]
        if txt_mysql:
            txt_web = [i.text for i in elem.find_elements_by_css_selector('.text_content p.idx')]
            ret = getEqualRate(txt_web, txt_mysql)
            CHECK_POINT('比对题目短文内容', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i).replace('<B>', '').replace('</B>', '') for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S) if ('<Idx></Idx>' not in i) and ('<img>' not in i)]
        ques_web = []
        for topic in elem.find_elements_by_css_selector('.question_content'):
            ques_web += [i.text for i in topic.find_elements_by_css_selector('.question_p')]
            ques_web += [re.sub(r'[A-Z]\. ', '', i.text) for i in
                         topic.find_elements_by_css_selector('label .space_space_option')]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('比对题目、选项', ret)

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_content')
        for i in range(len(sends_input)):
            chil = sends_input[i].find_element_by_css_selector(f'label:nth-of-type({right_answer[i]})')
            self.driver.execute_script("$(arguments[0]).click()", chil)

    # 补全对话
    def type_3000(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [re.sub(r'<Cob t=".*?"></Cob>', '', i).replace('(<Num></Num>)', '') for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S) if '<img>' not in i]
        ques_mysql = [i for i in ques_mysql if i]
        ques_web = [re.sub(r'\(\d+\)', '', i.text) for i in
                    elem.find_elements_by_css_selector('.first_text .question_text p') if i.text]
        if ques_web and ques_mysql:
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        # 答案
        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        sends_input = elem.find_elements_by_css_selector('.question_p')
        flg = False
        if '#' in right_answer[0]:
            flg = True
            right_answer = [i.replace('#', '') for i in right_answer]
            right = []
            for ii in right_answer:
                c = ii.split('*')
                right.extend(c)
            right_answer = right

            sends = []
            for ii in sends_input:
                d = ii.find_elements_by_css_selector('input')
                sends.extend(d)
            sends_input = sends

        for i in range(len(right_answer)):
            if flg:
                sends_input[i].send_keys(right_answer[i])
            else:
                # 创建Select对象
                select = Select(sends_input[i].find_element_by_tag_name('select'))

                # 通过 Select 对象选中小雷老师
                select.select_by_index(right_answer[i])

    #
    def type_7300(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i).replace('<p>', '') for i in
                      re.findall(r'<p>(.*?)</p>', ques, re.S) if '<img>' not in i]
        ques_mysql = [i for i in ques_mysql if i]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.first_text .text_content p') if i.text]
        if ques_web and ques_mysql:
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        right_answer1 = re.findall(r'As="(.*?)"', ques, re.S)
        right_answer = []
        for i in right_answer1:
            i = i.replace("#", "")
            if '*' in i:
                c = i.split('*')
                right_answer.extend(c)
            else:
                right_answer.append(i)

        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answer[i])

        # 音频
        mp3_mysql = re.findall(r'<La>\((17.*?\.mp3)\)', ques, re.S)
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')]
        flg = True
        for i in mp3_web:
            if i not in mp3_mysql:
                flg = False
                print(mp3_mysql, mp3_web)
                break
        CHECK_POINT('对比音频', flg)

        play_btn = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", play_btn)

    # 高中视频问答
    def type_14400(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i for i in re.findall(r'<Sr>(.*?)</Sr>', ques, re.S) if i]
        if ques_mysql:
            ques_web = [i.get_attribute('innerText') for i in elem.find_elements_by_css_selector('.question_li span')]
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        # 音频
        mp4_mysql = [i.replace('ogg', 'mp4') for i in re.findall(r'<Sm>\((144.*?\.ogg)\).*?</Sm>', ques, re.S)]
        mp4_web = [i.get_attribute('id') for i in elem.find_elements_by_css_selector('video')]
        flg = True
        if mp4_web[0] not in mp4_mysql:
            flg = False
            print(mp4_mysql, mp4_web)
        CHECK_POINT('对比音频', flg)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)

    # 高中视频问答
    def type_14300(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i for i in re.findall(r'<Sr>(.*?)</Sr>', ques, re.S) if i]
        if ques_mysql:
            ques_web = [i.get_attribute('data-text') for i in
                        elem.find_elements_by_css_selector('.question_li span')]
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比题目', ret)

        # 音频
        # mp3_mysql = [i for i in re.findall(r'\((14300.*?\.mp3)\)', ques, re.S)]
        # mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.question_li span')]
        # flg = True
        # for mp3 in mp3_web:
        #     if mp3 not in mp3_mysql:
        #         flg = False
        #         break
        # CHECK_POINT('对比音频', flg)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)

    # 听录音看图填空
    def type_13800(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [re.sub(r'<Blk>.*?</Blk>', '', i) for i in
                      re.findall(r'<T><p>(.*?)</p></T>', ques, re.S) if ('<img>' not in i) and ('<p>' not in i)]
        ques_mysql = [i for i in ques_mysql if i]
        ques_web = [i.text for i in elem.find_elements_by_css_selector('.first_text .question_text p') if i.text]
        ret = getEqualRate(ques_web, ques_mysql)
        CHECK_POINT('对比题目', ret)

        # 图片
        image_mysql = re.findall(r'<img>(.*?)</img>', ques, re.S)
        if image_mysql:
            image_web = [i.get_attribute('src') for i in elem.find_elements_by_css_selector('img')]
            CHECK_POINT('对比图片', image_mysql[0] in image_web[0])

        right_answer = re.findall(r'As="(.*?)"', ques, re.S)
        right_answers = []
        for anwsers in right_answer:
            anwsers = anwsers.replace('#', '')
            c = anwsers.split('*')
            right_answers.extend(c)
        sends_input = elem.find_elements_by_css_selector('input')
        for i in range(len(sends_input)):
            sends_input[i].send_keys(right_answers[i])

    # 高中音频问答2
    def type_14500(self, content, elem):
        ques = content[1]
        # 题目
        ques_mysql = [i for i in re.findall(r'<Sr>(.*?)</Sr>', ques, re.S) if i]
        if ques_mysql:
            ques_web = [i.get_attribute('innerText') for i in elem.find_elements_by_css_selector('.question_li div')]
            ques_web = [re.sub(r'[12]\.', '', re.sub(r'answer:', '', i)) for i in ques_web]
            ret = getEqualRate(ques_web, ques_mysql)
            CHECK_POINT('对比问题', ret)

        # 音频
        mp3_mysql = [i for i in re.findall(r'<Sm>\((14500.*?\.mp3)\).*?</Sm>', ques, re.S)]
        mp3_web = [i.get_attribute('data-mp3') for i in elem.find_elements_by_css_selector('.p_Laudio')]
        flg = True
        for mp3 in mp3_web:
            if mp3 not in mp3_mysql:
                flg = False
                break
        CHECK_POINT('对比音频', flg)

        btn_play = elem.find_element_by_css_selector('.btn_play.br_small')
        self.driver.execute_script("$(arguments[0]).click()", btn_play)


student_do_homework = DoTest()

if __name__ == "__main__":
    print(DoTest().quesHandler('290000952', 1700, '', ''))
