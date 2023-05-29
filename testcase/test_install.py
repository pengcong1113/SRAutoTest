#!/usr/bin/python
# _*_ coding: utf-8 _*_
"""
Created on 2023/1/10 20:58

Author: 彭璁
"""

# Filename: test_install.py

import pytest
import allure
from module.install import *
from tools.loggers import PCLogging

logger = PCLogging().getlogger()


@pytest.mark.usefixtures('driver_setup')
@allure.feature("安装测试")
class TestInstall:

    @pytest.fixture()
    def init_install(self, scope="class"):
        self.install = Install(self.driver)
        logger.info("初始化")
        self.base = self.install.base
        yield self.install
        logger.info("结束初始化")

    @allure.story("卸载")
    @allure.title("卸载APK")
    @allure.description("卸载测试APK")
    def test_uninstall_01(self, init_install):
        with allure.step("1. 点击忘记密码"):
            init_install.click_forget_password()
        with allure.step("2. 关闭提示"):
            init_install.click_close_adv()
        with allure.step("3. 输入密码"):
            init_install.input_password()
        with allure.step("4. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("5. 点击登录"):
            init_install.click_login()
        with allure.step("6. 关闭提示"):
            init_install.click_close_adv()
        with allure.step("7. 卸载测试APK"):
            init_install.uninstall_apk()
        assert not self.base.apk_exits(package_name), "********FAILED******测试APK卸载成功！"
        logger.info("PASS\t\tAPK卸载成功！")

    @allure.story("安装")
    @allure.title("本地安装")
    @allure.description("本地安装测试APK")
    def test_install_01(self, init_install):
        with allure.step("1、本地安装测试APK"):
            init_install.install_apk()
        assert self.base.apk_exits(package_name), "********FAILED******测试APK安装失败！"
        logger.info("PASS\t\tAPK安装成功！")

    @allure.story("登录")
    @allure.title("初次登录输入授权码后取消授权")
    @allure.description("取消授权后，退出测试APP")
    def test_login_01(self, init_install):
        with allure.step("1. 输入授权码"):
            init_install.set_auth_code()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 点击取消验证"):
            init_install.click_cancle_verifi()
        assert self.base.current_app_package() != package_name, "********FAILED******取消失败,没有退出测试APP！"
        logger.info("PASS\t\t取消验证成功，退出测试APP！")

    @allure.story("登录")
    @allure.title("初次登录输入正确授权码后进行授权")
    @allure.description("授权后，进入输入默认密码界面")
    def test_login_02(self, init_install):
        with allure.step("1. 输入授权码"):
            init_install.set_auth_code()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 点击验证"):
            init_install.click_verifi()
        assert self.base.element_exists('用户登录'), "********FAILED******验证失败！"
        logger.info("PASS\t\t验证成功，进入用户登录界面！")

    @allure.story("登录")
    @allure.title("初次登录输入默认密码后，进入强制更新密码界面")
    @allure.description("初次登录输入默认密码进入强制更新密码界面")
    def test_login_03(self, init_install):
        with allure.step("1. 输入默认密码"):
            init_install.input_default_password()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 点击确认进入强制更新密码界面"):
            init_install.click_login()
        assert self.base.elements_exist("修改密码"), "********FAILED*****登录失败！"
        logger.info("PASS\t\t验证成功，进入修改密码界面！")

    @allure.story("登录")
    @allure.title("设置新密码，再次登录需要输入更新后的密码登录")
    @allure.description("初次登录输入默认密码进入密码更改页面不勾选记住密码，点击确认进入APP")
    def test_login_04(self, init_install):
        with allure.step("1. 输入默认密码"):
            init_install.input_default_password()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 点击确认进入强制更新密码界面"):
            init_install.click_login()
        with allure.step("4. 2次输入相同新密码"):
            init_install.set_current_password()
        with allure.step("5. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("6. 点击确认进入APP"):
            init_install.click_cert()
        assert self.base.elements_exist("可连接范围内体外程控器"), "********FAILED*****登录失败！"
        logger.info("PASS\t\t验证成功，进入控制主界面！")

    @allure.story("登录")
    @allure.title("连续输错3次密码后，返回到系统界面")
    @allure.description("连续输错3次密码后，返回到系统界面")
    def test_login_05(self, init_install):
        with allure.step("1. 输入错误的密码"):
            init_install.input_default_password()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 点击确认"):
            init_install.click_login()
        with allure.step("4. 关闭错误提示"):
            init_install.click_close_adv()
        with allure.step("5. 输入错误的密码"):
            init_install.input_default_password()
        with allure.step("6. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("7. 点击确认"):
            init_install.click_login()
        with allure.step("8. 关闭错误提示"):
            init_install.click_close_adv()
        with allure.step("9. 输入错误的密码"):
            init_install.input_default_password()
        with allure.step("10. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("11. 点击确认"):
            init_install.click_login()
        # with allure.step("12. 关闭错误提示"):
        #     init_install.click_close_adv()
            self.base.wait_time(2)
        assert self.base.current_app_package() != package_name, "********FAILED******退出测试App失败！"
        logger.info("PASS\t\t退出测试APP成功！")

    @allure.story("登录")
    @allure.title("勾选记住密码,并登录")
    @allure.description("勾选记住密码后，输入已更新的密码，并登录")
    def test_login_06(self, init_install):
        with allure.step("1. 输入更新后的密码密码"):
            init_install.input_password()
        with allure.step("2. 隐藏键盘"):
            init_install.hide_keyboard()
        with allure.step("3. 勾选记住密码"):
            init_install.click_remember_password()
        with allure.step("4. 点击确认进入控制主界面"):
            init_install.click_login()
        assert self.base.elements_exist("可连接范围内体外程控器"), "********FAILED*****登录失败！"
        logger.info("PASS\t\t验证成功，进入控制主界面！")


if __name__ == '__main__':
    pytest.main(['-s', 'test_install.py::TestInstall::test_login_06'])
