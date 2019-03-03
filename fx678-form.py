# -*- coding = utf-8 -*-
import requests
import pandas
import numpy
from bs4 import BeautifulSoup

def download_fx678_form(URL, headers):

    resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', id='current_data')
    # print(table.prettify())

    # 收集表头
    columns = [x.text.replace('\xa0', ' ') for x in table.tr.findAll('th')]
    print(columns)

    # 计算表格行数，列数
    rows = [row for row in table.find_all('tr') if row.find('td') != None]
    height = len(rows)
    width = len(columns)

    # 创建表格
    df = pandas.DataFrame(data = numpy.full((height, width), ' ', dtype='U'), columns = columns)
    # 逐行解析表格
    for i in range(len(rows)):
        cells = rows[i].find_all('td')
        if len(cells) == width: # 当行列相同时
            df.iloc[i] = [cell.text.replace(' ', '').replace('\n', '') for cell in cells]

            for j in range(len(cells)): # 需要填充合并的单元格
                if cells[j].has_attr('rowspan'):
                    z = int(cells[j]['rowspan'])
                    df.iloc[i:i+z, j] = [cells[j].text.replace(' ','').replace('\n', '')] * z
        else: # 当行列不同时
            w = len(cells)
            df.iloc[i, width-w:] = [cell.text.replace(' ', '').replace('\n', '') for cell in cells]
    df.to_excel('财经日报.xlsx')

if __name__ == '__main__':
    start_url = 'https://rl.fx678.com/date/20171229.html'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}
    download_fx678_form(start_url, headers)