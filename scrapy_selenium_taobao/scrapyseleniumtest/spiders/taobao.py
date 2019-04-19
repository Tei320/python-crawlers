# -*- coding: utf-8 -*-
import time

import scrapy
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapyseleniumtest.items import ProductItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        keyword = self.settings.get('KEYWORD')
        url = self.base_url + quote(keyword)
        for page in range(1, self.settings.get('MAX_PAGE')):
            yield scrapy.Request(url=url, callback=self.parse, cookies=list, meta={'page': page}, dont_filter=True)


    def parse(self, response):
        print("------------------")
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"]//div[contains(@class, "item")]')
        print("***********", products)
        for product in products:
            item = ProductItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            print(item)