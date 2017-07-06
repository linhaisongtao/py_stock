import matplotlib.pyplot as plt

import sys
import datetime
import threading
import StockInfo
import SChart

from Tkinter import *

import threading
import rank as rk
import RankChart as rc
import benefit


class Window(object):
    def __init__(self, code_list):
        self.code_list = code_list
        pass

    def on_selected(self, event):
        lb = event.widget
        index = lb.curselection()[0]
        if (index < 0 or index >= len(self.code_list)):
            return
            pass
        code = self.code_list[index]['code']
        name = self.code_list[index]['name']
        title1 = name + "[" + code + "]%d" % 1
        s1 = StockInfo.get_pb_stocks(code, 1)
        SChart.SChart([title1], [s1]).show()
        pass

    def callCheckbutton(self):
        print ('you check this button')
        pass

    def button_clicked(self):
        print 'compare'
        titles = []
        stocks = []
        codes = []
        for i, state in enumerate(self.check_states):
            if state.get() == 1:
                titles.append("%s[%s]" % (self.code_list[i]['name'], self.code_list[i]['code']))
                stocks.append(StockInfo.get_pb_stocks(self.code_list[i]['code'], 5))
                codes.append(self.code_list[i]['code'])
                pass
            pass
        SChart.SChart(titles, stocks).show()
        # benefit.BenefitChart(titles, codes).show()
        pass

    def benefit_button_clicked(self):
        print 'benefit_button_clicked'
        codes = []
        names = []
        for i, state in enumerate(self.check_states):
            if state.get() == 1:
                codes.append(self.code_list[i]['code'])
                names.append(self.code_list[i]['name'])
                pass
            pass
        benefit.BenefitChart(names, codes).show()
        pass

    def rank5_button_clicked(self):
        print 'rank5_button_clicked'
        rank_list = rk.get_rank_list()
        for rank in rank_list:
            print rank
            pass
        rank_chart = rc.RankChart("rank in past 5 years", rank_list)
        rank_chart.show()
        pass

    def rank10_button_clicked(self):
        print 'rank10_button_clicked'
        rank_list = rk.get_rank_list(10)
        for rank in rank_list:
            print rank
            pass
        rank_chart = rc.RankChart("rank in past 10 years", rank_list)
        rank_chart.show()
        pass

    def show(self):
        root = Tk()
        listb = Listbox(root, width=100, height=len(self.code_list) + 1)
        for i, s in enumerate(self.code_list):
            listb.insert(i, "%s[%s]" % (s['name'], s['code']))
            pass
        listb.bind("<Double-Button-1>", self.on_selected)
        listb.grid(row=0, rowspan=len(self.code_list), column=0, columnspan=2)
        Button(root, text="rank in past 5 years", command=self.rank5_button_clicked).grid(row=len(self.code_list),
                                                                                          column=0)
        Button(root, text="rank in past 10 years", command=self.rank10_button_clicked).grid(row=len(self.code_list),
                                                                                            column=1)

        self.check_states = []
        for i, s in enumerate(self.code_list):
            var = IntVar()
            self.check_states.append(var)
            check_button = Checkbutton(root, text="%s[%s]" % (s['name'], s['code']), variable=var)
            check_button.grid(row=i, column=2, columnspan=2)
            pass
        Button(root, text="compare", command=self.button_clicked).grid(row=len(self.code_list), column=2)
        Button(root, text="benefit_10years", command=self.benefit_button_clicked).grid(row=len(self.code_list),
                                                                                       column=3)

        root.title(datetime.datetime.now().strftime("%Y-%m-%d"))
        root.mainloop()
        pass

    pass
