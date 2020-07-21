import re
import requests
import random
import json
import time


class TieBa:
    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?kw=" + name + "&ie=utf-8&pn={}"
        # 构造请求头
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        self.urls = [self.url.format(i * 50) for i in range(0, 1, 1)]
        self.datas = list()
        self.page_sun_num = 1

    def get_requese(self, url):
        # 随机取出请求头
        header = self.headers[random.randint(0, 1)]
        # 发送请求获得响应
        response = requests.get(url=url, headers=header)
        # 加入延时，防止系统读取过快，小于接收response的时间
        # time.sleep(1)
        return response.content

    def page_sun(self,url):
        header = self.headers[random.randint(0, 1)]
        response_sun = requests.get(url=url, headers=header)
        # 检索回帖
        pattern_sun = '<cc>.*?"j_ueg_post_content p_forbidden_tip".*?<div.*?"d_post_content j_d_post_content ".*?"display:;".*?>\s*(.*?)</div>'
        # 检索回帖图片
        pattern_sun_post_img = '.*?src="(.*?)".*?'
        # 检索回帖背景
        pattern_sun_post_bg = '<div class="post_bubble_top"'
        result_sun = re.compile(pattern_sun, re.S).findall(response_sun.content.decode())
        post_list = list()
        post_num = 1
        for post_sun in result_sun:
            post_sun_dirt = dict()
            if re.compile(pattern_sun_post_img, re.S).findall(post_sun):
                # 回帖的图片或者表情
                post_sun_dirt[str(post_num) + "楼"] = re.compile(pattern_sun_post_img, re.S).findall(post_sun)
                post_num += 1
                post_list.append(post_sun_dirt)
            elif re.compile(pattern_sun_post_bg, re.S).match(post_sun):
                # 贴吧背景 不提取
                pass
            else:
                post_sun_dirt[str(post_num) + "楼"] = post_sun.replace("<br>", "")
                post_num += 1
                post_list.append(post_sun_dirt)
        # print(post_list)
        with open("./tieba/" + "帖子详情" + str(self.page_sun_num) + ".json", "w") as file:
            print("打印帖子详情" + str(self.page_sun_num))
            d = dict()
            d['subjects'] = post_list
            file.write(json.dumps(d, ensure_ascii=False, indent=4))

    def parse_data(self, index):
        # with open("./post.json", "w") as file:
        #     file.write(index)
        pattern = '<div.*?"threadlist_lz clearfix">.*?href="(.*?)".*?title="(.*?)".*?<div.*?"threadlist_author pull_right">.*?title="主题作者: (.*?)".*?>.*?'
        # re.S会自动处理换行符
        result = re.compile(pattern, re.S).findall(index)
        print("帖子数目:" + str(len(result)))
        for post in result:
            post_dirt = dict()
            post_dirt["链接"] = "https://tieba.baidu.com" + post[0]
            self.page_sun(post_dirt["链接"])
            self.page_sun_num += 1
            post_dirt["标题"] = post[1]
            post_dirt["作者"] = post[2]
            self.datas.append(post_dirt)
        # 保存缩略图
        # pattern_img = 'class="threadlist_text pull_left".*?data-original="(.*?)"'
        # result_img = re.compile(pattern_img, re.S).findall(index)
        # print("缩略图数目:" + str(len(result_img)))
        # num = 0
        # for post_img in result_img:
        #     num += 1
        #     image_content = self.get_requese(post_img)
        #     with open("./images/" + "缩略图" + str(num) + ".jpg", "wb") as file:
        #         print("打印缩略图" + str(num) + " 剩余" + str(len(result_img) - num) +"张")
        #         file.write(image_content)


    def save_data(self, result):
        with open('./post.json', 'w', encoding='utf-8') as file:
            d = dict()
            d['subjects'] = result
            file.write(json.dumps(d, ensure_ascii=False, indent=4))

    def run(self):
        for url in self.urls:
            response = self.get_requese(url)
            self.parse_data(response.decode())
            self.save_data(self.datas)

if __name__ == "__main__":
    start = time.time()
    TieBa("艾斯").run()
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
