import datetime


def get_now_date_str():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H')
    pass


def convert_date_str_to_str(s):
    return datetime.datetime.strptime(s, '%Y%m%d').strftime('%Y-%m-%d')
    pass
