# 有道翻译的请求体
# i: 今天天气很好
# from: AUTO
# to: AUTO
# smartresult: dict
# client: fanyideskweb
# salt: 15952955675358
# sign: 0d5fa758a858b045705c389df047ff51
# ts: 1595295567535
# bv: 02a6ad4308a3443b3732d855273259bf
# doctype: json
# version: 2.1
# keyfrom: fanyi.web
# action: FY_BY_REALTlME

import requests
import time
import random
import _md5
import json
import re

word = input("请输入你要翻译的内容:")
ts = "" + str(int(time.time()*1000))
salt = ts + str(int(random.random()*10))
need_md5_str = "fanyideskweb" + word + salt + "mmbP%A-r6U3Nw(n]BjuEU"
# 1. 需要创建加密对象
md5_final = _md5.md5()
# 2. 先归档需要加密的字符串
md5_final.update(need_md5_str.encode())
# 3. 十六进制加密
sign = md5_final.hexdigest()
# md5_final.digest()   # 二进制加密

# 不同翻译的form_data中的salt、sign、ts不相同，我们需要在js文件中寻找这些值的变化
form_data = {
    "i": word,
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": salt,
    "sign": sign,
    "ts": ts,
    "bv": "02a6ad4308a3443b3732d855273259bf",
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTlME"
}

# 构造请求头 当请求出错时 添加请求头的参数即可
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Cookie": "_ntes_nnid=17cfe62729aa47f400f296ff1bc55914,1594340592953; OUTFOX_SEARCH_USER_ID_NCOO=1878401816.8479314; OUTFOX_SEARCH_USER_ID=-1687473551@10.169.0.102; JSESSIONID=aaaX-9TkkMgT48NLEbVnx; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1595300614606",
    "Referer": "http://fanyi.youdao.com/"
}

response = requests.post(url="http://fanyi.youdao.com/translate_o", data=form_data, headers= header)
result_dict = json.loads(response.content.decode())
pattern = ".*?smartResult.*?"
if(re.compile(pattern, re.S).findall(response.content.decode())):
    for result in result_dict["smartResult"]["entries"]:
        print(result)
else:
    print("无翻译结果")

