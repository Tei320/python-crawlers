import re
import threading
import requests
import os
from bs4 import BeautifulSoup

glock = threading.Lock() # 互斥锁
INITIAL_DIRECTORY = 'images' # 图片保存目录
ORIGINAL_URL = 'https://www.doutula.com'
FACE_URL_LIST = [] # 表情图片的URL列表
PAGE_URL_LIST = ['https://www.doutula.com/photo/list/?page=1'] # 各个分图片页面网址


# 处理特殊的图片名字
def process_special_filename(filename):
    if filename.endswith('!dta'):
        filename = filename[:-4]
    return filename

# 从链接里获取图片名
def get_filename_from_url(url):
    filename = url.split('/').pop()
    return process_special_filename(filename)

# 下载图片
def download_image(url):
    filename = get_filename_from_url(url)
    # print(filename)
    path = os.path.join(INITIAL_DIRECTORY, filename)
    # 下载图片保存到本地
    with requests.get(url) as resp:
        with open(path, 'wb') as fd:
            fd.write(resp.content)

# 爬取网页中图片的链接
def craw_image_links(url):
    # 请求网页
    resp = requests.get(url)
    html_doc = resp.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # 抓取下一页链接
    try:
        next_link = soup.find('a', attrs={'rel': 'next'})['href']
        limit = re.findall('\d+', next_link)[0] # 限制抓取页数，方便测试
        # print(next_link, limit)
        if next_link and int(limit) < 30:
            next_link = ''.join([ORIGINAL_URL, next_link])
            glock.acquire()
            PAGE_URL_LIST.append(next_link) # 新下一页链接加入PAGE_URL_lIST
            glock.release()
    except:
        print('----end-----')

    # 去抓图片链接
    image_list = soup.find_all('img', class_='img-responsive lazy image_dta')
    links = [image['data-original'] for image in image_list]
    # print(len(links))
    glock.acquire()
    for link in links:
        FACE_URL_LIST.append(link) # 图片URL加入表情URL队列
    glock.release()


# 生产者获取网页链接，追加图片链接和网页链接
def procuder():
    while True:
        glock.acquire()
        if len(PAGE_URL_LIST) == 0:
            glock.release()
            break
        else:
            page_url = PAGE_URL_LIST.pop()
            glock.release()
            craw_image_links(page_url)

# 消费者获取图片链接，下载图片
def consumer():
    while True:
        glock.acquire()
        if len(FACE_URL_LIST) == 0:
            glock.release()
            continue
        else:
            image_url = FACE_URL_LIST.pop()
            glock.release()
            download_image(image_url)
            # print("download done")


if __name__ == '__main__':
    # strat_url = 'https://www.doutula.com/photo/list/?page=1'
    # craw_image_links(strat_url)
    for x in range(3): # 开启3个生产者
        th = threading.Thread(target=procuder)
        th.start()

    for x in range(16): # 开启16个消费者
        th = threading.Thread(target=consumer)
        th.start()