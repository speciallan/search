# -*- coding:utf-8 -*-
# Author:Speciallan

from flask import Blueprint, jsonify, request
import datetime

api = Blueprint('api', __name__)


@api.route('/origin', methods = ['GET'])
@api.route('/origin/<int:page>')
def api_origin(page=1):

    from search.web.apps.admin.models import Origin

    per_page = 20
    total = Origin.query.count()

    results = Origin.query \
        .with_entities(Origin.id, Origin.name, Origin.label, Origin.site) \
        .order_by(Origin.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/category', methods = ['GET'])
@api.route('/category/<int:page>')
def api_category(page=1):

    from search.web.apps.admin.models import Product, Category, Crawler

    per_page = 20
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

    data ={}
    for d in first:
        data[d['id']] = d
        data[d['id']]['sub'] = []

    for d in second:
        data[d['parent_id']]['sub'].append(d)

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/product/list', methods = ['GET'])
@api.route('/product/list/<int:origin_id>/<int:cid>')
@api.route('/product/list/<int:origin_id>/<int:cid>/<int:page>')
def api_product(origin_id=1, cid=1, page=1):

    from search.web.apps.admin.models import Category, Product

    per_page = 20

    total = Product.query \
        .filter(Product.origin_id == origin_id) \
        .filter(Product.cate_id == cid) \
        .count()

    results = Product.query \
        .with_entities(Product.id, Product.origin_id, Product.goods_id, Product.name, Product.brand, Product.title, Product.price, Product.comment_num, Product.photo, Category.name.label('cate_name')) \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Product.origin_id == origin_id) \
        .filter(Product.cate_id == cid) \
        .order_by(Product.id).limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/product/date', methods = ['GET'])
@api.route('/product/date/<int:origin_id>/<string:goods_id>')
def api_product_date(origin_id=1, goods_id=1):

    from search.web.apps.admin.models import Product, Category, Crawler

    data = [
        {'product_name':'华为P30', 'date':'2019-09-09', 'price':5.00, 'sale_num': 100, 'comment_num': 330000},
        {'product_name':'华为P30', 'date':'2019-09-10', 'price':6.00, 'sale_num': 120, 'comment_num': 350000},
        {'product_name':'华为P30', 'date':'2019-09-11', 'price':5.00, 'sale_num': 140, 'comment_num': 400000},
        {'product_name':'华为P30', 'date':'2019-09-12', 'price':5.50, 'sale_num': 200, 'comment_num': 410000},
        {'product_name':'华为P30', 'date':'2019-09-13', 'price':5.00, 'sale_num': 700, 'comment_num': 450000},
        {'product_name':'华为P30', 'date':'2019-09-14', 'price':5.00, 'sale_num': 800, 'comment_num': 590000},
        {'product_name':'华为P30', 'date':'2019-09-15', 'price':5.00, 'sale_num': 1200, 'comment_num': 660000},
        {'product_name':'华为P30', 'date':'2019-09-16', 'price':5.00, 'sale_num': 1300, 'comment_num': 770000},
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
@api.route('/product/emotion/<int:origin_id>/<string:goods_id>')
def api_product_emotion(origin_id=1, goods_id=1):
    """情感分析"""

    from search.web.apps.admin.models import Product, Category, Crawler

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
@api.route('/comment/<int:origin_id>/<string:goods_id>')
@api.route('/comment/<int:origin_id>/<string:goods_id>/<string:level>')
@api.route('/comment/<int:origin_id>/<string:goods_id>/<string:level>/<int:page>')
def api_comment(origin_id=1, goods_id=1, level='a', page=1):

    from search.web.apps.admin.models import Product, Category, Crawler, Origin

    origin_id = 1

    if origin_id == 1:
        from search.web.apps.admin.models import CommentJd as Comment

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
        .filter(Comment.origin_id == origin_id) \
        .filter(Comment.goods_id == goods_id) \
        .filter(Comment.star.in_(star)) \
        .count()

    results = Comment.query \
        .with_entities(Comment.id, Comment.origin_id, Comment.goods_id, Comment.username, Comment.content, Comment.time, Comment.star, Comment.is_member, Comment.avater, Comment.year, Comment.month, Comment.day, Product.name.label('product_name'), Category.name.label('cate_name')) \
        .join(Product, Comment.origin_id == Product.origin_id and Comment.goods_id == Product.goods_id) \
        .join(Category, Category.id == Product.cate_id) \
        .filter(Comment.origin_id == origin_id) \
        .filter(Comment.goods_id == goods_id) \
        .filter(Comment.star.in_(star)) \
        .order_by(Comment.id).limit(per_page).offset((page - 1) * per_page).all()

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

    from search.web.apps.admin.models import Product, Category

    post_data = request.form

    if 'origin_id' in post_data.keys():
        origin_id = int(post_data['origin_id'])
    else:
        origin_id = 1

    if origin_id == 1:
        from search.web.apps.admin.models import CommentJd as Comment

    total = Product.query \
            .join(Category, Category.id == Product.cate_id) \

    results = Comment.query \
              .with_entities(Product.id.label('product_id'), Product.goods_id, Product.name, Product.title, Product.price, Product.comment_num, Product.photo, Category.name.label('cate_name')) \
              .join(Category, Category.id == Product.cate_id) \

    if 'keywords' in post_data.keys():
        total = total.filter(Product.title.like(f'%{post_data["keywords"]}%'))
        results = results.filter(Product.title.like(f'%{post_data["keywords"]}%'))

    if 'cate_id' in post_data.keys():
        total = total.filter(Product.cate_id == post_data['cate_id'])
        results = results.filter(Product.cate_id == post_data['cate_id'])

    if 'title' in post_data.keys():
        total = total.filter(Product.title.like(f'%{post_data["title"]}%'))
        results = results.filter(Product.title.like(f'%{post_data["title"]}%'))

    if 'brand' in post_data.keys():
        total = total.filter(Product.brand.like(f'%{post_data["brand"]}%'))
        results = results.filter(Product.brand.like(f'%{post_data["brand"]}%'))

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

    per_page = 20
    total = total.count()
    results = results.limit(per_page).offset((page - 1) * per_page).all()

    # flask_sqlalchemy reuslt->dict
    data = [dict(zip(result.keys(), result)) for result in results]

    for item in data:
        item['comment_str'] = '{:.1f}万'.format(item['comment_num'] / 10000)

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)


@api.route('/search/comment/', methods = ['GET', 'POST'])
@api.route('/search/comment/<int:origin_id>/<string:keywords>')
@api.route('/search/comment/<int:origin_id>/<string:keywords>/<int:page>')
def api_search_comment(origin_id=1, keywords='', page=1):

    from search.web.apps.admin.models import Product, Category, Crawler

    if origin_id == 1:
        from search.web.apps.admin.models import CommentJd as Comment

    post_data = request.form

    per_page = 20
    total = Comment.query \
        .filter(Comment.content.like(f'%{keywords}%')) \
        .filter(Comment.origin_id == origin_id)\
        .count()

    results = Comment.query \
        .with_entities(Product.id.label('product_id'), Product.goods_id, Product.name, Product.title, Product.price, Product.comment_num, Comment.id.label('comment_id'), Comment.content, Comment.username, Comment.time, Comment.is_member, Comment.star, Comment.avater, Comment.year, Comment.month, Comment.day) \
        .filter(Comment.content.like(f'%{keywords}%')) \
        .filter(Comment.origin_id == origin_id) \
        .limit(per_page).offset((page - 1) * per_page).all()

    data = [dict(zip(result.keys(), result)) for result in results]

    json_data = {'total':total, 'data':data}

    return jsonify(json_data)
