import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import SChart as sc
import datetime, time
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_selected_codes():
    lines = open('selected', 'r').readlines()

    code_list = []
    for l in lines:
        l = l.replace('\n', '').split('  ')
        s = {}
        s['code'] = l[0]
        s['name'] = l[1]
        code_list.append(s)
        pass
    return code_list
    pass
