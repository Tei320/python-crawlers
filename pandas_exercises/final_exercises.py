import time
import pandas, numpy, datetime
import matplotlib
import matplotlib.pyplot as plt

font = {
    'family': 'SimHei'
}
matplotlib.rc('font', **font)

student = pandas.read_excel('学生名册.xlsx')
score = pandas.read_excel('成绩表.xlsx')
course = pandas.read_excel('课程表.xlsx')

student['学号'] = student['入学时间'].str.slice(2, 4) + student['班号'].astype(str) + student['座号'].astype(str).str.zfill(3)
student['学号'] = student['学号'].astype(int)
student['年级'] = student['班级'].str.slice(0, 3)
student['班级'] = student['班级'].str.slice(5, 7)

# print(student)

score['总成绩'] = score['平时成绩'] * 0.3 + score['卷面成绩'] * 0.7
score['绩点'] = (score['总成绩'] / 10 - 5).astype(int)
new_score = score.groupby(by=['学号']).apply(lambda x: round(numpy.sum(x['学分'] * x['绩点']) / numpy.sum(x['学分']), 2))
new_score = new_score.reset_index().rename(columns={0: 'GPA'})
bins = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.1]
labels = ['E', 'D', 'C', 'B', 'A', 'S']
new_score['GPA评级'] = pandas.cut(new_score.GPA, bins=bins, right=False, labels=labels)

failed = score[(score.总成绩 < 60) & (score.录入时间 > datetime.datetime(2017,9,1))]
failed = pandas.merge(
    failed,
    student,
    how='left',
    on=['学号','姓名'],
    sort=True
)[['学号','姓名','年级','班级','性别','课程','课程编号','平时成绩','卷面成绩','总成绩']]
# 不能带上序号
failed.to_excel("Q1-failed.xlsx", index=False, header=True )

unfortunately = new_score[new_score['GPA评级'] == 'E']
unfortunately = pandas.merge(
    unfortunately,
    student,
    how='left',
    on=['学号'],
    sort=True
)[['学号', '姓名', '年级', '班级', '性别']]
unfortunately.to_excel('Q2-unfortunately.xlsx', index=False, header=True)

perfect = pandas.merge(
    new_score,
    student,
    how='left',
    on=['学号'],
    sort=True
)[['学号', '姓名', 'GPA', '年级', '班级', '性别']]
perfect = perfect[(perfect.学号.astype(str).str.slice(0,2) == '14') & (perfect.GPA >= perfect.GPA.quantile(0.9))]
if perfect.学号.size >= 5:
    perfect = perfect.sample(frac=0.2)
perfect.to_excel('Q3-perfect.xlsx', index=False, header=True)

bad_explain = pandas.merge(
    new_score,
    student,
    how='left',
    on=['学号'],
    sort=True
)[['学号', '姓名', 'GPA', '年级', '班级', '性别']]
bad_explain = bad_explain.groupby(by=['年级'])['GPA'].agg(['mean']).rename(columns={'mean': '平均绩点'})
bad_explain['平均绩点'] = bad_explain['平均绩点'].map('{:.2f}'.format)
bad_explain = bad_explain.reset_index()

bad_explain = bad_explain.sort_values(by='平均绩点')
plt.plot(bad_explain.年级, bad_explain.平均绩点, '--')
plt.title('最差的解释')
plt.savefig('Q4.png', format='png')
plt.close()

sex_ratio = student.groupby(by=['性别'])['学号'].agg(['size']).rename(columns={'size': '人数'})

plt.pie(sex_ratio.人数, labels=sex_ratio.index, autopct='%.2f%%')
plt.title('全校男女比例图')
plt.savefig('Q5-1.png', format='png')
plt.close()

sex_ratio = student.pivot_table(values='学号',
                                index='性别',
                                columns='年级',
                                aggfunc=numpy.size)

for grade in sex_ratio.columns:
    temp = sex_ratio[grade].reset_index().rename(columns={grade: '人数'})
    plt.pie(temp.人数, labels=temp.性别, autopct='%.2f%%')
    plt.title(grade + '男女比例图')
    plt.savefig('Q5-' + grade + '.png', format='png')
    plt.close()


teacher_score = pandas.merge(
    score,
    course,
    how='left',
    on=['课程编号', '教师编号', '学分'],
    sort=True
)
teacher_score = teacher_score[teacher_score.教师 == '胶水儿']

plt.hist(teacher_score.总成绩, bins=10)
plt.title('胶水儿老师所教课程分数段分布图')
plt.savefig('Q6.png', format='png')
plt.close()


course_pre_analysis = score.pivot_table(
    values='总成绩',
    index='学号',
    columns='课程',
    aggfunc=numpy.max
)[['Python从入门到精通', '计算机网络', 'Python网络爬虫']]
course_pre_analysis = course_pre_analysis[['Python从入门到精通', '计算机网络', 'Python网络爬虫']].corr()
course_pre_analysis.to_excel('Q7-course_pre_analysis.xlsx', index=True, header=True)

temp_table = pandas.merge(
    score,
    student,
    on=['学号', '姓名'],
    sort=True
)
female_score = temp_table[temp_table.性别 == '女']
male_score = temp_table[temp_table.性别 == '男']
# 宿舍字段无。。。后续无法处理
