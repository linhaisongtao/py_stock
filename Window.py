import matplotlib.pyplot as plt

import sys
import datetime
import threading
import StockInfo
import SChart

from Tkinter import *

import threading


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
        title = name + "[" + code + "]"
        s = StockInfo.get_pb_stocks(code)
        SChart.SChart([title], [s]).show()
        pass

    def callCheckbutton(self):
        print ('you check this button')
        pass

    def button_clicked(self):
        print 'compare'
        titles = []
        stocks = []
        for i, state in enumerate(self.check_states):
            if state.get() == 1:
                titles.append("%s[%s]" % (self.code_list[i]['name'], self.code_list[i]['code']))
                stocks.append(StockInfo.get_pb_stocks(self.code_list[i]['code']))
                pass
            pass
        SChart.SChart(titles, stocks).show()
        pass

    def show(self):
        root = Tk()
        listb = Listbox(root, width=100, height=len(self.code_list) + 1)
        for i, s in enumerate(self.code_list):
            listb.insert(i, "%s[%s]" % (s['name'], s['code']))
            pass
        listb.bind("<Double-Button-1>", self.on_selected)
        listb.grid(row=0, rowspan=len(self.code_list) + 1, column=0)

        self.check_states = []
        for i, s in enumerate(self.code_list):
            var = IntVar()
            self.check_states.append(var)
            check_button = Checkbutton(root, text="%s[%s]" % (s['name'], s['code']), variable=var)
            check_button.grid(row=i, column=1)
            pass
        Button(root, text="compare", command=self.button_clicked).grid(row=len(self.code_list), column=1)

        root.title(datetime.datetime.now().strftime("%Y-%m-%d"))
        root.mainloop()
        pass

    pass
