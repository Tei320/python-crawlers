from pandas import read_csv
import pandas

# 读入数据
df = read_csv('data.csv', encoding='utf-8')

# 字符串时间转化为datetime格式，并计算时间差
df['DealDateTime'] = pandas.to_datetime(df.DealDateTime, format='%Y-%m-%d')
df['DateDiff'] = pandas.to_datetime('today') - df['DealDateTime']

# 计算Recency
R_Agg = df.groupby(by=['CustomerID'])['DateDiff'].agg(['min']).rename(columns={'min': 'RecencyAgg'})
# 计算Frequency
F_Agg = df.groupby(by=['CustomerID'])['OrderID'].agg(['size']).rename(columns={'size': 'FrequencyAgg'})
# 计算Monetary
M_Agg = df.groupby(by=['CustomerID'])['Sales'].agg(['sum']).rename(columns={'sum': 'MonetaryAgg'})
# 合并数据
aggData = pandas.concat([R_Agg, F_Agg, M_Agg], axis=1)

# 5分制
bins = aggData.RecencyAgg.quantile(q=[0, 0.2, 0.4, 0.6, 0.8, 1], interpolation='nearest')
# 处理左不闭合问题
bins[0] = 0
labels = [5, 4, 3, 2, 1]
R_S = pandas.cut(aggData.RecencyAgg, bins, labels=labels)
# print(R_S)

bins = aggData.FrequencyAgg.quantile(q=[0, 0.2, 0.4, 0.6, 0.8, 1], interpolation='nearest')
bins[0] = 0
labels = [1, 2, 3, 4, 5]
F_S = pandas.cut(aggData.FrequencyAgg, bins, labels=labels)
# print(F_S)

bins = aggData.MonetaryAgg.quantile(q=[0, 0.2, 0.4, 0.6, 0.8, 1], interpolation='nearest')
bins[0] = 0
labels = [1, 2, 3, 4, 5]
M_S = pandas.cut(aggData.MonetaryAgg, bins, labels=labels)
# print(M_S)
aggData['R_S'] = R_S
aggData['F_S'] = F_S
aggData['M_S'] = M_S

aggData['RFM'] = 100 * aggData.R_S.astype(int) + 10 * aggData.F_S.astype(int) + aggData.M_S.astype(int)

# 8种不同客户
bins = aggData.RFM.quantile(q=[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1], interpolation='nearest')
bins[0] = 0
labels =[1, 2, 3, 4, 5, 6, 7, 8]
aggData['level'] = pandas.cut(aggData.RFM, bins, labels=labels)

print(aggData)
