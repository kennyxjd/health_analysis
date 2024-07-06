#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/6/6 11:57
# Author:kenny
# @File:merge_dict_by_same_key.py

# def merge_dicts(dict1, dict2):
#     """
#     合并两个字典，将dict2中的键值对添加到dict1中。
#     如果存在相同的键，dict2的值将覆盖dict1的值。
#     """
#     merged = dict1.copy()  # 创建dict1的副本
#     merged.update(dict2)  # 使用dict2更新副本
#     return merged
#
#
# def merge_lists_by_same_key(list_1, list_2, key_name):
#     """
#     合并两个列表中的字典，基于字典中的line_no值。
#     """
#     merged_list = []  # 用于存储合并后的结果
#     line_no_dict = {}  # 用于跟踪每个line_no的合并结果
#
#     # 将list_1中的字典添加到line_no_dict中
#     for item in list_1:
#         line_no = item.get(key_name)
#         if line_no is not None:
#             line_no_dict[line_no] = item
#
#     # 将list_2中的字典添加到line_no_dict中，如果line_no相同则进行合并
#     for item in list_2:
#         line_no = item.get(key_name)
#         if line_no is not None:
#             if line_no in line_no_dict:
#                 line_no_dict[line_no] = merge_dicts(line_no_dict[line_no], item)
#             else:
#                 line_no_dict[line_no] = item
#
#     # 将合并后的字典添加到结果列表中
#     merged_list = list(line_no_dict.values())
#
#     return merged_list
def merge_lists_by_same_key_value(list_1, list_2, key_name):
    """
    合并两个列表中的字典，基于字典中的相同的key值。
    """
    # 创建一个字典，用line_no作为键，字典本身作为值
    line_no_dict = {item[key_name]: item for item in list_1}

    for item in list_2:
        line_no = item[key_name]
        if line_no in line_no_dict:
            line_no_dict[line_no].update(item)
        else:
            line_no_dict[line_no] = item

    # 将合并后的字典转换为列表
    merged_list = list(line_no_dict.values())

    return merged_list
