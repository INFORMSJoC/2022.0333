# coding:utf-8
# @Time : 2022/5/11 17:54
# @Author : 郑攀
# @File ： kmeans聚类.py
# @Software : PyCharm
import csv

import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import KMeans

np.random.seed(123)

if __name__ == '__main__':

    words = []
    word = []
    data = []
    fp = open('Output/feature embedding.csv', 'r', encoding='utf8')
    lines = csv.reader(fp)
    for line in lines:
        if line[0] not in words:
            data.append([float(m) for m in line[1:]])
            word.append(line[0])
        words.append(line[0])

    data = np.array(data)
    print(len(data))
    kmeans_model = AffinityPropagation(random_state=10, damping=0.8, max_iter=500)
    labels = kmeans_model.fit_predict(data)
    print(labels)
    # print(words)
    print(max(labels))

    fp = open('Output/cluster_label.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp)

    triples = []
    fp = open('Data/feature triples_filter.csv', 'r', encoding='utf8')
    lines = csv.reader(fp)
    for line in lines:
        triples.append(line)

    for i in range(len(triples)):
        for j in range(len(word)):
            if word[j] == triples[i][0]:
                write.writerow(triples[i] + [labels[j]])