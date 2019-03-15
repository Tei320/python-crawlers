import csv
'''
# 基础写入
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'aa', '20'])
    writer.writerow(['10002', 'bb', '18'])
    writer.writerow(['10003', 'cc', '24'])

# 自定义分隔符
with open('data.csv', 'w', newline='') as cf:
    writer = csv.writer(cf, delimiter= ' ')
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'aa', '20'])
    writer.writerow(['10002', 'bb', '18'])
    writer.writerow(['10003', 'cc', '24'])

# 字典写入
with open('data.csv', 'w', newline='') as cf:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '10001', 'name': 'aa', 'age': 20})
    writer.writerow({'id': '10002', 'name': 'bb', 'age': 18})
    writer.writerow({'id': '10003', 'name': 'cc', 'age': 24})

# 批量写入
with open('data.csv', 'w', newline='') as cf:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([{'id': '10001', 'name': 'aa', 'age': 20}, {'id': '10002', 'name': 'bb', 'age': 18}, {'id': '10003', 'name': 'cc', 'age': 24}])

# 追加写入
with open('data.csv', 'a', newline='') as cf:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writerow({'id': '10004', 'name': 'dd', 'age': 28})

# 写入编码设置
with open('data.csv', 'a', newline='', encoding='utf-8') as cf:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writerow({'id': '10004', 'name': '王伟', 'age': 28})

# 基础读取
with open('data.csv', 'r', encoding='utf-8') as cf:
    reader = csv.reader(cf)
    for row in reader:
        print(row)
'''
import pandas as pd

df = pd.read_csv('data.csv')
print(df)

