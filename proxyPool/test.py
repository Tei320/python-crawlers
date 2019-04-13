import requests
base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.'
}
proxy = {
    'https': 'http://116.209.59.60:9999'
}
url = 'https://weixin.sogou.com/weixin?type=2&query=nba'

resp = requests.get(url=url, headers=base_headers, proxies=proxy)
print(resp.status_code)
print(resp.text)