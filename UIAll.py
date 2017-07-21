import matplotlib.pyplot as plt

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
        self.pb_list = StockInfo.get_pb_stocks(self.code)
        self.roes = StockInfo.get_roes(self.code)
        pass

    def show(self):
        self.process_data()

        roe_data = ChartRoe.RoeChart().show(plt.subplot(221), self.roes)
        plt.xticks(roe_data['x'], roe_data['dates'])

        pb_data = ChartPb.PbChart().show(plt.subplot(223), self.pb_list)
        plt.xticks(pb_data['x'], pb_data['dates'])

        ChartBenefit.BenefitChart().show(plt.subplot(222), roe_data, pb_data)

        plt.show()
        pass

    pass


UI('600016', 'xy').show()
