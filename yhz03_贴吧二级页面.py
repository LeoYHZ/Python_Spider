import re
import requests
import random
import json
import time

class TieBa:
    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?kw=" + name + "&ie=utf-8&pn={}"
        self.headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            },
            {
                "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            }
        ]
        self.urls = [self.url.format(i * 50) for i in range(0, 1, 1)]
        self.page_sun_num = 0

    def get_requese(self, url):
        header = self.headers[random.randint(0, 1)]
        response = requests.get(url=url, headers=header)
        return response.content.decode()

    def parse_data(self, index):
        pattern = '<div.*?"threadlist_lz clearfix">.*?href="(.*?)".*?title="(.*?)".*?<div.*?"threadlist_author pull_right">.*?title="主题作者: (.*?)".*?>.*?'
        result = re.compile(pattern, re.S).findall(index)
        print("帖子数目:" + str(len(result)))
        for post in result:
            post_dirt = dict()
            post_dirt["链接"] = "https://tieba.baidu.com" + post[0]
            post_dirt["标题"] = post[1]
            post_dirt["作者"] = post[2]
            self.page_sun_num += 1
            yield self.parse_data_detail(self.get_requese(post_dirt["链接"])),post_dirt["标题"]

    def parse_data_detail(self, index):
        # 检索回帖
        pattern_sun = '<cc>.*?"j_ueg_post_content p_forbidden_tip".*?<div.*?"d_post_content j_d_post_content ".*?"display:;".*?>\s*(.*?)</div>'
        # 检索带图片的回帖中的图片
        pattern_sun_post_img = '<img.*?src="(.*?)".*?'
        # 检索带图片的回帖中的文字
        pattern_sun_post_img_word = '(.*?)<.*>(.*?)'
        # 检索回帖背景
        pattern_sun_post_bg = '<div class="post_bubble_top"'
        result_sun = re.compile(pattern_sun, re.S).findall(index)
        post_list = list()
        post_num = 1
        for post_sun in result_sun:
            post_sun_dirt = dict()
            if re.compile(pattern_sun_post_img, re.S).findall(post_sun):
                # 带图片或表情的回帖
                post_sun_dirt[str(post_num) + "楼"] = re.compile(pattern_sun_post_img, re.S).findall(post_sun) + re.compile(pattern_sun_post_img_word, re.S).findall(post_sun)
                post_num += 1
                post_list.append(post_sun_dirt)
            elif re.compile(pattern_sun_post_bg, re.S).match(post_sun):
                # 贴吧背景 不提取
                pass
            else:
                post_sun_dirt[str(post_num) + "楼"] = post_sun.replace("<br>", "")
                post_num += 1
                post_list.append(post_sun_dirt)
        return post_list

    def save_data(self, result):
        with open("./tieba/" + "帖子详情" + str(self.page_sun_num) + ".json", "w") as file:
            print("打印帖子详情" + str(self.page_sun_num))
            d = dict()
            # 当前帖子标题
            d['title'] = result[1]
            # 当前帖子回帖详情
            d['subjects'] = result[0]
            file.write(json.dumps(d, ensure_ascii=False, indent=4))

    def run(self):
        for url in self.urls:
            response = self.get_requese(url)
            for result in self.parse_data(response):
                self.save_data(result)

if __name__ == "__main__":
    start = time.time()
    TieBa("艾斯").run()
    end = time.time()
    print('Running time: %s Seconds' % (end - start))