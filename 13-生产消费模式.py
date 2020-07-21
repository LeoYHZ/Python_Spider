# 单线程中的消费模式

# 进程 线程 协程
# 生产者模型----基于协程实现的
# 线程：解决异步并行
# 协程：解决交叉运行
# 角色：2个
# 1、生产者（产生数据）
# 2、消费者（使用数据）
def consumer():
    print("消费者需要消费")
    result = 'test'
    while True:
        # 商品
        n = yield result
        # 若没有商品
        if not n:
            return
        # 此处说明生产者提供了商品给消费者
        print("消费者消费了---%s"%n)
        result = '消费结束'

def product(consumer):
    print("生产者 生产商品")
    # 启动生成器
    # next(consumer)
    print(next(consumer))
    n = 0
    while n<5:
        n += 1
        print("生产者---生产了---%s商品" %n)
        # 把生产的商品交给消费者
        result = consumer.send(n)
        print("生产者售卖商品 得到---%s" %result)

if __name__ == "__main__":
    # 调用消费者返回生成器对象
    c = consumer()
    # 启动生成器对象
    product(c)