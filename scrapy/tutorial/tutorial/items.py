# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JdPhoneItem(scrapy.Item):

    url = scrapy.Field()    # 商品链接
    title = scrapy.Field()  # 商品标题
    price = scrapy.Field()  # 商品价格

class CommentItem(scrapy.Item):

    username = scrapy.Field()
    comment_num = scrapy.Field()
    content = scrapy.Field()
