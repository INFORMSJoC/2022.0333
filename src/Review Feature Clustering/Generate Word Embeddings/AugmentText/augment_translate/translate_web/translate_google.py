# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @Time     :2019/3/21 14:30
# @author   :Mo
# @function :回译调用谷歌翻译，模拟google token访问


# 适配linux
import sys
import os
path_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(path_root)
print(path_root)


import logging as logger
import urllib.parse as parse

import execjs
import requests

from conf.augment_constant import language_short_google
from utils.text_tools import judge_translate_english


class GoogleToken:
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def get_google_token(self, text):
        """
           获取谷歌访问token
        :param text: str, input sentence
        :return: 
        """
        return self.ctx.call("TL", text)


def open_url(url):
    """
      新增header，并request访问
    :param url: str, url地址
    :return: str, 目标url地址返回  
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    req = requests.get(url=url, headers=headers)
    # print('req.txt:')
    # print(req.text.encode('gbk', 'ignore').decode('gbk'))
    return req # .content.decode('utf-8')


def max_length(content):
    """
      超过最大长度就不翻译
    :param content: str, need translate
    :return: 
    """
    if len(content) > 4891:
        logger.info("翻译文本超过限制！")
        return 4891
    else:
        return None


def translate_result(result):
    """
      删去无关词
    :param result: str
    :return: str
    """
    result_last = ''
    for res in result[0]:
        if res[0]:
            result_last += res[0]
    return result_last


def any_to_any_translate(content, from_='zh-CN', to_='en'):
    """
       自定义选择
    :param content: str, 4891个字， 用户输入 
    :param from_: str, original language
    :param to_:   str, target language
    :return: str, result of translate
    """
    max_len = max_length(content)
    if max_len:
        content = content[0:max_len]
    tk = google_tokn.get_google_token(content)
    content = parse.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=t&sl={0}&tl={1}" \
          "&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&" \
          "ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=3&kc=0&tk={2}&q={3}".format(from_, to_, tk, content)
    result = open_url(url)
    result_json =  result.json()
    res = translate_result(result_json)
    return res


def any_to_any_translate_back(content, from_='zh-CN', to_='en'):
    """
      中英，英中回译
    :param content:str, 4891个字， 用户输入 
    :param from_: str, original language
    :param to_:   str, target language
    :return: str, result of translate
    """
    translate_content = any_to_any_translate(content, from_=from_, to_=to_)
    result = any_to_any_translate(translate_content, from_=to_, to_=from_)
    return result


if __name__ == '__main__':
    google_tokn = GoogleToken()
    while True:
        # sen_org = "过路蜻蜓喜欢口袋巧克力，这是什么意思"
        sen_org = "此外，李奇霖还认为，MLF期限是6个月，逆回购是7天，考虑到外汇占款流出的是长期限流动性，" \
                  "因此，无论哪一种货币投放模式都无法替代降准，降准的期限理论上是“无穷期”的。" \
                  "从资金利率看，MLF资金利率在3.35%，比起降准释放的“无成本”流动性仍然偏高，" \
                  "经济下行压力之下，实体能提供的高收益资产有限，较高的资金利率能否缓解外汇占款对信用派生的收缩作用，也是有疑虑的。" \
                  "“等汇率端稍见稳定后，我们能看到降准的出现，幅度约为100BP，时点预计在9月上旬。"

        for language_short_google_one in language_short_google:
            text_translate = any_to_any_translate_back(sen_org, from_='zh', to_=language_short_google_one)
            judge = judge_translate_english(sen_org, text_translate)
            if judge:
                print(language_short_google_one + " " + "True")
                print(text_translate.encode('gbk', 'ignore').decode('gbk'))
            else:
                print(language_short_google_one + " " + "False")
                print(text_translate.encode('gbk', 'ignore').decode('gbk'))
#测试结果
# en False
# 我喜欢口袋巧克力，这是什么意思？
# fr False
# 我喜欢口袋巧克力，这是什么意思？
# ru False
# 我喜欢口袋糖果，这是什么意思？
# de False
# 我喜欢袋巧克力，这是什么意思？
