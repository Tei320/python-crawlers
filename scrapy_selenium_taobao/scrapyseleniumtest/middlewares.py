# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware():
    def __init__(self, timeout=None, weibo_username=None, weibo_password=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.weibo_username = weibo_username
        self.weibo_password = weibo_password
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

        # 淘宝登录
        self.browser.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3DiPad')
        # 切换到密码登录
        login_swith = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-switch')))
        login_swith.click()
        # 点击微博登录
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'weibo-login')))
        weibo_login.click()
        # 输入微博用户名
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_input.send_keys(self.weibo_username)
        # 输入微博密码
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.weibo_password)
        # 提交
        weibo_submit = self.browser.find_element_by_class_name('W_btn_g')
        weibo_submit.send_keys(Keys.ENTER)


    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   weibo_username=crawler.settings.get('WEIBO_USERNAME'),
                   weibo_password=crawler.settings.get('WEIBO_PASSWORD'))

    def process_request(self, request, spider):
        '''
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        '''
        self.logger.debug('Chrome headless is Starting')
        page = request.meta.get('page', 1)
        try:
            # 不是第一页，跳转翻页
            if page > 1:
                # 跳转页面输入框
                input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                # 跳转确定
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                # 输入需要跳转的页面
                input.send_keys(page)
                submit.click()
            # 等待页面跳转
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            # 下拉界面到最下方
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # 等待商品页面加载完毕
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, request=request, status=500)