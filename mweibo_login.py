# coding: utf-8
import requests
from config import WEIBO_USERNAME, WEIBO_PASSWORD

class Login(object):
    def __init__(self):
        self.login_url = 'https://passport.weibo.cn/signin/login'
        self.post_url = 'https://passport.weibo.cn/sso/login'
        self.logined_url = 'https://m.weibo.cn/users/3075974333?set=1'
        self.session = requests.Session()

    def login(self, username, password):
        post_data = {
            'username': username,
            'password': password,
            'savestate': '1',
            'r': '',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }
        headers = {
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?display=0&retcode=6102',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'
        }

        resp = self.session.post(self.post_url, data=post_data, headers=headers)

    def profile(self):
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://m.weibo.cn/home/setting',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'
        }
        resp = self.session.get(self.logined_url, headers=headers)
        print(resp.url)
        print(resp.encoding)
        print(resp.status_code)
        print(resp.text)

a = Login()
a.login(WEIBO_USERNAME, WEIBO_PASSWORD)
a.profile()