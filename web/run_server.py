#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import time
import json
sys.path.append('../..')

from flask import Flask, request, render_template, url_for, redirect, jsonify
from search.web import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates',
            # static_folder='static',
            # static_url_path='/static'
            )
app.config.from_object(config)

from search.web import db


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('admin/login.html')

    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)

        return redirect('admin')

        if username == "zhangsan" and password == "123":
            return redirect('admin')
            # return "<h1>welcome, %s !</h1>" % username
        else:
            return "<h1>login Failure !</h1>"
            # return render_template('admin/index.html')


@app.route('/admin')
def admin():
    text = '2222'
    return render_template('admin/index.html',text=text)

    # if request.method == "POST":
    # username = request.form.get("username")
    # password = request.form.get("password")
    # password2 = request.form.get("password2")


@app.route('/crawler/list')
@app.route('/crawler/list/<int:page>', methods=['GET', 'POST'])
def crawler_list(page=1):
    # db.create_all() # 用来创建table，一般在初始化的时候调用
    # pagination = AppInfo.query.paginate(page, 20, False)
    return render_template('admin/crawler_list.html')
    # return render_template('admin/crawler_list.html', pagination=pagination)


@app.route('/crawler/add', methods = ['GET', 'POST'])
def crawler_add():
    return render_template('admin/crawler_add.html')

@app.route('/api/info', methods = ['GET'])
def api_info():
    data = {'name':'speciallan', 'age':28}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
