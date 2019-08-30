#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import time
import json
sys.path.append('../..')

from flask import Flask, request, render_template, url_for, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from search.web import config

app = Flask(__name__,
            template_folder='templates',
            # static_folder='static',
            # static_url_path='/static'
            )
app.config.from_object(config)

# 初始化数据库
# from search.web import database
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('admin/login.html')

    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if 1 == 1:
        # if username == "admin" and password == "123456":
            resp = make_response(redirect('admin'))
            resp.set_cookie('username', username)
            return resp
            # return redirect('admin')
            # return "<h1>welcome, %s !</h1>" % username
        else:
            return "<h1>登录失败!</h1>"
            # return render_template('admin/index.html')


@app.route('/admin')
def admin():
    username = request.cookies.get('username')
    if username:
        text = '2222'
        return render_template('admin/index.html',text=text)
    else:
        return redirect('login')


@app.route('/comment/list')
@app.route('/comment/list/<int:page>')
def comment_list(page=1):

    from search.web.apps.admin.models import Comment

    per_page = 100
    total = Comment.query.count()
    data = Comment.query.order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Comment.query.paginate(page, per_page)
    print(paginate.has_prev, paginate.has_next)

    return render_template('admin/comment_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)


@app.route('/crawler/list')
@app.route('/crawler/list/<int:page>', methods=['GET', 'POST'])
def crawler_list(page=1):
    from search.web.apps.admin.models import Comment
    data = Comment.query.limit(10).order_by(Comment.id).all()
    return render_template('admin/crawler_list.html',
                           data=data)


@app.route('/crawler/add', methods = ['GET', 'POST'])
def crawler_add():
    return render_template('admin/crawler_add.html')

@app.route('/api/info', methods = ['GET'])
def api_info():
    data = {'name':'speciallan', 'age':28}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
