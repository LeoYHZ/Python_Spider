import re
import requests
import random
import json

class Dytt:
    def __init__(self, book_type):
        self.url = "http://www.qishudu.com/" + book_type + "/index_{}.html"
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        self.datas = list()

    def get_response(self, url):
        response = requests.get(url=url, headers=self.headers[random.randint(0,len(self.headers)-1)])
        return response.content.decode("gbk")

    def parse_book_list(self, content, saver):
        next(saver)
        pattern_book = '<li>.*?<div class="s">(.*?)<br>.*?<em.*?</em>.*?<br>(.*?)</div>.*?<a href="(.*?)">.*?<img src="(.*?)">(.*?)</a>'
        results_book = re.compile(pattern_book, re.S).findall(content)
        if (len(results_book) == 0):
            print("规则有误")
        else:
            for result_detail in results_book:
                book_dict = dict()
                book_dict["IP_add"] = "http://www.qishudu.com" + result_detail[2]
                book_dict["name"] = result_detail[4]
                book_dict["time"] = result_detail[1].split("：")[-1]
                book_dict["size"] = result_detail[0].split("：")[-1]
                book_dict["author"] = result_detail[0].split("：")[1].split("<")[0]
                book_dict["img"] = result_detail[3]
                book_dict["link"] = ""
                book_dict["format"] = ""
                self.datas.append(book_dict)
                response_detail = self.get_response(book_dict["IP_add"])
                self.parse_book_detail(response_detail, saver)

    def parse_book_detail(self, content, saver):
        pattern = "<li>.*?<a.*?href='(.*?.(rar|txt|html))'"
        results = re.compile(pattern, re.S).findall(content)
        print(self.datas[-1]["name"] + "一"*(15 - len(self.datas[-1]["name"])) + " 下载链接数目:" + str(len(results)))
        if (len(results) == 0):
            print("无下载地址")
        else:
            for result_detail in results:
                self.datas[-1]["link"] += result_detail[0] + " "
                self.datas[-1]["format"] += result_detail[1].replace("html", "在线阅读") + " "
        saver.send(self.datas[-1])

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            with open('./book.txt', 'a', encoding='utf-8') as file:
                file.write(json.dumps(n, ensure_ascii=False, indent=4))

    def run(self):
        for index in range(1,4):
            url = self.url.format(index)
            if (index == 1):
                url = url.replace("_1", "")
            else:
                url = url
            response = self.get_response(url)
            c = self.save_data()
            self.parse_book_list(response,c)

if __name__ == '__main__':
    Dytt("xuanhuan").run()