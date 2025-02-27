#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-28 11:35
# @Name    : send_mail_util.py
# @Description   : 发送邮件
# @Author  : Hunter

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from common.allure_coolect import TestData, AllureFileHandle
from common.get_config import Config
from common.get_files_path import replace_html


class SendEmail:

    def __init__(self, target: TestData):
        self.target = target
        self.rece_email = Config.RECE_USER
        self.rece_list = self.rece_email.split(",")
        self.allure_data = AllureFileHandle()
        self.case_message = self.allure_data.get_failed_cases_message()

    @classmethod
    def send_mail(cls, user_mail: list, sub, content: str, body_html: str = None, attachments: list = None) -> None:
        """
        发送各种类型格式的邮件
        :param user_mail: 收件人邮箱
        :param sub: 邮件主题
        :param content: 邮件文本正文
        :param body_html: html正文
        :param attachments: 附件的路径列表
        :return:
        """
        user = "quan3.gan" + "<" + Config.SEND_USER + ">"

        msg = MIMEMultipart('mixed')
        msg['Subject'] = sub
        msg['From'] = user
        msg['TO'] = ";".join(user_mail)

        # 如果需要发送纯文本和html内容，则创建一个alternative MIME类型的对象
        if content or body_html:
            msg_alt = MIMEMultipart("alternative")
            msg.attach(msg_alt)

            # 添加文本正文
            if content:
                text_part = MIMEText(content,"plain")
                msg_alt.attach(text_part)

            # 添加html正文
            if body_html:
                html_part = MIMEText(body_html,"html")
                msg_alt.attach(html_part)

        # 添加附件
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb')as f:
                    # 创建一个MIMEBase对象，用于附件
                    file_part = MIMEBase('application','octet-stream')
                    file_part.set_payload(f.read())
                    encoders.encode_base64(file_part)  # 对附件内容进行base64编码
                    file_part.add_header(f'Content-Disposition',f'attachment;file_name="{attachment}"')
                    msg.attach(file_part)

        server = smtplib.SMTP(Config.EMAIL_HOST, Config.PORT)
        server.starttls()
        server.login(Config.SEND_USER, "qwer123321..")
        server.sendmail(user, user_mail, msg.as_string())
        server.close()

    def send_error_mail(self, error_message: str) -> None:
        """
        异常邮件通知
        :param error_message:
        :return:
        """
        sub = Config.PROJECT_NAME + "接口自动化执行异常通知"
        content = f"自动化测试执行完毕，程序中发现异常，请悉知。报错信息如下：\n{error_message}"
        self.send_mail(self.rece_list, sub, content)

    def send(self) -> None:
        """
        发送纯文本邮件
        :return:
        """
        # 收件人邮箱
        sub = Config.PROJECT_NAME + "接口自动化报告"
        content = f"""
        各位同事, 大家好:
            自动化用例执行完成，执行结果如下:
            用例运行总数: {self.target.total} 个
            通过用例个数: {self.target.passed} 个
            失败用例个数: {self.target.failed} 个
            异常用例个数: {self.target.broken} 个
            跳过用例个数: {self.target.skipped} 个
            成  功   率: {self.target.pass_rate} %{self.case_message}
        """
        self.send_mail(self.rece_list, sub, content)

    def send_all_type(self):
        """
        发送全量邮件
        :return:
        """
        sub = Config.PROJECT_NAME + "接口自动化报告"
        data = {
            "time": self.target.time,
            "total": self.target.total,
            "passed": self.target.passed,
            "failed": self.target.failed,
            "skipped": self.target.skipped,
            "broken": self.target.broken,
            "pass_tate": self.target.pass_rate
        }
        htm_out = replace_html(data)
        content = """
        各位同事，大家好！
            自动化测试执行完成，以下为本次自动化测试报告概览内容，请注意查收~
            更详细的测试报告，见附件
            谢谢！
        """
        self.send_mail(user_mail=self.rece_list, sub=sub, content=content, body_html=htm_out)


if __name__ == '__main__':
    # SendEmail(AllureFileHandle().get_case_number()).send()
    SendEmail(AllureFileHandle.get_case_number()).send_all_type()
