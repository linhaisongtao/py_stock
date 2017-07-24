import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import SChart as sc
import datetime, time
import json
import sys, csv

reload(sys)
sys.setdefaultencoding('utf-8')


def get_selected_codes():
    csv_reader = csv.reader(open('selected_sorted.csv', 'r'))
    code_list = []
    for row in csv_reader:
        m = {}
        m['code'] = row[1].replace('A', '')
        m['name'] = row[0]
        m['count'] = int(row[2])
        code_list.append(m)
        pass
    return code_list
    pass


def get_origin_selected_codes():
    lines = open('selected', 'r').readlines()

    code_list = []
    for l in lines:
        if l.startswith('#') or l.startswith(' ') or l == '\n':
            pass
        else:
            l = l.replace('\n', '').split('  ')
            s = {}
            s['code'] = l[0]
            s['name'] = l[1]
            s['count'] = 0
            code_list.append(s)
        pass
        pass
    return code_list
    pass

