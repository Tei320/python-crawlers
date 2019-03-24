import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from decimal import Decimal

KEYWORD = 'dota2自走棋糖果'
WEIBO_NAME = '你的微博用户名'
WEIBO_PASSWORD = '你的微博密码'

def calculate_the_profit(prices_item, sales_item):
    ''' 计算利润=销量*售价 '''

    temp_sum = Decimal(0)
    # 理论上销量和售价一一对应，这里不做验证
    for i in range(len(sales_item)):
        sale = Decimal(re.match('(\d+)', sales_item[i].text).group())
        price = Decimal(prices_item[i].text)
        print(price, sale)
        temp_sum += price * sale
    print(temp_sum)
    return temp_sum

def crawl_information(browser):
    ''' 爬取每页每个商品的销量和售价 '''

    # 抓取商品的价格和销量
    soup = BeautifulSoup(browser.page_source, 'lxml')
    prices_item = soup.select('.price.g_price.g_price-highlight strong')
    sales_item = soup.find_all(class_='deal-cnt')

    return prices_item, sales_item

def go_to_the_next_page(browser):
    ''' 前往下一个页面 '''

    wait = WebDriverWait(browser, 10)
    next_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-value='44']")))
    next_page.click()


def get_taobao_page(browser):
    ''' 从淘宝首页进入搜索关键字商品，控制网页 '''
    sum = Decimal(0)
    url = 'https://www.taobao.com'
    browser.get(url)
    # 取货搜索框，输入关键字，然后回车进行搜索
    input = browser.find_element_by_id('q')
    input.send_keys(KEYWORD)
    input.send_keys(Keys.ENTER)

    # 由于淘宝自身限制，用selenium爬取网页内容会要求登录，这里用第三方微博登录
    # 从二维码登录切换到密码登录
    login_swith = browser.find_element_by_class_name('login-switch')
    login_swith.click()
    # 点击微博登录
    weibo_login = browser.find_element_by_class_name('weibo-login')
    weibo_login.click()
    # 输入用户名
    username_input = browser.find_element_by_name('username')
    username_input.send_keys(WEIBO_NAME)
    # 输入密码
    password_input = browser.find_element_by_name('password')
    password_input.send_keys(WEIBO_PASSWORD)
    # 提交
    weibo_submit = browser.find_element_by_class_name('W_btn_g')
    weibo_submit.send_keys(Keys.ENTER)

    # 此时登录成功就会跳转到要搜索的页面，先按销量排序，显示等待元素加载
    wait = WebDriverWait(browser, 10)
    sale_sort = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-value='sale-desc']")))
    sale_sort.click()
    # 等待网页内容排序的时间
    time.sleep(3)


    # 然后爬取商品信息
    prices_item, sales_item = crawl_information(browser)
    # 待爬取完毕后，算计当前页利润总和，累计进总和
    sum += calculate_the_profit(prices_item, sales_item)

    # 前往下一页
    go_to_the_next_page(browser)
    time.sleep(3)
    prices_item, sales_item = crawl_information(browser)
    sum += calculate_the_profit(prices_item, sales_item)

    print(sum)

if __name__ == '__main__':
    browser = webdriver.Chrome()
    get_taobao_page(browser)
    browser.close()
