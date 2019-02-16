class UrlManager(object):

    def __init__(self): # 初始化URL集合
        self.new_urls = set() # 新URL集合
        self.old_urls = set() # 已经处理了的旧URL集合

    def add_new_url(self, url):
        if url is None:    # 非空
            return
        if url not in self.new_urls and url not in self.old_urls: # 确认URL是未出现过的新URL
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:  # 非空
            return
        for url in urls: # 依次按照单个新URL处理
            self.add_new_url(url)


    def has_new_url(self): # 判断新URL集合是否为空
        return len(self.new_urls) != 0

    def get_new_url(self): # 获取一个新的URL
        new_url = self.new_urls.pop() # 从新URL集合取出
        self.old_urls.add(new_url)    # 加入旧URL集合
        return new_url

