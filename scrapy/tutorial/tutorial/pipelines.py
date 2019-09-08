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

        # 写json
        for j in range(0, len(item["username"])):

            username = item["username"][j]
            time = item["time"][j]
            content = item["content"][j]

            goods1 = {"username": username, "time":time, "content": content}
            i = json.dumps(dict(goods1), ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)

        return item

    def open_spider(self, spider):
        print('爬虫开始了...')

    def close_spider(self, spider):
        self.file.close()
        print('爬虫结束了...')


