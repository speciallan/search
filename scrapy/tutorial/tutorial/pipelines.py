# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import re


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class CommentPipeline(object):
    """针对每一个items里面的对象"""

    def __init__(self):
        self.file = codecs.open("mydata1.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):

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

        # 处理会员
        for i in range(len(item['is_member'])):
            if '会员' in item['is_member'][i]:
                item['is_member'][i] = 1
            else:
                item['is_member'][i] = 0

        # 写json
        for j in range(0, len(item["username"])):

            crawler_id = item["crawler_id"][j]
            username = item["username"][j]
            time = item["time"][j]
            content = item["content"][j]
            star = item["star"][j]
            is_member = item["is_member"][j]

            goods1 = {"crawler_id":crawler_id,
                      "username": username,
                      "time":time,
                      "content": content,
                      'star': star,
                      'is_member': is_member}

            i = json.dumps(dict(goods1), ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)

        return item

    def open_spider(self, spider):
        print('爬虫开始了...')

    def close_spider(self, spider):
        self.file.close()
        print('爬虫结束了...')


