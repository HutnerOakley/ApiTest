#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-01-24 18:36
# @Name    : yaml_operate.py
# @Description   :  处理yaml中数据
# @Author  : Hunter

import os
import yaml
import ast
from common.regular_handle import regular,cache_regular


class YamlUtil(object):

    def __init__(self, yaml_path):
        self.yaml_path = str(yaml_path)

    def get_yaml_data(self):
        """
        获取yaml中的数据
        :return:
        """
        # 判断文件是否存在
        if os.path.exists(self.yaml_path):
            with open(self.yaml_path, 'r', encoding='utf-8')as f:
                yaml_value = yaml.load(stream=f, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError('文件路径不存在')
        return yaml_value

    def write_yaml_data(self, data):
        """
        向yaml中写入数据
        :return:
        """
        with open(self.yaml_path, 'w', encoding='utf-8')as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)

    def add_yaml_data(self,data):
        """
        向yaml中添加数据,跟上面的write方法区别
        在于它会保留之前的数据，在文件尾进行追加
        :param data:
        :return:
        """
        with open(self.yaml_path,'a',encoding='utf-8')as f:
            yaml.dump(data=data,stream=f,allow_unicode=True)

    def clear_yaml(self):
        """
        清楚yaml文件
        :return:
        """
        with open(self.yaml_path,'w',encoding='utf-8')as f:
            f.truncate()


class GetCaseData(YamlUtil):

    def get_formats_yaml_data(self):
        """
        获取不同格式的yaml数据
        :return:
        """
        res_lists = []
        for i in self.get_yaml_data():
            res_lists.append(i)
        return res_lists

    def get_yaml_case_data(self):
        """
        获取测试用例数据，转换成指定数据格式
        :return:
        """
        _yaml_data = self.get_yaml_data()
        # 通过正则匹配的方式来处理yaml文件中数据
        re_data = regular(str(_yaml_data))
        return ast.literal_eval(re_data)


if __name__ == '__main__':
    path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'test_data', 'machinetab_query.yaml')
    value = YamlUtil(path).get_yaml_data()
    print(value)
    data = GetCaseData(path).get_yaml_case_data()
    print(data)
    new_data = str(data)
    cache_value = cache_regular(new_data)
    print(cache_value)





