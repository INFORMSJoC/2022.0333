# coding:utf-8
# @Time : 2022/7/21 17:20
# @Author : 郑攀
# @File ： 字母小写.py
# @Software : PyCharm
import csv
import string
import inflect
p = inflect.engine()

fp = open('Output/feature triples_ls.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

content = []
with open("Output/feature triples.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        a = line[0].lower()
        b = line[1].lower()
        if p.singular_noun(a) != False:
            a = p.singular_noun(a)
        if p.singular_noun(b) != False:
            b = p.singular_noun(b)
        content.append([a,b,line[2].lower()])

for i in range(len(content)):
    write.writerow(content[i])