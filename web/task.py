#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.memory import MemoryJobStore
# from apscheduler.jobstores.redis import RedisJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.events import EVENT_JOB_MAX_INSTANCES, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import time

# client = MongoClient(host='127.0.0.1', port=27017)
# pool = redis.ConnectionPool(host='127.0.0.1', port=16379)
#
# jobstores = {'mongo': MongoDBJobStore(collection='job', database='test', client=client), 'redis': RedisJobStore(
#     connection_pool=pool), 'default': MemoryJobStore(), 'default_test': MemoryJobStore()}
#
# executors = {'default': ThreadPoolExecutor(200), 'processpool': ProcessPoolExecutor(10)}

job_defaults = {'coalesce': True, 'max_instances': 2, 'misfire_grace_time': 60}

def job():
    print('job 3s')

def job5():
    print('job 5s')

def write_to_datebase():

    file = open('../scrapy/tutorial/tutorial/spiders/mydata1.json')

    # 每天0点爬取 4点定时 增量同步文件数据到数据库
    body = []
    print('ttttt')
    time.sleep(5)
    for i in file.readlines():
        body.append(i)


sched = BackgroundScheduler(timezone='MST', job_defaults=job_defaults)
sched.add_job(write_to_datebase, 'interval', id='write_to_db', seconds=1)
# sched.add_job(job5, 'interval', id='5_second_job', seconds=5)
sched.start()
