# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 域名范围
    allowed_domains = ['movie.douban.com']
    # 入口URL
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # //div[@class='article']//ol[@class='grid_view']/li
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            # xpath匹配序号，名称，介绍，星级，评论数，描述
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content: # 处理字符
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span[1]/text()").extract_first()
            # print(douban_item)
            # 数据yield到piplines
            yield douban_item

        # xpath匹配下一页链接
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link: # 如果有下一页，继续爬取
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
