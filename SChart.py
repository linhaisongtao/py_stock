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
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.18, hspace=0.18)

        for i, title in enumerate(self.titles):
            datas = self.__show(plt.subplot(row * 100 + column * 10 + i + 1), self.stock_lists[i])
            plt.title(self.titles[i] + "_" + self.stock_lists[i][len(self.stock_lists[i]) - 1].date)
            plt.xticks(datas[0], datas[1])
            pass
        print 'show chart'
        plt.show()
        pass

    def __show(self, subplot, list):
        x = []
        x_label = []
        p = []
        pb_list = []
        roe5_p = []
        roe1_p = []

        maxY = 0
        start = max(0, len(list) - 1250)
        print 'start index', start
        for index, l in enumerate(list):
            if index >= start:
                x.append(index - start)
                x_label.append(l.date)
                p.append(l.pb)
                pb_list.append(l.pb)
                roe5_p.append(l.pb5_wanted)
                roe1_p.append(l.pb1_wanted)
                pass
            pass

        count = len(x_label) / 5
        for index, label in enumerate(x_label):
            if index != 0 and (index + 1) % count != 0:
                x_label[index] = ''
                pass
            pass

        # find bottom 20% value
        pb_list = sorted(pb_list)
        pb_bottom_20 = pb_list[int(len(pb_list) * 0.2)]
        pb_bottom_10 = pb_list[int(len(pb_list) * 0.1)]
        pb_average = sum(pb_list) / len(pb_list)

        total = len(p)
        subplot.plot(x, p)
        subplot.text(total, p[total - 1], ' pb[%.2f]' % p[total - 1], fontsize=10, verticalalignment="center",
                     horizontalalignment="left")
        subplot.plot(x, roe5_p, color='m')
        subplot.text(total, roe5_p[total - 1], ' pb5[%.2f]' % roe5_p[total - 1], fontsize=10, verticalalignment="center",
                     horizontalalignment="left")
        subplot.plot(x, roe1_p, color='r')
        subplot.text(total, roe1_p[total - 1], ' pb1[%.2f]' % roe1_p[total - 1], fontsize=10, verticalalignment="center",
                     horizontalalignment="left")

        subplot.axhline(pb_bottom_20, color='g', linestyle='--')
        subplot.text(0, pb_bottom_20, '20[%.2f] ' % pb_bottom_20, fontsize=10, verticalalignment="bottom",
                     horizontalalignment="right")
        subplot.axhline(pb_bottom_10, color='darkgreen', linestyle='--')
        subplot.text(0, pb_bottom_10, '10[%.2f] ' % pb_bottom_10, fontsize=10, verticalalignment="top",
                     horizontalalignment="right")

        subplot.axhline(pb_average, color='c', linestyle=':')
        subplot.text(0, pb_average, 'aver[%.2f] ' % pb_average, fontsize=10, verticalalignment="bottom",
                     horizontalalignment="right")

        # subplot.legend(['pb', 'roe5_pb', 'roe1_pb'])
        subplot.axis([0, len(x) + 1, 0, max([max(p), max(roe5_p), max(roe1_p)]) * 1.03])
        # subplot.xticks(x, x_label)
        # subplot.title(self.titles)
        return (x, x_label)
        pass

    pass
