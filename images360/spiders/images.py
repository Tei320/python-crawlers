# -*- coding: utf-8 -*-
import json

import scrapy
from urllib.parse import urlencode
from images360.items import ImageItem

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new', 'temp': '1'}
        base_url = 'http://images.so.com/zj?'
        for i in range(3):
            data['sn'] = i * 30
            params = urlencode(data)
            url = base_url + params
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item

