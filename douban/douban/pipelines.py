# -*- coding: utf-8 -*-
import pymongo
from douban.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_collection
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):

    def __init__(self):
        host = mongo_host # 地址
        port = mongo_port # 端口
        dbname = mongo_db_name # 数据库名称
        sheetname = mongo_db_collection # 表
        client = pymongo.MongoClient(host = host, port = port) # 建立数据库链接
        mydb =client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item) # 转成字典
        self.post.insert(data) # 插入数据
        return item
