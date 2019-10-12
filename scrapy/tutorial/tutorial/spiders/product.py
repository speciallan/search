# -*- coding: utf-8 -*-

import scrapy

from ..items import ProductItem
import re


class ProductSpider(scrapy.Spider):

    name = "product"
    # allowed_domains = ["jd.com"]

    cates = {'1':'手机', '2':'计算机'}
    origins = {'1':'https://search.jd.com/Search?keyword={}&enc=utf-8&page={}'}

    def __init__(self, cate_id, origin_id, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.pre_url = self.origins[origin_id]
        self.cate_id = cate_id
        self.origin_id = origin_id

        start_urls = []
        # 获取前十页的链接
        for i in range(1, 5):
            url = self.pre_url.format(self.cates[cate_id], 2*i-1)
            start_urls.append(url)
        self.start_urls = start_urls

    # 获取商品的链接，标题，价格
    def parse(self, response):

        item = ProductItem()

        item['goods_id'] = response.xpath("//li[@class='gl-item']/@data-sku").extract()
        item["url"] = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        item["title"] = response.xpath("//div[@class='p-name p-name-type-2']/a/em/text()").extract()
        item["price"] = response.xpath("//div[@class='p-price']/strong/i/text()").extract()
        item['photo'] = response.xpath("//div[@class='p-img']/a/img/@source-data-lazy-img").extract()

        item['origin_id'] = []
        item['cate_id'] = []
        for i in range(len(item['goods_id'])):
            item['origin_id'].append(self.origin_id)
            item['cate_id'].append(self.cate_id)

        return item


