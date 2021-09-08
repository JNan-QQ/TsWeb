# -*- coding:utf-8 -*-
# @FileName  :ReadExcel.py
# @Time      :2021/7/22 16:32
# @Author    :姜楠
# @Tool      :PyCharm

import xlrd
from config.config import CasesConfig


def read_excel_homework():
    book = xlrd.open_workbook(CasesConfig.cases_path)
    # 获取名为cases的表单对象
    sheet = book.sheet_by_name('cases_homework')
    # 行数
    nums = sheet.nrows
    cases_dict = {}
    for i in range(1, nums):
        mode = sheet.cell_value(rowx=i, colx=1)

        homework_name = sheet.cell_value(rowx=i, colx=2)

        grade = sheet.cell_value(rowx=i, colx=3)

        unit = sheet.cell_value(rowx=i, colx=4)
        if '|' in str(unit):
            unit = [int(ii) for ii in unit.split('|')]
        else:
            unit = [int(unit)]

        book_type = int(sheet.cell_value(rowx=i, colx=5))
        dict1 = {}
        paper = sheet.cell_value(rowx=i, colx=6)
        if "|" in str(paper) or "," in str(paper):
            paper = paper.split("|")
            for ii in range(1, len(paper) + 1):
                dict1[ii] = paper[ii - 1].split(",")
        else:
            dict1 = {1: [int(paper)]}

        send_mode = int(sheet.cell_value(rowx=i, colx=7))

        vip = sheet.cell_value(rowx=i, colx=8)

        need_do = sheet.cell_value(rowx=i, colx=9)

        cases_dict[sheet.cell_value(rowx=i, colx=0)] = [int(mode), homework_name, grade, unit, book_type, dict1,
                                                        send_mode, vip, need_do]

    return cases_dict


def read_excel_paper():
    book = xlrd.open_workbook(CasesConfig.cases_path)
    # 获取名为cases的表单对象
    sheet = book.sheet_by_name('cases_paper')
    # 行数
    nums = sheet.nrows
    cases_dict = {}
    for i in range(1, nums):
        mode = sheet.cell_value(rowx=i, colx=1)

        grade = sheet.cell_value(rowx=i, colx=2)

        paper_name = sheet.cell_value(rowx=i, colx=3)

        paper_unit = sheet.cell_value(rowx=i, colx=4)

        cases_dict[sheet.cell_value(rowx=i, colx=0)] = [int(mode), grade, paper_name,paper_unit]

    return cases_dict


if __name__ == "__main__":
    print(read_excel_homework())
