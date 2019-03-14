import json
import re
import requests
from fake_useragent import UserAgent

def fetch_movie_information(html_doc):
    pattern = re.compile('class="board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?class="name">.*?>(.*?)</a>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>', re.S)
    results = re.findall(pattern, html_doc)
    for result in results:
        yield {
            'index': result[0],
            'image': result[1],
            'titile': result[2],
            'actor': result[3].strip(),
            'time': result[4],
            'score': result[5] + result[6]
        }

def get_one_page(page_url):
    headers  = {
        'user-agent': UserAgent().random
    }
    response = requests.get(page_url, headers)
    # print(response.encoding)
    return  response.text

def write_to_file(content):
    with open('maoyan_movie_top100.txt', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(content, ensure_ascii=False) + '\n')

def iterate_over_all_page(base_url):
    for i in range(0, 10):
        page_url = base_url + str(i * 10)
        html_doc = get_one_page(page_url)
        for item in fetch_movie_information(html_doc):
            print(item)
            write_to_file(item)

if __name__ == '__main__':
    base_url = 'https://maoyan.com/board/4?offset='
    iterate_over_all_page(base_url)
