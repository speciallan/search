#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

# !/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: flaskclicent.py
@time: 2019/2/19 10:34
@describe: flask_sockets 客户端
"""
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from websocket import create_connection

# websocket-client
# 通过socket路由访问
now = datetime.datetime.now()
print(now)


def send_query_webSocket():
    ws = create_connection("ws://10.10.20.21:9000/test")
    result_1 = ws.recv()  # 接收服务端发送的连接成功消息
    print(result_1)
    """
    上面recv()方法接收服务端 发送的第一条消息：ws.send(str("message test!"))  # 回传给clicent
    下面再要接收消息，必须先给服务端发送一条消息，不然服务端message = ws.receive() 的receive方法
    没有收到消息，而这里直接调用rece()方法去接收服务端消息，则会导致服务端关闭此次连接；
    底层方法介绍：Read and return a message from the stream. If `None` is returned, then
        the socket is considered closed/errored.
    虽然此次连接关闭了，但是对于客户端来说并不知情，而客户端recv()方法又是一个阻塞方式运行，所以会导致
    客户端永远阻塞在这里无法关闭，这也是flask_sockets 客户端服务端交互的一个缺点吧。
    """
    ws.send("I am test msg!")
    result = ws.recv()
    print(result)
    ws.close()
    return True


if __name__ == '__main__':
    send_query_webSocket()
