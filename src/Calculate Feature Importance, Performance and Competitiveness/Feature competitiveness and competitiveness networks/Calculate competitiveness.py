# coding:utf-8
# @Time : 2022/8/5 8:10
# @Author : 郑攀
# @File ： 计算竞争性.py
# @Software : PyCharm

import csv

import numpy as np

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X',
       'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD', 'B07756QYST']
features = []
for n in range(len(pro)):
    product_name = pro[n]
    with open('Feature importance_ performance/' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            features.append(line[0])
features_set = list(set(features))

content = []
with open("Output/Com_network.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        content.append([float(m) for m in line])

content = content[len(pro):]

com = []
for i in range(len(content[0])):
    com_column = []
    for j in range(len(content)):
        com_column.append(content[j][i])
    com.append(np.mean(com_column))

fp = open('Output/Feature competitiveness.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

for i in range(len(com)):
    write.writerow([features_set[i],com[i]])

print(com)