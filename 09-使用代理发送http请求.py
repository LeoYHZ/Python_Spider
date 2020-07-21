import requests
import random

# 175.172.189.249	9000

# 代理,需要经常更新
# delegate = {
#     "HTTP": "http://175.43.156.54:9999"
# }
# 代理池
delegates ={
    "delegate":[
        {
            "HTTP": "http://123.169.166.127:9999",
            "count":1
        },
        {
            "HTTP": "http://110.243.26.86:9999",
            "count":1
        },
        {
            "HTTP": "http://118.212.107.10:9999",
            "count":1
        },
        {
            "HTTP": "http://127.0.0.1:7892",
            "count": 1
        }
    ]
}
# 请求地址
url = "http://www.baidu.com"
# 请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}
# 随机获取代理
delegate = delegates["delegate"][random.randint(0, len(delegates["delegate"])-1)]
print(delegate)


if delegate["count"] > 5:
    delegate_new = delegates["delegate"][random.randint(0, len(delegates["delegate"]) - 1)]
    delegate["count"] += 1
else:
    delegate["count"] += 1
    response = requests.get(url=url, headers=header, proxies=delegate)
    print(response.status_code)

