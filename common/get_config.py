#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-28 14:29
# @Name    : get_config.py
# @Description   :  获取配置文件的数据
# @Author  : Hunter

import os
from common.yaml_operate import YamlUtil

_data = YamlUtil(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'config.yaml')).get_yaml_data()


class Config:
    PROJECT_NAME = _data.get("project_name")
    HOST = _data.get("host")
    DB = _data.get("db")
    SEND_USER = _data.get("email").get("send_user")
    EMAIL_HOST = _data.get("email").get("email_host")
    PORT = _data.get("email").get("port")
    RECE_USER = _data.get("email").get("rece_users")


if __name__ == '__main__':
    name = Config.PROJECT_NAME
    RECE_USER = Config.RECE_USER
    print(RECE_USER,type(RECE_USER))
    print(Config.PORT,type(Config.PORT))
    print(Config.EMAIL_HOST,type(Config.EMAIL_HOST))