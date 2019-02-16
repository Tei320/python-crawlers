import urllib.request


class HtmlDownLoader(object):
    def download(self, url):
        if url is None: # url不为空
            return None

        response = urllib.request.urlopen(url)

        if response.getcode() != 200: # 访问不成功
            return None

        return response.read() # 读取response内容
