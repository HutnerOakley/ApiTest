#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-19 16:50
# @Name    : cache_control.py
# @Description   : 缓存文件处理
# @Author  : Hunter

import os
import yaml


class CacheControl(object):
    """缓存处理"""

    def __init__(self, filename=None):
        if filename:
            self.path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', filename)
        else:
            self.path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'csrf.yaml')

    def set_cache_value(self, key, value):
        """
        设置缓存，只支持设置单字典类型
        :param key:
        :param value:
        :return:
        """
        with open(self.path, 'w', encoding='utf-8')as f:
            f.write(str({key: value}))

    def set_caches(self, value):
        """
        设置多组缓存数据
        :param value:
        :return:
        """
        with open(self.path, 'w', encoding='utf-8')as f:
            f.write(str(value))

    def get_cache(self):
        """
        获取缓存数据
        :return:
        """
        try:
            with open(self.path, 'r', encoding='utf-8')as f:
                return f.read()
        except FileNotFoundError:
            raise

    def clean_cache(self):
        """
        删除缓存文件
        :return:
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"您要删除的缓存文件不存在 {self.path}")
        os.remove(self.path)

    def get_cache_value(self, data):
        """
        根据key，获取缓冲文件中的值
        :return:
        """
        try:
            with open(self.path, 'r', encoding='utf-8')as f:
                yaml_value = yaml.load(stream=f, Loader=yaml.FullLoader)
        except KeyError:
            raise KeyError(f"{data}的缓存数据未找到，请检查数据是否正常写入缓存中")
        return yaml_value[data]


_cache_config = {}


class CacheHandler(object):

    @staticmethod
    def get_cache(cache_data):
        try:
            return _cache_config[cache_data]
        except KeyError:
            raise KeyError(f"{cache_data}的缓存数据未找到，请检查数据是否正常写入缓存中")

    @staticmethod
    def update_cache(cache_key, cache_value):
        _cache_config[cache_key] = cache_value


if __name__ == '__main__':
    # 测试代码
    CacheHandler.update_cache('token', 'aasdadqeqzcxvg4567')
    CacheHandler.update_cache('api-token', 'ZjFiY2ZmYjgtNDJkYy00OTAyLThiMjktNDc0YTcxNThiMzQ1')
    print(_cache_config)
    print(CacheHandler.get_cache(cache_data='token'))
    print(CacheControl().get_cache_value('token'))