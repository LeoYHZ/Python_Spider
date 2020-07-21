from lxml import etree

html = """
<html>
    <div>
        <ul>
            <li class='i1'><a href='link1.html'>c语言</a></li>
            <li class='i2'><a href='link2.html'>c++</a></li>
            <li class='i3'><a href='link3.html'>python</a></li>
            <li class='i4'><a href='link4.html'>mongodb</a></li>
            <li class='i5'><a href='link5.html'>mysql</a></li>
            <li class='i6'><a href='link6.html'>lua</a></li>       
        </ul>
    </div>
    <div class='neuedu'>
        <ul>
            <li class='i1'><a href='link1.html'>aa</a></li>
            <li class='i2'><a href='link2.html'>bb</a></li>
            <li class='i3'><a href='link3.html'>cc</a></li>
            <li class='i4'><a href='link4.html'>dd</a></li>
            <li class='i5'><a href='link5.html'>ee</a></li>
            <li class='i6'><a href='link6.html'>ff</a></li>       
        </ul>

        <ul>
            <li class='i1'><a href='link1.html'>连城诀</a></li>
            <li class='i2'><a href='link2.html'>射雕英雄</a></li>
            <li class='i3'><a href='link3.html'>倚天屠龙</a></li>
            <li class='i4'><a href='link4.html'>笑傲江湖</a></li>
            <li class='i5'><a href='link5.html'>鹿鼎记</a></li>
            <li class='i6'><a href='link6.html'>大唐双龙</a></li>       
        </ul>
    </div>
    <ul class='neuedu'>
        <ul>
            <li class='i1'><a href='link1.html'>aa1</a></li>
            <li class='i2'><a href='link2.html'>bb1</a></li>
            <li class='i3'><a href='link3.html'>cc1</a></li>
            <li class='i4'><a href='link4.html'>dd1</a></li>
            <li class='i5'><a href='link5.html'>ee1</a></li>
            <li class='i6'><a href='link6.html'>ff1</a></li>       
        </ul>
    </ul>
</html>
"""
# 创建xpath对象
html_obj = etree.HTML(html)
# 根据xpath语法查找对象
# 提取class=i1的li节点中的a标签内容 text函数提取标签内容
# result = html_obj.xpath("//li[@class='i1']/a/text()")
# result = html_obj.xpath("//div/ul/li[@class='i1']/a/text()")
# result = html_obj.xpath("//ul/li/a[@href='link1.html']/text()")

# 提取所有a标签的href属性
# result = html_obj.xpath("//a/@href")

# 提取div class是neuedu标签下的第一个ul节点下的a节点
# result = html_obj.xpath("//div[@class='neuedu']/ul[1]//a/text()")
# 提取div class是neuedu标签下的最后一个ul节点下的a节点
# result = html_obj.xpath("//div[@class='neuedu']/ul[last()]//a/text()")

# 提取所有class是neuedu标签下的第一个ul节点下的a节点
result = html_obj.xpath("//*[@class='neuedu']/ul//a/text()")

for result_final in result:
    print(result_final)