import random
import requests
import json

class Tencent:
    def __init__(self):
        self.url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1594713733225&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId={}&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn"
        self.headers = [
            {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
            },
            {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"
            }
        ]
        # parentCategoryId部分进行分页标记
        self.urls = [self.url.format(40001+i) for i in range(0,3,1)]
        self.datas = list()

    def get_requese(self, url):
        header = self.headers[random.randint(0,3)]
        response = requests.get(url=url, headers=header)
        return response.content

    def parse_data(self, js_content):
        """
        保存json中的RecruitPostName、LocationName、PostURL
        """
        work_obj = json.loads(js_content)
        # 方法1
        # for info in work_obj["Data"]["Posts"]:
        #     info_dirt = dict()
        #     info_dirt["work_name"] = info["RecruitPostName"]
        #     info_dirt["work_loc"] = info["LocationName"]
        #     info_dirt["work_res"] = info["Responsibility"].replace('\n', '').replace('\r', '')
        #     self.datas.append(info_dirt)
        # 方法2
        for key, values in work_obj.items():
            if key == "Data":
                work = values
        for info in work["Posts"]:
            info_dirt = dict()
            info_dirt["work_name"] = info["RecruitPostName"]
            info_dirt["work_loc"] = info["LocationName"]
            info_dirt["work_res"] = info["Responsibility"].replace('\n', '').replace('\r', '')
            self.datas.append(info_dirt)

    def save_data(self, content):
        with open('./work.json', 'w', encoding='utf-8') as f:
            d = dict()
            d['subjects'] = content
            f.write(json.dumps(d, ensure_ascii=False, indent=4))

    def run(self):
        for url in self.urls:
            response = self.get_requese(url).decode()
            self.parse_data(response)
            self.save_data(self.datas)

if __name__ == "__main__":
    Tencent().run()
