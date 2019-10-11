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

class ProductItem(scrapy.Item):

    goods_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    photo = scrapy.Field()

class CommentItem(scrapy.Item):

    crawler_id = scrapy.Field()
    goods_id = scrapy.Field()
    username = scrapy.Field()
    comment_num = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    star = scrapy.Field()
    is_member = scrapy.Field()
