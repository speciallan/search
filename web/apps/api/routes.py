# -*- coding:utf-8 -*-
# Author:Speciallan

from flask import Blueprint, jsonify, request
import datetime

api = Blueprint('api', __name__)


@api.route('/category', methods = ['GET'])
@api.route('/category/<int:page>')
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


@api.route('/product/list', methods = ['GET'])
@api.route('/product/list/<int:cid>')
@api.route('/product/list/<int:cid>/<int:page>')
def api_product(cid=1, page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    per_page = 20
    total = Product.query \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Category.id == cid) \
        .count()

    results = Product.query \
        .with_entities(Product.id, Product.name, Product.brand, Product.title) \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Category.id == cid) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/product/date', methods = ['GET'])
@api.route('/product/date/<int:product_id>')
def api_product_date(product_id=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    data = [
        {'product_name':'华为P30', 'date':'2019-09-09', 'price':5.00, 'sale': 100},
        {'product_name':'华为P30', 'date':'2019-09-10', 'price':6.00, 'sale': 120},
        {'product_name':'华为P30', 'date':'2019-09-11', 'price':5.00, 'sale': 140},
        {'product_name':'华为P30', 'date':'2019-09-12', 'price':5.50, 'sale': 200},
        {'product_name':'华为P30', 'date':'2019-09-13', 'price':5.00, 'sale': 700},
        {'product_name':'华为P30', 'date':'2019-09-14', 'price':5.00, 'sale': 800},
        {'product_name':'华为P30', 'date':'2019-09-15', 'price':5.00, 'sale': 1200},
        {'product_name':'华为P30', 'date':'2019-09-16', 'price':5.00, 'sale': 1300},
    ]
    json_data = {'total':len(data), 'data':data}
    return jsonify(json_data)

    per_page = 20
    total = Product.query \
        .join(Category, Category.id == Product.cate_id) \
        .count()

    results = Product.query \
        .with_entities(Product.id, Product.name, Product.title) \
        .join(Category, Category.id == Product.cate_id) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/product/emotion', methods = ['GET'])
@api.route('/product/emotion/<int:product_id>')
def api_product_emotion(product_id=1):
    """情感分析"""

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    data = [
        {'product_name':'华为P30', 'date':'2019-09-09', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-10', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-11', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-12', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-13', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-14', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-15', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}},
        {'product_name':'华为P30', 'date':'2019-09-16', 'attr':{'电池容量':0.6, '摄像头':0.3, '接口类型':0.3, '网络支持':0.5, '存储容量':0.8, '屏幕大小':-0.3}}
    ]
    json_data = {'total':len(data), 'data':data}
    return jsonify(json_data)

    per_page = 20
    total = Product.query \
        .join(Category, Category.id == Product.cate_id) \
        .count()

    results = Product.query \
        .with_entities(Product.id, Product.name, Product.title) \
        .join(Category, Category.id == Product.cate_id) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/comment', methods = ['GET', 'POST'])
@api.route('/comment/<int:pid>')
@api.route('/comment/<int:pid>/<string:level>')
@api.route('/comment/<int:pid>/<string:level>/<int:page>')
def api_comment(pid=1, level='a', page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler, Origin

    star = []
    if level == 'a':
        star = [1,2,3,4,5]
    elif level == 'l':
        star = [1]
    elif level == 'm':
        star = [2,3]
    elif level == 'h':
        star = [4,5]


    per_page = 20
    total = Comment.query \
        .join(Crawler, Comment.crawler_id == Crawler.id) \
        .join(Product, Crawler.product_id == Product.id) \
        .filter(Product.id == pid) \
        .filter(Comment.star.in_(star)) \
        .count()

    results = Comment.query \
        .with_entities(Comment.id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Comment.avater, Crawler.origin_id, Origin.name.label('origin_name'), Product.name.label('product_name'), Category.name.label('cate_name')) \
        .join(Crawler, Comment.crawler_id == Crawler.id) \
        .join(Product, Crawler.product_id == Product.id) \
        .join(Category, Category.id == Product.cate_id) \
        .join(Origin, Origin.id == Crawler.origin_id) \
        .filter(Product.id == pid) \
        .filter(Comment.star.in_(star)) \
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

@api.route('/search/product/', methods = ['GET', 'POST'])
# @api.route('/search/product/<string:keywords>', methods = ['GET', 'POST'])
# @api.route('/search/product/<string:keywords>/<int:page>')
def api_search_product(keywords='', page=1):

    from search.web.apps.admin.models import Comment, Product, Category

    total = Product.query \
            .join(Category, Category.id == Product.cate_id) \

    results = Comment.query \
              .with_entities(Product.id.label('product_id'), Product.goods_id, Product.name, Product.title, Product.price, Product.comment_num, Product.photo, Category.name.label('cate_name')) \
              .join(Category, Category.id == Product.cate_id) \

    post_data = request.form
    if 'keywords' in post_data.keys():
        total = total.filter(Product.title.like(f'%{post_data["keywords"]}%'))
        results = results.filter(Product.title.like(f'%{post_data["keywords"]}%'))

    if 'cate_id' in post_data.keys():
        total = total.filter(Product.cate_id == post_data['cate_id'])
        results = results.filter(Product.cate_id == post_data['cate_id'])

    if 'brand' in post_data.keys():
        total = total.filter(Product.brand.like(post_data['brand']))
        results = results.filter(Product.brand.like(post_data['brand']))

    if 'price_min' in post_data.keys() and 'price_max' in post_data.keys():
        total = total.filter(Product.price >= int(post_data['price_min']))
        total = total.filter(Product.price <= int(post_data['price_max']))
        results = results.filter(Product.price >= int(post_data['price_min']))
        results = results.filter(Product.price <= int(post_data['price_max']))

    if 'order' in post_data.keys():
        if post_data['order'] == 'comment_asc':
            results = results.order_by(Product.comment_num.asc())
        if post_data['order'] == 'comment_desc':
            results = results.order_by(Product.comment_num.desc())
        if post_data['order'] == 'sale_asc':
            results = results.order_by(Product.comment_num.asc())
        if post_data['order'] == 'sale_desc':
            results = results.order_by(Product.comment_num.desc())
        if post_data['order'] == 'price_asc':
            results = results.order_by(Product.price.asc())
        if post_data['order'] == 'price_desc':
            results = results.order_by(Product.price.desc())

    total = total.count()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['comment_str'] = '{:.1f}万'.format(item['comment_num'] / 10000)

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/search/comment/', methods = ['GET', 'POST'])
@api.route('/search/comment/<string:keywords>')
@api.route('/search/comment/<string:keywords>/<int:page>')
def api_search_comment(keywords='', page=1):

    from search.web.apps.admin.models import Comment, Product, Category, Crawler

    post_data = request.form

    per_page = 20
    total = Comment.query \
        .join(Crawler, Crawler.id == Comment.crawler_id) \
        .join(Product, Product.id == Crawler.product_id) \
        .filter(Comment.content.like(f'%{keywords}%')) \
        .count()

    results = Comment.query \
        .with_entities(Product.id.label('product_id'), Product.goods_id, Product.name, Product.title, Product.price, Product.comment_num, Comment.id.label('comment_id'), Comment.content, Comment.username, Comment.time, Comment.is_member, Comment.star) \
        .join(Crawler, Crawler.id == Comment.crawler_id) \
        .join(Product, Product.id == Crawler.product_id) \
        .filter(Comment.content.like(f'%{keywords}%')) \

    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)
