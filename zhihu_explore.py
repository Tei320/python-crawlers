import requests
from pyquery import PyQuery
from fake_useragent import UserAgent

url = 'https://www.zhihu.com/explore'

headers = {
    'user-agent': UserAgent().random
}

resp = requests.get(url, headers=headers)

doc = PyQuery(resp.text)
items = doc('.explore-tab .explore-feed.feed-item').items()
for item in items:
    question = item('h2').text()
    author = item('.author-link').text()
    answer = PyQuery(item('.content').html()).text()
    with open('explore.txt', 'a', encoding='utf-8') as fp:
        fp.write('\n'.join([question, author, answer]))
        fp.write('\n' + '='* 48 + '\n')