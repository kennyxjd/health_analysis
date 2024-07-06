#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/14 13:52
# Author:kenny
# @File:__init__.py.py

from .routers.data_check import health_data_check
from .routers.name_check import health_name_check

__all__ = ["health_data_check", "health_name_check"]
