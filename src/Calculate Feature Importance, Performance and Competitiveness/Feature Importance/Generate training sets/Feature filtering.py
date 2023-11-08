# coding:utf-8
# @Time : 2022/5/18 18:54
# @Author : 郑攀
# @File ： 筛选指定特征.py
# @Software : PyCharm
import csv
import random

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X', 'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']
threshold = [0.6,0.6,0.6,0.6,0.6,0.6,0.5,0.3,0.4,0.1,0.4,0.3,0.4,0.4]

for n in range(len(pro)):

    product_name = pro[n]

    data = []
    feture = []
    with open('All product features frequencies vary with price/FVP_' + product_name + '.csv', 'r', encoding='utf8') as f1:  # 打开文件
        lines = csv.reader(f1)
        for line in lines:
            data.append([float(m) for m in line[0:-1]])
            feture.append(line[-1])

    data_select = []
    feature_name = []
    for i in range(len(data)):
        if i == 0:
            data_select.append(data[i][0:-1])
            feature_name.append(feture[i])
        else:
            if abs(data[i][-1]) > threshold[n]:
                a1 = data[i][0:-1]
                data_select.append(a1)
                feature_name.append(feture[i])

    print(len(feature_name))

    fp = open('Filtered feature training set/SF_' + product_name + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp)
    write.writerow(feature_name)

    for i in range(len(data_select[0])):
        row = []
        for j in range(len(data_select)):
            row.append(data_select[j][i])
        write.writerow(row)