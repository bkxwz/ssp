# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SspPipeline(object):
#     def process_item(self, item, spider):
#         return item
import  pymongo
import time
from scrapy.item import Item
from datetime import datetime

#处理时间和文章格式
class SspDataClean(object):
    def process_item(self, item, spider):
        c_time = item['c_time']
        # date_time = datetime.strftime(date_time,)
        #  = time.ctime(c_time)
        #时间戳转datetime对象
        d = datetime.fromtimestamp(c_time)
        # str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        str1 = d.strftime("%Y-%m-%d %H:%M:%S")
        item['c_time'] = str1

        #清理文章格式
        content = item['content']
        L = []
        for i in content:
            v = i.strip()
            if v:
                L.append(i)
        item['content'] = L
        return item

#储存数据到mongodb
class SspPipeline(object):
    collection = 'wenzhang'
    # c = 4
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''

        self.client.close()
        print('close sussessfully')

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''
        # if not item['title']:
        #     return item
        # print('进入数据库')
        # data = {
        #     'title': item['title'],
        #     'content': item['content'],
        #     'author' : item['author'],
        #     'article_time' : item['article_time'] ,
        #     'article_id' : item['article_id'],
        #     'url' : item['url'],
        #     'keywords' : item['keywords'],
        #     'c_time' : item['c_time']
        #
        #
        # }
        data = dict(item) if isinstance(item,Item) else item
        table = self.db[self.collection]
        table.insert_one(data)
        return item