from lxml import etree
import re
import requests
import random
import json
import time

class KuaiDelegate:
    def __init__(self):
        self.url = "https://www.kuaidaili.com/free/inha/{}/"
        # 构造请求头
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        self.urls = [self.url.format(i) for i in range(1, 3, 1)]
        self.datas = list()

    def get_requese(self, url):
        # 随机取出请求头
        header = self.headers[random.randint(0, 1)]
        # 发送请求获得响应
        response = requests.get(url=url, headers=header)
        # 加入延时，防止系统读取过快，小于接收response的时间
        time.sleep(1)
        return response.content.decode()

    def parse_data(self, index):
        index_obj = etree.HTML(index)
        result_ip = index_obj.xpath('//div[@id="content"]//div[@id="list"]//tbody//td[1]/text()')
        result_port = index_obj.xpath('//div[@id="content"]//div[@id="list"]//tbody//td[2]/text()')
        result_time = index_obj.xpath('//div[@id="content"]//div[@id="list"]//tbody//td[last()]/text()')
        for i in range(0, len(result_ip), 1):
            delegate_dirt = dict()
            delegate_dirt["IP地址"] = result_ip[i]
            delegate_dirt["端口号"] = result_port[i]
            delegate_dirt["最后验证时间"] = result_time[i]
            self.datas.append(delegate_dirt)

    def save_data(self, result):
        with open('./delegate.json', 'w', encoding='utf-8') as file:
            d = dict()
            d['subjects'] = result
            file.write(json.dumps(d, ensure_ascii=False, indent=4))

    def run(self):
        for url in self.urls:
            response = self.get_requese(url)
            self.parse_data(response)
            self.save_data(self.datas)

if __name__ == "__main__":
    KuaiDelegate().run()