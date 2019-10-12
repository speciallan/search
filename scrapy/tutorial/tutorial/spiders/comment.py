# -*- coding: utf-8 -*-

import scrapy

from ..items import CommentItem
import re
import urllib.request


class CommentSpider(scrapy.Spider):

    name = "comment"
    classes = 5
    comment_page = 20 # <=50

    # 打开存放链接得txt文件
    links = open("product_url.txt")
    link = links.read()
    link = link.split('-----')[:-1]
    link = link[:classes]

    start_urls = []
    # 从商品链接中提取商品id，并构造评论页url
    for i in range(0, len(link)):
        pattern = r'(\d+)\.html---(.*)'
        # 这里我们读取的评论是单个手机的评论
        # 可以改变link[]的下标索引来读取不同的手机的评论
        # match = re.findall(pattern, link[i])[0]
        origin_id, goods_id, cate_id, url, title, price, photo, comment_num = link[i].split('---')

        # 得到评论页数
        if int(comment_num) % 30 == 0:
            comment_page_num = int(int(comment_num) / 30)
        else:
            comment_page_num = int(int(comment_num) / 30) + 1

        comment_page_num = comment_page if comment_page_num > comment_page else comment_page_num

        for j in range(1, comment_page_num + 1):
            url = "https://club.jd.com/review/" + str(goods_id) + "-1-" + str(j) + "-0.html" + '?id={}---{}---{}'.format(origin_id, goods_id, cate_id)
            start_urls.append(url)

    def parse(self, response):

        item = CommentItem()

        # item["goods_id"] = response.xpath("//li[@class='p-name']/a/@href").extract()
        # 用户名
        item["username"] = response.xpath("//div[@class='i-item']/@data-nickname").extract()
        # crawler_id
        # item['crawler_id'] = [id for i in range(len(item['username']))]
        # 评论时间
        item["time"] = response.xpath("//div[@class='i-item']/div[@class='o-topic']/span[@class='date-comment']/a/text()").extract()
        # 评论内容
        item["content"] = response.xpath("//div[@class='comment-content']/dl/dd/text()").extract()
        # 星星
        item["star"] = response.xpath("//div[@class='i-item']/div[@class='o-topic']/span[contains(@class, 'star')]").extract()
        # 会员
        item["is_member"] = response.xpath("//div[@class='user']").extract()
        # item["is_member"] = response.xpath("//div[@class='user']/span[@class='u-level']/span[1]/text()").extract()

        item["avater"] = response.xpath("//div[@class='user']/div[@class='u-icon']/img/@src | //div[@class='user']/div[@class='u-icon']/a/img/@src").extract()

        # goodsid
        id = str(response.url).strip().split("id=")[-1]
        origin_id, goods_id, cate_id = id.split('---')
        item['origin_id'] = [origin_id for i in range(len(item['content']))]
        item['goods_id'] = [goods_id for i in range(len(item['content']))]
        item['cate_id'] = [cate_id for i in range(len(item['content']))]

        return item

