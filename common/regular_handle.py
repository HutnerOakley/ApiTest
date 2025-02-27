#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-18 17:35
# @Name    : regular_handle.py
# @Description   : 正则方式处理请求数据
# @Author  : Hunter

import re
import random
from faker import Faker
from datetime import date, timedelta, datetime
from common.logger import LogHandler
from common.cache_control import CacheControl, CacheHandler


class ReplaceFunc(object):
    """正则替换"""

    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def get_random(cls):
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def get_phone(self):
        """
        :return: 随机生成手机号
        """
        phone = self.faker.phone_number()
        return phone

    def get_id_card(self):
        """
        :return: 随机身份证号码
        """
        id_num = self.faker.ssn()
        return id_num

    @classmethod
    def get_now_time(cls):
        """
        :return: 计算当前时间
        """
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return now_time

    @classmethod
    def today_date(cls):
        """获取今日0点整时间"""

        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def time_after_week(cls):
        """获取一周后12点整的时间"""

        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week


def regular(strs):
    '''
    使用正则替换请求数据
    :param data:
    :return:
    '''
    try:
        re_pattern = r'\${{(.*?)}}'
        while re.findall(re_pattern, strs):
            # 通过正则将表达式提取出来
            key = re.search(re_pattern, strs).group(1)
            values = ['int', 'bool', 'list', 'dict', 'tuple', 'float']
            if any(i in key for i in values) is True:
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(ReplaceFunc(), func_name)()
                else:
                    value_data = getattr(ReplaceFunc(), func_name)(*value_name.split(","))
                re_int_pattern = r'\'\${{(.*?)}}\''
                strs = re.sub(re_int_pattern, str(value_data), strs, 1)
            else:
                # 获取需要执行的函数名以及函数执行所需要的参数
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    # 通过反射来找到函数并执行
                    value_data = getattr(ReplaceFunc(), func_name)()
                else:
                    value_data = getattr(ReplaceFunc(), func_name)(*value_name.split(","))
                strs = re.sub(re_pattern, str(value_data), strs, 1)
        return strs

    except AttributeError:
        LogHandler(level='error').logger.error(f"没有找到对应替换的数据，请检查数据是否正确 {strs}")
        raise
    except IndexError:
        LogHandler(level='info').logger.error("yaml中的${{}}函数方法不正确，正确语法实例:${{get_now_time()}}")
        raise


def cache_regular(cache_value):
    """
    通过正则的方式，读取缓冲中的内容
    :param cache_value:
    :return:
    """
    # 正则获取$cache{token}中的值 -》token
    re_ca_pattern = r'\$cache\{(.*?)\}'
    re_list = re.findall(re_ca_pattern, cache_value)

    for re_data in re_list:
        values = ['int', 'bool', 'list', 'dict', 'tuple', 'float']
        if any(i in re_data for i in values):
            values = re_data.split(":")[0]
            re_data = re_data.split(":")[1]
            pattern = re.compile(r'\'\$cache\{' + values.split(":")[0] + ":" + re_data + r'\}\'')
        else:
            pattern = re.compile(r'\$cache\{' + re_data.replace('$', "\$").replace('[', '\[') + r'\}')
        try:
            cache_data = CacheControl().get_cache_value(re_data)
            # cache_data = CacheHandler.get_cache(re_data)
            cache_value = re.sub(pattern, str(cache_data), cache_value)
        except Exception:
            pass
    return cache_value


if __name__ == '__main__':
    CacheHandler.update_cache('token', 'aasdadqeqzcxvg4567')
    CacheHandler.update_cache('api-token', 'ZjFiY2ZmYjgtNDJkYy00OTAyLThiMjktNDc0YTcxNThiMzQ1')
    text = "${{get_id_card()}}"
    b = regular(text)
    # print(b)
    import os
    from common.yaml_operate import YamlUtil
    query_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'test_data', 'query_test.yaml')
    value = YamlUtil(query_path).get_yaml_data()
    # text_cache = '$cache{token}'
    c = cache_regular(value)
    print(c)
    # a = regular(c)
    # print(a)