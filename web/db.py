#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from flask_sqlalchemy import SQLAlchemy
from search.web.run_server import app
from search.web.app.admin.models import User

# 数据库
db = SQLAlchemy(app)
db.init_app(app)


# db.drop_all()
db.create_all()

# admin = User('admin', '222')
# db.session.add(admin)
# db.session.commit()

# select
result = User.query.filter(User.username == 'admin').first()
print(result.username)
print('-----------')

result = User.query.all()
[print(i.id, i.username) for i in result]

# update
# result.username = 'admin1'
# db.session.commit()

# delete
# db.session.delete(result)
# db.session.commit()


"""
1 {"username": "不***子", "content": "用了一段时间过来评论了，新手机很不错，比我之前那破手机强太多了，用着不卡，吃鸡全
高无压力，续航可以，拍照也不错。"}
2 {"username": "j***b", "content": "手机收到了，打游戏挺流畅的，相信华为支持华为"}
3 {"username": "137*****716_p", "content": "一直考虑的很久，终于下定决心买这款手机，运行内存和储存内存够大，挺适合，喜
欢的不得了…"}
4 {"username": "爱购恨购", "content": "第一次使用HUAWEI Nova5Pro  像素真是太清晰了  手感光滑  屏幕尺寸非常适手  支持国
产！刚收到货 物流太给力了，等待更多惊喜出现！"}
5 {"username": "z***8", "content": "一天到货，这速度厉害了，很满意"}
6 {"username": "132*****501_p", "content": "非常好，华为手机用实力说话，京东服务物流特别棒，感谢大家！"}
7 {"username": "jd_185955owr", "content": "手机到手颜值高，没耳机插孔，陪耳机啥用。发过来盒子胶带又开裂"}
8 {"username": "DXWTWL", "content": "以前都是用vivo的，现在用华为感觉挺流畅的"}
9 {"username": "j***1", "content": "此用户未填写评价内容"}

"""

