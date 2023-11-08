# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/5/8 20:04
# @author   :Mo
# @function :extract feature of bert and keras

import codecs
import os

import keras.backend.tensorflow_backend as ktf_keras
import numpy as np
import tensorflow as tf
from keras.layers import Add
from keras.models import Model
from keras_bert import load_trained_model_from_checkpoint, Tokenizer

from FeatureProject.bert.layers_keras import NonMaskingLayer
from conf.feature_config import gpu_memory_fraction, config_name, ckpt_name, vocab_file, max_seq_len, layer_indexes

from FeatureProject.xlnet import args

# 全局使用，使其可以django、flask、tornado等调用
graph = None
model = None


# gpu配置与使用率设置
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = args.gpu_memory_fraction
sess = tf.compat.v1.Session(config=config)
# ktf_keras.set_session(sess)

class KerasBertVector():
    def __init__(self):
        self.config_path, self.checkpoint_path, self.dict_path, self.max_seq_len = config_name, ckpt_name, vocab_file, max_seq_len
        # 全局使用，使其可以django、flask、tornado等调用
        global graph
        graph = tf.compat.v1.get_default_graph()
        global model
        model = load_trained_model_from_checkpoint(self.config_path, self.checkpoint_path,
                                                   seq_len=self.max_seq_len)
        print(model.output)
        print(len(model.layers))
        # lay = model.layers
        #一共104个layer，其中前八层包括token,pos,embed等，
        # 每8层（MultiHeadAttention,Dropout,Add,LayerNormalization） resnet
        # 一共12层
        layer_dict = [7]
        layer_0 = 7
        for i in range(12):
            layer_0 = layer_0 + 8
            layer_dict.append(layer_0)
        # 输出它本身
        if len(layer_indexes) == 0:
            encoder_layer = model.output
        # 分类如果只有一层，就只取最后那一层的weight，取得不正确
        elif len(layer_indexes) == 1:
            if layer_indexes[0] in [i+1 for i in range(13)]:
                encoder_layer = model.get_layer(index=layer_dict[layer_indexes[0]]).output
            else:
                encoder_layer = model.get_layer(index=layer_dict[-1]).output
        # 否则遍历需要取的层，把所有层的weight取出来并拼接起来shape:768*层数
        else:
            # layer_indexes must be [1,2,3,......13]
            # all_layers = [model.get_layer(index=lay).output if lay is not 1 else model.get_layer(index=lay).output[0] for lay in layer_indexes]
            all_layers = [model.get_layer(index=layer_dict[lay-1]).output if lay in [i+1 for i in range(13)]
                          else model.get_layer(index=layer_dict[-1]).output  # 如果给出不正确，就默认输出最后一层
                          for lay in layer_indexes]
            print(layer_indexes)
            print(all_layers)
            # 其中layer==1的output是格式不对，第二层输入input是list
            all_layers_select = []
            for all_layers_one in all_layers:
                all_layers_select.append(all_layers_one)
            encoder_layer = Add()(all_layers_select)
            print(encoder_layer.shape)
        print("KerasBertEmbedding:")
        print(encoder_layer.shape)
        output_layer = NonMaskingLayer()(encoder_layer)
        model = Model(model.inputs, output_layer)
        # model.summary(120)
        # reader tokenizer
        self.token_dict = {}
        with codecs.open(self.dict_path, 'r', 'utf8') as reader:
            for line in reader:
                token = line.strip()
                self.token_dict[token] = len(self.token_dict)

        self.tokenizer = Tokenizer(self.token_dict)


    def bert_encode(self, texts):
        # 文本预处理
        input_ids = []
        input_masks = []
        input_type_ids = []
        for text in texts:
            print(text)
            tokens_text = self.tokenizer.tokenize(text)
            print('Tokens:', tokens_text)
            input_id, input_type_id = self.tokenizer.encode(first=text, max_len=self.max_seq_len)
            input_mask = [0 if ids == 0 else 1 for ids in input_id]
            input_ids.append(input_id)
            input_type_ids.append(input_type_id)
            input_masks.append(input_mask)

        input_ids = np.array(input_ids)
        input_masks = np.array(input_masks)
        input_type_ids = np.array(input_type_ids)

        # 全局使用，使其可以django、flask、tornado等调用
        # with graph.as_default():
        predicts = model.predict([input_ids, input_type_ids], batch_size=1)
        print(predicts.shape)
        tokens_text = tokens_text if len(tokens_text) <= self.max_seq_len - 2 else tokens_text[:self.max_seq_len - 2]
        for i, token in enumerate(tokens_text):
            print(token, [len(predicts[0][i].tolist())], predicts[0][i].tolist())

        # 相当于pool，采用的是https://github.com/terrifyzhao/bert-utils/blob/master/graph.py
        mul_mask = lambda x, m: x * np.expand_dims(m, axis=-1)
        masked_reduce_mean = lambda x, m: np.sum(mul_mask(x, m), axis=1) / (np.sum(m, axis=1, keepdims=True) + 1e-9)

        pools = []
        for i in range(len(predicts)):
            pred = predicts[i]
            masks = input_masks.tolist()
            mask_np = np.array([masks[i]])
            pooled = masked_reduce_mean(pred, mask_np)
            pooled = pooled.tolist()
            pools.append(pooled[0])
        print('bert:', pools)
        return pools


if __name__ == "__main__":
    bert_vector = KerasBertVector()
    pooled = bert_vector.bert_encode(['你是谁呀', '小老弟'])
    print(pooled)
    while True:
        print("input:")
        ques = input()
        print(bert_vector.bert_encode([ques]))

