#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Created on 2022/12/13 17:08

Author:  彭璁
"""

# Filename： loggers

import os
import socket
import logging
from logging.handlers import TimedRotatingFileHandler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PCLogging(metaclass=Singleton):
    """
    PCLogging是一个单例类，用于初始化、配置和获取logger实例。

    Attributes:
    -----------
    logger : logger实例
    """

    def __init__(self, log_path='logs', log_level=logging.INFO, log_format=None,
                 log_date_format='%Y-%m-%d %H:%M:%S', log_file_name='system.log',
                 log_file_split='midnight', log_file_backup_count=10):
        """
        初始化logger实例。

        Arguments:
        ----------
        log_path : str
            log文件存放路径，默认为'logs'
        log_level : int
            log的级别，默认为logging.INFO
        log_format : str
            log的格式，默认为'[%(asctime)s] [%(levelname)s] [%(hostname)s] [%(module)s.py - line:%(lineno)d] %(message)s'
        log_date_format : str
            log的时间格式，默认为'%Y-%m-%d %H:%M:%S'
        log_file_name : str
            log文件的名称，默认为'system.log'
        log_file_split : str
            log文件的切分方式，可选值为midnight或S（按大小切分），默认为'midnight'
        log_file_backup_count : int
            log文件的备份数量，默认为10
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # 如果没有指定log_format，则使用默认格式
        if not log_format:
            hostname = socket.gethostname()
            log_format = '[%(asctime)s] [%(levelname)s] [%(hostname)s] [%(module)s.py - line:%(lineno)d] %(message)s'

        # 拼接log文件路径并创建目录
        log_file = os.path.join(log_path, log_file_name)
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # 配置log文件的handler
        file_handler = TimedRotatingFileHandler(log_file,
                                                when=log_file_split,
                                                backupCount=log_file_backup_count,
                                                encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(log_format, log_date_format))
        self.logger.addHandler(file_handler)

    @staticmethod
    def get_logger(name=None):
        """
        获取logger实例。

        Arguments:
        ----------
        name : str
            logger实例的名称，如果为None则返回默认的logger实例

        Returns:
        --------
        logger : logger实例
        """
        return logging.getLogger(name) if name else PCLogging().logger
