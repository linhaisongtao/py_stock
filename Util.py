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


import datetime


def get_now_date_str():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H')
    pass


def convert_date_str_to_str(s):
    return datetime.datetime.strptime(s, '%Y%m%d').strftime('%Y-%m-%d')
    pass