#!/usr/bin/python
# _*_ coding: utf-8 _*_
"""
Created on 2023/1/10 11:09

Author: 彭璁
"""

# Filenema: install.py

from module.base import Base
from tools.loggers import PCLogging
from config import *

logger = PCLogging().getlogger()

_d = {
    "授权码": "com.sceneray.dbs:id/auth_edit",
    "取消": "com.sceneray.dbs:id/btn_no",
    "验证": "com.sceneray.dbs:id/btn_yes",
    "收键盘1": "com.android.systemui:id/back",
    "密码": "com.sceneray.dbs:id/et_pwd",
    "收键盘2": "com.huawei.secime:id/keyboard_hide_btn",
    "登录": "com.sceneray.dbs:id/btn_login",
    "修改密码": "com.sceneray.dbs:id/etPassword",
    "确认修改": "com.sceneray.dbs:id/etConfirmPassword",
    "记住密码": "com.sceneray.dbs:id/tvRememberPassword",
    "确定": "com.sceneray.dbs:id/tvOk",
    "忘记密码？": "com.sceneray.dbs:id/tvForgetPassword",
    "关闭重置提示框": "com.sceneray.dbs:id/img_close"
}


class Install(Base):
    def __init__(self, driver):
        self.base = Base(driver)

    def install_apk(self):
        return self.base.install_apk(install_cmd)

    def uninstall_apk(self):
        return self.base.uninstall_apk(uninstall_cmd)

    def set_auth_code(self):
        return self.base.set_text(_d['授权码'], auth_code)

    def click_verifi(self):
        return self.base.click(_d['验证'])

    def click_cancle_verifi(self):
        return self.base.click(_d['取消'])

    def hide_keyboard(self):
        if self.base.element_exists(_d['收键盘1']):
            return self.base.click(_d['收键盘1'])
        else:
            return self.base.click(_d['收键盘2'])

    def input_default_password(self):
        return self.base.set_text(_d['密码'], default_password)

    def input_password(self):
        return self.base.set_text(_d['密码'], password)

    def click_login(self):
        return self.base.click(_d['登录'])

    def set_current_password(self):
        s1 = self.base.set_text(_d['修改密码'], password)
        s2 = self.base.set_text(_d['确认修改'], password)
        return s1, s2

    def click_remember_password(self):
        return self.base.click(_d['记住密码'])

    def click_cert(self):
        return self.base.click(_d['确定'])

    def app_exist(self):
        return self.base.apk_exits(package_name)

    def click_forget_password(self):
        return self.base.click(_d['忘记密码？'])

    def click_close_adv(self):
        return self.base.click(_d['关闭重置提示框'])

