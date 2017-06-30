import matplotlib.pyplot as plt

import sys
import datetime
import threading
import StockInfo
import SChart

from Tkinter import *


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
        SChart.SChart(StockInfo.get_pb_stocks(code)).show()
        pass

    def show(self):
        root = Tk()
        listb = Listbox(root, width=100, height=len(self.code_list) + 1)
        for i, s in enumerate(self.code_list):
            listb.insert(i, "%s[%s]" % (s['name'], s['code']))
            pass
        listb.bind("<Double-Button-1>", self.on_selected)
        listb.pack()
        root.title(datetime.datetime.now().strftime("%Y-%m-%d"))
        root.mainloop()
        pass

    pass
