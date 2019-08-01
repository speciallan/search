#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
import time
import json
sys.path.append('..')

from flask import Flask, request, render_template

app = Flask(__name__, template_folder='./')

# 代码热更新
app.debug = True
file = open('../search/mydata1.json')
body = file.readlines()

@app.route('/spider')
def spider():
    text = '2222'
    return render_template('spider.html',text=text)

@app.route('/spider_data')
def spider_data():

    get = request.args
    i = get['index']
    write_body = body[int(i)]

    # print(body[0])
    str = ''
    # for i in range(len(write_body)):
    str += write_body + '<br>'
    return str

@app.route('/search')
def search():
    text = '2222'
    return render_template('search.html',text=text)

@app.route('/search_data')
def search_data():

    get = request.args
    keywords = get['keywords']

    from search.test import connect, query

    es = connect()
    result = query(es, keywords)

    show = '搜索关键词为 "{}" 的结果如下：<br>----------------------------------------------------------------------------------<br/>'.format(keywords)

    for i in range(len(result)):
        source = result[i]['_source']
        show += '用户名:{}, 时间:{}, 评论内容:{} <br>'.format(source['username'], source['time'], source['content'])

    return show

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8888)

