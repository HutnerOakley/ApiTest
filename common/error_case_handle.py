#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-28 10:38
# @Name    : error_case_handle.py
# @Description   : 运行失败用例的处理
# @Author  : Hunter

import os
import json
import ast
from common.get_files_path import get_all_files
from common.allure_coolect import AllureFileHandle


class ErrorCase:

    def __init__(self):
        self.case_path =  os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report', 'html', 'data', 'test-cases')

    def get_error_case(self):
        """
        获取所有失败用例的数据
        """
        file_name = get_all_files(self.case_path)
        files = []
        for path in file_name:
            with open(path,'r',encoding='utf-8')as f:
                data = json.load(f)
                if data['status'] == 'failed' or data['status'] == 'broken':
                    files.append(data)
        return files

    @classmethod
    def get_case_name(cls,test_case):
        """
        获取测试用例名称
        :return:
        """
        name = test_case['name'].split('[')
        case_name = name[1][:-1]
        return case_name
