#!/usr/bin/python
# -*- coding: utf-8 -*-

import openpyxl


def _get_fene_list(col):
    temp = [(i.value) for i in col]
    for i, v in enumerate(temp):
        if v == None:
            temp[i] = 0
        else:
            temp[i] = int(temp[i])
    return temp


def _get_chiyou_fene(l):
    t = l[:]
    minus_sum = 0
    for i, v in enumerate(t):
        if v < 0:
            minus_sum += abs(v)
            t[i] = 0

    for i, v in enumerate(t):
        if minus_sum <= 0:
            break
        if v > 0:
            temp = max(0, v - minus_sum)
            minus_sum -= (v - temp)
            t[i] = temp

    return t


def _date_str_formatting(date_str):
    return str(date_str).split(' ', 1)[0].replace('-', '/')[2:]


# def get_hold_data():
#     d = {}
#     h = []
#     df = pd.read_csv('data.csv')
#     for i, col in df.iteritems():
#         # header 日期列
#         if i == 'name':
#             h = [_date_str_formatting(i)[2:] for i in col[1:]]
#         # 买入卖出列
#         else:
#             fene = _get_fene_list(col)
#             chiyou_fene = _get_chiyou_fene(fene)  # csv中数据处理，得到现有的持有的日期对应关系
#             code = str(int(col[0])).zfill(6)
#             t = dict(zip(h, chiyou_fene))
#             t = {k: v for k, v in t.items() if v != 0}
#             d.update({code: t})

#     return d


def get_hold_data_from_excel():
    book = openpyxl.load_workbook('data.xlsx')
    sheet = book[book.sheetnames[0]]
    table = tuple(sheet.columns)

    date_col_index = 0
    data_start_col_index = 1

    code_row_index = 1
    date_start_row_index = 3

    dates = [_date_str_formatting(i.value)
             for i in table[date_col_index][date_start_row_index:]]

    d = {}
    for i in range(data_start_col_index, len(table)):
        fene_list = _get_fene_list(table[i][date_start_row_index:])
        chiyou_fene = _get_chiyou_fene(fene_list)  # 数据处理，得到现有的持有的日期对应关系
        code = str(int(table[i][code_row_index].value)).zfill(6)
        t = dict(zip(dates, chiyou_fene))
        t = {k: v for k, v in t.items() if v != 0}
        d.update({code: t})

    return d


if __name__ == "__main__":
    # ret = get_hold_data()
    # print(ret)
    get_hold_data_from_excel()
