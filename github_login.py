import requests
from pyquery import PyQuery as pq
from config import USERNAME, PASSWORD

class Login(object):
    def __init__(self):
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        # 请求登陆页面
        resp = self.session.get(self.login_url)
        # 提取 authenticity_token 的 value，
        doc = pq(resp.text)
        token = doc('input[name="authenticity_token"]').attr("value").strip()
        return token

    def login(self, username, passwrod):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': username,
            'password': passwrod,
        }

        resp = self.session.post(self.post_url, data=post_data)
        print(resp.status_code)
        if resp.status_code == 200:
            print(resp.url)


a = Login()
a.login(USERNAME, PASSWORD)