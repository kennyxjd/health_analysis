#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/16 13:52
# Author:kenny
# @File:__init__.py.py

from pydantic import BaseModel, Field


class HealthDataInput(BaseModel):
    """
    健康分析
    """
    age: int = Field(..., description="小朋友的年龄")
    gender: str = Field(..., description="小朋友的性别，用girl或者boy表示")
    height: int = Field(..., description="小朋友的身高，单位为厘米或者cm")
    weight: float = Field(..., description="小朋友体重，单位为公斤或者kg")

class HealthNameInput(BaseModel):
    name: str = Field(..., description="小朋友的姓名")

class GenerateInput(BaseModel):
    text: str = Field(..., description="生成的文案")
    model: str = Field("gpt-4", description="使用的GPT模型版本")


class Output(BaseModel):
    """
    输出
    """

    code: int = Field(200, description="状态码")
    data: GenerateInput = Field(..., description="生成的文案")
    success: bool = Field(True, description="是否成功")
    timestampDate: str = Field(..., description="时间戳")
