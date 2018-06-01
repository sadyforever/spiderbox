import hashlib
import json
import re
from random import randint

import requests
import time




class Trans(object):
    def __init__(self,text):
        # 有道翻译是ajax请求,找到具体针对翻译的那个js
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        # 如果不行可能是头中少内容
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            # 必须携带来源
            'Referer' : 'http://fanyi.youdao.com/',
            # 'Accept' : 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language' : 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=787139482@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=364165130.64408207; JSESSIONID=aaaBlfPxX3hhZ7TVWdWow; fanyi-ad-id=44881; fanyi-ad-closed=1; ___rl__test__cookies=1527673999106',
            # 'Host': 'fanyi.youdao.com',
            # 'Origin' : 'http://fanyi.youdao.com',
            # 'X-Requested-With': 'XMLHttpRequest'

        }
        self.text = text


    def get_salt(self):
        # 参数salt是时间戳 + 随机数 1-9
        self.salt = str(int(time.time() * 1000) + randint(1,9))
        return self.salt

    def get_sign(self):
        '''
        str = 'fanyideskwebcaptcha1527670933553ebSeFb%=XZ%T[KZ)c(sy!'
        h = hashlib.md5()
        h.update(str.encode(encoding='utf-8'))
        print(str)
        print(h.hexdigest())
        :return: 有道使用的md5加密自己写的,但是sign是13位的内容,使用有道翻译过的salt和sign来验证,python中的md5加密结果相同
        '''
        # 加密使用的密匙是在js中找到的
        str = 'fanyideskweb' + self.text + self.salt + 'ebSeFb%=XZ%T[KZ)c(sy!'
        # python的md5加密使用hashlib模块
        h = hashlib.md5()
        h.update(str.encode(encoding='utf-8'))
        # print(str)
        secret_str = h.hexdigest()
        # print(secret_str)
        return secret_str

    def get_json(self):
        # post请求data参数直接使用字典就可以,不用是json
        data = {
            'i' : self.text,
            'from' : 'AUTO',
            'to' : 'AUTO',
            'smartresult' : 'dict',
            'client' : 'fanyideskweb',
            'salt' : self.get_salt(),
            'sign' : self.get_sign(),
            'doctype' : 'json',
            'version' : '2.1',
            'keyfrom' : 'fanyi.web',
            'action' : 'FY_BY_CLICKBUTTION',
            'typoResult' : 'false'
        }
        return data

    def get_data(self):
        data = self.get_json()
        response = requests.post(self.url,data=data,headers=self.headers)
        trans_data = response.content.decode()
        print(trans_data) # 就是str不用进行json的操作
        # print(type(trans_data)) # <class 'str'>
        # trans_dict = json.dumps(trans_data)
        # print(type(trans_dict))
        # print(trans_dict)
        # trans_ret = trans_dict["translateResult"][0][0]["tgt"]   # 这样拿结果出错了

        trans_ret = re.findall('tgt":"(.*)","src"',trans_data)
        # trans_ret = re.findall('entries":["","(.*)\r\n"',trans_data)  # 报错了为什么

        # print(trans_ret)



        print('翻译结果是: %s' % trans_ret)

if __name__ == '__main__':
    text = input('请输入:')
    trans = Trans(text)
    trans.get_data()

'''
i: 崇山峻岭
from: AUTO
to: AUTO
smartresult: dict                               int(time.time() * 1000)
client: fanyideskweb                   强转字符串     13位的数字        + 随机数
salt: 1527667642834              r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
sign: 87fe48e330bfd575b2a27c6ec78b18bb          o = u.md5(S + n + r + D)
doctype: json                                   S = 'fanyideskweb'
version: 2.1                                    n = self.text
keyfrom: fanyi.web                              r = salt 保持两次的salt相同
action: FY_BY_CLICKBUTTION                      D = 'ebSeFb%=XZ%T[KZ)c(sy!'  浏览器有区分大小写的搜索
                                                跟 u 没关系 
typoResult: false
  .md5('fanyideskweb'+'life'+'1527672085984'+'ebSeFb%=XZ%T[KZ)c(sy!')
'''
'''
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 236
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: OUTFOX_SEARCH_USER_ID=787139482@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=364165130.64408207; JSESSIONID=aaaBlfPxX3hhZ7TVWdWow; fanyi-ad-id=44881; fanyi-ad-closed=1; ___rl__test__cookies=1527673999106
Host: fanyi.youdao.com
Origin: http://fanyi.youdao.com
Referer: http://fanyi.youdao.com/
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36
X-Requested-With: XMLHttpRequest

Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 207
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: OUTFOX_SEARCH_USER_ID=787139482@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=364165130.64408207; JSESSIONID=aaaBlfPxX3hhZ7TVWdWow; fanyi-ad-id=44881; fanyi-ad-closed=1; ___rl__test__cookies=1527670909402
Host: fanyi.youdao.com
Origin: http://fanyi.youdao.com
Referer: http://fanyi.youdao.com/

'''
