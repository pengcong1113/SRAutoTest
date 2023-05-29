#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/14 09:53

Author:  彭璁
"""

# Filename： driver


import uiautomator2 as u2
from config import *
from tools.loggers import PCLogging
logger = PCLogging().getlogger()


class Driver(object):
    """初始化待测设备和其它配测设备"""
    def init_phone(self, phoneId):
        """
        Function:
            本函数用来初始化手机
        Args：
            手机serialNo.
        Returns：
            class 'uiautomator2.Device'
        """
        try:
            logger.info(phoneId)
            d = u2.connect(phoneId)
            d.implicitly_wait = wait_timeout
            d.click_post_delay = click_post_delay
            d().click_exists()
            logger.info("连接设备：{}".format(phoneId))
            return d
        except Exception as e:
            logger.info("初始化手机异常！{}".format(e))

    def init_ixchart(self):
        pass


