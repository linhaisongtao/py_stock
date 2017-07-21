#!/usr/bin/python
# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import matplotlib.pyplot as plt


class RoeChart(object):
    def show(self, sub_plot, roes):
        roes.reverse()

        x = []
        dates = []
        roe_list = []
        for index, roe in enumerate(roes):
            x.append(index)
            dates.append(roe.date[0:4])
            roe_list.append(roe.roe)
            pass

        last5 = roe_list[-5:]
        average5 = sum(last5) / len(last5)

        x.append(len(roes))
        roe_list.append(average5)
        dates.append("AVER5")

        rects = sub_plot.bar(x, roe_list)
        self.add_labels(sub_plot, rects)

        return {'x': x, 'dates': dates, 'average5': average5}
        pass

    # 添加数据标签
    def add_labels(self,sub_plot, rects):
        for rect in rects:
            height = rect.get_height()
            sub_plot.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
            # 柱形图边缘用白色填充，纯粹为了美观
            rect.set_edgecolor('white')

    pass
