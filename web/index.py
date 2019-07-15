#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

import sys
sys.path.append('..')

from flask import Flask, request, render_template
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__, template_folder='./')

# 代码热更新
app.debug = True

@app.route('/spider')
def spider():
    return render_template('spider.html')


@app.route('/search')
def search():

    get = request.args
    keywords = get['keywords']

    from search.test import connect, query

    es = connect()
    result = query(es, keywords)

    show = '搜索关键词为 "{}" 的结果如下：<br>'.format(keywords)

    for i in range(len(result)):
        source = result[i]['_source']
        show += 'username:{}, comment:{} <br>'.format(source['username'], source['content'])

    return show

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8888)

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()