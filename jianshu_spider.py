import re
import requests
from bs4 import BeautifulSoup

def check_image_element(tag): # 判断满足要求img元素
    return tag.name == 'img' and tag.has_attr('data-original-src')

def get_jianshu_image_links(URL, headers):

    resp = requests.get(URL, headers=headers) # 抓取网页
    soup = BeautifulSoup(resp.text, 'html.parser')
    imgs = soup.find_all(check_image_element) # 寻找满足要求的元素
    for img in imgs:
        download_jianshu_image('https:' + img['data-original-src'], headers)

def download_jianshu_image(URL, headers):

    print(URL)
    filename = re.search('\d+\-[0-9a-z]+\.jpg', URL).group() # 匹配图片名
    print(filename)

    # 抓取图片网页，打开流传输,可避免大量数据立即读入内存
    with requests.get(URL, headers=headers, stream=True) as resp:
        with open(filename, 'wb') as fd: # 打开文件
            for chunk in resp.iter_content(128):
                fd.write(chunk)    # 存入数据块
    '''
    with requests.get(URL, headers=headers) as resp:
        with open(filename, 'wb') as fd:  # 打开文件
            fd.write(resp.content)  # 存入数据块
    '''

if __name__=='__main__':
    strat_url = 'https://www.jianshu.com/p/1376959C3679'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}
    get_jianshu_image_links(strat_url, headers)