#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/17 11:45
# Author:kenny
# @File:decoration_plan.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.health_check_app.data_check_app import calhealth
from util.decorator import fastapi_dec
from ..schemas import HealthDataInput

health_data_check = APIRouter()

@health_data_check.post("/data-check", summary="根据小朋友的性别、年龄、身高和体重，分析其健康问题，包括消瘦、正常、超重、肥胖。")
@fastapi_dec
async def health_data_check_func(request: Request, params: HealthDataInput):
    """健康问题分析

    Args:

        request: Request

        params: Input

    Returns:
    """
    age = params.age
    gender = params.gender
    height = params.height
    weight = params.weight

    message = calhealth.search_health_result(age, height, gender, weight)

    return JSONResponse(content={'health_status': message}, status_code=200)
