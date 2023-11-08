# coding:utf-8
# @Time : 2022/5/18 8:32
# @Author : 郑攀
# @File ： shap实验.py
# @Software : PyCharm
import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost
import shap

shap.initjs()

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X',
       'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']
threshold = [210, 239, 392, 219, 344, 206, 364, 233, 205, 350, 206, 337, 373, 200, ]

for n in range(len(pro)):

    product_name = pro[n]

    data_all = []
    lables = []

    with open('../Generate training sets/Filtered feature training set/SF_' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            if line[0] == 'price':
                feature_name_all = line[1:]
            else:
                data_all.append([float(m) for m in line[1:]])
                lables.append(float(line[0]))

    feature_name = []
    data = []
    for i in range(len(lables)):
        data.append([])

    for i in range(len(feature_name_all)):
        if feature_name_all[i] not in feature_name:
            feature_name.append(feature_name_all[i])
            for j in range(len(lables)):
                data[j].append(data_all[j][i])

    # print(data_all[0][0])
    print(data)
    X = pd.DataFrame(data, columns=feature_name)
    y = np.array(lables)

    # XGBoost的参数
    n_estimators = 1000  # for the initial model before tuning. default = 100
    max_depth = 100  # for the initial model before tuning. default = 3
    learning_rate = 0.1  # for the initial model before tuning. default = 0.1
    min_child_weight = 1  # for the initial model before tuning. default = 1
    subsample = 1  # for the initial model before tuning. default = 1
    colsample_bytree = 1  # for the initial model before tuning. default = 1
    colsample_bylevel = 1  # for the initial model before tuning. default = 1
    train_test_split_seed = 111  # 111
    model_seed = 100

    # 训练XGBoost回归模型
    model = xgboost.XGBRegressor(seed=model_seed,
                                 n_estimators=n_estimators,
                                 max_depth=max_depth,
                                 learning_rate=learning_rate,
                                 min_child_weight=min_child_weight)

    model.fit(X, y)
    result = model.predict(X)
    # print(result)
    explainer = shap.Explainer(model)
    shap_values = explainer(X)
    shap.summary_plot(shap_values,plot_type='bar',max_display=15)
    shap.summary_plot(shap_values,plot_type='dot',max_display=15)

    value = shap_values.values

    ave = []
    for i in range(len(value[0])):
        v = [abs(value[j][i]) for j in range(len(value))]
        ave.append(np.mean(v))

    ave_max = []
    feature_name_max = []
    for i in range(threshold[n]):
        ind = ave.index(max(ave))
        ave_max.append(ave[ind])
        feature_name_max.append(feature_name[ind])
        ave[ind] = -1

    fp = open('Feature importance/' + product_name + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp)

    for i in range(len(ave_max)):
        write.writerow([feature_name_max[i], ave_max[i]])
