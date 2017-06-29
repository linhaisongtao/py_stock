import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import SChart as sc
import datetime, time
import json
import Window
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

lines = open('selected', 'r').readlines()

code_list = []
for l in lines:
    l = l.replace('\n', '').split('  ')
    print l
    s = {}
    s['code'] = l[0]
    s['name'] = l[1]
    code_list.append(s)
    pass
print code_list

Window.Window(code_list).show()

# list = si.get_stocks('600048')
# sc.SChart(list).show()
