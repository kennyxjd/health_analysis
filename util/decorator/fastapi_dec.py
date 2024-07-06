#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/11 14:55
# Author:kenny
# @File:fastapi.py

import datetime
import json
import time
import uuid
from functools import wraps
from util import beijing_tz

from fastapi import Request
from fastapi.responses import JSONResponse
import os
import logging
from util.verification_key import verify_key_of_allowed


# 获取当前文件的目录
current_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_path))
log_dir = os.path.join(root_dir, 'log')

# 如果log文件夹不存在，创建它
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_path = os.path.join(log_dir, 'health.txt')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=log_path)


"""
FastAPI专用
"""


def fastapi_dec(func):
    """记录接口的入参出参和处理时间等信息
    """

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        task_id = str(uuid.uuid4())
        try:
            time_st = str(datetime.datetime.now(beijing_tz))
            t0 = time.time()

            # 获取请求入参信息
            try:
                request_path = request.url.path
                request_body = await request.json()  # 获取请求参数
            except:
                request_path = func.__name__
                request_body = {}

            # 从接口调用的都要验证用户key，不在白名单的不允许调用
            allow_type = verify_key_of_allowed(request_body.get("user_key")) if request_body.get("user_key") else False
            if not allow_type:
                return JSONResponse(
                    content={"message": "type is not allow, please check it or contact admin!", "code": 401},
                    status_code=401)
            pre_info = {"task_id": task_id, "request_path": request_path, "request_body": request_body}
            logging.info(f"request info: {pre_info}")
            # 调用原始函数并获取返回结果
            response = await func(request, *args, **kwargs)
            all_cost_time = time.time() - t0
            # 检查返回结果是否为 JSONResponse
            if isinstance(response, JSONResponse):
                response_content = json.loads(response.body)
            else:
                response_content = response
            time_end = str(datetime.datetime.now(beijing_tz))

            # 记录接口的入参、出参和处理时间等信息
            post_info = {"task_id": task_id, "request_path": request_path, "request_body": request_body,
                         "response_content": response_content, "response_time": all_cost_time,
                         "start_time": time_st, "end_time": time_end}
            logging.info(f"response info: {post_info}")
            return response
        except Exception as e:
            logging.error(f"task id: {task_id}, error info: {e}")
            return JSONResponse(content={"message": str(e), "code": 500}, status_code=500)

    return wrapper
