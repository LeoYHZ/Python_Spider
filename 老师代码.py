import re
import requests
import random


class MovieType:
    action = 2         # 动作
    story = 0          # 故事
    love = 3           # 爱情
    science = 4        # 科幻
    terror = 8         # 恐怖
    animation = 5      # 动画
    panic = 7          # 惊悚


class Dytt:
    def __init__(self, movie_type):
        # 请求的地址
        self.url = "https://www.dy2018.com/" + str(movie_type) + "/index_{}.html"
        # 请求头列表
        self.headers = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"},
            {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
        ]

    def get_response(self, url):
        """
        发送请求获取响应
        :return: response body
        """
        response = requests.get(url=url, headers=self.headers[random.randint(0, len(self.headers)-1)])
        return response.content.decode('gbk')

    def parse_movie_list(self, content):
        """
        解析电影列表页
        @电影的名称
        @电影的评分
        :param content:
        :return:
        """
        # 1. 定义提取规则
        pattern_movie_name = '<table width="100%".*?<td height="26".*?<a href="(.*?)".*?title="(.*?)">'
        pattern_movie_rate = '<table width="100%".*?<td style="padding-left:3px">.*?<font color="#F98E6A">(.*?)<'

        # 2. 根据规则匹配结果
        results_movie_name = re.compile(pattern_movie_name, re.S).findall(content)
        results_movie_rate = re.compile(pattern_movie_rate, re.S).findall(content)

        # 3. 判断匹配结果中有没有结果
        if len(results_movie_name) == 0 and len(results_movie_rate) == 0:
            print("提取规则有误!没有匹配到内容---------")
            return

        print(results_movie_name)
        print(results_movie_rate)

        # 4. 创建空字典来保存数据
        film = {}
        # for rt in results_movie_name:
        #     # 保存电影名称
        #     film['file_name'] = rt[1]
        #     # 获取电影的详情地址
        #     film_detail_url = "https://www.dy2018.com" + rt[0]
        #
        # for rt in results_movie_rate:
        #     # '\r\n◎评分: 6.1'
        #     film['rate'] = rt.strip()[rt.strip().index(":") + 1:].strip()

        # print(film)

        # 解析
        for rt in zip(results_movie_name, results_movie_rate):
            # 保存电影名称
            film['file_name'] = rt[0][1]
            # 保存电影评分
            film['rate'] = rt[1].strip()[rt[1].strip().index(":") + 1:].strip()
            # 获取电影的详情地址
            film_detail_url = "https://www.dy2018.com" + rt[0][0]

            # 解析详情页面的数据
            yield self.parse_movie_detail(film_detail_url, film)

    def parse_movie_detail(self, url, film):
        """
        解析电影详情页
        @电影的下载链接
        :param content:
        :return:
        """
        # 1. 向详情地址发送请求获取详情页面的内容
        content = self.get_response(url)
        # 2. 定义匹配规则匹配内容
        pattern = '<td style="WORD-WRAP.*?<a href="(.*?)">'
        # 3. 根据规则提取电影的下载地址
        results = re.compile(pattern, re.S).findall(content)
        # 4. 有的电影是没有下载地址的, 有下载地址就保存
        if len(results) > 0:
            film['download_link'] = results[0]
        # 返回处理好的一个电影(一个字典)
        return film

    def save_data(self, data):
        print("写入文件中")
        print(data)

    def run(self):
        # 1. 构造url
        for index in range(1, 4):
            url = self.url.format(index)
            # 处理一下首页, 因为首页的地址和其他页的地址格式不一致
            # 首页: index.html
            # 第n页: index_n.html
            if index == 1:
                # xxxxx/index_1.html
                url = url[:url.index('_')] + ".html"
            else:
                url = self.url.format(index)
            # 2. 发送请求并获取响应
            content = self.get_response(url)
            # 3. 解析数据
            for x in self.parse_movie_list(content):
                self.save_data(x)


if __name__ == '__main__':
    Dytt(MovieType.terror).run()