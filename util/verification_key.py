#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/14 17:41
# Author:kenny
# @File:type_allowed.py


"""
判断用户key, 通过Nacos获取配置信息
"""


def verify_key_of_allowed(type_value):
    """验证key

    :param type_value:
    :return:
    """
    if not type_value:
        return False
    # allow_type_list = get_conf_of_user_key()
    allow_type_list = ['ctw']
    if type_value not in allow_type_list:
        return False
    return True

#
# def get_conf_of_user_key():
#     """获取key配置信息
#
#     :return:
#     """
#     yaml_cfg = conf_info_of_common.get("user_key")
#     return yaml_cfg
