import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderMain(): # 爬虫主程序

    def __init__(self): # 初始化
        self.urls = url_manager.UrlManager()  # 调度器
        self.downloader = html_downloader.HtmlDownLoader()  # 网页下载器
        self.parser = html_parser.HtmlParser()  # 网页解析器
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url): # 爬取程序
        count = 1 # 网页计数器
        self.urls.add_new_url(root_url)  # 添加起始URL到待爬URL
        while self.urls.has_new_url():  # 是否存在待爬URL
            try:
                new_url = self.urls.get_new_url()  # 获取一个新url
                html_cont = self.downloader.download(new_url)  # 下载网页内容
                new_urls, new_data = self.parser.parse(new_url, html_cont)  # 解析网页内容
                self.urls.add_new_urls(new_urls)  # 新URL加入待爬页面
                self.outputer.collet_data(new_data)  # 保存数据

                if count == 100: # 只爬取100个页面
                    break
                count += 1
            except: # 处理异常情况
                print("craw failed")

        self.outputer.output_html()  # 输出数据


if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/Python/407313"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
