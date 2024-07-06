#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/10 16:46
# Author:kenny
# @File:logger.py

import os
import logging

# 获取当前文件的目录
current_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_path)
log_path = os.path.join(root_dir, 'log')

# 如果log文件夹不存在，创建它
if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='./log')
