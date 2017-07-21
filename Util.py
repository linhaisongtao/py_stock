#!/usr/bin/python
# coding:utf-8
def get_list_last(list, max_count=-1):
    if max_count <= 0:
        return list
        pass
    else:
        start_index = max(0, len(list) - max_count)
        s_list = []
        for i in range(start_index, len(list)):
            s_list.append(list[i])
            pass
        return s_list
        pass
    pass


def format_float(f):
    if isinstance(f, float):
        return '%.2f' % f
        pass
    return f
    pass


def format_to_percentage(f):
    if isinstance(f, float):
        return '%.2f%%' % (f * 100)
        pass
    return f
    pass


import datetime


def get_now_date_str():
    return datetime.datetime.now().strftime('%Y-%m-%d')
    pass


def convert_date_str_to_str(s):
    return datetime.datetime.strptime(s, '%Y%m%d').strftime('%Y-%m-%d')
    pass


import os


def get_dir_name():
    if not os.path.exists('.data'):
        os.mkdir('.data')
        pass

    dir_name = '.data/' + get_now_date_str()
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        pass

    return dir_name
    pass


import csv


def print_row(list, writer=None, print_console=True):
    if writer != None:
        writer.writerow(list)
        pass
    if print_console:
        s = ''
        for l in list:
            s += str(l) + '\t'
            pass
        print s
        pass
    pass


def get_benefit_dir():
    if not os.path.exists('select_stock'):
        os.mkdir('select_stock')
        pass

    dir_name = 'select_stock/' + get_now_date_str()
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        pass

    return dir_name
    pass
