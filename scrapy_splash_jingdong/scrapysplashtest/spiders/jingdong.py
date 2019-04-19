# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy_splash import SplashRequest
from scrapysplashtest.items import GoodItem

script = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  js = string.format("document.querySelector('.page .input-txt').value=%d;document.querySelector('.page .btn.btn-default').click()", args.page)
  splash:evaljs(js)
  assert(splash:wait(args.wait))
  local scroll_to = splash:jsfunc("window.scrollTo")
  scroll_to(0, 6000)
  splash:set_viewport_full()
  assert(splash:wait(args.wait))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""

class TaobaoSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    url = 'https://search.jd.com/Search?keyword=ipad'

    def start_requests(self):
        for page in range(1, 2):
            yield SplashRequest(url=self.url, callback=self.parse, endpoint='execute',
                            args={'lua_source': script, 'page': page,  'wait': 7})

    def parse(self, response):
        goods = response.xpath('//div[@id="J_goodsList"]/ul/li')
        #print(len(goods))
        for good in goods:
            item = GoodItem()
            item['name'] = good.xpath('string(.//div[contains(@class, "p-name")]/a/em)').extract_first()
            item['name'] = good.xpath('string(.//div[contains(@class, "p-name")]/a/em)').extract_first()
            item['price'] = good.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            item['comment'] = good.xpath('.//div[@class="p-commit"]/strong/a/text()').extract_first()
            item['shop'] = good.xpath('.//div[@class="p-shop"]/span/a/text()').extract_first()
            yield item
