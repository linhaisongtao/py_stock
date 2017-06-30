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
        pures = []
        count = len(list) / 5
        maxY = 0
        for index, l in enumerate(list):
            x.append(index)
            if index % count == 0:
                x_label.append(l.date)
                pass
            else:
                x_label.append("")
                pass
            p.append(l.pb)
            roe15_p.append(l.pb_wanted)
            pures.append(1)
            pass

        plt.plot(x, p)
        plt.plot(x, roe15_p)
        plt.plot(x, pures)
        plt.legend(['p', 'roe15_price', 'pure'])
        plt.axis([0, len(x) + 1, 0, max([max(p), max(roe15_p), max(pures)]) + 1])
        plt.xticks(x, x_label)
        plt.title(list[0].code)
        plt.show()
        pass

    pass
