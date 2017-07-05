import urllib2
import cookielib, os
import matplotlib.pyplot as plt
import tushare as ts
import pandas as pd
import StockInfo as si
import SChart as sc
import json, datetime, time
import DateUtil

data_dir = '.p'
pb_data_dir = '.pb'
roe_data_dir = '.roe'
# roe_selected_date = ['0331', '0630', '0930', '1231']
roe_selected_date = ['1231']


class StockInfo(object):
    def __init__(self, date="", price=0, pure=0, roe=0, roe5_price=0, code='', roe5=0, pb=0, pb5_wanted=0, roe1=0,
                 pb1_wanted=0):
        self.date = date
        self.price = price
        self.pure = pure
        self.roe = roe
        self.roe5_price = roe5_price
        self.code = code
        self.roe5 = roe5
        self.pb = pb
        self.pb5_wanted = pb5_wanted
        self.roe1 = roe1
        self.pb1_wanted = pb1_wanted
        pass

    def __str__(self):
        return "date=%s\tprice=%.2f\tpure=%.2f\troe=%.2f\troe5_price=%.2f\troe5=%.2f\tpb=%.2f\tpb5_wanted=%.2f\tpb1_wanted=%.2f" % (
            self.date, self.price, self.pure, self.roe, self.roe5_price, self.roe5, self.pb, self.pb5_wanted,
            self.pb1_wanted)
        pass

    pass


def get_stocks(code='601166', average_year_count=1):
    date_str = DateUtil.get_now_date_str()
    # get basic history info
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        pass
    file_name = data_dir + "/" + code + "_" + date_str + ".json"
    list = []
    if os.path.exists(file_name):
        print 'read from file', file_name
        arr = json.loads(open(file_name, 'r').read())
        for a in arr:
            list.append(StockInfo(**a))
            pass
        pass
    else:
        print 'read from net'
        df = ts.get_hist_data(code, start='2010-01-01')
        for d in df.iterrows():
            s = si.StockInfo()
            s.date = d[0]
            s.price = d[1][2]
            s.code = code
            s.pure = 12
            s.roe = 15
            s.roe5_price = 12
            list.append(s)
            pass
        list.reverse()
        __write_to_file(file_name, list)
        pass

    reo_list = __get_roes(code=code, average_year_count=average_year_count)
    for l in list:
        matched_s = __find_matched_roe(l, reo_list)
        if matched_s == None:
            l.pure = 0
            l.roe = 0
            l.roe5_price = 0
            l.roe5 = 0
            pass
        else:
            l.pure = matched_s.pure
            l.roe = matched_s.roe
            l.roe5 = matched_s.roe5
            l.roe5_price = l.pure * l.roe5 / 15
            pass
        pass

    return list
    pass


def __write_to_file(name, list):
    json_string = json.dumps(list, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    open(name, 'w').write(json_string)
    pass


def __get_roes(code, average_year_count=1):
    date_str = DateUtil.get_now_date_str()
    if not os.path.exists("." + date_str):
        os.mkdir("." + date_str)
        pass
    file_name = "." + date_str + "/roe_" + code + "_" + ".json"
    if os.path.exists(file_name):
        print 'read roe from file', file_name
        result_string = open(file_name, 'r').read()
        pass
    else:
        print 'read reo from net'
        result_string = __request_roe_from_net(market_name='SH', code=code)
        list = json.loads(result_string)['list']
        if list == None or len(list) == 0:
            result_string = __request_roe_from_net(market_name='SZ', code=code)
            pass
        open(file_name, 'w').write(result_string)
        pass

    json_list = json.loads(result_string)['list']
    s_list = []
    for o in json_list:
        s = StockInfo()
        report_date = o['reportdate']
        # according to q
        roe_ratio = 1.0
        if report_date.find("0331") > 0:
            roe_ratio = 4
            pass
        elif report_date.find("0630") > 0:
            roe_ratio = 2
            pass
        elif report_date.find("0930") > 0:
            roe_ratio = 4 / 3
            pass
        else:
            roe_ratio = 1
            pass

        if o['naps'] == None:
            s.pure = 0
            pass
        else:
            s.pure = o['naps']
            pass

        if o['weightedroe'] == None:
            s.roe = 0
            pass
        else:
            s.roe = o['weightedroe'] * roe_ratio
            pass

        s.date = datetime.datetime.strptime(o['reportdate'], '%Y%m%d').strftime('%Y-%m-%d')
        s.code = code
        if __apply_roe_date(report_date):
            s_list.append(s)
            pass
        else:
            pass
        pass
    for i, s in enumerate(s_list):
        s.roe5 = __compute_roe_average(s_list, i, 5)
        s.roe1 = __compute_roe_average(s_list, i, 1)
        pass
    return s_list
    pass


def __compute_roe_average(roe_list, start_index, count=1):
    end = min(start_index + count, len(roe_list))
    total = end - start_index
    roe_l = []
    for i in range(start_index, end):
        roe_l.append(roe_list[i].roe)
        pass
    return sum(roe_l) / total
    pass


def __apply_roe_date(roe_date_str):
    result = False
    for d in roe_selected_date:
        if roe_date_str.find(d) > 0:
            result = True
            break
            pass
        pass
    return result
    pass


def __request_roe_from_net(market_name="SH", code='601166'):
    timestamp = (((long)(time.mktime(datetime.datetime.now().timetuple()) * 1000)))
    url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=%s%s&page=1&size=100&_=%d" % (
        market_name, code, timestamp)
    print url
    request = urllib2.Request(url)
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    request.add_header("Cookie",
                       "s=ew15skiac9; webp=0; device_id=0e265d4368be601f15cc880fe55a241b; aliyungf_tc=AQAAALYpOj2IgwwA/jdr2ifXsmgqx7+k; xq_a_token=0a52c567442f1fdd8b09c27e0abb26438e274a7e; xq_a_token.sig=dR_XY4cJjuYM6ujKxH735NKcOpw; xq_r_token=43c6fed2d6b5cc8bc38cc9694c6c1cf121d38471; xq_r_token.sig=8d4jOYdZXEWqSBXOB9N5KuMMZq8; u=861498716068684; __utma=1.368657217.1497955103.1498636561.1498735155.5; __utmb=1.4.10.1498735155; __utmc=1; __utmz=1.1497955103.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1498636757,1498716069,1498719015,1498735149; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1498735172")
    response = urllib2.urlopen(request)
    result_string = response.read()
    return result_string
    pass


def __find_matched_roe(s, roe_list):
    s_date = datetime.datetime.strptime(s.date, "%Y-%m-%d")
    for roe in roe_list:
        roe_date = datetime.datetime.strptime(roe.date, "%Y-%m-%d")
        if s_date >= roe_date:
            return roe
            pass
        pass
    pass


def __request_pb_from_net(market='SH', code='601166'):
    timestamp = (long)(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    url = "https://www.joudou.com/stockinfogate/stock/logpepbs/%s.SH?_t=%d" % (code, timestamp)
    print url
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response.read()
    pass


def get_pb_stocks(code='601166', average_year_count=1, max_count=-1):
    date_str = DateUtil.get_now_date_str()
    # get basic history info
    if not os.path.exists("." + date_str):
        os.mkdir("." + date_str)
        pass
    file_name = "." + date_str + "/pb_" + code + ".json"
    list = []

    if os.path.exists(file_name):
        print 'read from file', file_name
        json_string = open(file_name, 'r').read()
        pass
    else:
        print 'read from net'
        json_string = __request_pb_from_net('SH', code)
        open(file_name, 'w').write(json_string)
        pass

    json_list = json.loads(json_string)['data']['data']
    for data in json_list:
        s = StockInfo()
        s.date = datetime.datetime.strptime(data[0], '%Y%m%d').strftime('%Y-%m-%d')
        s.code = code
        s.pb = data[3]
        list.append(s)
        pass

    reo_list = __get_roes(code=code, average_year_count=average_year_count)
    for l in list:
        matched_s = __find_matched_roe(l, reo_list)
        if matched_s == None:
            l.pure = 0
            l.roe = 0
            l.roe5_price = 0
            l.roe5 = 0
            l.pb5_wanted = 0
            l.roe1 = 0
            l.pb1_wanted = 0
            pass
        else:
            l.pure = matched_s.pure
            l.roe = matched_s.roe
            l.roe5 = matched_s.roe5
            l.roe5_price = l.pure * l.roe5 / 15
            l.pb5_wanted = l.roe5 / 15

            l.roe1 = matched_s.roe1
            l.pb1_wanted = l.roe1 / 15
            pass
        pass

    # for l in list:
    #     print l
    #     pass
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
