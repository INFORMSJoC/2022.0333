# coding:utf-8
# @Time : 2022/5/17 12:18
# @Author : 郑攀
# @File ： 特征频率情感随价格变动样例产品.py
# @Software : PyCharm
import csv
import time
import matplotlib.pyplot as plt
import numpy as np

def calc_corr(a, b):
    a_avg = sum(a) / len(a)
    b_avg = sum(b) / len(b)
    # 计算分子，协方差————按照协方差公式，本来要除以n的，由于在相关系数中上下同时约去了n，于是可以不除以n
    cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
    # 计算分母，方差乘积————方差本来也要除以n，在相关系数中上下同时约去了n，于是可以不除以n
    sq = (sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b])) ** 0.5
    corr_factor = cov_ab / sq
    return corr_factor

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X', 'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']

for name in pro:

    product_name = name

    times = []
    reviews = []
    with open('phone review data/' + name + ".csv", "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            if '年' in line[2] and '月' in line[2] and '日' in line[2] and '审核' in line[2]:
                reviews.append(line[0] + '.' + line[1])
                time_review = line[2].split(' ')[0]
                # print(time_review)
                year = time_review.split('年')[0]
                month = time_review.split('年')[1].split('月')[0]
                day = time_review.split('年')[1].split('月')[1].split('日')[0]
                time_result = str(year) + '/' + str(month) + '/' + str(day)
                times.append(time_result)

    time_utc = []
    for t in times:
        time_utc.append(time.mktime(time.strptime(t, "%Y/%m/%d")))

    price_time = []
    prices = []
    with open("Product price changes (normalized)/" + name + "价格变动.csv", "r", encoding='utf8') as f1:  # 打开文件
        lines = csv.reader(f1)
        for line in lines:
            price_time.append([time.mktime(time.strptime(line[0], "%Y/%m/%d")), float(line[1])])
            prices.append(float(line[1]))

    # print(time.strftime("%Y/%m/%d", time.gmtime(min(time_utc))))

    feature_dic = {
        'surface': ['touch', 'scratch', 'body', 'back', 'case', 'scratch', 'rubber', 'shape', 'size', 'color', 'corner',
                    'wear', 'look', 'side', 'cell', 'volume', 'type', 'plastic', 'light', 'inch', 'box', 'edge',
                    'display',
                    'metal', 'top', 'design', 'paper'],

        'screen & camera': ['screen', 'photo', 'camera', 'angle', 'glass', 'zoom', 'resolution', 'night', 'light',
                            'image', 'picture', 'selfie', 'pixel', 'gorilla', 'quality', 'lens'],

        'phone call': ['sim', 'stereo', 'card', 'notch', 'holder', 'headphone', 'bluetooth', 'sound', 'ear', 'voice',
                       'video', 'call', 'radio', 'speaker', 'port', 'talk', 'audio'],

        'security': ['print', 'fingerprint', 'water', 'protection', 'sensor', 'face', 'recognition', 'touch', 'finger',
                     'security', 'protector'],

        'other device': ['device', 'hand', 'specs', 'button', 'cable', 'note', 'devices', 'sprint', 'gps', 'point',
                         'home',
                         'pocket', 'stylus', 'scanner', 'data'],

        'network & performance': ['signal', 'web', 'internet', 'sensor', 'response', 'processing', 'network', 'wifi',
                                  'performance', 'setup', 'processor', 'connection'],

        'battery & storage': ['power', 'battery', 'life', 'charge', 'charger', 'health', 'storage', 'memory',
                              'garbage'],

        'software': ['updates', 'carrier', 'music', 'verizon', 'system', 'bar', 'google', 'setting', 'mode', 'app',
                     'notification', 'android', 'software', 'reader', 'boot', 'smart', 'email', 'operating', 'keyboard',
                     'bloatware', 'response', 'window'],

        'phone information': ['design', 'budget', 'flagship', 'review', 'price', 'work', 'country', 'customer', 'plus',
                              'factory', 'verizon', 'range', 'line', 'usage', 'store', 'condition', 'quality', 'type',
                              'media', 'money', 'use', 'portrait', 'trade-in', 'service', 'version', 'repair',
                              'seller', 'cost', 'company', 'warranty', 'series', 'brand']}

    feature_key = list(feature_dic.keys())

    PS_feature = []
    for key in feature_key:
        fp2 = open('../secondary features/' + key + '.csv', "r", encoding='utf8', newline='')
        lines = csv.reader(fp2)
        for line in lines:
            PS_feature.append(line)

    fp3 = open('All product features frequencies vary with price/FVP_' + name + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp3)
    write.writerow(prices + [0, 'price'])

    for PS in PS_feature:
        frequency = []
        for i in range(len(price_time)):
            tem_reviews = []
            count = 0
            for j in range(len(time_utc)):
                if time_utc[j] <= price_time[i][0]:
                    tem_reviews.append(reviews[j])

            for j in range(len(tem_reviews)):
                if PS[0] in tem_reviews[j] and PS[1] in tem_reviews[j]:
                    count = count + 1

            frequency.append(count / (len(tem_reviews) + 0.00000000000001))

        frequency_nor = []
        for fre in frequency:
            frequency_nor.append(fre * (1.2 / np.mean(frequency)))

        print(PS[0], PS[1], calc_corr(prices, frequency_nor))

        write.writerow(frequency_nor + [calc_corr(prices, frequency_nor)] + [PS[0] + '_' + PS[1]])
        # plt.plot(frequency_nor)
        # plt.plot(prices)
        # plt.show()