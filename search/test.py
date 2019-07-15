#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

# 加载模块
from elasticsearch import Elasticsearch
import json


# 连接ES
def connect():
    es = Elasticsearch(["172.20.53.47"], port=9200)
    return es

def del_index(es):
    es.indices.delete(index='comment')

# 建立索引
def index(es):

    mappings = {
        "mappings": {
            "comment": {
                "properties": {
                    "username": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "ik_smart"
                    },
                    "createTime": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "updateTime": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    }
                }
            }
        }
    }
    result = es.indices.create(index='comment', body=mappings)
    print(result)

def insert(es):

    for k, v in enumerate(body):
        # print(v)
        # print(json.loads(v))
        result = es.index(index='comment', doc_type='comment', body=v)
        print(result)

def query(es, keywords):

    body = {
        "query": {
            # 'match_all': {}
            "match": {
                "content": keywords
            }
        }
    }
    res = es.search(index='comment', doc_type='comment', body=body)
    # print(res)
    result = res['hits']['hits']

    return result


# https://elasticsearch-py.readthedocs.io/en/5.0.0/api.html
if __name__ == '__main__':

    es = connect()

    file = open('mydata1.json')

    body = []
    for i in file.readlines():
        body.append(i)

    # del_index(es)
    # insert(es)
    keywords = '厉害 流程'
    result = query(es, keywords)

    for i in range(len(result)):
        print(result[i])

