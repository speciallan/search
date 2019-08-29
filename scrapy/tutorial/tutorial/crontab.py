#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import time
import os
import sched
from scrapy import cmdline

# while True:
#   os.system("scrapy crawl News")
#   time.sleep(86400) #每隔一天运行一次 24*60*60=86400s或者，使用标准库的sched模块

# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
# schedule = sched.scheduler(time.time, time.sleep)


def test():

    schedule = sched.scheduler( time.time,time.sleep)

    def func(string1):
        print("now excuted func is %s"%string1)

    while True:
        print("now excuted func is 1")
        time.sleep(2)
    print("start")
    schedule.enter(2,0,func,(1,))
    schedule.enter(2,0,func,(2,))
    schedule.enter(3,0,func,(3,))
    schedule.enter(4,0,func,(4,))
    schedule.enter(6,0,func,(6,))
    schedule.run()

    print("end")

# 被周期性调度触发的函数
def func():
    os.system("scrapy crawl comment")
    # cmdline.execute("scrapy crawl comment".split())


def perform1(inc):
    schedule.enter(inc,0,perform1,(inc,))
    func()  # 需要周期执行的函数


def mymain():
    schedule.enter(0,0,perform1,(86400,))


if __name__=="__main__":

    test()
    # mymain()
    # schedule.run() # 开始运行，直到计划时间队列变成空为止关于cmd的实现方法，本人在单次执行爬虫程序时使用的是


