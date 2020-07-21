from collections.abc import Iterable

# 列表
list_1 = []
list_2 = list()
print(type(list_1))
print(type(list_2))
# 字典
dict_1 = {}
dict_2 = dict()
print(type(dict_1))
print(type(dict_2))
# 元组（与list的区别：元组定义之后无法修改)
tuple_1 = ()
tuple_2 = tuple()
print(type(tuple_1))
print(type(tuple_2))
# 判断是否是可迭代对象
print(isinstance(list_1,Iterable))
print(isinstance(dict_1,Iterable))
print(isinstance(tuple_1,Iterable))
