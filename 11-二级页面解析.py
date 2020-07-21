import re
import requests
import random
import json

class MovieType:
    # 动作 2
    # 剧情 0
    # 爱情 3
    # 喜剧 1
    # 科幻 4
    # 恐怖 8
    # 动画 7
    Action = 2
    Plot = 0
    Love = 3
    Comedy = 1
    Sci_Fi = 4
    Horror = 8
    Animation = 7

class Dytt:
    def __init__(self, movie_type):
        # 请求地址
        self.url = "https://www.dy2018.com/" + movie_type + "/index_{}.html"
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
        # UTF-8无法解析 更换gbk
        return response.content.decode("gbk")

    def parse_movie_list(self, content):
        # 解析电影列表
        pattern_movie_name = '<table width="100%".*?<tr>.*?<tr>.*?<td height="26".*?<b>.*?<a href="(.*?)".*?title="(.*?)">'
        pattern_movie_rate = '<table width="100%".*?<tr>.*?<tr>.*?<tr>.*?<font.*?>(.*?)<.*?<font.*?>(.*?)</font>'
        results_movie_name = re.compile(pattern_movie_name, re.S).findall(content)
        results_movie_rate = re.compile(pattern_movie_rate, re.S).findall(content)
        print("results_movie_name:" + str(len(results_movie_name)))
        print("results_movie_rate:" + str(len(results_movie_rate)))
        results = zip(results_movie_name, results_movie_rate)
        if (len(results_movie_name) + len(results_movie_rate) == 0):
            print("规则有误")
        else:
            for result_detail in results:
                movie_dict = dict()
                movie_dict["IP_add"] = "https://www.dy2018.com" + result_detail[0][0]
                # 取出位于"《"和"》"之间的电影名称
                movie_dict["name"] = result_detail[0][1].split("《")[-1].split("》")[0]
                # 取出位于"："和" "之间的电影时间
                movie_dict["time"] = result_detail[1][0].split("：")[-1].split(" ")[0]
                # 取出位于" "之间的电影评分
                movie_dict["rate"] = result_detail[1][1].split(" ")[1]
                # 留白 存放电影下载地址
                movie_dict["link"] = ""
                # 留白 区分mp4和mkv
                movie_dict["format"] = ""
                self.datas.append(movie_dict)
                # 解析电影详情
                response_detail = self.get_response(movie_dict["IP_add"])
                yield self.parse_movie_detail(response_detail)

    def parse_movie_detail(self, content):
        # 解析电影详情 注意区分mkv和mp4格式
        pattern = '<td style="WORD-WRAP: break-word".*?href="(.*?.(mp4|mkv)).*?".*?</a>'
        results = re.compile(pattern, re.S).findall(content)
        print(self.datas[-1]["name"] + "一"*(25 - len(self.datas[-1]["name"])) + " 下载链接数目:" + str(len(results)))
        if (len(results) == 0):
            print("无下载地址")
        else:
            for result_detail in results:
                # 多个链接使用空格区分
                self.datas[-1]["link"] += result_detail[0] + " "
                self.datas[-1]["format"] += result_detail[1] + " "
        return self.datas[-1]

    def save_data(self, result):
        # 连续写入 不再使用json文件
        with open('./movie.txt', 'a', encoding='utf-8') as file:
            file.write(json.dumps(result, ensure_ascii=False, indent=4))


    def run(self):
        for index in range(1,4):
            url = self.url.format(index)
            if (index == 1):
                # 处理首页 index.html 切除"index_1.html"部分为"index.html"
                # url = url[:url.index('_')] + ".html"
                url = url.replace("_1", "")
            else:
                url = url
            print(url)
            response = self.get_response(url)
            for result in self.parse_movie_list(response):
                self.save_data(result)
        # 保存json文件
        with open('./movie.json', 'w', encoding='utf-8') as file:
            result_dict = dict()
            result_dict['subjects'] = self.datas
            file.write(json.dumps(result_dict, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    Dytt(str(MovieType.Comedy)).run()