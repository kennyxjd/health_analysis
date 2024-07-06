#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/17 11:45
# Author:kenny
# @File:decoration_plan.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.health_check_app.name_check_app import calhealthname
from util.decorator import fastapi_dec
from ..schemas import HealthNameInput

health_name_check = APIRouter()

@health_name_check.post("/name-check", summary="根据小朋友的姓名查询小朋友的健康数据。")
@fastapi_dec
async def health_name_check_func(request: Request, params: HealthNameInput):
    """健康问题分析

    Args:

        request: Request

        params: Input

    Returns:
    """
    name = params.name
    message = calhealthname.check_info(name)

    return JSONResponse(content={'health_info': message}, status_code=200)
