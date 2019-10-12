#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Speciallan

from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'product', "-a", "cate_id=1", "-a", "origin_id=1"])
execute(['scrapy', 'crawl', 'comment'])
