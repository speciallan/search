# -*- coding: utf-8 -*-

import scrapy

from ..items import CommentItem
import re
import urllib.request


class CommentSpider(scrapy.Spider):

    name = "comment"

    # 打开存放链接得txt文件
    links = open("product_url.txt")
    link = links.readlines()

    # 从商品链接中提取商品id，并构造评论页url
    for i in range(1, 2):
        pattern = r'(\d+)\.html$'
        # 这里我们读取的评论是单个手机的评论
        # 可以改变link[]的下标索引来读取不同的手机的评论
        id = re.findall(pattern, link[0])
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
        start_urls = []
        for i in range(1, comment_page_num + 1):
            url = "http://club.jd.com/review/" + str(id[0]) + "-1-" + str(i) + "-0.html"
            start_urls.append(url)

    def parse(self, response):

        item = CommentItem()
        # 用户名
        item["username"] = response.xpath("//div[@class='i-item']/@data-nickname").extract()
        # 评论内容
        item["content"] = response.xpath("//div[@class='comment-content']/dl/dd/text()").extract()

        return item

