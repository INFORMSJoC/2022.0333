# coding:utf-8
# @Time : 2022/2/28 21:55
# @Author : 郑攀
# @File ： 依赖分析.py
# @Software : PyCharm
import csv
from langdetect import detect
from stanfordcorenlp import StanfordCoreNLP

noise = ['phone','phones','Galaxy','galaxy','Samsung','cellphone','Motorola','end','Amazon','S21','s21','FE','one','s20','iPhones','<br>','iPhone']
punctuation = [',','!']
non_english = ['una','de','día','un','uso','la','diario','primeros','par','daó','uno']


pro = ['B08BGD4G36', 'B08BJJ1T9F', 'B07755LZ67', 'B077578W38', 'B09RG132Q5', 'B08BFLCLFW', 'B07KNB1TN8', 'B07TCCKNKZ', 'B08BJJKZ9X', 'B07ZQZF8JB', 'B08FYVMRM5', 'B07ZQZ15YK', 'B08CFSZLQ4', 'B07RBNTVMV', 'B079JPRTKD']

reviews = []
for i in range(len(pro)):
    with open('Data/phone review data (split)/' + pro[i] + '.csv', "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        for line in lines:
            try:
                if detect(line[0]) == 'en' and len(line[0]) > 50:
                    reviews.append(line[0])
            except:
                print(line[0])

print(len(reviews))

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-01-31',lang='en')
fp_word = open("Output/seed feature triples.csv", "w+", encoding='utf8', newline='')
write = csv.writer(fp_word)

for p in range(len(reviews)):
    print(p)
    sentence = reviews[p]
    # sentence = "The resolution of the screen is not very high"
    # print(nlp.word_tokenize(sentence))
    # print(nlp.pos_tag(sentence))
    # print(nlp.dependency_parse(sentence))

    token = nlp.word_tokenize(sentence)
    pos = nlp.pos_tag(sentence)
    dependency = nlp.dependency_parse(sentence)

    for i in range(len(dependency)):
        cell = [[], [], [[], [], []]]
        # if dependency[i][0] == 'nmod':
        if dependency[i][0] == 'compound' or dependency[i][0] == 'nmod' and pos[dependency[i][2] - 1][1][0] == 'N' and \
                pos[dependency[i][1] - 1][1][0] == 'N':
            # print(token[dependency[i][2]-1] , token[dependency[i][1]-1])
            cell[0].append(token[dependency[i][2] - 1])
            cell[1].append(token[dependency[i][1] - 1])

            for j in range(len(dependency)):
                if dependency[j][0] == 'nsubj' and dependency[i][1] in dependency[j] and pos[dependency[j][1] - 1][
                                                                                             1][
                                                                                         0:2] == 'JJ':
                    cell[2][2].append(token[dependency[j][1] - 1])
                    # print(dependency[j])

                    for k in range(len(dependency)):
                        if dependency[k][0] == 'advmod' and dependency[j][1] in dependency[k]:
                            # print(token[dependency[k][2]-1])
                            cell[2][1].append(token[dependency[k][2] - 1])

                        if dependency[k][0] == 'neg' and dependency[j][1] in dependency[k]:
                            # print(token[dependency[k][2]-1])
                            cell[2][0].append(token[dependency[k][2] - 1])

                if dependency[j][0] == 'amod' and dependency[i][1] in dependency[j] and pos[dependency[j][2] - 1][
                                                                                            1][
                                                                                        0:2] == 'JJ':
                    cell[2][2].append(token[dependency[j][2] - 1])
                    # print(dependency[j])

                    for k in range(len(dependency)):
                        if dependency[k][0] == 'advmod' and dependency[j][1] in dependency[k]:
                            # print(token[dependency[k][2]-1])
                            cell[2][1].append(token[dependency[k][2] - 1])

                        if dependency[k][0] == 'neg' and dependency[j][1] in dependency[k]:
                            # print(token[dependency[k][2]-1])
                            cell[2][0].append(token[dependency[k][2] - 1])

        if cell[0] and cell[1] and cell[2][2] and cell[0][0] not in noise + punctuation + non_english and cell[
            1][0] not in noise + punctuation +non_english and len(cell[0][0]) > 2 and len(cell[1][0]) > 2:
            print(sentence)
            print(cell)
            print()
            opinion_all = list(set(cell[2][0] + cell[2][1] + cell[2][2]))
            opinion = ''
            for k in range(len(opinion_all)):
                opinion = opinion + opinion_all[k] + ' '
            write.writerow([cell[0][0], cell[1][0], opinion[0:-1]])

nlp.close()