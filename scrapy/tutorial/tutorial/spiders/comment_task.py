# -*- coding: utf-8 -*-

import scrapy

from ..items import CommentItem
import re
import urllib.request
import json


class CommentTaskSpider(scrapy.Spider):

    name = "comment_task"
    classes = 50
    comment_page = 20 # <=50

    # 打开存放链接得txt文件
    # links = open("product_url.txt")
    # link = links.readlines()
    # link = link[:classes]
    file = open('crawlers.txt', 'r')
    content = file.readlines()[0]
    content = json.loads(content)

    print(content)
    link, crawler_ids = [], []
    for k,v in enumerate(content):
        link.append(v['product_website'])
        crawler_ids.append(v['id'])

    start_urls = []
    # 从商品链接中提取商品id，并构造评论页url
    for i in range(0, len(link)):
        pattern = r'(\d+)\.html'
        # 这里我们读取的评论是单个手机的评论
        # 可以改变link[]的下标索引来读取不同的手机的评论
        id = re.findall(pattern, link[i])
        # 得到评论数
        commentUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(id[0])
        commentData = urllib.request.urlopen(commentUrl).read().decode("utf-8", "ignore")
        patt1 = r'"CommentCount":(\d+),'
        comment_num = re.findall(patt1, commentData)

        # 得到评论页数
        if int(comment_num[0]) % 30 == 0:
            comment_page_num = int(int(comment_num[0]) / 30)
        else:
            comment_page_num = int(int(comment_num[0]) / 30) + 1

        comment_page_num = comment_page if comment_page_num > comment_page else comment_page_num

        for j in range(1, comment_page_num + 1):
            url = "http://club.jd.com/review/" + str(id[0]) + "-1-" + str(j) + "-0.html"
            url += '?id={}'.format(crawler_ids[i])
            start_urls.append(url)

        # print(start_urls)

    def parse(self, response):

        item = CommentItem()

        id = str(response.url).strip().split("id=")[-1]
        # 用户名
        item["username"] = response.xpath("//div[@class='i-item']/@data-nickname").extract()
        # crawler_id
        item['crawler_id'] = [id for i in range(len(item['username']))]
        # 评论时间
        item["time"] = response.xpath("//div[@class='i-item']/div[@class='o-topic']/span[@class='date-comment']/a/text()").extract()
        # 评论内容
        item["content"] = response.xpath("//div[@class='comment-content']/dl/dd/text()").extract()
        # 星星
        item["star"] = response.xpath("//div[@class='i-item']/div[@class='o-topic']/span[contains(@class, 'star')]").extract()
        # 会员
        item["is_member"] = response.xpath("//div[@class='user']").extract()
        # item["is_member"] = response.xpath("//div[@class='user']/span[@class='u-level']/span[1]/text()").extract()

        return item


