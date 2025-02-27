#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-26 11:31
# @Name    : enum_config.py
# @Description   :枚举配置
# @Author  : Hunter

import types
from enum import Enum, unique
from typing import Union, Text, Dict, Callable
from dataclasses import dataclass


@unique
class AssertMethod(Enum):
    """断言类型"""
    equals = "=="
    less_than = "lt"
    less_than_equals = "le"
    greater_than = "gt"
    greater_than_equals = "ge"
    not_equals = "not_eq"
    contains = "contains"
    startwiths = "startwiths"


@unique
class MySqlDB(Enum):
    """数据库配置"""
    switch = False
    host: Union[Text, None] = "127.0.0.1"
    user: Union[Text, None] = "root"
    password: Union[Text, None] = "123456"
    port: Union[int, None] = 3306


@dataclass
class TestData:
    """用例执行的数据"""
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


@unique
class AllureAnnexType(Enum):
    """
    allure报告中附件的文件类型枚举
    """
    TEXT = "text"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "MP4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


def load_module_functions(module) -> Dict[Text, Callable]:
    """获取module中方法的名称和所在的内存地址"""
    module_functions = {}
    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


if __name__ == '__main__':
    name = AssertMethod("==").name
    print(name)
    print(MySqlDB.switch)
