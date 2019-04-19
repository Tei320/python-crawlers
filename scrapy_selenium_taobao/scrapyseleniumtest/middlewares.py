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
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.PhantomJS(service_args=service_args)
        self.browser.set_window_size(1920, 1080)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.browser.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3DiPad')
        login_swith = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-switch')))
        login_swith.click()
        # 点击微博登录
        time.sleep(3)
        with open('ttt.text', 'w', encoding='utf-8') as fp:
            fp.write(self.browser.page_source)
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'weibo-login')))
        weibo_login.click()
        # 输入用户名
        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_input.send_keys('18106892890')
        # 输入密码
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('weibo_4882089')
        # 提交
        weibo_submit = self.browser.find_element_by_class_name('W_btn_g')
        weibo_submit.send_keys(Keys.ENTER)


    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))

    def process_request(self, request, spider):
        '''
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        '''
        self.logger.debug('PhantomJS is Starting')
        page = request.meta.get('page', 1)
        try:
            time.sleep(10)
            print(request.url)
            # self.browser.get(request.url)
            if page > 1:
                input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)') # 下拉操作
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, request=request, status=500)