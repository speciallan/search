# -*- coding: utf-8 -*-

import scrapy

from search.scrapy.tutorial.tutorial.items import JdPhoneItem
import re


class JdPcSpider(scrapy.Spider):

    name = "jd_pc"
    allowed_domains = ["jd.com"]
    start_urls = []
    # 获取前十页的链接
    for i in range(1, 11):
        url = "https://search.jd.com/Search?keyword=笔记本&enc=utf-8&page=" + str(2 * i - 1)
        start_urls.append(url)

    # 获取商品的链接，标题，价格
    def parse(self, response):

        item = JdPhoneItem()

        # 获取标题
        item["title"] = response.xpath("//div[@class='p-name p-name-type-2']/a[@target='_blank']/@title").extract()
        # 得到价格
        item["price"] = response.xpath("//div[@class='p-price']/strong/@data-price").extract()
        # 得到链接
        item["url"] = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()

        # 将链接存入txt文件中，方便抓取评论，
        for i in range(0, len(item["url"])):
            # 过滤无用链接
            pattern = 'https'
            bool = re.match(pattern, item["url"][i])
            if (bool):
                continue
            else:
                with open('product_pc_url.txt', 'a') as f:
                    f.write(item["url"][i] + '---' + item['title'][i] + '\n')
        return item


