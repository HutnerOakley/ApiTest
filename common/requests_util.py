#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-01-24 16:10
# @Name    : requests_util.py
# @Description   : 请求统一封装
# @Author  : Hunter

import requests
import json as js
from common.logger_decorator import log_decorator
from common.get_config import Config


class HttpRequest(object):

    def __init__(self, url=Config.HOST):
        self.url = url
        self.session = requests.session()

    def get(self, url, **kwargs):
        return self.send_request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.send_request(url, 'POST', data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.send_request(url, "PUT", data, **kwargs)

    def delete(self, url, **kwargs):
        return self.send_request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.send_request(url, "PATCH", data, **kwargs)

    @log_decorator(switch=True)
    def send_request(self, uri, method, data=None, json=None, **kwargs):
        url = self.url + uri
        method = str(method).lower()
        if method == 'get':
            return self.session.get(url, **kwargs)
        if method == 'post':
            return self.session.post(url, data, json, **kwargs)
        if method == 'put':
            # put请求中没有json参数，需要用data传参
            if json:
                data = js.dumps(json)
            return self.session.put(url, data, **kwargs)
        if method == 'delete':
            return self.session.delete(url, **kwargs)
        if method == 'patch':
            if json:
                data = js.dumps(json)
            return self.session.patch(url, data, **kwargs)


if __name__ == '__main__':
    params = {
        "sys_version": "V8-T652T01-LF1V426",
        "mac": "00:30:1b:ba:02:db",
        "app_version": "7590",
        "client_type": "TCL-CN-MT9652-T7G",
        "dnum": "603779331"

    }
    res_obj = HttpRequest("https://test.launcher.tcloudfamily.com").get(url="/api/v2/waterfall/getLogo", params=params)
    # res_obj = HttpRequest().send_request("tpl/machinetab/getAuthTab","GET")
    print(res_obj.url)
