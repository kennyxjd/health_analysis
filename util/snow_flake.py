#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/11 11:07
# Author:kenny
# @File:snow_flake.py


from datetime import datetime
import threading
import socket
import struct
import os

machine_name = socket.getfqdn(socket.gethostname())
ip_machine = socket.gethostbyname(machine_name)
machine_address = struct.unpack("!L", socket.inet_aton(ip_machine))[0]
machine_address = machine_address ^ int(os.getpid())  # 使用当前运行进程和IP作为机器ID的生成条件
t_lock = threading.Lock()
machine_ID = 0  # 机器ID
data_center_ID = 0  # 数据ID
sequence = 0  # 计数从零开始
twepoch = 1288834974657  # 687888001020  # 唯一时间随机量
machine_id_bits = 5  # 机器码位数
datacenter_id_bits = 5  # 数据位数
max_machine_id = -1 ^ (-1 << machine_id_bits)  # 最大机器ID
max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)  # 最大数据ID
sequence_bits = 12  # 计数器位数，12个位用来保存计数码
machine_id_shift = sequence_bits  # 机器码数据左移位数，就是后面计数器占用的位数
datacenter_id_shift = sequence_bits + machine_id_bits
timestamp_left_shift = sequence_bits + machine_id_bits + datacenter_id_bits  # 时间戳左移动位数就是机器码+计数器总位数+数据位数
sequence_mask = -1 ^ -1 << sequence_bits  # 一微秒内可以产生计数，如果达到该值则等到下一微妙在进行生成
last_timestamp = -1  # 最后时间戳
machine_ID = machine_address & max_machine_id  # 机器ID
data_center_ID = machine_address & max_datacenter_id  # 数据ID


def get_timestamp():
    return int(datetime.now().timestamp() * 1000)


def get_next_timestamp(timestamp_input):
    timestamp = get_timestamp()
    while timestamp <= timestamp_input:
        timestamp = get_timestamp()
    return timestamp


def get_id():
    """
    线程安全的
    雪花算法，获取ID
    """
    with t_lock:
        global last_timestamp, sequence
        timestamp = get_timestamp()
        print(datetime.now())
        # print(timestamp)
        if last_timestamp == timestamp:
            # 同一微妙中生成ID
            sequence = (sequence + 1) & sequence_mask  # 用&运算计算该微秒内产生的计数是否已经到达上限
            if sequence == 0:
                # 一微妙内产生的ID计数已达上限，等待下一微妙
                timestamp = get_next_timestamp(last_timestamp)
        else:
            # 不同微秒生成ID
            sequence = 0
        if timestamp < last_timestamp:
            raise Exception("时间戳比上一次生成ID时时间戳还小，故异常")
        last_timestamp = timestamp  # 把当前时间戳保存为最后生成ID的时间戳
        id_generate = ((timestamp - twepoch) << timestamp_left_shift) | (data_center_ID << datacenter_id_shift) | (
                machine_ID << machine_id_shift) | sequence
        print(id_generate)
        return id_generate
