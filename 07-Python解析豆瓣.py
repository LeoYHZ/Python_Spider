# 热门电影
# https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0
# 热门电视剧
# https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0

import random
import requests
import json

class DouBan:
    def __init__(self, type):
        self.url = "https://movie.douban.com/j/search_subjects?type=" + type + "&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start={}"
        # 构造请求头
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
        self.urls = [self.url.format(i*50) for i in range(0,1,1)]
        self.datas = list()

    def get_requese(self, url):
        # 随机取出请求头
        header = self.headers[random.randint(0,3)]
        # 发送请求获得响应
        response = requests.get(url=url, headers=header)
        # 此处去掉decode()是因为图片请求response的时候不需要边解码，在网页请求时候加上decode()即可
        return response.content

    def parse_data(self, js_content):
        """
        保存json中的title、rate、cover
        """
        video_obj = json.loads(js_content)
        for video in video_obj["subjects"]:
            video_dirt = dict()
            video_dirt["video_name"] = video["title"]
            video_dirt["video_rate"] = video["rate"]
            video_dirt["video_image"] = video["cover"]
            self.datas.append(video_dirt)
            # image_content = self.get_requese(video["cover"])
            # # 使用replace("/","_")来把/替换为_，防止系统报错。
            # with open("./images/" + video["title"].replace("/","_") + ".jpg","wb") as file:
            #     file.write(image_content)



    def save_data(self, content):
        with open('./video.json', 'w', encoding='utf-8') as f:
            # for c in content:
            #     # 不使用ASCii编码码，否则中文有问题。并在前方缩进4个单位
            #     f.write(json.dumps(c, ensure_ascii=False, indent=4))
            #     f.write(',\n')
            # 下面演示的是保存json文件
            d = dict()
            d['subjects'] = content
            f.write(json.dumps(d, ensure_ascii=False, indent=4))

    def run(self):
        for url in self.urls:
            # 此处加上decode()是因为get_requese方法中去掉了decode()
            response = self.get_requese(url).decode()
            self.parse_data(response)
            self.save_data(self.datas)

if __name__ == "__main__":
    # 实例化对象
    DouBan("movie").run()
