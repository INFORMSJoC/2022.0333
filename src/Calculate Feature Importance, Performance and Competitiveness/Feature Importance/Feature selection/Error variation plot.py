# coding:utf-8
# @Time : 2022/7/28 10:11
# @Author : 郑攀
# @File ： 画图.py
# @Software : PyCharm
import csv

import matplotlib.pyplot as plt

content = []
with open("Feature filtering error/B07756QYST_target.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        if line[0] != 'err':
            content.append(float(line[1][10:-26]))

num = range(10,len(content)+10)

content_jump = []
num_jump = []
for i in range(len(content)):
    if i % 1 == 0:
        content_jump.append(content[i])
        num_jump.append(num[i])


plt.figure(figsize=(8,5))
plt.plot(num_jump,content_jump)
# plt.scatter(num_jump[279],content_jump[279])
plt.xlabel('Number of features',fontsize=13)
plt.ylabel('MSE',fontsize=13)
plt.show()

print('Minimum error serial number : ',content.index(min(content)))