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
from search.web import utils

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
        return render_template('admin/crawler_add.html')

    elif request.method == "POST":
        category_name = request.form.get('category_name')
        print(category_name)


@app.route('/crawler/list')
@app.route('/crawler/list/<int:page>', methods=['GET', 'POST'])
def crawler_list(page=1):
    from search.web.apps.admin.models import Crawler
    per_page = 100
    total = Crawler.query.count()
    data = Crawler.query.order_by(Crawler.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Crawler.query.paginate(page, per_page)


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

    from search.web.apps.admin.models import Comment, Product, Category

    per_page = 100
    total = Comment.query.count()
    data = Comment.query\
        .with_entities(Comment.id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Product.name, Category.name.label('cate_name'))\
        .join(Product, Comment.product_id == Product.id) \
        .join(Category, Category.id == Product.cate_id)\
        .order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Comment.query.paginate(page, per_page)
    print(paginate.has_prev, paginate.has_next)

    return render_template('admin/comment_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)



@app.route('/api/comment', methods = ['GET'])
@app.route('/api/comment/<int:page>')
def api_info(page=1):

    from search.web.apps.admin.models import Comment
    per_page = 10

    total = Comment.query.count()
    data = Comment.query.order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()
    json_data = utils.orm_to_json(data)

    result = {'total':total, 'data':json_data}
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
