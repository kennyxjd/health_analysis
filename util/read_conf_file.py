#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/10 15:12
# Author:kenny
# @File:read_conf_file.py

import configparser
import os
from util.logger import Logger


class GetConfInfoFromINI:
    """获取配置文件中的信息, 当前仅支持ini格式的配置文件
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式

        :param args:
        :param kwargs:
        """
        if not cls.__instance:
            cls.__instance = super(GetConfInfoFromINI, cls).__new__(cls)
        return cls.__instance

    def __init__(self, dir_path=None, file_name=None):
        self.conf = configparser.RawConfigParser()
        path_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.conf_path = os.path.join(path_file, dir_path, file_name)
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("配置文件不存在")
        self.conf.read(self.conf_path)
        self.env_value = os.getenv("ENV")  # 获取环境变量
        Logger().logger.info(f"当前环境变量为：{self.env_value}")
        self.field = self.get_field()

    def get_field(self):
        """根据环境变量ENV记录的值，获取不同环境的配置参数

        :return:
        """
        field = "ENV-DEV"
        if not self.env_value:
            return field
        content_split = str(self.env_value).lower()
        if 'test' in content_split:
            field = "ENV-TEST"
        elif 'uat' in content_split:
            field = "ENV-UAT"
        elif 'prod' in content_split:
            field = "ENV-PROD"
        return field

    def get_conf_info(self, key):
        """获取key对应的配置信息

        :param key:
        :return:
        """
        conf_info = self.conf.get(self.field, key)
        return conf_info
