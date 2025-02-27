#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-01-24 16:44
# @Name    : logger.py
# @Description   : logg的统一封装
# @Author  : Hunter

import logging
import os
import time

# 日志路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class LogHandler(object):
    # 日志级别
    level_mapping = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, name=__name__,level='info',
                 fmt="%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s"):
        # 使用传入的名称或模块
        self.logger = logging.getLogger(name)
        # 设置日志级别
        self.logger.setLevel(self.level_mapping.get(level))
        self.log_name = os.path.join(LOG_PATH, "{}.log".format(time.strftime('%Y%m%d')))

        # 设置日志输出格式
        self.formatter = logging.Formatter(fmt)

        # 添加日志处理器
        self._set_handlers()

    def _set_handlers(self):
        # 判断当前日志对象有没有处理器(处理日志重复打印的问题)
        if not self.logger.handlers:
            # 控制台输出
            self.con_handler = logging.StreamHandler()
            # 设置控制台输出样式
            self.con_handler.setFormatter(self.formatter)

            # 文件输出
            self.file_handler = logging.FileHandler(self.log_name, mode='a', encoding='utf-8')
            # 设置文件输入样式
            self.file_handler.setFormatter(self.formatter)

            # 添加handler到logger中
            self.logger.addHandler(self.con_handler)
            self.logger.addHandler(self.file_handler)


if __name__ == '__main__':
    logger = LogHandler().logger
    logger.info("-----开始-----")
    logger.info("-----结束-----")
