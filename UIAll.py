#!/usr/bin/python
# coding:utf-8
import matplotlib.pyplot as plt
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import ChartBenefit
import ChartPb
import ChartRoe
import StockInfo


class UI(object):
    def __init__(self, code, name):
        self.code = code;
        self.name = name;
        pass

    def process_data(self):
        self.pb_list = StockInfo.get_pb_stocks(self.code, max_count=2000)
        self.roes = StockInfo.get_roes(self.code, max_count=10)
        pass

    def show(self):
        self.process_data()

        roe_data = ChartRoe.RoeChart().show(plt.subplot(311), self.roes)
        plt.xticks(roe_data['x'], roe_data['dates'])
        plt.title(self.get_base_title())

        pb_data = ChartPb.PbChart().show(plt.subplot(312), self.pb_list)
        plt.xticks(pb_data['x'], pb_data['dates'])

        ChartBenefit.BenefitChart().show(plt.subplot(313), roe_data, pb_data)

        plt.show()
        pass

    def get_base_title(self):
        return self.name + "[" + self.code + "]"
        pass

    pass
