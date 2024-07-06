#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/10 13:30
# Author:kenny
# @File:main.py

import uvicorn
from fastapi import FastAPI

from api.health_check import health_data_check, health_name_check

app = FastAPI(summary="幼儿健康咨询服务", version="0.1.0", title="幼儿健康咨询服务")


# 注册路由
app.include_router(health_data_check, prefix="/health-check")  #
app.include_router(health_name_check, prefix="/health-check")  #


# @app.get("/health-check")
# def health_check():
#     """健康检查"""
#     return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # 启动服务
