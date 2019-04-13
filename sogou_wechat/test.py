import requests

proxy = '110.52.235.54:9999'
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}
url = 'https://weixin.sogou.com/weixin?type=2&query=nba'
resp = requests.get(url, proxies=proxies)
print(resp.text)