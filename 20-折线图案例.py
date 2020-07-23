from matplotlib import pyplot as plt
import random

# 正常人心率：60-100
# 用一张图描述一个人在10点钟的心率变化
# 10点0分 10点1分 10点2分。。。
plt.figure(figsize=(20, 8), dpi=80)
# 支持中文
plt.rcParams['font.sans-serif'] = 'SimHei'

# 准备刻度：x和y（x1,y1）需要注意x轴数据和y轴必须一致（x2, y2）
x = range(0, 60, 1)
y1 = [random.randint(60, 100) for i in x]
y2 = [random.randint(60, 100) for i in x]


# 设置刻度
x_new = ["10点{}分".format(i) for i in x]
plt.xticks(list(x), x_new, rotation=45)
plt.yticks(range(60, 100, 1))

plt.xlabel("时间")
plt.ylabel("心率")
# 绘制
plt.plot(x, y1, color="r", marker="o")
plt.plot(x, y2, color="b", marker="x")


# 绘制虚线
plt.grid(alpha=0.2, color='black')
# 显示
# plt.show()
plt.savefig("plot.png")