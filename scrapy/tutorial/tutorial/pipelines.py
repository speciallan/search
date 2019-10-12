# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import re
from .items import ProductItem
import urllib.request


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class CommentPipeline(object):
    """针对每一个items里面的对象"""


    def process_item(self, item, spider):

        if isinstance(item, ProductItem):

            item['comment_num'] = []
            for i in range(len(item["goods_id"])):
                # 得到评论数
                # https://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=
                commentUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(item['goods_id'][i])
                commentData = urllib.request.urlopen(commentUrl).read().decode("utf-8", "ignore")
                patt1 = r'"CommentCount":(\d+),'
                comment_num = re.findall(patt1, commentData)
                item['comment_num'].append(comment_num[0])

            # 将链接存入txt文件中，方便抓取评论，
            for i in range(0, len(item["url"])):

                item["url"][i] = 'https:' + item["url"][i]
                item["photo"][i] = 'https:' + item["photo"][i]

                with open('product_url.txt', 'a') as f:
                    f.write(item['origin_id'][i] + '---' + item['goods_id'][i] + '---' + item['cate_id'][i] + '---' + item["url"][i] + '---' + item['title'][i] + '---' + item['price'][i] + '---' + item['photo'][i] + '---' + item['comment_num'][i] + '-----')
                    f.close()

            return item

        # 评论pipeline
        count = 0

        # print('len:', len(item['time']), len(item['content']))
        # print(item['content'])


        for i in range(len(item["time"])):

            # time
            item['time'][i] = item["time"][i].replace('\r\n', '')

        # 去掉换行符与回车符
        for i in range(len(item["content"])):

            # content
            pattern = re.match('(\r\n)+', item["content"][i])
            if (not pattern):
                item["content"][count] = item["content"][i]
                count += 1
            else:
                continue

        # 处理星星
        for i in range(len(item['star'])):
            # result = re.match(r'sa(\d+)', item["star"][i])
            result = re.findall(r'\d+', item['star'][i])[0]
            item['star'][i] = int(result)

        # 处理头像
        for i in range(len(item['avater'])):
            item['avater'][i] = 'https:' + item['avater'][i]

        # 处理会员
        for i in range(len(item['is_member'])):
            if '会员' in item['is_member'][i]:
                item['is_member'][i] = 1
            else:
                item['is_member'][i] = 0

        # 写json
        file = codecs.open("mydata1.json", "a", encoding="utf-8")
        for j in range(0, len(item["username"])):

            # crawler_id = item["crawler_id"][j]
            origin_id = item["origin_id"][j]
            goods_id = item["goods_id"][j]
            username = item["username"][j]
            time = item["time"][j]
            content = item["content"][j]
            star = item["star"][j]
            is_member = item["is_member"][j]
            avater = item["avater"][j]

            goods1 = {
                # "crawler_id":crawler_id,
                      "origin_id": origin_id,
                      "goods_id": goods_id,
                      "username": username,
                      "time":time,
                      "content": content,
                      'star': star,
                      'is_member': is_member,
                      'avater': avater}

            i = json.dumps(dict(goods1), ensure_ascii=False)
            line = i + '-----'
            file.write(line)
        file.close()

        return item

    def open_spider(self, spider):
        print('爬虫开始了...')

    def close_spider(self, spider):
        print('爬虫结束了...')


