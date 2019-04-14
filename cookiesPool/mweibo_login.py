# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WeiboCookies(object):
    def __init__(self, username, password, browser):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def login(self):
        '''
        输入用户名密码并点击登陆微博
        :return:
        '''
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password[0].send_keys(self.password)
        time.sleep(1)
        submit.click()

    def password_error(self):
        '''
        判断是否密码错误
        :return:
        '''
        try:
            return WebDriverWait(self.browser, 5).until(EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False

    def login_successful(self):
        '''
        判断是否登陆成功
        :return:
        '''
        try:
            return WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lite-iconf-profile')))
        except TimeoutException:
            return False

    def get_cookies(self):
        '''
        获取cookies
        :return:
        '''
        return self.browser.get_cookies()

    def main(self):
        '''
        入口
        :return:
        '''
        self.login()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        if self.login_successful():
            return {
                'status': 1,
                'content': self.get_cookies()
            }
        else:
            return {
                'status': 3,
                'content': '登陆失败'
            }