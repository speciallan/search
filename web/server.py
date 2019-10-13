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


# 注册路由
from search.web.apps.api.routes import api
app.register_blueprint(api, url_prefix='/api')


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
        from search.web.apps.admin.models import Product, Origin
        product_list = Product.query.with_entities(Product.id, Product.name).all()
        origin_list = Origin.query.with_entities(Origin.id, Origin.name).all()

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
    from search.web.apps.admin.models import Crawler, Product, Origin

    per_page = 100
    total = Crawler.query.count()
    results = Crawler.query.with_entities(Crawler.id, Crawler.website, Crawler.origin_id, Crawler.starttime, Crawler.endtime, Crawler.schedule, Crawler.fields, Crawler.is_use, Origin.name.label('origin_name'), Product.name.label('product_name'))\
        .join(Origin, Crawler.origin_id == Origin.id) \
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


@app.route('/origin/add', methods = ['GET', 'POST'])
def origin_add():
    if request.method == "GET":
        return render_template('admin/origin_add.html')

    elif request.method == "POST":
        from search.web.apps.admin.models import Origin
        name = request.form.get('name')
        label = request.form.get('label')
        site = request.form.get('site')

        origin = Origin(name, label, site)
        db.session.add(origin)
        db.session.commit()
        return redirect('origin/list')


@app.route('/origin/list')
@app.route('/origin/list/<int:page>', methods=['GET', 'POST'])
def origin_list(page=1):
    from search.web.apps.admin.models import Origin
    per_page = 100
    total = Origin.query.count()
    data = Origin.query.order_by(Origin.id).limit(per_page).offset((page - 1) * per_page).all()
    paginate = Origin.query.paginate(page, per_page)

    return render_template('admin/origin_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)


@app.route('/category/add', methods = ['GET', 'POST'])
def category_add():
    if request.method == "GET":
        return render_template('admin/category_add.html')

    elif request.method == "POST":
        from search.web.apps.admin.models import Category
        parent_id = request.form.get('parent_id')
        name = request.form.get('name')

        cate = Category(parent_id, name)
        db.session.add(cate)
        db.session.commit()
        return redirect('category/list')


@app.route('/category/list')
@app.route('/category/list/<int:page>', methods=['GET', 'POST'])
def category_list(page=1):
    from search.web.apps.admin.models import Category
    per_page = 100
    total = Category.query.count()
    first = Category.query.with_entities(Category.id, Category.parent_id, Category.name).filter(Category.parent_id == 0)

    second = Category.query \
        .with_entities(Category.id, Category.parent_id, Category.name) \
        .filter(Category.parent_id.in_(
        Category.query.with_entities(Category.id).filter(Category.parent_id == 0)
    )) \
        .order_by(Category.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict

    first = [dict(zip(result.keys(), result)) for result in first]
    second = [dict(zip(result.keys(), result)) for result in second]

    data = {}
    for d in first:
        data[d['id']] = d
        data[d['id']]['sub'] = []

    for d in second:
        data[d['parent_id']]['sub'].append(d)

    arr = []
    for k,v in data.items():
        arr.append(v)

    return render_template('admin/category_list.html',
                           total=total,
                           data=arr)


@app.route('/attribute/add', methods = ['GET', 'POST'])
def attribute_add():
    if request.method == "GET":
        from search.web.apps.admin.models import Category
        category_list = Category.query.all()
        return render_template('admin/attribute_add.html', category_list=category_list)

    elif request.method == "POST":
        from search.web.apps.admin.models import Attribute
        cate_id = request.form.get('cate_id')
        name = request.form.get('name')
        rule = request.form.get('rule')

        attr = Attribute(cate_id, name, rule)
        db.session.add(attr)
        db.session.commit()
        return redirect('attribute/list')


@app.route('/attribute/list')
@app.route('/attribute/list/<int:page>', methods=['GET', 'POST'])
def attribute_list(page=1):
    from search.web.apps.admin.models import Attribute, Category
    per_page = 100
    total = Attribute.query.count()
    data = Attribute.query.with_entities(Attribute.id, Attribute.name, Attribute.rule, Category.name.label('cate_name')) \
        .join(Category, Attribute.cate_id == Category.id) \
        .order_by(Attribute.id).limit(per_page).offset((page - 1) * per_page).all()

    return render_template('admin/attribute_list.html',
                           total=total,
                           data=data)


@app.route('/product/add', methods = ['GET', 'POST'])
def product_add():
    if request.method == "GET":
        from search.web.apps.admin.models import Category
        category_list = Category.query.all()
        return render_template('admin/product_add.html', category_list=category_list)

    elif request.method == "POST":
        from search.web.apps.admin.models import Product
        goods_id = request.form.get('goods_id')
        name = request.form.get('name')
        cate_id = request.form.get('cate_id')
        brand = request.form.get('brand')
        title = request.form.get('title')
        price = request.form.get('price')
        comment_num = request.form.get('comment_num')
        photo = request.form.get('photo')

        product = Product(goods_id, name, cate_id, brand, title, price, comment_num, photo)
        db.session.add(product)
        db.session.commit()
        return redirect('product/list')


@app.route('/product/list')
@app.route('/product/list/<int:page>', methods=['GET', 'POST'])
def product_list(page=1):
    from search.web.apps.admin.models import Product, Category, Origin

    origin_id = 1
    per_page = 100
    total = Product.query.count()
    data = Product.query.with_entities(Product.id, Product.goods_id, Product.name, Product.brand, Product.title, Product.price, Product.comment_num, Category.name.label('cate_name'), Origin.name.label('origin_name'))\
        .join(Category, Product.cate_id == Category.id) \
        .join(Origin, Product.origin_id == Origin.id)\
        .filter(Product.origin_id == origin_id) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    paginate = Product.query.paginate(page, per_page)

    return render_template('admin/product_list.html',
                           total=total,
                           data=data,
                           paginate=paginate)

@app.route('/comment/list')
@app.route('/comment/list/<int:page>')
def comment_list(page=1):

    from search.web.apps.admin.models import Product, Category, Crawler, Origin

    origin_id = 1
    if origin_id == 1:
        from search.web.apps.admin.models import CommentJd as Comment

    per_page = 200
    total = Comment.query \
        .filter(Comment.origin_id == origin_id) \
        .count()

    results = Comment.query\
        .with_entities(Comment.id, Comment.origin_id, Comment.goods_id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Origin.name.label('origin_name'), Product.name.label('product_name'), Category.name.label('cate_name'))\
        .join(Product, Product.goods_id == Comment.goods_id) \
        .join(Category, Category.id == Product.cate_id) \
        .join(Origin, Origin.id == Comment.origin_id) \
        .filter(Comment.origin_id == origin_id) \
        .order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['time'] = 0 if item['time'] == '' else item['time']
        item['time_str'] = datetime.datetime.utcfromtimestamp(int(item['time'])).strftime('%Y-%m-%d %H:%M:%S')
        item['is_member_str'] = '是' if item['is_member'] == 1 else '否'

    return render_template('admin/comment_list.html',
                           total=total,
                           data=data)


@app.route('/update_product')
def update_product():

    from search.web.apps.admin.models import Product, ProductStatisticsJd, CommentJd, ProductEmotionJd

    # db.drop_all()
    db.create_all()

    links = open("../scrapy/tutorial/tutorial/spiders/product_url.txt")
    link = links.read()
    link = link.split('-----')[:-1]
    for i in link:
        re = i.split('---')
        origin_id, goods_id, cate_id, url, title, price, photo, comment_num = re

        origin_id = int(origin_id)
        cate_id = int(cate_id)
        name = title[:15]
        brand = title[:15]

        product = Product.query.filter(Product.origin_id == origin_id).filter(Product.goods_id == goods_id).first()

        if not product:
            product = Product(origin_id, goods_id, name, cate_id, brand, title, price, comment_num, photo)
            db.session.add(product)
        else:
            product.origin_id = origin_id
            product.goods_id = goods_id
            product.name = name
            product.cate_id = cate_id
            product.brand = brand
            product.title = title
            product.price = price
            product.comment_num = comment_num
            product.photo = photo
        db.session.flush()
    db.session.commit()

@app.route('/update_product2')
def update_product2():

    from search.web.apps.admin.models import Product, ProductStatisticsJd, CommentJd, ProductEmotionJd
    links = open("../scrapy/tutorial/tutorial/spiders/product_url.txt")
    link = links.read()
    link = link.split('-----')[:-1]
    for i in link:
        re = i.split('---')
        origin_id, goods_id, cate_id, url, title, price, photo, comment_num = re

        origin_id = int(origin_id)
        cate_id = int(cate_id)

        price = float(price)
        comment_num = int(comment_num)
        sale_num = int(comment_num)

        date = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d')
        year, month, day = date.split('-')

        pro_sta_jd = ProductStatisticsJd.query\
            .filter(ProductStatisticsJd.origin_id == origin_id)\
            .filter(ProductStatisticsJd.goods_id == goods_id)\
            .filter(ProductStatisticsJd.year == year) \
            .filter(ProductStatisticsJd.month == month)\
            .filter(ProductStatisticsJd.day == day)\
            .first()

        if not pro_sta_jd:
            # 插入不进去
            pro_sta_jd = ProductStatisticsJd(origin_id, goods_id, price, comment_num, sale_num, year, month, day)
            db.session.add(pro_sta_jd)
        else:
            pro_sta_jd.price = price
            pro_sta_jd.comment_num = comment_num
            pro_sta_jd.sale_num = sale_num

        db.session.flush()
    db.session.commit()

    return 'successfully update'

@app.route('/update_comment')
def update_comment():

    from search.web.apps.admin.models import Product, ProductStatisticsJd, CommentJd, ProductEmotionJd
    import json
    links = open("../scrapy/tutorial/tutorial/spiders/mydata1.json", 'r', encoding='utf-8')
    links = links.read()
    links = links.split('-----')[:-1]

    for i in links:
        re = json.loads(i)
        origin_id, goods_id, username, time1, content, star, is_member, avater = re.values()

        origin_id = int(origin_id)

        if origin_id == 1:
            from search.web.apps.admin.models import CommentJd as Comment

        db.create_all()

        star = int(star)
        is_member = int(is_member)
        crawler_id = 0

        year, month, day = time1.split(' ')[0].split('-')

        time1 = '1970-01-01 00:00' if time1 < '1970-01-01 00:00' else time1
        timeint = int(time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M")))

        comment = Comment.query \
            .filter(Comment.origin_id == origin_id) \
            .filter(Comment.goods_id == goods_id) \
            .filter(Comment.username == username) \
            .filter(Comment.time == timeint) \
            .first()

        if not comment:
            # 插入不进去
            comment = Comment(crawler_id, origin_id, goods_id, username, content, timeint, is_member, star, avater, year, month, day)
            db.session.add(comment)

        db.session.flush()
    db.session.commit()

    return 'successfully update'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
