from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

desired_caps = {}
desired_caps['platformName'] = "Android"          # 声明是ios还是Android系统
desired_caps['deviceName'] = '127.0.0.1:62001'   # 连接的设备名称
desired_caps['appPackage'] = 'com.tencent.mm'
desired_caps['appActivity'] = '.ui.LauncherUI'

server = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(server, desired_caps)      # 建立 session

time.sleep(3)

# appium desktop 录制的代码
el1 = driver.find_element_by_id("com.tencent.mm:id/drq")
el1.click()
el2 = driver.find_element_by_id("com.tencent.mm:id/ji")
el2.send_keys("18877665544")
el3 = driver.find_element_by_id("com.tencent.mm:id/ast")
el3.click()


driver.quit()      # 退出 session
