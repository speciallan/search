#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

# 加载模块
from elasticsearch import Elasticsearch

# 连接ES
es = Elasticsearch(["172.30.6.12"])

# 查询
res = es.search(index="test-index", body={"query":{"match_all":{}}})  #    注   index  后面的是索引的名字

# 查询请求主机是ai.baidu.com 所有信息
res = es.search(index="packetbeat-*", body={'query':{'match':{'http.request.headers.host':'ai.baidu.com'}}})

res = es.search(index="test-index", body={'query':{'match':{'any':'data'}}}) #获取any=data的所有值