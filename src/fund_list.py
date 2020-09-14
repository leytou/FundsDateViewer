#!/usr/bin/python 
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
import requests
from utils import *


def get_fund_list():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    response =  get_resonse(url)
    tmp = re.findall(r"(\".*?\")" , response)
    fund_dict={}
    code=''
    name=''
    for i in range(0,len(tmp)):
        if i%5==0:
            code = eval(tmp[i])
        elif i%5==2:
            name = eval(tmp[i])
        elif i%5==4:
            fund_dict.update({code:name})

    return fund_dict
    



if __name__ == "__main__":
    l = get_fund_list()
    print(l['009549'])