#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-26 10:27
# @Name    : assert_type.py
# @Description   : 断言类型出来
# @Author  : Hunter


from typing import Any, Union, Text


def equals(check_value: Any, expect_value: Any, message: Text = ""):
    """判断是否相等"""
    assert check_value == expect_value, message


def less_than(check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果小于预期结果"""
    assert check_value < expect_value, message


def less_than_equals(check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果小于等于预期结果"""
    assert check_value <= expect_value, message


def greater_than(check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果大于预期结果"""
    assert check_value > expect_value, message


def greater_than_equals(check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果大于等于预期结果"""
    assert check_value >= expect_value, message


def not_equals(check_value: Any, expect_value: Any, message: Text = ""):
    assert check_value != expect_value, message


def contains(check_value: Any, expect_value: Any, message: Text = ""):
    """判断实际结果包含预期结果"""
    assert expect_value in check_value, message


def startwiths(check_value: Any, expect_value: Any, message: Text = ""):
    """检查响应内容的开头是否和预期结果内容开头相等"""
    assert str(check_value).startswith(str(expect_value)), message
