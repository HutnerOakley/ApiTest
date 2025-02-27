#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-23 16:54
# @Name    : assert_control.py
# @Description   : 断言的统一封装
# @Author  : Hunter

import ast
import json
from jsonpath import jsonpath
from common.regular_handle import cache_regular
from common import assert_type
from common.enum_config import AssertMethod, MySqlDB, load_module_functions
from common.logger import LogHandler


class AssertUtil:

    def __init__(self, validate, sql_data, request_data, response_data, status_code):
        self.validate = validate
        self.sql_data = sql_data
        self.request_data = request_data
        self.response_data = response_data
        self.status_code = status_code
        self.sql_switch = MySqlDB.switch.value

    @property
    def get_validate_data(self):
        """
        获取断言数据
        :return:
        """
        assert self.validate is not None, (
                "'%s' should either include a `validate` attribute, "
                % self.__class__.__name__
        )
        return ast.literal_eval(cache_regular(str(self.validate)))

    @property
    def get_type(self):
        """获取断言中的type"""
        assert 'type' in self.get_validate_data.keys(), (
                " 断言数据: '%s' 中缺少 `type` 属性 " % self.get_validate_data
        )
        name = AssertMethod(self.get_validate_data.get("type")).name
        return name

    @property
    def get_assert_type(self):
        assert 'AssertType' in self.get_validate_data.keys(), (
                " 断言数据: '%s' 中缺少 `AssertType` 属性 " % self.get_validate_data
        )
        return self.get_validate_data.get("AssertType")

    @property
    def get_value(self):
        """获取断言中的value"""
        assert 'value' in self.get_validate_data.keys(), (
                " 断言数据: '%s' 中缺少 `value` 属性 " % self.get_validate_data
        )
        return self.get_validate_data.get("value")

    @property
    def get_response_data(self):
        return json.loads(self.response_data)

    @property
    def get_jsonpath(self):
        assert 'jsonpath' in self.get_validate_data.keys(), (
                " 断言数据: '%s' 中缺少 `jsonpath` 属性 " % self.get_validate_data
        )
        return self.get_validate_data.get("jsonpath")

    @property
    def get_sql_data(self):
        """获取断言中的sql数据"""
        if self.sql_switch:
            assert self.sql_data != {'sql': None}, (
                "请在用例中添加您要查询的SQL语句"
            )
        else:
            LogHandler().logger.info(
                "检测到数据库开关是关闭，不进行数据库断言，断言值:%s" % self.get_validate_data
            )
        # 将sql查询的数据是bytes，转换成str类型
        if isinstance(self.sql_data, bytes):
            return self.sql_data.decode('utf-8')

        # sql_data = jsonpath(self.sql_data, self.get_value)
        if self.sql_data:
            sql_data = self.sql_data.get("value")
            if sql_data:
                if len(sql_data) > 1:
                    return sql_data
                else:
                    return sql_data[0]
        return self.sql_data

    @property
    def get_message(self):
        """获取断言的描述信息"""
        return self.get_validate_data.get("message", None)

    @staticmethod
    def functions_map():
        return load_module_functions(assert_type)

    def _assert(self, check_value, expect_value, message):
        self.functions_map()[self.get_type](check_value, expect_value, message)

    @property
    def _assert_res_data(self):
        """根据断言中的jsonpath提取响应数据"""
        res_data = jsonpath(self.get_response_data, self.get_jsonpath)
        assert res_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.get_response_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(res_data) > 1:
            return res_data
        return res_data[0]

    def assert_type_manage(self):
        """
        :return:
        """
        if self.get_assert_type == "SQL":
            self._assert(self._assert_res_data, self.get_sql_data, self.get_message)
        elif self.get_assert_type is None:
            self._assert(self._assert_res_data, self.get_value, self.get_message)
        else:
            raise Exception("断言失败，目前只支持数据库和响应两种断言方式")


class Assert(AssertUtil):

    def assert_list_data(self):
        assert_list = []
        for k, v in self.validate.items():
            if k == 'status_code':
                assert self.status_code == v.get('value'), "接口响应状态码断言失败"
            else:
                assert_list.append(v)
        return assert_list

    def assert_type_manage(self):
        for i in self.assert_list_data():
            self.validate = i
            super().assert_type_manage()


if __name__ == '__main__':
    funcs = load_module_functions(assert_type)
    print(funcs)
