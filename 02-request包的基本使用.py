import requests


request_url = "https://www.baidu.com/"
# 发送一个请求并得到一个响应
response = requests.get(url=request_url)

# 验证是否请求成功
print(response.status_code)  #200时成功
if response.status_code == 200:
    print("Success!")

# 获取网页内容 (响应体）
# print(response.content)

# 获取网页内容 (str类型）
# print(response.content.decode())
print(response.text)
