from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import time

class Action(object):
    def __init__(self):
        self.desired_caps = {
            "platformName": PLATFORM,
            "deviceName": DEVICE_NAME,
            "appPackage": APP_PACKAGE,
            "appActivity": APP_ACTIVITY,
            "noReset": True,
            'unicodeKeyboard': True,
            'resetKeyboard': True
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def scroll(self, distance):
        self.driver.swipe(FLICK_START_X, FLICK_START_Y + distance, FLICK_START_X, FLICK_START_Y)
        time.sleep(SCROLL_SLEEP_TIME)

    def comments(self):
        # 点击进入搜索页面
        classify = self.wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.FrameLayout[@content-desc="分类"]')))
        classify.click()
        search = self.wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="搜索框,维达京东超级品牌日"]')))
        search.set_text(KEYWORD)
        enter = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/aud')))
        enter.click()

        # 商品,选第一个
        view = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.jd.lib.search:id/a2w')))
        view[0].click()

        self.scroll(1100)
        self.scroll(1200)
        # 评论
        tab = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/a25')))
        tab.click()

        while True:
            self.scroll(FLICK_DISTANCE)

if __name__ == '__main__':
    action = Action()
    action.comments()