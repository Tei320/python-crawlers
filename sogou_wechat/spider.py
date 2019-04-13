from requests import Session, ReadTimeout, ConnectionError
import requests
from urllib.parse import urlencode
from db import RedisQueue
from request import WeixinRequest
from settings import VALID_STATUSES
from pyquery import PyQuery as pq
from settings import MAX_FAILED_TIME, PROXY_POOL_URL

class Spider(object):
    base_url = 'https://weixin.sogou.com/weixin'
    keyword = 'NBA'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SUV=00A00B5AB79B98A75B56AA93A616E713; CXID=98F2DE60C4FFA370BA1B6B0D4A47AD45; SUID=356117245E68860A5B62B4E5000B2140; ABTEST=8|1555121000|v1; IPLOC=CN3306; weixinIndexVisited=1; SNUID=493FC3502327A57DF152EF0B23585A25; JSESSIONID=aaaikt2ZNvhox8zfS_qOw; sct=1; ppinf=5|1555125604|1556335204|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OlRpbnRpbjkzN3xjcnQ6MTA6MTU1NTEyNTYwNHxyZWZuaWNrOjk6VGludGluOTM3fHVzZXJpZDo0NDpvOXQybHVGd0JaSnh3WFk3amtTemFET193WlFNQHdlaXhpbi5zb2h1LmNvbXw; pprdig=fu3YLOziP_GZ9EirPNuy9MvITksqchqImz41kSG1GQkZ3iXjVcOjCLwXpPlnemdAeJw6hTkgBkEtxPvzG-SjsG7MTZWbfjx09AcoQT965xhYgyvWPA5J5bnHzBX5xWDt5POkk9hBIlHq69XQeltnH8eWjDk4_46xJi1YhjyeDjY; sgid=26-37898303-AVyxVWQGlluVNg1a7Bcpiam8; ppmdig=1555125604000000d3186b1d50b395065c19cac2821391a1',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'
    }
    session = Session()
    queue = RedisQueue()

    def get_proxy(self):
        '''
        从代理池获取代理
        :return:
        '''
        '''
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HJ418XB78UK222HD"
        proxyPass = "5D5DB07D7DE9E07A"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        return proxyMeta
        '''
        try:
            resp = requests.get(PROXY_POOL_URL)
            if resp.status_code == 200:
                print('Get Prxoy:', resp.text)
                return resp.text
            return None
        except requests.ConnectionError:
            print('代理服务器连接超时')
            return None

    def start(self):
        # 全局更新
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(weixin_request)

    def parse_index(self, resp):
        '''
        解析索引页
        :param resp: 响应
        :return: 新响应
        '''
        doc = pq(resp.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.arrr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url = str(next)
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield weixin_request

    def parse_detail(self, resp):
        '''
        解析详情页
        :param resp: 响应
        :return: 微信公众号文章
        '''
        doc = pq(resp.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content ').text(),
            'date': doc('#publish_time').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:first-child > span').text()
        }
        yield data

    def error(self, weixin_request):
        '''
        处理错误
        :param weixin_request: 请求
        :return:
        '''
        weixin_request.fail_time = weixin_request.fail_time + 1
        print('Request Failed', weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)

    def request(self, weixin_request):
        '''
        执行请求
        :param weixin_request: 请求
        :return: 响应
        '''
        try:
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                print(proxy)
                if proxy:
                    proxies = {
                        'http': proxy,
                        'https': proxy
                    }
                    return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)
                    # return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False)
            # return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def schedule(self):
        '''
        调度请求
        '''
        while not self.queue.empty():
            weixin_request = self.queue.pop()
            callback = weixin_request.callback
            print('Schedule->', weixin_request.url)
            resp = self.request(weixin_request)
            if resp and resp.status_code in VALID_STATUSES:
                results = list(callback(resp))
                if results:
                    for result in results:
                        print('New Result', result)
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            # self.mysql.insert('articles', result)
                            print('articles', result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def run(self):
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()