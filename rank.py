import StockInfo
import source
import pandas as pd
import hashlib
import datetime, os, json


class RankInfo(object):
    def __init__(self, pb=0, pb_position=0, pb5_wanted=0, pb1_wanted=0, code='', name=''):
        self.pb = pb
        self.pb_position = pb_position
        self.pb5_wanted = pb5_wanted
        self.pb1_wanted = pb1_wanted
        self.code = code
        self.name = name
        pass

    pass


class Rank(object):
    def __init__(self, rankInfo5=RankInfo(), rankInfo10=RankInfo(), name='', code=''):
        self.rankInfo5 = rankInfo5
        self.rankInfo10 = rankInfo10
        self.name = name
        self.code = code
        pass

    # def __str__(self):
    #     return 'code=%s,pb_position(5)=%.2f,pb_position(10)=%.2f' % (
    #         self.code, self.rankInfo5.pb_position, self.rankInfo10.pb_position)
    #     pass

    pass


def __get_list_last(list, max_count=-1):
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


def __find_position_in_list(list, number):
    position = 0
    for i, l in enumerate(list):
        if l >= number:
            position = i
            break
            pass
        pass
    return position
    pass


def __compute_rank_info(s_list, year=5):
    list = []
    if year == 5:
        list = __get_list_last(s_list, 1250)
        pass
    elif year == 10:
        list = __get_list_last(s_list, 2500)
        pass
    else:
        list = __get_list_last(s_list, 1250)
        pass

    pb_list = []
    for l in list:
        pb_list.append(l.pb)
        pass

    pb_list = sorted(pb_list)
    rank_info = RankInfo()
    s_info = s_list[len(s_list) - 1]
    rank_info.pb = s_info.pb
    rank_info.pb1_wanted = s_info.pb1_wanted
    rank_info.pb5_wanted = s_info.pb5_wanted
    rank_info.pb_position = 1.0 * __find_position_in_list(pb_list, rank_info.pb) / len(pb_list)
    return rank_info
    pass


def __cmp5(rank1, rank2):
    return int(10000 * (rank1.rankInfo5.pb_position - rank2.rankInfo5.pb_position))
    pass


def __cmp10(rank1, rank2):
    return int(10000 * (rank1.rankInfo10.pb_position - rank2.rankInfo10.pb_position))
    pass


def __get_md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def get_rank_list(sort_year=5):
    codes = source.get_selected_codes()

    str = ''
    for c in codes:
        str += c['code']
        pass
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H')
    file_name = '.rank/date[%s]_year[%d]_%s.json' % (date_str, sort_year, __get_md5(str))
    print file_name
    if not os.path.exists('.rank'):
        os.mkdir('.rank')
        pass

    if os.path.exists(file_name):
        print 'read from file', file_name
        arr = json.loads(open(file_name, 'r').read())
        rank_list = []
        for a in arr:
            rank = Rank()
            rank.name = a['name']
            rank.code = a['code']

            rank5 = a['rankInfo5']
            rank_info5 = RankInfo()
            rank_info5.code = rank5['code']
            rank_info5.name = rank5['name']
            rank_info5.pb_position = rank5['pb_position']
            rank_info5.pb = rank5['pb']
            rank_info5.pb5_wanted = rank5['pb5_wanted']
            rank_info5.pb1_wanted = rank5['pb1_wanted']
            rank.rankInfo5 = rank_info5

            rank10 = a['rankInfo10']
            rank_info10 = RankInfo()
            rank_info10.code = rank10['code']
            rank_info10.name = rank10['name']
            rank_info10.pb_position = rank10['pb_position']
            rank_info10.pb = rank10['pb']
            rank_info10.pb5_wanted = rank10['pb5_wanted']
            rank_info10.pb1_wanted = rank10['pb1_wanted']
            rank.rankInfo10 = rank_info10

            rank_list.append(rank)
            pass
        return rank_list
        pass
    else:
        rank_list = []
        for c in codes:
            list = StockInfo.get_pb_stocks(c['code'], average_year_count=5)
            rank = Rank()
            rank.rankInfo5 = __compute_rank_info(list, 5)
            rank.rankInfo5.name = c['name']
            rank.rankInfo5.code = c['code']

            rank.rankInfo10 = __compute_rank_info(list, 10)
            rank.rankInfo10.name = c['name']
            rank.rankInfo10.code = c['code']

            rank.name = c['name']
            rank.code = c['code']
            rank_list.append(rank)
            pass
        if sort_year == 5:
            rank_list = sorted(rank_list, cmp=__cmp5)
        elif sort_year == 10:
            rank_list = sorted(rank_list, cmp=__cmp10)
        else:
            rank_list = sorted(rank_list, cmp=__cmp5)
            pass
        json_string = json.dumps(rank_list, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        open(file_name, 'w').write(json_string)
        return rank_list
        pass
    pass
