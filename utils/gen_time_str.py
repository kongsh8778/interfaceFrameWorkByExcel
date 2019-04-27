# -*-coding:utf-8 -*-
import time


def get_date():
    """获取日期字符串"""
    time_tuple = time.localtime(time.time())
    return "{0}年{1}月{2}日".format(str(time_tuple.tm_year),str(time_tuple.tm_mon), str(time_tuple.tm_mday))


def get_time():
    """获取时间字符串"""
    time_tuple = time.localtime(time.time())
    return "{0}时{1}分{2}秒".format(str(time_tuple.tm_hour), str(time_tuple.tm_min), str(time_tuple.tm_sec))


def get_datetime():
    """生成日期+日期字符串，格式为xxxx年xx月xx日 xx时xx分xx秒"""
    return get_date() + ' ' + get_time()


if __name__ == "__main__":
    print(get_date())
    print(get_time())
    print(get_datetime())