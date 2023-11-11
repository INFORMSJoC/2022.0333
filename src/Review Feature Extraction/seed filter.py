# coding:utf-8
# @Time : 2023/10/27 19:37
# @Author : 郑攀
# @File ： filter.py
# @Software : PyCharm
import csv

filter_feature = []
with open("Output/seed filter feature.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        filter_feature.append(line[0])

seed_feature = []
with open("Output/seed feature triples.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        seed_feature.append(line)

fp = open('Output/seed feature triples_filter.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

for i in range(len(seed_feature)):
    if seed_feature[i][0] in filter_feature:
        write.writerow(seed_feature[i])

