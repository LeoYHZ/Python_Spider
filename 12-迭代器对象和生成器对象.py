from collections.abc import Iterable

# 迭代器对象
# [] () {}

# 列表生成式：快速的根据规则生成数据
# 利用列表生成式生成一个迭代器对象

# 举例 1
# 一个列表 生成10个数字 0-10

# list = []
# num = 1
# while num <= 10:
#     list.append(num)
#     num +=1
# print(list)

# 利用列表生成式生成数据 迭代器对象
# list_1 = [i for i in range(1,11,1) if i%2 == 0]
# print(list_1)

# 创建生成器对象方式1 生成器对象
# list_2 = (i for i in range(1,11,1) if i%2 == 0)
# print(list_2)
# print([list_2])
# while True:
#     try:
#         # next函数 返回可迭代对象的下一个项目
#         print(next(list_2))
#     except StopIteration:
#         break

# 斐波那契数列  0 1 1 2 3 5 8 13 21 34 55 89 ...
# 创建生成器对象方式2
# 只要某个方法中含有yield对象，那么该方法就不再是普通的方法，而是一个生成器对象
def fibonacci(num):
    # 初始化前两位
    print("------------1-------------")
    num1,num2 = 0,1
    # 索引
    index = 0
    while index < num:
        print("------------2-------------")
        # 保存结果
        result = num1
        # num1, num2 = num2, num1+num2
        num1 = num2
        num2 = result + num2
        # 索引增加
        index += 1
        # yield后面是数据作为next(函数名)的输出
        yield result
        print("------------3-------------")

f = fibonacci(10)
for x in f:
    print(x)