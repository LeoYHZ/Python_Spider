import requests
from lxml import etree
import random
import json
from matplotlib import pyplot as plt

class Mooc:
    def __init__(self):
        self.url = "https://www.imooc.com/course/list?page={}"
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
        results = index_obj.xpath('//div[@class="moco-course-list"]//div[@class="course-card-container"]')
        for result in results:
            mooc_dict = dict()
            mooc_dict["title"] = result.xpath('.//h3/text()')[0]
            mooc_dict["url"] = "https://www.imooc.com/learn/" + result.xpath('./a/@href')[0].split("/")[-1]
            if result.xpath('.//label/text()'):
                mooc_dict["label"] = "".join(result.xpath('.//label/text()'))
            else:
                mooc_dict["label"] = "教师姓名:" + result.xpath('.//span[@class="teacher-name"]/text()')[0]
            mooc_dict["img_url"] = "https:" + result.xpath('.//img[@class="course-banner lazy"]/@data-original')[0]
            base = result.xpath('.//div[@class="course-card-info"]/span/text()')
            mooc_dict["difficulty"] = base[0]
            mooc_dict["number"] = base[1]
            mooc_dict["desc"] = result.xpath('.//div[@class="clearfix course-card-bottom"]/p/text()')[0]
            mooc_dict["price"] = result.xpath('.//div[@class="price-box"]/span/text()')[0]
            mooc_dict["time"] = ""
            mooc_dict["rate"] = ""
            mooc_dict["detail"] = ""
            print(mooc_dict["url"])
            self.datas.append(mooc_dict)
            response_detail = self.get_request(mooc_dict["url"]).decode()
            self.parse_data_detail(response_detail, saver)

    def parse_data_detail(self, content, saver):
        detail_obj = etree.HTML(content)
        time_rate = detail_obj.xpath('.//span[@class="meta-value"]/text()')
        self.datas[-1]["time"] = time_rate[1]
        if(len(time_rate) > 2):
            self.datas[-1]["rate"] = time_rate[2]
        courses = detail_obj.xpath('.//div[@class="course-chapters"]//a[@class="J-media-item" or @href="javascript:void(0);"]/text()')
        courses_list = list()
        num = 0
        while num <len(courses):
            courses[num] = courses[num].replace("\n", "").replace(" ", "")
            if len(courses[num]) != 0:
                courses_list.append(courses[num])
            num += 1
        self.datas[-1]["detail"] = courses_list
        saver.send(self.datas[-1])
        img_content = requests.get(url=self.datas[-1]["img_url"]).content
        saver.send(img_content)

    def save_data(self):
        while True:
            n = yield
            if not n:
                return
            if(str(type(n)) == "<class 'dict'>"):
                with open('./mooc.txt', 'a', encoding='utf-8') as file:
                    file.write(json.dumps(n, ensure_ascii=False, indent=4))
            else:
                with open('./mooc/'+ self.datas[-1]["title"] + ".jpg", 'wb') as file:
                    file.write(n)

    def plot_data(self):
        i = 0
        x = range(0, len(self.datas), 1)
        x1_new = list()
        x2_new = list()
        y1 = list()
        y2 = list()
        while i <len(self.datas):
            x1_new.append(self.datas[i]["title"])
            y1.append(int(self.datas[i]["number"]))
            if len(self.datas[i]["rate"])!=0:
                x2_new.append(self.datas[i]["title"])
                y2.append(float(self.datas[i]["rate"]))
            i += 1
        plt.figure(figsize=(60, 30), dpi=100)
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.xticks(list(x), x1_new, rotation=75, fontsize=20)
        plt.xlabel("课程名称", fontsize=50)
        plt.ylabel("学习人数", fontsize=50)
        plt.plot(x1_new, y1, color="r", marker="o")
        for a, b in zip(x1_new, y1):
            plt.text(a, b + 0.1, '%d' %b, ha='center', va='bottom', fontsize=16)
        plt.grid(alpha=0.2, color='black')
        plt.title('各个课程的学习人数', fontsize=50)
        plt.savefig("number.png")
        plt.figure(figsize=(60, 30), dpi=100)
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.xticks(rotation=75, fontsize=20)
        plt.xlabel("课程名称", fontsize=50)
        plt.ylabel("综合评分", fontsize=50)
        plt.plot(x2_new, y2, color="b", marker="x")
        for a, b in zip(x2_new, y2):
            plt.text(a, b + 0.1, '%.2f' %b, ha='center', va='bottom', fontsize=30)
        plt.grid(alpha=0.2, color='black')
        plt.title('各个课程的综合评分', fontsize=50)
        plt.savefig("rate.png")

    def run(self):
        for url in self.urls:
            response = self.get_request(url)
            c = self.save_data()
            self.parse_data(response,c)
            self.plot_data()

if __name__ == "__main__":
    Mooc().run()