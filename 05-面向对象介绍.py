
class Person:
    """
    特征和行为
    特征就是类中的属性（动态属性和类属性）
    行为就是类中的方法（动态方法和静态方法，类方法）
    """
    # 静态属性
    name = "Jack"
    age = "18"
    def eat(self):
        print("%s is eating!" % Person.name)

class Person_New:
    eye = 2
    # 初始化函数，相当于构造函数，创建对象时自动运行
    def __init__(self ,name ,age):
        print("Class %s is building!" % Person_New.__name__)
        # 定义实例属性（动态属性）
        self.name = name
        self.age = age
    # 动态方法
    def introduce(self):
        print("%s is %d years old." % (self.name,self.age))
    # 类方法
    @classmethod
    def run(cls):
        print("%s have %d eyes." % (Person_New.__name__,Person_New.eye))


if __name__ == "__main__":
    # 创建对象
    # 通过对象调用属性及行为
    p1 = Person()
    p1.eat()

    p2 = Person()
    # 修改类中的属性
    Person.name = "Mary"
    p2.eat()
    p1.eat()

    p3 = Person()
    p3.name = "Lora"
    p3.eat()

    p4 = Person_New("Leo",19)
    p4.introduce()
    Person_New.introduce(p4)
    p4.run()
    Person_New.run()