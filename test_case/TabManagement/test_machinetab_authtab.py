#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-03-04 11:02
# @Name    : test_machinetab_authtab.py
# @Description   :  查询用户授权接口
# @Author  : Hunter

import os
import sys
import pytest
import allure

path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(path)
from common.requests_util import HttpRequest
from common.regular_handle import cache_regular
from common.yaml_operate import GetCaseData
from common.assert_control import Assert

machinetab_yaml_path = os.path.join(os.path.split(os.path.dirname(os.path.dirname(__file__)))[0], 'test_data',
                                    'TabManagement', 'machinetab_authtab.yaml')

re_data = GetCaseData(machinetab_yaml_path).get_yaml_case_data()
case_data = cache_regular(str(re_data))


@allure.epic("cms云端接口")
@allure.feature("机型TAB管理模块")
class TestAllMachine:

    @allure.story("查询用户授权的机型Tab名称")
    @pytest.mark.parametrize('case_info', eval(case_data), ids=[i['api_name'] for i in re_data])
    def test_machinetab_all_machine(self, case_info):
        url = case_info['api_request']['url']
        method = case_info['api_request']['method']
        data = case_info['api_request']['data']
        headers = case_info['api_request']['headers']
        validate_data = case_info['validate']
        sql_data = case_info['sql']
        res = HttpRequest().send_request(uri=url, method=method, params=data, headers=headers)
        Assert(
            validate=validate_data,
            sql_data=sql_data,
            request_data=data,
            response_data=res.text,
            status_code=res.status_code
        ).assert_type_manage()
