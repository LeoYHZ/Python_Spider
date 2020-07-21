import os
import requests

# 定义类 包含属性与方法
class BaiDu:
    # 该类实现百度贴吧的内容爬取
    # 属性
    def __init__(self, name):
        # 需要保存的贴吧名称
        self.bar_name = name
        self.url = "https://tieba.baidu.com/f?kw=" + self.bar_name + "&ie=utf-8&pn={}"

    def get_response(self, url):
        # 发送请求获取响应
        response = requests.get(url=url)
        return response.content.decode()

    def save_date(self, content, page):
        # 保存数据
        file_name = "{}吧-{}页".format(self.bar_name, page)
        with open('./tieba/' + file_name, "w", encoding="UTF-8") as file:
            file.write(content)


    def run(self):
        # 启动程序
        for index in range(1,6,1):
            # 拼接请求地址
            url = self.url.format(index * 50)
            # 请求响应
            content = self.get_response(url)
            # 保存数据
            self.save_date(content, index)


if __name__ == "__main__":
    # 实例化对象
    b = BaiDu("艾斯")
    b.run()
