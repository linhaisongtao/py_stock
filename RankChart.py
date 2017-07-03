import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import math


class RankChart(object):
    def __init__(self, title, rank_list, year=5):
        self.rank_list = rank_list
        self.year = year
        self.title = title
        pass

    def show(self):
        print 'start draw RankChart'

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15, wspace=0.18, hspace=0.18)
        xes5 = []
        xes10 = []
        x_mids = []
        x_labels = []
        pb_5_positions = []
        pb_10_positions = []
        bar_width = 0.4
        opacity = 0.4
        for i, r in enumerate(self.rank_list):
            xes5.append(i)
            xes10.append(i + bar_width)
            x_mids.append(i + bar_width / 2)
            x_labels.append(r.name)
            pb_5_positions.append(r.rankInfo5.pb_position)
            pb_10_positions.append(r.rankInfo10.pb_position)
            pass
        plt.bar(xes5, pb_5_positions, bar_width, alpha=opacity, color='r', label='pb_5_position')
        plt.bar(xes10, pb_10_positions, bar_width, alpha=opacity, color='g', label='pb_10_position')
        plt.xticks(x_mids, x_labels, rotation=-45, fontsize=10)
        plt.axhline(0.2, color='c', linestyle=':')
        plt.legend()
        plt.title(self.title)
        plt.show()
        pass

    pass
