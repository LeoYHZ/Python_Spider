import requests
from lxml import etree
import random
import json

class LianHome:
    def __init__(self, city):
        self.url = "https://" + city +".lianjia.com/ershoufang/pg{}/"
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        self.urls = [self.url.format(i) for i in range(1, 2, 1)]
        self.datas = list()

    def get_request(self, url):
        header = self.headers[random.randint(0, 1)]
        response = requests.get(url=url, headers=header)
        return response.content

    def parse_data(self, index, saver):
        next(saver)
        index_obj = etree.HTML(index)
        results = index_obj.xpath('//li[@class="clear LOGCLICKDATA" or @class="clear LOGVIEWDATA LOGCLICKDATA"]//div[@class="info clear"]')
        for result in results:
            home_dict = dict()
            home_dict["title"] = result.xpath('./div[@class="title"]/a/text()')[0]
            home_dict["url"] = result.xpath('./div[@class="title"]/a/@href')[0]
            home_dict["location"] = "".join(result.xpath('./div[@class="flood"]//a/text()'))
            home_dict["base"] = result.xpath('.//div[@class="houseInfo"]/text()')[0]
            home_dict["time"] = result.xpath('./div[@class="followInfo"]/text()')[0]
            price = result.xpath('./div[@class="priceInfo"]//span/text()')
            home_dict["price_total"] = "总价" + price[0] + "万"
            home_dict["price_ave"] = price[1]
            home_dict["img_urls"] = ""
            home_dict["detail"] = ""
            home_dict["special"] = ""
            self.datas.append(home_dict)
            response_detail = self.get_request(home_dict["url"]).decode()
            self.parse_data_detail(response_detail, saver)

    def parse_data_detail(self, content, saver):
        detail_obj = etree.HTML(content)
        img_urls = detail_obj.xpath('//ul[@class="smallpic"]//img/@src')
        detail_dec = "".join(detail_obj.xpath('//div[@class="transaction"]//span/text()'))
        special_dec = "".join(detail_obj.xpath('//div[@class="baseattribute clear"]//div[@class="content"]/text()'))
        self.datas[-1]["detail"] += detail_dec.replace("\n                              ", "")
        self.datas[-1]["special"] += special_dec.replace("\n                  ", "")
        self.num = 0
        for img in img_urls:
            self.num += 1
            url_final = img.split("?")[0].replace("120x80", "1420x800")
            self.datas[-1]["img_urls"] += url_final + " "
            img_content = requests.get(url=url_final).content
            print("下载：" + self.datas[-1]["title"] + str(self.num))
            saver.send(self.datas[-1])
            saver.send(img_content)
        self.datas = list()

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            if(str(type(n)) == "<class 'dict'>"):
                with open('./home.txt', 'a', encoding='utf-8') as file:
                    file.write(json.dumps(n, ensure_ascii=False, indent=4))
            else:
                with open('./home/'+ self.datas[-1]["title"] + str(self.num) + ".jpg", 'wb') as file:
                    file.write(n)

    def run(self):
        for url in self.urls:
            response = self.get_request(url)
            c = self.save_data()
            self.parse_data(response,c)

if __name__ == "__main__":
    LianHome("hz").run()