# coding:utf-8
# @Time : 2022/5/16 18:00
# @Author : 郑攀
# @File ： 斯坦福情感倾向.py
# @Software : PyCharm
import csv
import json, requests
import random

import numpy as np


class StanfordCoreNLP:
    """
        Modified from https://github.com/smilli/py-corenlp (https://github.com/smilli/py-corenlp)
        """

    def __init__(self, server_url):
        # TODO: Error handling? More checking on the url?
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):
        assert isinstance(text, str)

        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict)

        # Checks that the Stanford CoreNLP server is started.
        try:
            requests.get(self.server_url)
        except requests.exceptions.ConnectionError:
            raise Exception('Check whether you have started the CoreNLP server e.g.\n'
                            '$ cd <path_to_core_nlp_folder>/stanford-corenlp-full-2016-10-31/ \n'
                            '$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port <port>')

        data = text.encode()
        r = requests.post(
            self.server_url, params={
                'properties': str(properties)
            }, data=data, headers={'Connection': 'close'})

        output = r.text

        if ('outputFormat' in properties
                and properties['outputFormat'] == 'json'):
            try:
                output = json.loads(output, encoding='utf-8', strict=True)
            except:
                pass
        return output


def sentiment_analysis_on_sentence(sentence):
    # The StanfordCoreNLP server is running on http://127.0.0.1:9000 (http://127.0.0.1:9000)
    nlp = StanfordCoreNLP('http://127.0.0.1:9000')
    # Json response of all the annotations
    output = nlp.annotate(sentence, properties={
        "annotators": "tokenize,ssplit,parse,sentiment",
        "outputFormat": "json",
        # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
        "ssplit.eolonly": "true",
        # Setting enforceRequirements to skip some annotators and make the process faster
        "enforceRequirements": "false"
    })
    # Only care about the result of the first sentence because we assume we only annotate a single sentence

    return output['sentences'][0]['sentimentDistribution']


# print(len("with the phone is pretty impressive and fast, there is the ability to change the lighting and shadows in the pic after its been taken, again have not had enough time to deep dive but the few things I've tried have worked well- The phone is fast fast fast, so far everything I've done from playing games to other apps have been fast, installing apps is impressively fast- 5G really works on this, I've seen speeds upto 190MBPS with T-Mobile so far, so very impressed on that and its supposed to get faster as the networks get built out- Good battery life so far"))
#
# print(sentiment_analysis_on_sentence("with the phone is pretty impressive and fast, there is the ability to change the lighting and shadows in the pic after its been taken, again have not had enough time to deep dive but the few things I've tried have worked well- The phone is fast fast fast, so far everything I've done from playing games to other apps have been fast, installing apps is impressively fast- 5G really works on this, I've seen speeds upto 190MBPS with T-Mobile so far, so very impressed on that and its supposed to get faster as the networks get built out- Good battery life so far"))

pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X',
       'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']

for n in range(len(pro)):

    product_name = pro[n]

    reviews = []
    with open('phone review data (split)/' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            reviews.append(line[0])

    feature_key = []
    importance = []
    with open('Feature importance/' + product_name + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            feature_key.append(line[0])
            importance.append(line[1])

    PS_feature = []
    fp1 = open('Feature importance_ performance/' + product_name + '.csv', "w+", encoding='utf8', newline='')
    write = csv.writer(fp1)

    for p in range(len(feature_key)):
        score = []
        keys = feature_key[p].split('_')
        for i in range(len(reviews)):
            if keys[0] in reviews[i] and keys[1] in reviews[i] and len(reviews[i]) < 560:
                sentence = reviews[i].replace('"', '').replace('(', '').replace(')', '')
                try:
                    sentiment = sentiment_analysis_on_sentence(sentence)
                except:
                    print(sentence,'Error')
                    # score.append(random.random())
                    break
                # print(sentence)
                score.append(float(sentiment[2]) + float(sentiment[3]) + float(sentiment[4]))
                # print(sentence,sentiment)

        mean_score = np.mean(score)

        print(feature_key[p], mean_score)
        write.writerow([feature_key[p], importance[p], 1-mean_score])
    print('\n')

