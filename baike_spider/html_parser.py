import re
import urllib.parse

from bs4 import BeautifulSoup


class HtmlParser(object):
    # 解析网页
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None: # 空
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup) # 处理URL
        new_data = self._get_new_data(page_url, soup) # 处理数据
        return new_urls, new_data

    # 获取网页中的URL
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # 一般URL/item/Python
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links: # 遍历链接
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url) # 转换成绝对URL
            new_urls.add(new_full_url)
        return new_urls

    # 获取网页中的数据
    def _get_new_data(self, page_url, soup):
        res_data = {}
        # url
        res_data['url'] = page_url
        # 标题<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()
        # 介绍 <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        if summary_node != None: # summary不为空，大部分异常来源于此
            res_data['summary'] = summary_node.get_text()

        return res_data