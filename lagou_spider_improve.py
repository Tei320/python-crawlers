# -*- codeing: utf-8 -*-

import json
import requests
import time


# 第一次请求
def get_first_web_cookie():
    req_url1 = 'https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput='
    headers1 = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'
    }
    resp1 = requests.get(req_url1, headers=headers1)
    # print(resp1.text.encode(resp1.encoding).decode())
    # 获取cookies
    cookies1 = requests.utils.dict_from_cookiejar(resp1.cookies)
    # print(cookies1)
    return cookies1


# 构造cookie
def structrue_cookie():
    cookies1 = get_first_web_cookie()
    time.sleep(2)
    cookies1['user_trace_token'] = cookies1['LGRID']
    cookies1['LGUID'] = cookies1['LGRID']
    cookies1['LGSID'] = cookies1['LGRID']
    # print(cookies1)
    cookies2 = {
        '_ga': 'GA1.2.99274319.1551621388',
        '_gid': 'GA1.2.1953957939.1551621388',
        'user_trace_token': '20190303215306-ac286bfa-3dbb-11e9-87ec-525400f775ce',
        'LGUID': '20190303215306-ac286f4f-3dbb-11e9-87ec-525400f775ce',
        'LGSID': '20190304142918-d6cdf9c2-3e46-11e9-8bf0-525400f775ce',
        'index_location_city': '%E6%9D%AD%E5%B7%9E',
        'JSESSIONID': 'ABAAABAAAFCAAEG435BE274018366CA7914FCE89565C1F4',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1551627858,1551628040,1551670729,1551682021',
        'X_MIDDLE_TOKEN': '7795483921bc533e04adb914b42d8cef',
        'TG-TRACK-CODE': 'search_code',
        '_gat': '1',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1551686270',
        'LGRID': '20190304155426-bb390b59-3e52-11e9-8a08-5254005c3644',
        'SEARCH_ID': '7fdbe62a48f1450f9a22530530a68688'
    }
    # 更新cookie
    cookies2.update(cookies1)
    # print(cookies2)
    return cookies2

def crawl_position_information():
    cookies2 = structrue_cookie()
    headers2 = {
        'Connection': 'keep-alive',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 共30页，逐页请求
    position_results = []
    for pn in range(1, 31):
        form_data = {
            'first': 'true',
            'pn': pn,
            'kd': 'python'
        }
        req_url2 = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false'
        resp2 = requests.post(req_url2, headers=headers2, cookies=cookies2, data=form_data)

        page_results = resp2.json()['content']['positionResult']['result']
        print('-' * 30)
        for result in page_results:
            print(result)
        print('-' * 30)
        position_results.extend(page_results)
        time.sleep(5)

    line = json.dumps(position_results, ensure_ascii=False)
    with open('lagou_python_position.json', 'wb') as fp:
        fp.write(line.encode('utf-8'))


if __name__ == '__main__':
    crawl_position_information()
