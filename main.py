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

lines = open('selected', 'r').readlines()

code_list = []
for l in lines:
    code_list.append(l.replace('\n', ''))
    pass
print code_list


Window.Window(code_list).show()

# list = si.get_stocks('600048')
# sc.SChart(list).show()
