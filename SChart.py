import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import math


class SChart(object):
    def __init__(self, titles, stock_lists=[]):
        self.stock_lists = stock_lists
        self.titles = titles
        pass

    def show(self):
        print 'start draw chart'
        total = len(self.titles)
        row = (int)(math.ceil(math.sqrt(total)))
        column = (int)(math.ceil(1.0 * total / row))
        for i, title in enumerate(self.titles):
            datas = self.__show(plt.subplot(row * 100 + column * 10 + i + 1), self.stock_lists[i])
            plt.title(self.titles[i])
            plt.xticks(datas[0],datas[1])
            pass
        print 'show chart'
        plt.show()
        pass

    def __show(self, subplot, list):
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

        subplot.plot(x, p)
        subplot.plot(x, roe15_p)
        subplot.plot(x, pures)
        subplot.legend(['pb', 'roe15_price', 'pure'])
        subplot.axis([0, len(x) + 1, 0, max([max(p), max(roe15_p), max(pures)]) + 1])
        # subplot.xticks(x, x_label)
        # subplot.title(self.titles)
        return (x, x_label)
        pass

    pass
