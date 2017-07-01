import tushare as ts
import pandas as pd
import StockInfo
import threading
import json
import os, datetime


def __request_pbs(index, code, name):
    print '------------------------------------------------------------------------------------------------------'
    print 'No.%d get %s[%s]' % (index + 1, name, code)
    print '------------------------------------------------------------------------------------------------------'
    try:
        StockInfo.get_pb_stocks(code)
        pass
    except Exception as e:
        print e
        pass
    print 'No.%d received %s[%s]' % (index + 1, name, code)
    pass


def get_hs300_pb_roe_datas():
    df = ts.get_hs300s()
    stock_infos = []
    for row in df.iterrows():
        m = {}
        m['code'] = row[1][0]
        m['name'] = row[1][1]
        stock_infos.append(m)
        pass
    print len(stock_infos)
    threads = []
    for index, s in enumerate(stock_infos):
        t = threading.Thread(target=__request_pbs, args=(index + 1, s['code'], s['name']))
        threads.append(t)
        t.start()

        if (index + 1) % 10 == 0:
            for t in threads:
                t.join()
                pass
            print '---------------------------------------------------------------finished count =', (index + 1)
            threads = []
            pass

        pass

    pass


# get_hs300_pb_roe_datas()

def __get_price(index, code, name):
    df = ts.get_h_data(code, start='2000-01-01')
    if not os.path.exists('.price'):
        os.mkdir('.price')
        pass
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = '.price/' + code + "_" + date_str + ".json"
    if os.path.exists(file_name):
        print 'read from file', file_name
        pass
    else:
        stock_infos = []
        for row in df.iterrows():
            m = {}
            m['code'] = code
            m['date'] = row[0].__str__()
            m['price'] = row[1][2]
            stock_infos.append(m)
            pass
        json_string = json.dumps(stock_infos, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        open(file_name, 'w').write(json_string)
        pass
    print 'No.%d finished' % (index)
    pass


def get_hs300_history_price():
    df = ts.get_hs300s()
    stock_infos = []
    for row in df.iterrows():
        m = {}
        m['code'] = row[1][0]
        m['name'] = row[1][1]
        stock_infos.append(m)
        pass
    print len(stock_infos)
    threads = []
    for index, s in enumerate(stock_infos):
        t = threading.Thread(target=__get_price, args=(index + 1, s['code'], s['name']))
        threads.append(t)
        t.start()

        if (index + 1) % 3 == 0:
            for t in threads:
                t.join()
                pass
            print '---------------------------------------------------------------finished count =', (index + 1)
            threads = []
            pass

        pass

    pass


def get_hs300():
    df = ts.get_hs300s()
    s = ''
    for row in df.iterrows():
        code = row[1][0]
        name = row[1][1]
        s += (code + "  " + name + "\n")
        pass
    open('hs300.txt', 'w').write(s)
    pass

# get_hs300_history_price()
get_hs300()