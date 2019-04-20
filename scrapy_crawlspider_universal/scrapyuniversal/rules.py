from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule

rules = {
    'china': (
        Rule(LinkExtractor(allow='article\/.*\.html',
                           restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]/div[@class="conR"]/h2/a'),
             callback='parse_item'),
        # 当是指定页面时，自动下一页不爬取
        # Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(.,"下一页")]'))
    )
}