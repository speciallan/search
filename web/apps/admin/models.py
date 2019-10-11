#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from sqlalchemy.ext.declarative import declarative_base
from search.web.server import db


class BaseModel(db.Model):

    __abstract__= True  ##加了该属性后生成表的时候不会生成该表
    _include_fields = []

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def double_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_dict1(self):
        """Return a dictionary representation of this model."""
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()

        # fields that should be included when sent as json
        self.includes = self._include_fields

        # data object that is later returned
        data = {}

        for column in columns:
            path = column
            print(path, path in self.includes)
            if path in self.includes:
                data[column] = getattr(self, column)

        if relationships:
            for rel_key in relationships:
                data[rel_key] = self.get_relationship_data(self, rel_key)

        return data


class User(BaseModel):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), default='')

    def __init__(self, username, email=''):
        self.username = username
        self.email = email


class Category(BaseModel):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), default='')

    def __init__(self, name):
        self.name = name


class Attribute(BaseModel):
    __tablename__ = "attribute"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cate_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), default='')
    rule = db.Column(db.String(100), default='')

    def __init__(self, cate_id, name, rule):
        self.cate_id = cate_id
        self.name = name
        self.rule = rule


class Product(BaseModel):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goods_id = db.Column(db.String(20), default='')
    name = db.Column(db.String(20), default='')
    cate_id = db.Column(db.Integer)
    brand = db.Column(db.String(20), default='')
    title = db.Column(db.String(100), default='')
    price = db.Column(db.Float, default=0)
    comment_num = db.Column(db.Integer, default=0)
    photo = db.Column(db.String(255), default='')

    def __init__(self, goods_id, name, cate_id, brand, title, price, comment_num, photo):
        self.goods_id = goods_id
        self.name = name
        self.cate_id = cate_id
        self.brand = brand
        self.title = title
        self.price = price
        self.comment_num = comment_num
        self.photo = photo


class Comment(BaseModel):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crawler_id = db.Column(db.Integer)
    username = db.Column(db.String(20), default='')
    content = db.Column(db.Text(), default='')
    time = db.Column(db.Integer)
    is_member = db.Column(db.Integer(), default=0)
    star = db.Column(db.Integer(), default=0)
    avater = db.Column(db.String(255), default='')

    def __init__(self, crawler_id, username, content, time, is_member, star, avater):
        self.crawler_id = crawler_id
        self.username = username
        self.content = content
        self.time = time
        self.is_member = is_member
        self.star = star
        self.avater = avater


class Crawler(BaseModel):
    __tablename__ = "crawler"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, default=0)
    # 同一个产品涉及多个网站
    origin_id = db.Column(db.Integer, default=0)
    website = db.Column(db.String(100), default='')
    starttime = db.Column(db.Integer, default=0)
    endtime = db.Column(db.Integer, default=0)
    schedule = db.Column(db.Integer, default=0)
    fields = db.Column(db.Text(), default='')
    is_use = db.Column(db.Integer, default=1)

    def __init__(self, product_id, origin_id, website, starttime, endtime, schedule, fields, is_use):
        self.product_id = product_id
        self.origin_id = origin_id
        self.website = website
        self.starttime = starttime
        self.endtime = endtime
        self.schedule = schedule
        self.fields = fields
        self.is_use = is_use


class Origin(BaseModel):
    __tablename__ = 'origin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), default='')
    site = db.Column(db.String(100), default='')

    def __init__(self, name, site):
        self.name = name
        self.site = site


class Brand(BaseModel):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), default='')

    def __init__(self, name):
        self.name = name

