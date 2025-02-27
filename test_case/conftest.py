#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-21 16:16
# @Name    : conftest_test.py
# @Description   : 
# @Author  : Hunter

import os
import json
import time
import sys
import requests
import pytest
path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(path)
from common.cache_control import CacheHandler
from common.yaml_operate import YamlUtil
from common.get_files_path import del_file, create_file_or_dir
from common.logger import LogHandler

csrf_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'csrf.yaml')
report_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report')


@pytest.fixture(scope="session", autouse=True)
def clear_file():
    YamlUtil(csrf_path).clear_yaml()


@pytest.fixture(scope="session", autouse=True)
def clear_report():
    del_file(report_path)
    create_file_or_dir(report_path, "tmp")


@pytest.fixture(scope="session", autouse=True)
def get_jessionid():
    """
    获取jessionid
    :return:
    """
    jessionid_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'JESSIONID.txt')
    with open(jessionid_path, 'r')as f:
        value = f.read()
    api_token = json.loads(value).get('api-token')
    CacheHandler.update_cache(cache_key='api-token', cache_value=api_token)
    YamlUtil(csrf_path).add_yaml_data({'api-token': api_token})
    return api_token


@pytest.fixture(scope="session", autouse=True)
def work_login(get_jessionid):
    """
    获取登录的cookie
    :return:
    """
    # pytest中fixture可以调用fixture
    api_token = get_jessionid
    url = "https://idsaas.test.leiniao.com/idsaas/generateToken"
    headers = {
        "Cookie": (
                      "rhp=https://idsaas.test.leiniao.com; JSESSIONID=%s; return-url=https://idsaas.test.leiniao.com/page/cms-api-docs/#/") % api_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,es-US;q=0.6,es;q=0.5,pt-PT;q=0.4,pt;q=0.3,it-IT;q=0.2,it;q=0.1,zh-CN;q=0.1,zh;q=0.1,ar-IL;q=0.1,ar;q=0.1,ru-RU;q=0.1,ru;q=0.1,zh-TW;q=0.1,en-US;q=0.1,es-ES;q=0.1,smn-FI;q=0.1,smn;q=0.1,hy-AM;q=0.1,hy;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/json;charset=UTF-8",
        "traditional": "true"
    }
    res = requests.get(url=url, headers=headers).json()
    token = res["data"]["generatedToken"]
    CacheHandler.update_cache(cache_key='token', cache_value=token)
    YamlUtil(csrf_path).add_yaml_data({'token': token})


def pytest_terminal_summary(terminalreporter):
    """
    pytest_terminal_summary是钩子函数
    统计测试结果
    :param terminalreporter:
    :return:
    """
    _passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _total = terminalreporter._numcollected
    # terminalreporter._sessionstarttime 会话开始时间
    _times = time.time() - terminalreporter._sessionstarttime
    info_logger = LogHandler().logger
    info_logger.error(f"用例总数：{_total}")
    info_logger.error(f"异常用例数：{_error}")
    info_logger.error(f"失败用例数：{_failed}")
    info_logger.error(f"跳过用例数：{_skipped}")
    info_logger.error(f"用例执行时长：%0.2f" % _times + " s")

# def pytest_collection_modifyitems(items):
#     """解决ids中文导致编码乱码"""
#     for item in items:
#         item.name = item.name.encode("utf-8").decode('unicode_escape')
#         item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
