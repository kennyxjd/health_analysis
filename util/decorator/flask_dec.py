#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/11 14:56
# Author:kenny
# @File:flask.py

import datetime
import time
import uuid
from functools import wraps

from flask import request
from util.verification_key import verify_key_of_allowed

"""
Flask专用
"""


def flask_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = Logger()
        task_id = str(uuid.uuid4())
        try:
            time_st = str(datetime.datetime.now())
            t0 = time.time()
            router_name = request.url  # 获取名称
            param_content = request.args
            if not param_content:
                param_content = ""
            req_content = param_content.to_dict()
            # 获取请求参数, 并判断是否符合要求
            type_input = req_content.get("type")
            res_type_judge = verify_key_of_allowed(type_input)
            if not res_type_judge:
                return {"message": "type is not allow, please check it or contact admin!"}
            pre_info = {"task_id": task_id, "router_name": router_name, "param_content": param_content}
            logger.info(f"request info: {pre_info}")
            # 调用原始函数并获取返回结果
            response = func(*args, **kwargs)
            all_cost_time = time.time() - t0
            time_end = str(datetime.datetime.now())
            post_info = {"task_id": task_id, "router_name": router_name, "param_content": param_content,
                         "response_content": response, "response_time": all_cost_time,
                         "start_time": time_st, "end_time": time_end}
            logger.info(f"response info: {post_info}")
            return response
        except Exception as e:
            logger.error(f"task id: {task_id}, error info: {e}")
            return {"message": "error"}

    return wrapper
