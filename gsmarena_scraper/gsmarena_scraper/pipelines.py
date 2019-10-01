# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        file = open('items.json', 'a')
        file.write(line)
        file.close()
        return item