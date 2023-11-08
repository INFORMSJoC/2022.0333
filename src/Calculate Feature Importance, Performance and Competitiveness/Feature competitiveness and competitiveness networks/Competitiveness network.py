# coding:utf-8
# @Time : 2022/6/3 16:15
# @Author : 郑攀
# @File ： pagerank.py
# @Software : PyCharm

# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import random
import operator
import csv

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
all_node = pro + features_set

Graph = nx.DiGraph()
Graph.add_nodes_from(all_node)

per = []
for n in range(len(pro)):
    product_name = pro[n]
    with open('Feature importance_ performance/' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            Graph.add_edge(product_name, line[0], weight=float(line[1]))
            per.append(float(line[2]))

pos = nx.spring_layout(Graph,k=0.02)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(Graph, pos, node_size=100, node_color='r',linewidths=1,edgecolors='black')

# edges
nx.draw_networkx_edges(Graph, pos, width=2, alpha=0.4,edge_color='#A6CF8B', style='dashed')

# pos = nx.spring_layout(Graph, scale=5)  # positions for all nodes
# nx.draw_networkx_nodes(Graph, pos, node_size=300)
# nx.draw(Graph, color="b", alpha=0.5, cmap=0.5, vmin=0.5)
plt.show()
# print(Graph.succ)


fp = open('Output/Com_network.csv', "w+", encoding='utf8', newline='')
write = csv.writer(fp)

for f in range(len(all_node)):
    personalization_dic = {}
    dangling_dic = {}
    for i in range(len(pro)):
        personalization_dic[all_node[i]] = random.random()
        dangling_dic[all_node[i]] = 1
    for i in range(len(pro), len(all_node)):
        personalization_dic[all_node[i]] = random.random()
        dangling_dic[all_node[i]] = 0

    personalization_dic[all_node[f]] = 0.01*per[len(pro) + f]

    # pr = nx.pagerank(Graph, alpha=0.85, personalization={0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4, 4: 0.5, 5: 0.7})  # 得到的是字典
    pr = nx.pagerank(Graph, max_iter=1000, alpha=0.85, personalization=personalization_dic,
                     dangling=dangling_dic)
    m = nx.google_matrix(Graph, personalization=personalization_dic)
    # print("最大PR值对应的节点：", max(pr.items(), key=operator.itemgetter(1))[0])
    # print("PR值为：", pr)
    # print(m)

    pr_value = list(pr.values())[len(pro):]
    print(f)
    write.writerow(pr_value)