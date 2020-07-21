import re
# 假设页结构为下
html = '''
    <html>
        <div class="application" id="b">
            <book><p>C语言</p></book>
            <book><p>Python入门</p></book>
            <book><p>第一行代码</p></book>
        </div>
        <div class="eat" id="b">
            <book><p>厨神</p></book>
            <book><p>蛋炒饭</p></book>
            <book><p>黄焖鸡</p></book>
        </div>
    </html>
'''
# 贪婪匹配 一次尽可能多的匹配
# pattern = "<p>(.*)</p>"
# 非贪婪匹配 一次尽可能少的匹配
# pattern = "<p>(.*?)</p>"

# pattern = '<div class="application".*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>'
pattern = '<div.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>'
# re.S会自动处理换行符
result = re.compile(pattern, re.S).findall(html)
for book in result:
    print(book)

html_song = '''
<div id="songs-list">
    <h2 class="title">经典老歌</h2>
    <p class="introduction">经典老歌列表</p>
    <ul id="list" class="list-group">
        <li data-view="2"><a href="/1.mp3" singer="吴奇隆">一路上有你</a></li>
        <li data-view="7"><a href="/2.mp3" singer="任贤齐">沧海一声笑</a></li>
        <li data-view="4"><a href="/3.mp3" singer="齐秦">往事随风</a></li>
        <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
        <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
        <li data-view="5"><a href="/6.mp3" singer="邓丽君">但愿人长久</a></li>
    </ul>
</div>
'''
# 提取歌手和歌名
pattern_song = '<li.*?singer="(.*?)">(.*?)</a>'
result_song = re.compile(pattern_song, re.S).findall(html_song)
for song in result_song:
    print(song[0] + " " + song[1])

"""
user_input = input("请输入任何字符串:")
# 从字符串起始位置匹配正则表达式，如果匹配就返回匹配值，否则None
# 是否以Hello开头
pattern = "^Hello"
print(re.match(pattern, user_input))
# 匹配整个字符串，返回第一个匹配的结果，否则None
# 匹配电话号 TEL + 11位数字(13 15 18开头)
pattern = "^TEL:1[358]\d{9}$"
if (re.search(pattern, user_input)):
    print(re.search(pattern, user_input).group())
else:
    print("未匹配到电话号")
# 匹配json文件名 json JSON Json等
pattern = "^[a-zA-Z0-9]+\.[jJ][sS][oO][nN]"
if (re.search(pattern, user_input)):
    print(re.search(pattern, user_input).group())
else:
    print("未匹配到Json文件")
# 匹配密码 字母开头 7-16位 中间只有字母、数字和下划线
pattern = "^[a-zA-Z]\w{7,16}$"
if (re.search(pattern, user_input)):
    print(re.search(pattern, user_input).group())
else:
    print("未匹配到密码")
"""

"""
s = "A B C D"
# 提取结果是A B和C D规则
pattern = "([A-Z]\s[A-Z])\s([A-Z]\s[A-Z])"
print("提取结果是A B和C D规则")
if (re.search(pattern, s)):
    print(re.search(pattern, s).group(1))
    print(re.search(pattern, s).group(2))
else:
    print("未匹配到A B和C D")
# 提取结果是A 和C 规则
pattern = "([A-Z]\s)[A-Z]\s([A-Z]\s)[A-Z]"
print("提取结果是A 和C 规则")
if (re.search(pattern, s)):
    print(re.search(pattern, s).group(1))
    print(re.search(pattern, s).group(2))
else:
    print("未匹配到A 和C ")
# 提取结果是(A,B)和(C,D)规则
pattern = "([A-Z])\s([A-Z])"
print("提取结果是(A,B)和(C,D)规则")
if (re.findall(pattern, s)):
    print(re.findall(pattern, s))
else:
    print("未匹配到(A,B)和(C,D)")
"""