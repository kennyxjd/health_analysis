#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/14 14:17
# Author:kenny
# @File:suggestion_generate.py
import os
import pandas as pd
# from config import conf_info_of_env

class CalNameHealth:
    def __init__(self, file_path):
        self.health_name_dict = self.load_csv_name_files(file_path)

    def load_csv_name_files(self, file_path):
        health_name_dict = {}
        df = pd.read_csv(file_path, skiprows=1, encoding='utf-8')
        for _, row in df.iterrows():
            health_name_dict[row.iloc[1]] = {'name': row.iloc[0],
                                             'gender': row.iloc[2],
                                             'age': row.iloc[3],
                                             'height': row.iloc[4],
                                             'weight': row.iloc[5],
                                             'weight_status': row.iloc[6],
                                             'eye': row.iloc[7],
                                             'eye_status': row.iloc[8]}
        return health_name_dict

    def check_info(self, name):
        result = ''
        for id in self.health_name_dict.keys():
            name_temp = self.health_name_dict[id]['name']
            if name_temp == name:
                gender = self.health_name_dict[id]['gender']
                age = self.health_name_dict[id]['age']
                height = self.health_name_dict[id]['height']
                weight = self.health_name_dict[id]['weight']
                weight_status = self.health_name_dict[id]['weight_status']
                eye = self.health_name_dict[id]['eye']
                eye_status = self.health_name_dict[id]['eye_status']
                info = f"姓名：{name} 学号：{id} 性别：{gender} 年龄：{age} 身高：{height} 体重：{weight} 体重情况：{weight_status} " \
                       f"视力：{eye} 视力状态：{eye_status} \n"
                result += info
        if result == '':
            return '没有查询到该学生'
        else:
            return result

calhealthname = CalNameHealth("./data/stu_info/health_name.csv")
