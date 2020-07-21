# get请求
# 1、获取数据

# post请求
# 1、上传表单(账号、密码等)
# 2、获取数据
# 例：https://tieba.baidu.com/f?kw=%E8%89%BE%E6%96%AF&ie=utf-8&pn=50
# ?后都是请求参数
# kw 和 pn多个请求参数之间使用&连接
import requests

# params = {
#     "kw" : "艾斯",
#     "pn" : "0"
# }
# response = requests.get(url="https://tieba.baidu.com/f", params=params)
# print(response.status_code)
# print(response.url)

# post请求
url = "http://www.renren.com/PLogin.do"
form_data = {
    "email" : "15978476217",
    "password" : "**************OK-test"
}
response = requests.post(url=url, data=form_data)
print(response.status_code)
print(response.content.decode())
# 今天天气非常好 但是github不同步代码
