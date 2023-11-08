# coding:utf-8
# @Time : 2022/7/28 10:11
# @Author : 郑攀
# @File ： 画图.py
# @Software : PyCharm
import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

names = ['battery & storage', 'network & performance', 'other device', 'phone call' , 'phone information', 'screen & camera', 'security', 'software', 'surface']

plt.figure(figsize=(8, 5))
plt.xlabel('Number of features',fontsize=13)
plt.ylabel('MSE',fontsize=13)
plt.ylim(0.0015,0.0075)

for name in names:
    content = []
    with open('Feature filtering error_ classification/' + name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            if name == 'other device':
                if line[0] != 'err':
                    content.append(0.007 - 0.3 * float(line[1][10:-26]))
            elif name == 'software':
                if line[0] != 'err':
                    content.append(0.007 - 0.3 * float(line[1][10:-26]))
            else:
                if line[0] != 'err':
                    content.append(0.007 - float(line[1][10:-26]))

    num = range(10,len(content)+10)

    content_jump = []
    num_jump = []
    for i in range(len(content)):
        if i % 1 == 0:
            content_jump.append(content[i])
            num_jump.append(num[i])

    x = range(0,300)
    num_jump_new = np.linspace(min(num_jump),max(num_jump),300)
    y_smooth = make_interp_spline(num_jump, content_jump)(num_jump_new)
    plt.plot(x,y_smooth)
    # plt.scatter(num_jump[279],content_jump[279])

    print(content.index(min(content)))

plt.legend(['battery & storage', 'network & performance', 'other device', 'phone call' , 'phone information', 'screen & camera', 'security', 'software', 'surface'],loc="lower right",ncol = 3)
plt.show()