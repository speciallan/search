#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from search.web.server import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), default='')

    def __init__(self, username, email=''):
        self.username = username
        self.email = email


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), default='')
    
    content = db.Column(db.Text(), default='')
    time = db.Column(db.String(20), default='')
    is_member = db.Column(db.Integer(), default=0)
    star = db.Column(db.Integer(), default=0)

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), default='')
    content = db.Column(db.Text(), default='')
    time = db.Column(db.String(20), default='')
    is_member = db.Column(db.Integer(), default=0)
    star = db.Column(db.Integer(), default=0)

    def __init__(self, username, content, time, is_member, star):
        self.username = username
        self.content = content
        self.time = time
        self.is_member = is_member
        self.star = star


class Crawler(db.Model):
    __tablename__ = "crawler"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), default='')

    def __init__(self, username, email=''):
        self.username = username
        self.email = email
