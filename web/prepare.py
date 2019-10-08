#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from search.web.apps.admin.models import Crawler
import json

results = Crawler.query.with_entities(Crawler.id, Crawler.website, Crawler.fields) \
    .filter(Crawler.is_use == 1) \
    .order_by(Crawler.id)\
    .all()

# flask_sqlalchemy reuslt->dict
config = [dict(zip(result.keys(), result)) for result in results]

# 写爬虫
file = open('../scrapy/tutorial/tutorial/spiders/crawlers.txt', 'w')
file.write(json.dumps(config))
file.close()


# url = 'https://item.jd.com/100004404916.html?id=1'
# print(url.strip().split('id=')[-1])


