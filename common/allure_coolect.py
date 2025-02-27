#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-27 17:08
# @Name    : allure_coolect.py
# @Description   : 收集allure报告
# @Author  : Hunter

import json
import os
from typing import List, Text
from common.get_files_path import get_all_files
from common.enum_config import TestData

case_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report', 'html', 'data', 'test-cases')


class AllureFileHandle:
    """allure报告数据清洗"""

    @classmethod
    def get_testcase(cls) -> List:
        """获取所有allure报告中用例执行的情况"""
        files = []
        for i in get_all_files(case_path):
            with open(i, 'r', encoding='utf-8')as f:
                data = json.load(f)
                files.append(data)
        return files

    def get_failed_case(self) -> List:
        """获取所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcase():
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        return error_case

    def get_failed_cases_message(self) -> Text:
        """获取失败的测试用例相关信息"""
        data = self.get_failed_case()
        values = ""
        # 判断有失败用例，则返回内容
        if len(data) >= 1:
            values = "失败用例:\n"
            values += "      *****************\n"
            for i in data:
                values += "    " + i[0] + ":" + i[1] + "\n"
        return values

    @classmethod
    def get_case_number(cls) -> "TestData":
        """统计用例数量"""
        try:
            file_name = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report', 'html', 'widgets',
                                     'summary.json')
            with open(file_name, 'r', encoding='utf-8')as f:
                data = json.load(f)
            _case_count = data['statistic']
            _time = data['time']
            keys_dict = {"passed", "failed", "broken", "skipped", "total"}
            case_data = {k: v for k, v in data['statistic'].items() if k in keys_dict}
            # 判断运行用例数大于0
            if _case_count["total"] > 0:
                # 计算用例执行通过率
                case_data["pass_rate"] = round(
                    (_case_count["passed"] + _case_count["skipped"]) / _case_count["total"] * 100, 2
                )
            else:
                # 没有运行用例的话 成功率为0
                case_data["pass_rate"] = 0.0
            # 用例运行时长
            case_data["time"] = _time if case_data["total"] == 0 else round(_time["duration"] / 1000, 2)
            return TestData(**case_data)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "您未生成allure报告，"
                "请检查allure的环境配置"
            )from e


if __name__ == '__main__':
    data = AllureFileHandle().get_case_number()
    print(data)
