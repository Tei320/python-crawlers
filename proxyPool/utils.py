import requests
from requests.exceptions import ConnectionError

base_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}

def get_page(url, options={}):
    '''
    抓取代理
    :param url: 需要爬取URL地址
    :param options: 其他headers选项
    :return: response.text or None
    '''
    headers = dict(base_headers, **options)
    print('正在抓取', url, '...')

    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
    return None
