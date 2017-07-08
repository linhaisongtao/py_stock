import datetime
from Tkinter import *

import RankChart as rc
import SChart
import StockInfo
import benefit
import rank as rk

reload(sys)
sys.setdefaultencoding('utf-8')


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
        rank_chart = rc.RankChart("rank in past 5 years", rank_list)
        rank_chart.show()
        pass

    def rank10_button_clicked(self):
        print 'rank10_button_clicked'
        rank_list = rk.get_rank_list(10)
        rank_chart = rc.RankChart("rank in past 10 years", rank_list)
        rank_chart.show()
        pass

    def check_button_double_clicked(self, event, index):
        print 'check_button_double_clicked', index
        benefit.BenefitChart([self.code_list[index]['name']], [self.code_list[index]['code']]).show()
        pass

    def handlerAdaptor(self, fun, **kwds):
        return lambda event, fun=self.check_button_double_clicked, kwds=kwds: fun(event, **kwds)
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
            check_button = Checkbutton(root, text="%s[%s]C[%d]" % (s['name'], s['code'], s['count']), variable=var)
            check_button.grid(row=i, column=2, columnspan=2)
            index = int(i)
            check_button.bind("<Double-Button-1>", self.handlerAdaptor(self.check_button_double_clicked, index=index))
            pass
        Button(root, text="compare", command=self.button_clicked).grid(row=len(self.code_list), column=2)
        Button(root, text="benefit_10years", command=self.benefit_button_clicked).grid(row=len(self.code_list),
                                                                                       column=3)

        base_column = 4
        base_row = 0
        Label(root, text='-------benefit calculator------  ').grid(row=base_row, column=base_column, columnspan=2)
        base_row += 1
        Label(root, text='year:').grid(row=base_row, column=base_column)
        year_str = StringVar()
        year_str.set('10')
        self.year_entry = Entry(root, textvariable=year_str)
        self.year_entry.grid(row=base_row, column=base_column + 1)
        base_row += 1
        Label(root, text='roe:').grid(row=base_row, column=base_column)
        roe_str = StringVar()
        roe_str.set('0.15')
        self.roe_entry = Entry(root, textvariable=roe_str)
        self.roe_entry.grid(row=base_row, column=base_column + 1)
        base_row += 1
        Label(root, text='pb_buy:').grid(row=base_row, column=base_column)
        pb_buy_str = StringVar()
        pb_buy_str.set('1')
        self.pb_buy_entry = Entry(root, textvariable=pb_buy_str)
        self.pb_buy_entry.grid(row=base_row, column=base_column + 1)
        base_row += 1
        Label(root, text='pb_future:').grid(row=base_row, column=base_column)
        pb_future_str = StringVar()
        pb_future_str.set('1')
        self.pb_future_entry = Entry(root, textvariable=pb_future_str)
        self.pb_future_entry.grid(row=base_row, column=base_column + 1)
        base_row += 1
        Button(root, text='calculate', command=self.calculate_button_clicked).grid(row=base_row, column=base_column,
                                                                                   columnspan=2)

        root.title(datetime.datetime.now().strftime("%Y-%m-%d"))
        root.mainloop()
        pass

    def calculate_button_clicked(self):
        print 'calculate_button_clicked', self.pb_buy_entry.get()
        benefit.BenefitChart(None, None).show_chart(int(self.year_entry.get()), float(self.roe_entry.get()),
                                                    float(self.pb_buy_entry.get()), float(self.pb_future_entry.get()))
        pass

    pass
