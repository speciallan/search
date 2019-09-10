#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import time
import json
import datetime
sys.path.append('../..')

from flask import Flask, request, render_template, url_for, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from search.web import config
from search.web import utils
from flask_cors import CORS

app = Flask(__name__,
            template_folder='templates',
            # static_folder='static',
            # static_url_path='/static'
            )
app.config.from_object(config)

# 初始化数据库
from search.web import database
db = SQLAlchemy(app)
db.init_app(app)

# 准备
from search.web import prepare

# 初始化任务
from search.web import task

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('admin/login.html')

    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "123456":
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



@app.route('/crawler/add', methods = ['GET', 'POST'])
def crawler_add():
    if request.method == "GET":
        from search.web.apps.admin.models import Product
        product_list = Product.query.with_entities(Product.id, Product.name).all()
        origin_list = [{'id':'jd', 'name':'京东'}]
        return render_template('admin/crawler_add.html',
                               product_list=product_list,
                               origin_list=origin_list)

    elif request.method == "POST":
        from search.web.apps.admin.models import Crawler
        product_id = request.form.get('product_id')
        product_origin = request.form.get('product_origin')
        product_website = request.form.get('product_website')
        starttime = request.form.get('starttime')
        endtime = request.form.get('endtime')
        schedule = request.form.get('schedule')

        names, fields = [], []
        names.append(request.form.get('name1'))
        names.append(request.form.get('name2'))
        names.append(request.form.get('name3'))
        names.append(request.form.get('name4'))
        fields.append(request.form.get('fields1'))
        fields.append(request.form.get('fields2'))
        fields.append(request.form.get('fields3'))
        fields.append(request.form.get('fields4'))

        starttime = '1970-01-01 00:00:00' if starttime == '' else starttime
        endtime = '1970-01-01 00:00:00' if endtime == '' else endtime
        starttime = time.mktime(time.strptime(starttime, "%Y-%m-%d %H:%M:%S"))
        endtime = time.mktime(time.strptime(endtime, "%Y-%m-%d %H:%M:%S"))

        avalible_fileds = {}
        for i,name in enumerate(names):
            if name != '' and fields[i] != '':
                avalible_fileds[name] = fields[i]

        avalible_fileds = json.dumps(avalible_fileds)
        # print(avalible_fileds, json.dumps(avalible_fileds))
        in_use = 1

        crawler = Crawler(product_id, product_origin, product_website, starttime, endtime, schedule, avalible_fileds, in_use)
        db.session.add(crawler)
        db.session.commit()

        return redirect('crawler/list')


@app.route('/crawler/list')
@app.route('/crawler/list/<int:page>', methods=['GET', 'POST'])
def crawler_list(page=1):
    from search.web.apps.admin.models import Crawler, Product

    per_page = 100
    total = Crawler.query.count()
    results = Crawler.query.with_entities(Crawler.id, Crawler.product_website, Crawler.product_origin, Crawler.starttime, Crawler.endtime, Crawler.schedule, Crawler.fields, Crawler.is_use, Product.name.label('product_name'))\
        .join(Product, Crawler.product_id == Product.id)\
        .order_by(Crawler.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Crawler.query.paginate(page, per_page)

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['starttime_str'] = datetime.datetime.utcfromtimestamp(int(item['starttime'])).strftime('%Y-%m-%d %H:%M:%S')
        item['endtime_str'] = datetime.datetime.utcfromtimestamp(int(item['endtime'])).strftime('%Y-%m-%d %H:%M:%S')
        item['schedule_str'] = '每天0点' if item['schedule'] == 0 else '无'
        item['is_use_str'] = '是' if item['is_use'] == 1 else '否'


    return render_template('admin/crawler_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)


@app.route('/category/add', methods = ['GET', 'POST'])
def category_add():
    if request.method == "GET":
        return render_template('admin/category_add.html')

    elif request.method == "POST":
        from search.web.apps.admin.models import Category
        name = request.form.get('name')

        cate = Category(name)
        db.session.add(cate)
        db.session.commit()
        return redirect('category/list')


@app.route('/category/list')
@app.route('/category/list/<int:page>', methods=['GET', 'POST'])
def category_list(page=1):
    from search.web.apps.admin.models import Category
    per_page = 100
    total = Category.query.count()
    data = Category.query.order_by(Category.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Category.query.paginate(page, per_page)

    return render_template('admin/category_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)


@app.route('/product/add', methods = ['GET', 'POST'])
def product_add():
    if request.method == "GET":
        from search.web.apps.admin.models import Category
        category_list = Category.query.all()
        return render_template('admin/product_add.html', category_list=category_list)

    elif request.method == "POST":
        from search.web.apps.admin.models import Product
        name = request.form.get('name')
        cate_id = request.form.get('cate_id')
        title = request.form.get('title')

        product = Product(name, cate_id, title)
        db.session.add(product)
        db.session.commit()
        return redirect('product/list')


@app.route('/product/list')
@app.route('/product/list/<int:page>', methods=['GET', 'POST'])
def product_list(page=1):
    from search.web.apps.admin.models import Product, Category
    per_page = 100
    total = Product.query.count()
    data = Product.query.with_entities(Product.id, Product.name, Product.title, Category.name.label('cate_name'))\
        .join(Category, Product.cate_id == Category.id)\
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    paginate = Product.query.paginate(page, per_page)

    return render_template('admin/product_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)

@app.route('/comment/list')
@app.route('/comment/list/<int:page>')
def comment_list(page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    per_page = 100
    total = Comment.query.count()
    results = Comment.query\
        .with_entities(Comment.id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Crawler.product_origin, Product.name.label('product_name'), Category.name.label('cate_name'))\
        .join(Crawler, Comment.crawler_id == Crawler.id) \
        .join(Product, Crawler.product_id == Product.id) \
        .join(Category, Category.id == Product.cate_id)\
        .order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Comment.query.paginate(page, per_page)

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['time'] = 0 if item['time'] == '' else item['time']
        item['time_str'] = datetime.datetime.utcfromtimestamp(int(item['time'])).strftime('%Y-%m-%d %H:%M:%S')
        item['is_member_str'] = '是' if item['is_member'] == 1 else '否'

    return render_template('admin/comment_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)


@app.route('/api/category', methods = ['GET'])
@app.route('/api/category/<int:page>')
def api_category(page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    per_page = 20
    total = Category.query.count()

    results = Category.query \
        .with_entities(Category.id, Category.name) \
        .order_by(Category.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@app.route('/api/product', methods = ['GET'])
@app.route('/api/product/<int:cid>')
@app.route('/api/product/<int:cid>/<int:page>')
def api_product(cid=1, page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    per_page = 20
    total = Product.query \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Category.id == cid) \
        .count()

    results = Product.query \
        .with_entities(Product.id, Product.name, Product.title) \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Category.id == cid) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@app.route('/api/comment', methods = ['GET'])
@app.route('/api/comment/<int:pid>')
@app.route('/api/comment/<int:pid>/<int:page>')
def api_comment(pid=1, page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    per_page = 20
    total = Comment.query \
        .join(Crawler, Comment.crawler_id == Crawler.id) \
        .join(Product, Crawler.product_id == Product.id) \
        .filter(Product.id == pid) \
        .count()

    results = Comment.query \
        .with_entities(Comment.id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Crawler.product_origin, Product.name.label('product_name'), Category.name.label('cate_name')) \
        .join(Crawler, Comment.crawler_id == Crawler.id) \
        .join(Product, Crawler.product_id == Product.id) \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Product.id == pid) \
        .order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Comment.query.paginate(page, per_page)

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['time'] = 0 if item['time'] == '' else item['time']
        item['time_str'] = datetime.datetime.utcfromtimestamp(int(item['time'])).strftime('%Y-%m-%d %H:%M:%S')
        item['is_member_str'] = '是' if item['is_member'] == 1 else '否'

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
