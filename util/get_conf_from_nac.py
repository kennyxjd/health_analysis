#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/13 20:03
# Author:kenny
# @File:get_conf_from_nac.py

import ast
import os



def get_conf_info_from_nac(nac_space):
    """

    :param nac_space: nac命名空间
    :return:
    """
    get_conf_ins = GetConfInfo()  # 获取nac配置信息
    conf_info_in_nac = ast.literal_eval(get_conf_ins.get_conf_info(nac_space))  # 获取nac中的配置信息
    return conf_info_in_nac


def get_field():
    """根据log env记录的值，获取不同环境的配置参数

    :return:
    """
    field = "ENV-DEV"
    log_env_path = os.path.join(os.getcwd(), "logenv")
    if not os.path.exists(log_env_path):
        # log env路径不存在，返回dev配置
        return field
    with open(log_env_path) as f:
        content_log = f.read()
        content_split = content_log.split('/')
    content_split = str(content_split).lower()
    if 'test' in content_split:
        field = "ENV-TEST"
    elif 'uat' in content_split:
        field = "ENV-UAT"
    elif 'prod' in content_split:
        field = "ENV-PROD"
    return field
