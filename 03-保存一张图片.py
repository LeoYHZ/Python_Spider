import requests

request_url = "https://5b0988e595225.cdn.sohucs.com/images/20170930/f323fa5f3b334060988bf1c3d8500522.jpeg"

response = requests.get(url=request_url)

img_content = response.content
# 保存图片
save_dir = "./img.jpg"
# 打开文件 若没有该文件 则新建文件
with open(save_dir, 'wb') as file:
    file.write(img_content)