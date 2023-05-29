#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/14 13:21

Author:  彭璁
"""

# Filename： conftest

import pytest
import time
import base64
import subprocess
import allure
from driver import Driver
from config import *
from tools.loggers import PClogging

logger = PClogging().getlogger()


def allow(driver):
    """
    监听一些跳过和确定
    :param driver:
    :return:
    """
    driver.watcher.when("始终允许").click()


@pytest.fixture()
def driver_setup(request):
    '''实现App的打开和关闭'''
    logger.info("测试开始！")
    request.instance.driver = Driver().init_phone(phoneId)
    logger.info("进入测试APP！")
    request.instance.driver.app_start(package_name, activity, stop=True)
    allow(request.instance.driver)
    time.sleep(launch_time)
    request.instance.driver.watcher.start(1.0)

    def driver_teardown():
        logger.info("测试结束，退出测试APP！")
        request.instance.driver.app_stop(package_name)
        request.instance.driver.watcher.stop()

    request.addfinalizer(driver_teardown)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    hook pytest失败
    :param item:
    :param call:
    :return:
    """

    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        pic_info = adb_screen_shot()
        with allure.step('添加失败截图...'):
            allure.attach.file(pic_info, "失败截图", attachment_type=allure.attachment_type.PNG)


def screen_shot(driver):
    """
    截图操作
    pic_name:截图名称
    :return:
    """
    try:
        fail_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        fail_pic = str(fail_time) + "截图"
        pic_name = os.path.join(screenshot_folder, fail_pic)
        driver.screenshot("{}.png".format(pic_name))
        logger.info('截图:{}'.format(pic_name))
        f = open(pic_name, 'rb')  # 二进制方式打开图文件
        base64_str = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        f.close()
        return base64_str
    except Exception as e:
        logger.info("{}截图失败!{}".format(pic_name, e))


def adb_screen_shot():
    """
    adb截图
    :return:
    """
    fail_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    fail_pic = str(fail_time) + "截图.jpg"
    pic_name = os.path.join(screenshot_folder, fail_pic)
    cmd = 'adb shell /system/bin/screencap -p /sdcard/screenshot.jpg'
    subprocess.call(cmd, shell=True)
    cmd = 'adb pull /sdcard/screenshot.jpg {}'.format(pic_name)
    subprocess.call(cmd, shell=True)
    return pic_name

