#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/14 21:26

Author:  彭璁
"""

# Filename： config


import os

package_name = 'com.sceneray.dbs'
activity = 'com.sceneray.dbs.modules.splash.ActSplash'
phoneId = 'UPK9X20C23001241'
wait_timeout = 20
click_post_delay = 0.5
device_name = ""
launch_time = 3
install_cmd = "pm install -g /data/local/tmp/SR1620_2.0.0_17731_release_20230105112826.apk"
uninstall_cmd = "pm uninstall com.sceneray.dbs"
auth_code = 'A89DCB45'
default_password = '123456'
password = 'sr@123456'
WLC = '8110P01950'
IPG = ''

current_path = os.path.abspath(os.path.dirname(__file__))
screenshot_folder = os.path.join(current_path, "screenshot")
if not os.path.exists(screenshot_folder):
    os.mkdir(screenshot_folder)
    print("创建截图目录：{}".format(screenshot_folder))
