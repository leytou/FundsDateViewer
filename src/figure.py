#!/usr/bin/python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdate
import pandas as pd
import datetime
import math
import fl

import platform


_c_line = '#cb3a56'
_c_fl = 'r'
_c_days = 'r'

_c_bar = '#cb3a56'


def _num2data_str(num):
    return str(mdate.num2date(num)).split(' ', 1)[0].replace('-', '/')


def _date_str_formatting(date_str):
    date_num = mdate.datestr2num(date_str)
    return _num2data_str(date_num)


def draw(hold_data, fund_list):
    if platform.system() == 'Darwin':
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
    elif platform.system() == 'Windows':
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    if len(hold_data) <= 4:
        col_count = 2
    else:
        col_count = 3

    c = math.ceil(len(hold_data)/col_count)
    figure = plt.figure(c, figsize=(16, 10), dpi=80)
    figure.suptitle('基金份额持有期分布图', fontsize=18)

    index = 0
    for code, data in hold_data.items():
        title = '%s %s' % (fund_list[code], code)
        print('title:', title)

        date_list = list(data.keys())
        data_list = list(data.values())
        print(date_list, data_list)

        index += 1
        axes = plt.subplot(c, col_count, index)
        axes.title.set_text(title)

        months = mdate.MonthLocator()
        dateFmt = mdate.DateFormatter("%m/%d")

        axes.xaxis.set_major_formatter(dateFmt)
        axes.xaxis.set_minor_locator(months)
        #axes.tick_params(axis="both", direction="out", labelsize=10)

        first_day = date_list[0]
        t_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = t_tomorrow.strftime("%y/%m/%d")  # date_list[-1]

        date1 = datetime.datetime.strptime(first_day, '%y/%m/%d').date()
        date2 = datetime.datetime.strptime(tomorrow, '%y/%m/%d').date()
        delta = datetime.timedelta(days=1)
        dates = mdate.drange(date1, date2, delta)

        fene = []
        for i in dates:
            ds = _num2data_str(i)[2:]
            if ds in data:
                fene.append(data[ds])
            else:
                fene.append(0)

        axes.bar(dates, fene, width=1)
        for a, b in zip(dates, fene):
            t = round(b, 2)
            if t != 0:
                date_str = _num2data_str(a)[5:]
                text = '%d\n%s' % (t, date_str)
                plt.text(a, b,  text, ha='center',
                         va='bottom', fontsize=12)

        axes.xaxis_date()
        plt.xticks(rotation=45)
        plt.tight_layout(pad=3.0)

        axes.set_ylim(axes.get_ylim()[0], axes.get_ylim()[1]*1.35)

        today_num = dates[-1]
        fl_table = fl.get_fl_table(code)
        print('fl_table', code, fl_table)
        #print('dates', dates)
        print('today:', _num2data_str(today_num)[5:])
        note_list = []
        t = today_num
        for d, f in fl_table:
            xline = today_num - d + 1
            if xline in dates:
                axes.axvline(x=xline, color=_c_line,
                             linewidth=1, linestyle='--')
                note_text = '%d天\n%s' % (d, _num2data_str(xline)[5:])
                axes.annotate(note_text, xy=(xline, axes.get_ylim()[1]*0.05),
                              color=_c_days, size=12)
                note_list.append(((xline + t)/2, f))
                t = xline
            else:
                if t != 0:
                    note_list.append(((dates[0] + t)/2, f))
                    t = 0
                else:
                    break

        print('note_list:', note_list)
        for d, f in note_list:
            axes.annotate(f, xy=(d, axes.get_ylim()[1]*0.5),
                          color=_c_fl, ha='center', size=20)

        axes.annotate(str(fl_table), xy=(dates[0], axes.get_ylim()[1]*0.9),
                      color=_c_fl, size=10)
        print('')

    plt.subplots_adjust(left=None, bottom=None, right=None, top=0.9,
                        wspace=0.15, hspace=0.35)
    # figure.autofmt_xdate(rotation=45)
    # figure.xticks(rotation=45)


def show():
    # left  = 0.02  # 子图(subplot)距画板(figure)左边的距离
    # right = 0.9    # 右边
    # bottom = 0.1   # 底部
    # top = 0.9      # 顶部
    # wspace = 0.2   # 子图水平间距
    # hspace = 0.2   # 子图垂直间距
    plt.show()


if __name__ == "__main__":
    pass
