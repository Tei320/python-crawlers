from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from processor import Processor
from config import *
import time

class Moments(object):
    def __init__(self):
        '''
        初始化
        '''
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,           # 声明是ios还是Android系统
            'deviceName': DEVICE_NAME,    # 连接的设备名称
            'appPackage':  APP_PACKAGE,    # 查看AndroidManiFest.xml获取
            'appActivity': APP_ACTIVITY,
            'noReset': True               # 启动结束都不清空应用数据
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)      # 建立 session
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.processor = Processor()
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def login(self):
        try:
            login = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4i')))
            login.click()
        except Exception as e:
            print('已登录。', e.args)
            return

        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/ki')))
        phone.set_text(USERNAME)

        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axu')))
        next.click()

        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/ki')))
        password.set_text(PASSWORD)

        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axu')))
        submit.click()

        tongxunlu = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/az_')))
        tongxunlu.click()

    def enter(self):
        '''
        进入朋友圈
        :return:
        '''
        tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="发现"]')))
        tab.click()

        moments = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="朋友圈"]')))
        moments.click()

    def crawl(self):
        '''
        爬取内容
        :return:
        '''
        while True:
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/avj"]//android.widget.FrameLayout')))
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/b5p').get_attribute('text')
                    # 正文
                    try:
                        content = item.find_element_by_id('com.tencent.mm:id/eje').get_attribute('text')
                    except Exception as e:
                        # print(e.args)
                        content = ''
                    # 日期
                    date = item.find_element_by_id('com.tencent.mm:id/eee').get_attribute('text')
                    date = self.processor.date(date)
                    data = {
                        'nickname': nickname,
                        'content': content,
                        'date': date
                    }
                    print(data)
                    # 插入MongoDB
                    self.collection.update_one({'nickname': nickname, 'content': content, 'date': date}, {'$set': data}, True)
                    time.sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    pass

if __name__ == '__main__':
    moments = Moments()
    moments.login()
    moments.enter()
    moments.crawl()
