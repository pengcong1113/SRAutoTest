#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/14 15:42

Author:  彭璁
"""

# Filename： run

import os
import pytest
import subprocess

from tools.loggers import PCLogging

logger = PCLogging().getlogger()


def init_report():
    cmd = "allure generate result -o reports --clean"
    subprocess.call(cmd, shell=True)
    project_path = os.path.abspath(os.path.dirname(__file__))
    report_path = project_path + "/reports/" + "index.html"
    logger.info("报告地址:{}".format(report_path))


if __name__ == "__main__":
    pytest.main(["-sv", "--alluredir=result", 'testcase/'])
    init_report()

