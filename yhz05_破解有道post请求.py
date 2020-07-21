import requests
import time
import random
import _md5
import json
import re

class Translate:
    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o"
        self.word = ""
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                "Cookie": "_ntes_nnid=17cfe62729aa47f400f296ff1bc55914,1594340592953; OUTFOX_SEARCH_USER_ID_NCOO=1878401816.8479314; OUTFOX_SEARCH_USER_ID=-1687473551@10.169.0.102; JSESSIONID=aaaX-9TkkMgT48NLEbVnx; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1595300614606",
                "Referer": "http://fanyi.youdao.com/"
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                "Cookie": "_ntes_nnid=17cfe62729aa47f400f296ff1bc55914,1594340592953; OUTFOX_SEARCH_USER_ID_NCOO=1878401816.8479314; OUTFOX_SEARCH_USER_ID=-1687473551@10.169.0.102; JSESSIONID=aaaX-9TkkMgT48NLEbVnx; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1595300614606",
                "Referer": "http://fanyi.youdao.com/"
            }
        ]
        self.datas = list()

    def get_response(self, word):
        ts = "" + str(int(time.time() * 1000))
        salt = ts + str(int(random.random() * 10))
        need_md5_str = "fanyideskweb" + word + salt + "mmbP%A-r6U3Nw(n]BjuEU"
        md5_final = _md5.md5()
        md5_final.update(need_md5_str.encode())
        sign = md5_final.hexdigest()
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
        response = requests.post(url=self.url, data=form_data, headers=self.headers[random.randint(0,len(self.headers)-1)])
        return response.content.decode()

    def parse_result(self, content, saver):
        next(saver)
        result_dict = json.loads(content)
        pattern = ".*?smartResult.*?"
        if (re.compile(pattern, re.S).findall(content)):
            (result_dict["smartResult"]["entries"])[0] = "原数据：" + self.word
            for i in range(0,len(result_dict["smartResult"]["entries"])):
                result_dict["smartResult"]["entries"][i] = result_dict["smartResult"]["entries"][i].replace("\r\n","")
                print(result_dict["smartResult"]["entries"][i])
            saver.send(result_dict["smartResult"]["entries"])
        else:
            print("无翻译结果")

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./translate.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))

    def run(self):
        while True:
            self.word = input("请输入你要翻译的内容:")
            response = self.get_response(self.word)
            c = self.save_data()
            self.parse_result(response, c)

if __name__ == '__main__':
    Translate().run()