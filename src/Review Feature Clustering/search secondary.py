# coding:utf-8
# @Time : 2022/5/16 19:23
# @Author : 郑攀
# @File ： 生成最终特征.py
# @Software : PyCharm
import csv

feature_dic = {
    'surface': ['touch', 'scratch', 'body', 'back', 'case', 'scratch', 'rubber', 'shape', 'size', 'color', 'corner',
                'wear', 'look', 'side', 'cell', 'volume', 'type', 'plastic', 'light', 'inch', 'box', 'edge', 'display',
                'metal', 'top', 'design', 'paper'],

    'screen & camera': ['screen', 'photo', 'camera', 'angle', 'glass', 'zoom', 'resolution', 'night', 'light',
                        'image', 'picture', 'selfie', 'pixel', 'gorilla', 'quality', 'lens'],

    'phone call': ['sim', 'stereo', 'card', 'notch', 'holder', 'headphone', 'bluetooth', 'sound', 'ear', 'voice',
                   'video', 'call', 'radio', 'speaker', 'port', 'talk', 'audio'],

    'security': ['print', 'fingerprint', 'water', 'protection', 'sensor', 'face', 'recognition', 'touch', 'finger',
                 'security', 'protector'],

    'other device': ['device', 'hand', 'specs', 'button', 'cable', 'note', 'devices', 'sprint', 'gps', 'point', 'home',
                     'pocket', 'stylus', 'scanner', 'data'],

    'network & performance': ['signal', 'web', 'internet', 'sensor', 'response', 'processing', 'network', 'wifi',
                              'performance', 'setup', 'processor', 'connection'],

    'battery & storage': ['power', 'battery', 'life', 'charge', 'charger', 'health', 'storage', 'memory', 'garbage'],

    'software': ['updates', 'carrier', 'music', 'verizon', 'system', 'bar', 'google', 'setting', 'mode', 'app',
                 'notification', 'android', 'software', 'reader', 'boot', 'smart', 'email', 'operating', 'keyboard',
                 'bloatware', 'response', 'window'],

    'phone information': ['design', 'budget', 'flagship', 'review', 'price', 'work', 'country', 'customer', 'plus',
                          'factory', 'verizon', 'range', 'line', 'usage', 'store', 'condition', 'quality', 'type',
                          'media', 'money', 'use', 'portrait', 'trade-in', 'service', 'version', 'repair',
                          'seller', 'cost', 'company', 'warranty', 'series', 'brand']}

words = []
single_word = []
with open("Data/feature triples_filter.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    for line in lines:
        single_word.append(line[0])
        words.append([line[0], line[1]])

    word = []
    for i in range(len(words)):
        if words.count(words[i]) > 1:
            word.append(words[i])

    # print(word)

feature_key = list(feature_dic.keys())

for key in feature_key:
    # for key in ['battery']:
    PS_feature = []
    fp1 = open('Output/secondary features/' + key + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp1)
    for i in range(len(word)):
        if word[i][0] in feature_dic[key] and word[i] not in PS_feature:
            PS_feature.append(word[i])

    for f in PS_feature:
        write.writerow(f)
