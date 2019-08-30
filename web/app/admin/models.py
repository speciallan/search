#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from search.web.run_server import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), default='')

    def __init__(self, username, email=''):
        self.username = username
        self.email = email
