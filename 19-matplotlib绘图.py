from matplotlib import pyplot

# 面板 figure对象
pyplot.figure(figsize=(20, 8), dpi=60)

# 准备刻度：x和y（x1,y1）需要注意x轴数据和y轴必须一致（x2, y2）
x = range(1, 10, 2)
y = [16, 12, 2, 9, 17]

# 设置刻度
pyplot.xticks(range(1, 10, 2))
pyplot.yticks(range(min(y), max(y) + 1, 2))

# 绘制
pyplot.plot(x, y)
# 显示
# pyplot.show()
# wsl下无图形界面 更换为保存图片
pyplot.savefig("matplotlib.png")