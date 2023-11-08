# coding:utf-8
# @Time : 2022/5/18 10:39
# @Author : 郑攀
# @File ： shap解释模型.py
# @Software : PyCharm
import csv
import numpy as np
import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense, \
    concatenate
from tensorflow.keras import Model, Input
from tensorflow.keras.losses import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X',
       'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']

for n in range(len(pro)):

    product_name = pro[n]

    with open('../Generate training sets/Filtered feature training set/SF_' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            column = len(line)

    print(column)

    err = []
    val_err = []

    for i in range(50, column):
        # print(i)
        data = []
        lables = []

        with open('../Generate training sets/Filtered feature training set/SF_' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
            lines = csv.reader(f)
            for line in lines:
                if line[0] == 'price':
                    feature_name = line[1:i + 1]
                else:
                    # print(len(line))
                    data.append([float(m) for m in line[1:i + 1]])
                    lables.append(float(line[0]))
        # print(feature_name)
        X = pd.DataFrame(data, columns=feature_name)
        y = np.array(lables)

        X_train = X.iloc[0: int(len(X) * 0.8), :]
        y_train = y[0: int(len(X) * 0.8)]

        X_test = X.iloc[int(len(X) * 0.8):, :]
        y_test = y[int(len(X) * 0.8):]

        forest = RandomForestRegressor(n_estimators=50, n_jobs=-1, max_depth=50)
        history = forest.fit(X_train, y_train)

        pre = forest.predict(X_train)
        err0 = mean_squared_error(y_train, pre)

        val_pre = forest.predict(X_test)
        val_err0 = mean_squared_error(y_test, val_pre)

        err.append(err0)
        val_err.append(val_err0)

        # plt.plot(loss, label='Training Loss')
        # plt.plot(val_loss, label='Validation Loss')
        # plt.title('Training and Validation Loss')
        # plt.legend()
        # plt.show()

    print(product_name, 'Minimum error serial number : ', val_err.index(max(val_err[200:400])))

    fp = open('特征筛选误差/' + product_name + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp)
    write.writerow(['err', 'val_err'])

    for i in range(len(err)):
        write.writerow([err[i], val_err[i]])

    # plt.plot(err)
    # plt.plot(val_err)
    # plt.legend(['err','val_err'])
    # plt.show()
