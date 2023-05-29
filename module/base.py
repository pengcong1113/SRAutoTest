#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/31 10:44

Author:  彭璁
"""

# Filename： base.py

import re
import time
from PIL import Image
from tools.loggers import PCLogging
logger = PCLogging().getlogger()


class Base:
    """
    封装App常用操作
    """
    def __init__(self, driver):
        self.d = driver
        self.width = self.get_window_size()[0]
        self.height = self.get_window_size()[1]

    def __find_element(self, element):
        """
        查找元素，目前实现 resourceID，text，以及xpath 3种方式，后续有需要可以拓展
        目前Uiautomator2支持以下种类的关键字参数:text（已实现）, textContains, textMatches, textStartsWith
        className, classNameMatches
        description, descriptionContains, descriptionMatches, descriptionStartsWith
        checkable, checked
        clickable, longClickable
        scrollable, enabled,focusable, focused, selected
        packageName, packageNameMatches
        resourceId（已实现）, resourceIdMatches
        index, instance
        """
        # 查找元素前等待，使页面加载完成，防止执行太快而定位不到元素或者过早的定位到元素
        time.sleep(3)
        if str(element).startswith("com"):
            elem = self.d(resourceId=element)
            logger.info("通过 resourceId 查找元素:【{}】".format(str(element)))
            return elem
        elif re.findall("//", str(element)):
            elem = self.d.xpath(element)
            logger.info("通过 xpath 查找元素:【{}】".format(str(element)))
            return elem
        else:
            elem = self.d(text=element)
            logger.info("通过 text 查找元素:【{}】".format(str(element)))
            return elem

    def find(self, element):
        """
        通过 text，resourceId 以及 xpath 方式查找元素
        return：True or False
        """
        ele = self.__find_element(element)
        if not ele.exists:
            logger.info("元素[{}]未找到".format(str(element)))
        else:
            logger.info("元素已找到")
            return ele

    def set_text(self, element, text):
        logger.info("找到【[{0}】 查找元素并输入【{1}】".format(str(element), str(text)))
        return self.find(element).set_text(text)

    def get_text(self, element):
        s = self.find(element).info.get("text")
        logger.info("根据元素获取到对应的text：【{}】".format(s))
        return s

    def element_exists(self, element):
        """
        通过 text，resourceId 以及 xpath 方式查找元素
        return：True or False
        """
        ele = self.__find_element(element)
        # 判断是否通过xpath来查找，如果是xpath 调用exists 返回的是 bool类型
        if re.findall("//", str(element)):
            if not ele.exists:
                logger.info("元素[{}]未找到".format(str(element)))
            else:
                logger.info("元素已找到")
                return ele.exists
        # 如果不是xpath来查找，调用exists()方法，返回的是bool类型，而exists返回的是 uiautomator2.utils.Exists
        else:
            if not ele.exists():
                logger.info("元素[{}]未找到".format(str(element)))
            else:
                logger.info("元素已找到")
                return ele.exists()

    def click(self, element):
        """
        元素点击
        element:元素名称
        :return:
        """
        self.find(element).click(timeout=20)
        logger.info("点击元素:[{}]".format(element))

    def click_advance(self, element_list):
        """
        根据绝对坐标点击 包含坐标和坐标描述
        例：{"location":(0.848, 0.91),"description":"修改"}
        :param element_list:
        :return:
        """
        x = element_list[0]
        y = element_list[1]
        self.d.click(x, y)
        logger.info("点击坐标[{}]".format(element_list))

    def send_keys(self, element, sendtext):
        """
        文本输入
        element:元素名称
        sendtext:输入的文案
        :return:
        """
        self.find(element).set_text(sendtext)
        logger.info("输入文字[{}]".format(sendtext))

    def long_click(self, element):
        """
        长按
        element
        :return:
        """
        self.find(element).long_click()
        logger.info("长按元素:[{}]".format(element))

    def get_window_size(self):
        """
        获取屏幕尺寸
        :return:
        """
        window_size = self.d.window_size()
        width = int(window_size[0])
        height = int(window_size[1])
        return width, height

    def swipe_up(self, duration=0.5):
        """
        向上滑动,查看下面的内容
        :return:
        """
        self.d.drag(self.width / 2, self.height * 3 / 4, self.width / 2, self.height / 4, duration)
        logger.info("向上滑动")

    def swipe_down(self, duration=0.5):
        """
        向下滑动，查看上面的内容
        :return:
        """
        self.d.drag(self.width / 2, self.height / 4, self.width / 2, self.height * 3 / 4, duration)
        logger.info("向下滑动")

    def swipe_ext(self, direction, scale=0.9):
        """
        :param direction 向任意方向滑动，right left up down
        :param scale 滑动距离为屏幕宽度/高度的90%
        :return:
        """
        self.d.swipe_ext(direction, scale)
        logger.info("direction:[{0}], scale:[{1}]".format(direction, scale))

    def element_direction_swipe(self, direction, element):
        """
        将元素按方向滑动
        :param direction: 方向 right left up down
        :param element:  元素
        :param steps:  1 steps is about 5ms, so 20 steps is about 0.1s
        :return:
        """
        self.find(element).swipe(direction)
        logger.info("向[{}]滑动".format(direction))

    def swipe_to_element(self, element1, element2, duration=0.25):
        """
        滑动到某个元素
        :param element1: 起始元素
        :param element2: 目标元素
        :param duration: 滑动时间
        :return:
        """
        self.d(text=element1).drag_to(text=element2, duration=duration)
        logger.info("拖动元素[{}]至元素[{}]处".format(element1, element2))

    def swipe_down_element(self, element):
        """
        向下滑动到某个元素
        :return:
        """
        # is_find = False
        max_count = 5
        while max_count > 0:
            if self.find_elements(element):
                logger.info("向下滑动到:[{}]".format(element))
            else:
                self.swipe_down()
                max_count -= 1
                logger.info("向下滑动")

    def swipe_up_element(self, element):
        """
        向上滑动到某个元素
        :return:
        """
        # is_find = False
        max_count = 10
        while max_count > 0:
            if self.find_elements(element):
                logger.info("向上滑动到:[{}]".format(element))
            else:
                self.swipe_up()
                max_count -= 1
                logger.info("向上滑动")

    def back(self):
        """
        模拟物理键返回
        :return:
        """
        self.d.press("back")
        logger.info("点击返回")

    def toast_show(self, text, duration=5):
        """
        页面出现弹窗提示时间，默认时间5s
        :param text:弹窗内容
        :param duration:弹窗提示时间
        :return:
        """
        self.d.toast.show(text, duration)
        logger.info("展示文字")

    def wait_element_appear(self, element, timeout=5):
        """
        等待某个元素出现，默认等待时间5s
        :param element: 元素内容
        :param timeout:超时时间
        :return:
        """
        self.find(element).wait(timeout=timeout)
        logger.info("等待[{}]元素出现".format(str(element)))

    def wait_element_gone(self, element, timeout=120):
        """
        等待某个元素消失，默认等待时间120s
        :param element: 元素内容
        :param timeout:超时时间
        :return:
        """
        self.find(element).wait_gone(timeout=timeout)
        logger.info("等待[{}]元素消失".format(str(element)))

    def find_elements(self, element, timeout=5):
        """
        查找元素是否存在当前页面
        :param element: 元素内容
        :param timeout:log元素内容
        :return:
        """
        is_exist = False
        try:
            while timeout > 0:
                xml = self.d.dump_hierarchy()
                if re.findall(element, xml):
                    is_exist = True
                    logger.info("查询到[{}]".format(element))
                    break
                else:
                    timeout -= 1
        except Exception as e:
            logger.info("[{}]查找失败![{}]".format(element, e))
        finally:
            return is_exist

    def elements_exist(self, element):
        """
        判断当前界面元素【通过text方式实现】是否存在
        :param element:
        :return:
        """
        is_exist = False
        if self.d(text=element).exists(timeout=5):
            is_exist = True
        return is_exist

    def assert_exist(self, element):
        """
        断言当前页面存在要查找的元素,存在则判断成功
        wait Settings appear in 5s, same as .wait(3)
        :param element:
        :return:
        """
        assert self.d(text=element).exists(timeout=5) == True, "断言[{}]元素存在,失败了!".format(element)
        logger.info("断言[{}]元素存在,成功了!".format(element))

    def assert_not_exist(self, element):
        """
        假设九秒走满 还没有找到这个页面有这个元素 判断这个页面元素不存在
        wait Settings appear in 3s, same as .wait(3)
        :param element:
        :return:
        """
        start_time = time.time()
        self.d(text=element).exists(timeout=10)
        end_time = time.time()
        assert (end_time - start_time > 9) == True, "断言[{}]元素不存在,失败了!".format(element)
        logger.info("断言[{}]元素不存在,成功了!".format(element))

    def assert_contain_text(self, localtion, element):
        """
        断言页面的某个位置是否含有该文字
        :param localtion: 直接是x,y 坐标
        :param element:
        :return:
        """
        element_details = self.d(localtion).info
        assert element == element_details["text"], "断言[{}]位置没有[{}]元素失败!".format(localtion, element)
        logger.info("断言[{}]位置存在[{}]元素成功!".format(localtion, element))

    def wait_time(self, timeout=2):
        time.sleep(timeout)

    def screenshot(self, element):
        """
        截取元素的图片

        :param element:
        :return:Image
        """
        return self.find(element).screenshot()

    def install_apk(self, install_cmd):
        """
        安装apk
        :return:
        """
        _info = self.d.shell(install_cmd).output
        assert _info == 'Success\n', "安装失败[{}]".format(_info)
        logger.info("安装成功[{}]".format(_info))

    def uninstall_apk(self, uninstall_cmd):
        """
        卸载apk
        :param uninstall_cmd:
        :return:
        """
        _info = self.d.shell(uninstall_cmd).output
        assert _info == 'Success\n', "卸载失败[{}]".format(_info)
        logger.info("卸载成功[{}]".format(_info))

    def apk_exits(self, package_name):
        """
        查看测试apk是否存在
        :return: True or False
        """
        return package_name in self.d.app_list()

    def current_app_package(self):
        """
        获取当前运行的package
        :return:
        """
        return self.d.app_current().get('package')