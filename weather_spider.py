import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyecharts import Bar

ALL_DATA = []

def parse_page(url):
    headers = {
        'user-agent': UserAgent().random
    }
    resp = requests.get(url, headers=headers)
    html_doc = resp.content.decode()
    # 使用容错性最好，效率较低的html5lib解析器
    soup = BeautifulSoup(html_doc, 'html5lib')
    conMidtab = soup.find('div', class_= 'conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            if index == 0:
                tds = tr.find_all('td')
                city = tds[1].a.string
                min_temp = tds[-2].string
            else:
                tds = tr.find_all('td')
                city = tds[0].a.string
                min_temp = tds[-2].string
                ALL_DATA.append({'city': city, 'min_temp': int(min_temp)})

if __name__ == '__main__':
    URL_LIST = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml',
    ]
    for url in URL_LIST:
        parse_page(url)

    ALL_DATA.sort(key = lambda data:data['min_temp'])
    top_data = ALL_DATA[:10]
    # print(top_data)
    cities = []
    temps = []
    for data in top_data:
        cities.append(data['city'])
        temps.append(data['min_temp'])
    bar = Bar('中国天气最低气温排行榜')
    bar.add('城市', cities, temps, is_yaxis_inverse=True)
    bar.render()