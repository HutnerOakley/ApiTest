#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-01-25 14:24
# @Name    : logger_decorator.py
# @Description   : 日志装饰器
# @Author  : Hunter

from common.logger import LogHandler


def log_decorator(switch: bool):
    """
    日志装饰器，打印请求信息
    :return:
    """

    def decorator(func):
        def swapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if switch:
                log_msg = f"\n=======================请求开始===============================\n" \
                          f"请求args参数: {args}\n" \
                          f"请求kwargs参数: {kwargs}\n" \
                          f"Http状态码: {res.status_code}\n" \
                          f"接口响应内容: {res.text}\n" \
                          "======================请求结束==============================="
                LogHandler().logger.info(log_msg)
            return res
        return swapper
    return decorator
