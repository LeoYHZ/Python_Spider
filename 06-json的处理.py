import json

with open("./student.json", "r", encoding="UTF-8") as file:
    content = file.read()

# print(content)
# 查看数据类型
# print(type(content))
# json的带有一定格式的（key-value字典格式）的字符串

# 把json转成Python中的数据类型（字典）
py_obj = json.loads(content)
# print(py_obj)
print(type(py_obj))

# 提取数据
for stu in py_obj["class_stu"]:
    print("%s is %d years old." % (stu["stu_name"],stu["stu_age"]))
    # print(stu["stu_id"])
    # print(stu["stu_name"])
    # print(stu["stu_age"])
    for subject in stu["stu_score"]:
        print(subject["subject_name"] + " " + str(subject["score"]))
    print("\r")
