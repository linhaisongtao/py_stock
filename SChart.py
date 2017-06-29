import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si


class SChart(object):
    def __init__(self, stock_list=[]):
        self.stock_list = stock_list
        pass

    def show(self):
        list = self.stock_list
        x = []
        x_label = []
        p = []
        roe15_p = []
        count = len(list) / 5
        for index, l in enumerate(list):
            x.append(index)
            if index % count == 0:
                x_label.append(l.date)
                pass
            else:
                x_label.append("")
                pass
            p.append(l.price)
            roe15_p.append(l.roe15_price)
            pass

        plt.plot(x, p)
        plt.plot(x, roe15_p)
        plt.legend(['p', 'roe15_price'])
        plt.xticks(x, x_label)
        plt.title(list[0].code)
        plt.show()
        pass

    pass
