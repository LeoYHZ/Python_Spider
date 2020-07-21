

import requests
import time
import random
import _md5
import json
import re

word = input("请输入你要翻译的内容:")
# ts = "" + str(int(time.time()*1000))
# salt = ts + str(int(random.random()*10))
# need_md5_str = "fanyideskweb" + word + salt + "mmbP%A-r6U3Nw(n]BjuEU"
# # 1. 需要创建加密对象
# md5_final = _md5.md5()
# # 2. 先归档需要加密的字符串
# md5_final.update(need_md5_str.encode())
# # 3. 十六进制加密
# sign = md5_final.hexdigest()
# # md5_final.digest()   # 二进制加密

# 不同翻译的form_data中的salt、sign、ts不相同，我们需要在js文件中寻找这些值的变化
form_data = {
    "from": "zh",
    "to": "en",
    "query": word,
    "transtype": "translang",
    "simple_means_flag": "3",
    "sign": "324970.5723",
    "token": "870d84d155e079926177dc773adfda5c",
    "domain": "common"
}

# 构造请求头 当请求出错时 添加请求头的参数即可
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Cookie": "BIDUPSID=024DB026D5BE974590623DE02AA485FC; PSTM=1594179957; BAIDUID=024DB026D5BE97454D2A766EE5493A84:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-2912%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=32100_1432_32046_32231_32116_32299_31639; delPer=0; PSINO=6; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1594305414,1595304972; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1595305019; __yjsv5_shitong=1.0_7_dca0bcca2860634f53cff198c8425ef0e2c5_300_1595305019330_113.140.11.4_e8bccaea; yjs_js_security_passport=88fbfc5edc1c28898ab3753a9585b8286548b729_1595305020_js",
    "Referer": "https://fanyi.baidu.com/?aldtype=16047"
}

response = requests.post(url="https://fanyi.baidu.com/v2transapi", data=form_data, headers= header)
result_dict = json.loads(response.content.decode())
print(result_dict)
# pattern = ".*?smartResult.*?"
# if(re.compile(pattern, re.S).findall(response.content.decode())):
#     for result in result_dict["smartResult"]["entries"]:
#         print(result)
# else:
#     print("无翻译结果")
