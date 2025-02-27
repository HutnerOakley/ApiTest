"""
运行框架的脚本
"""

import os
import pytest
import sys
import traceback

path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(path)

from common.logger import LogHandler
from common.allure_coolect import AllureFileHandle
from common.get_config import Config
from common.send_mail_util import SendEmail


def run():
    try:
        LogHandler().logger.info(
            """
                                         _    _         _      _____         _
                          __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
                         / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
                        | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
                         \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                              |_|
                              开始执行{}项目...
                            """.format(Config.PROJECT_NAME)
        )

        pytest.main(['-vs', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                     "--alluredir", "./report/tmp", "--clean-alluredir"])
        os.system(r"allure generate ./report/tmp -o ./report/html --clean")
        allure_data = AllureFileHandle().get_case_number()
        # SendEmail(allure_data).send()
        SendEmail(allure_data).send_all_type()
    except Exception:
        e = traceback.format_exc()
        SendEmail(AllureFileHandle().get_case_number()).send_error_mail(e)
        raise


if __name__ == '__main__':
    run()
