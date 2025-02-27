#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-28 10:31
# @Name    : allure_util.py
# @Description   :  allure报告附件处理
# @Author  : Hunter


import json
import allure
from common.enum_config import AllureAnnexType


def allure_step(step: str, msg: str) -> None:
    """
    :param step: 步骤及附件名称
    :param msg: 附件内容
    :return:
    """
    with allure.step(step):
        allure.attach(
            json.dumps(str(msg), ensure_ascii=False, indent=4), step,
            allure.attachment_type.JSON
        )


def allure_attach(source: str, name: str, extend) -> None:
    """
    allure报告上传附件、图片、excel
    :param source: 文件路径
    :param name: 附件名称
    :param extend: 附件扩展名称
    :return:
    """
    # 获取上传附件的后缀
    _name = name.split(".")[-1].upper()
    _annex_type = getattr(AllureAnnexType, name, None)

    allure.attach.file(
        source=source,
        name=name,
        attachment_type=_annex_type if _annex_type is None else _annex_type.value,
        extension=extend
    )
