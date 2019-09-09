#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.memory import MemoryJobStore
# from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.events import EVENT_JOB_MAX_INSTANCES, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from scrapy import cmdline
import time
import json


class ScheduleFactory(object):
    """单例工厂"""

    _scheduler = None

    @staticmethod
    def new_instance():
        # pool = redis.ConnectionPool(
        #     host='10.94.99.56',
        #     port=6379,
        # )
        # r = redis.StrictRedis(connection_pool=pool)
        jobstores = {
            # 'redis': RedisJobStore(2, r),
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
        }
        executors = {
            'default': ThreadPoolExecutor(max_workers=10),
            'processpool': ProcessPoolExecutor(max_workers=10)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': 3600
        }
        # scheduler = BackgroundScheduler(timezone='MST', jobstores=jobstores, executors=executors, job_defaults=job_defaults, daemonic=False)
        scheduler = BackgroundScheduler(timezone='MST', job_defaults=job_defaults)
        return scheduler

    @staticmethod
    def get_instance():
        if not __class__._scheduler:
            __class__._scheduler = __class__.new_instance()
        return __class__._scheduler

def job():
    print('job 3s')

def job5():
    print('job 5s')

def scheduler_lock(name, state):
    file = open('../scrapy/tutorial/tutorial/spiders/scheduler.lock', 'w')

def crawl_to_file():
    import os
    os.system('cd ../scrapy/tutorial/tutorial/spiders && scrapy crawl comment_task')
    # cmdline.execute('scrapy crawl comment_task'.split())
    print('爬取数据完毕')

def write_to_datebase():

    file = open('../scrapy/tutorial/tutorial/spiders/mydata1.json', 'r')

    # 每天0点爬取 4点定时 增量同步文件数据到数据库
    body = []
    for i in file.readlines():
        body.append(i)

    from search.web.server import db
    from search.web.apps.admin.models import Comment

    if len(body) == 0:
        return False

    for k,v in enumerate(body):
        item = json.loads(v)
        comment_time = time.mktime(time.strptime(item['time'], "%Y-%m-%d %H:%M"))
        insert = Comment(item['crawler_id'], item['username'], item['content'], comment_time, item['star'], item['is_member'])
        db.session.add(insert)
    db.session.commit()

    # 删除所有本地记录
    file = open('../scrapy/tutorial/tutorial/spiders/mydata1.json', 'w')
    file.write('')
    file.close()
    print('写到数据库完毕')

    return True


sched = ScheduleFactory.get_instance()
# sched.add_job(crawl_to_file, trigger='interval', id='crawl_to_file', seconds=3)
# sched.add_job(write_to_datebase, trigger='interval', id='write_to_db', seconds=1)
sched.add_job(crawl_to_file, trigger='cron', id='crawl_to_file_cron', day_of_week='*', hour=0, minute=0)
sched.add_job(write_to_datebase, trigger='cron', id='write_to_db_cron', day_of_week='*', hour=2, minute=0)
sched.start()
