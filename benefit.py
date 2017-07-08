#!/usr/bin/python
# coding:utf-8
import csv
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')


def compute_benefit(year=0, roe=0, pb_buy=1, pb_future=1):
    pure = math.pow(1 + roe, year)
    price_future = pure * pb_future
    price_buy_future = pure * pb_buy
    pb_benefit = (pure - pb_buy) / pb_buy
    pb_future_benefit = (price_future - pb_buy) / pb_buy
    pb_buy_future_benefit = (price_buy_future - pb_buy) / pb_buy

    m = {}
    m['pure'] = pure
    m['price_future'] = price_future
    m['pb_benefit'] = pb_benefit
    m['pb_future_benefit'] = pb_future_benefit
    m['year'] = year
    m['roe'] = roe
    m['pb_buy'] = pb_buy
    m['pb_future'] = pb_future
    m['price_buy_future'] = price_buy_future
    m['pb_buy_future_benefit'] = pb_buy_future_benefit
    return m
    pass


import StockInfo
import Util


class BenefitChart(object):
    def __init__(self, names, codes):
        self.names = names
        self.codes = codes
        self.line_styles = [  # hidden names deprecated
            '-',
            '--',
            '-.',
            ':'
        ]
        pass

    def __cmp_pb(self, o1, o2):
        return (int)(10000 * (o1.pb - o2.pb))
        pass

    def show(self):
        legends = []
        max_year = 10
        for i, code in enumerate(self.codes):
            print code
            roes = StockInfo.get_roes(code)
            roe = roes[0].roe5 * 0.85
            pbs = Util.get_list_last(StockInfo.get_pb_stocks(code), 1250)
            pb_count = len(pbs)
            pb_now = pbs[pb_count - 1].pb
            pb20 = sorted(pbs, cmp=self.__cmp_pb)[int(pb_count * 0.2)].pb
            print roe, pb_now, pb20
            # pb20 = min([pb20, pb_now])
            benefit_future = self.__draw_benefit(i, max_year, roe / 100, pb_now, pb20, len(self.codes) == 1)
            legends.append(
                "%sroe=%.2f%%买=%.2f卖=%.2f收益=%.2f%%" % (self.names[i], roe, pb_now, pb20, benefit_future * 100))
            pass
        plt.axhline(0, color='c', linestyle='-')

        plt.axhline(1, color='y', linestyle=":")
        if max_year > 5:
            plt.axvline(5, color='y', linestyle=':')
            pass

        plt.axhline(3, color='r', linestyle=':')
        if max_year >= 10:
            plt.axvline(10, color='r', linestyle=':')
            pass

        plt.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.1, wspace=0.18, hspace=0.18)
        plt.legend(legends, 'upper left')
        plt.xlabel('year')
        plt.ylabel('benefit')
        plt.title('roe为最近5年平均数的85%,卖pb为近5年20%点位值')
        plt.show()
        pass

    def __draw_benefit(self, index, max_year, roe, pb_buy, pb_future, only_one=False):
        years = np.arange(0, max_year + 1)
        future_benefits = []
        buy_pb_benefits = []
        pure_benefits = []

        if not os.path.exists('benefit'):
            os.mkdir('benefit')
            pass
        csv_writer = csv.writer(open('benefit/' + self.codes[index] + ".csv", 'wb'))
        Util.print_row([Util.get_now_date_str()], csv_writer)
        Util.print_row(['净资产收益率', roe, '买入时PB', pb_buy, '未来PB', pb_future], csv_writer)
        Util.print_row(['年', '净资产收益率', '净资产', '1倍市净率买入成本', '未来1倍市净率收益率', '预期股价', '当前市净率买入成本', '预期市净率收益率'
                           , '买入时pb的未来股价', '买入时pb的未来收益率'], csv_writer)

        # m['pure'] = pure
        # m['price_future'] = price_future
        # m['pb_benefit'] = pb_benefit
        # m[''] = pb_future_benefit
        # m['year'] = year
        # m['roe'] = roe
        # m['pb_buy'] = pb_buy
        # m['pb_future'] = pb_future

        for y in years:
            b = compute_benefit(y, roe, pb_buy, pb_future)
            future_benefits.append(b['pb_future_benefit'])
            if only_one:
                buy_pb_benefits.append(b['pb_buy_future_benefit'])
                pure_benefits.append(b['pb_benefit'])
                pass

            row = [y, Util.format_float(roe), Util.format_float(b['pure']), 1,
                   Util.format_to_percentage(b['pb_benefit']),
                   Util.format_float(b['price_future']),
                   Util.format_float(b['pb_buy']),
                   Util.format_to_percentage(b['pb_future_benefit']),
                   Util.format_float(b['price_buy_future']),
                   Util.format_to_percentage(b['pb_buy_future_benefit'])
                   ]
            Util.print_row(row, csv_writer)
            pass
        line_style = self.line_styles[index % len(self.line_styles)]
        plt.plot(years, future_benefits, linestyle=line_style)
        if only_one:
            plt.plot(years, buy_pb_benefits, linestyle=line_style)
            plt.plot(years, pure_benefits, linestyle=line_style)
            plt.text(max_year, future_benefits[max_year], '20点位[%.2f%%] ' % (future_benefits[max_year] * 100),
                     fontsize=10, verticalalignment="center", horizontalalignment="left")
            plt.text(max_year, buy_pb_benefits[max_year], '买入pb[%.2f%%] ' % (buy_pb_benefits[max_year] * 100),
                     fontsize=10, verticalalignment="center", horizontalalignment="left")
            plt.text(max_year, pure_benefits[max_year], '1倍pb[%.2f%%] ' % (pure_benefits[max_year] * 100),
                     fontsize=10, verticalalignment="center", horizontalalignment="left")
            pass
        return future_benefits[len(future_benefits) - 1]
        pass

    def show_chart(self, year, roe, pb_buy, pb_future):
        if not os.path.exists('benefit'):
            os.mkdir('benefit')
            pass
        name = "year[%d]-roe[%.2f]-pb_buy[%.2f]-pb_future[%.2f]" % (year, roe, pb_buy, pb_future)
        csv_writer = csv.writer(open('benefit/' + name + ".csv", 'wb'))
        Util.print_row([Util.get_now_date_str()], csv_writer)
        Util.print_row(['净资产收益率', roe, '买入时PB', pb_buy, '未来PB', pb_future], csv_writer)
        Util.print_row(['年', '净资产收益率', '净资产', '1倍市净率买入成本', '未来1倍市净率收益率', '预期股价', '当前市净率买入成本', '预期市净率收益率'
                           , '买入时pb的未来股价', '买入时pb的未来收益率'], csv_writer)
        years = np.arange(0, year + 1)
        future_benefits = []
        buy_pb_benefits = []
        pure_benefits = []
        for y in years:
            b = compute_benefit(y, roe, pb_buy, pb_future)
            future_benefits.append(b['pb_future_benefit'])
            buy_pb_benefits.append(b['pb_buy_future_benefit'])
            pure_benefits.append(b['pb_benefit'])
            row = [y, Util.format_float(roe), Util.format_float(b['pure']), 1,
                   Util.format_to_percentage(b['pb_benefit']),
                   Util.format_float(b['price_future']),
                   Util.format_float(b['pb_buy']),
                   Util.format_to_percentage(b['pb_future_benefit']),
                   Util.format_float(b['price_buy_future']),
                   Util.format_to_percentage(b['pb_buy_future_benefit'])
                   ]
            Util.print_row(row, csv_writer)
            pass
        line_style = self.line_styles[0]
        plt.plot(years, future_benefits, linestyle=line_style)
        plt.plot(years, buy_pb_benefits, linestyle=line_style)
        plt.plot(years, pure_benefits, linestyle=line_style)
        plt.text(year, future_benefits[year], '20点位[%.2f%%] ' % (future_benefits[year] * 100),
                 fontsize=10, verticalalignment="center", horizontalalignment="left")
        plt.text(year, buy_pb_benefits[year], '买入pb[%.2f%%] ' % (buy_pb_benefits[year] * 100),
                 fontsize=10, verticalalignment="center", horizontalalignment="left")
        plt.text(year, pure_benefits[year], '1倍pb[%.2f%%] ' % (pure_benefits[year] * 100),
                 fontsize=10, verticalalignment="center", horizontalalignment="left")

        plt.axhline(0, color='c', linestyle='-')
        plt.axhline(1, color='y', linestyle=":")
        if year > 5:
            plt.axvline(5, color='y', linestyle=':')
            pass

        plt.axhline(3, color='r', linestyle=':')
        if year >= 10:
            plt.axvline(10, color='r', linestyle=':')
            pass
        plt.xlabel('year')
        plt.ylabel('benefit')
        plt.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.1, wspace=0.18, hspace=0.18)
        plt.show()
        pass

    def benefit_sort(self):
        b_list = []
        for i, code in enumerate(self.codes):
            print code
            roes = StockInfo.get_roes(code)
            roe = roes[0].roe5 * 0.85
            pbs = Util.get_list_last(StockInfo.get_pb_stocks(code), 1250)
            pb_count = len(pbs)
            pb_now = pbs[pb_count - 1].pb
            pb20 = sorted(pbs, cmp=self.__cmp_pb)[int(pb_count * 0.2)].pb
            print roe, pb_now, pb20, 1
            benefit_map = compute_benefit(10, roe / 100, pb_now, pb20)
            benefit_map['name'] = self.names[i]
            benefit_map['code'] = code
            b_list.append(benefit_map)
            benefit_map['count'] = 0
            if benefit_map['pb_benefit'] >= 3:
                benefit_map['count'] += 1
                pass
            if benefit_map['pb_future_benefit'] >= 3:
                benefit_map['count'] += 1
                pass
            if benefit_map['pb_buy_future_benefit'] >= 3:
                benefit_map['count'] += 1
                pass
            pass
        b_list = sorted(b_list, cmp=self.__cmp_benefit_list)
        return b_list
        pass

    def __cmp_benefit_list(self, o1, o2):
        if o1['count'] != o2['count']:
            return o2['count'] - o1['count']
            pass
        else:
            return int(10000 * (o1['pb_buy'] - o2['pb_buy']))
            pass
        pass

    pass


import source


def sort_benefit():
    c_list = source.get_origin_selected_codes()
    names = []
    codes = []
    for c in c_list:
        names.append(c['name'])
        codes.append(c['code'])
        pass
    print names
    print codes
    list = BenefitChart(names, codes).benefit_sort()
    csv_writer = csv.writer(open(Util.get_benefit_dir() + "/select.csv", 'wb'))
    csv_writer1 = csv.writer(open('selected_sorted.csv', 'wb'))
    Util.print_row(['名字', 'code', '满足数量', '买入pb', '1pb收益率', '买pb收益率', '20%pb收益率'], csv_writer)
    for m in list:
        row = [m['name'], 'A' + m['code'], m['count'], Util.format_float(m['pb_buy']),
               Util.format_to_percentage(m['pb_benefit']),
               Util.format_to_percentage(m['pb_buy_future_benefit']), Util.format_to_percentage(m['pb_future_benefit'])]
        Util.print_row(row, csv_writer1)
        Util.print_row(row, csv_writer, False)
        pass
    pass
