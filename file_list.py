import os

file_path = "/workspace/images/references/"
file_list = os.listdir(file_path)
name_list = []
f = open("/workspace/list_files/final_references", 'w')
for el in file_list:
    name, _ = el.split(".")
    name_list.append(name)

name_list.sort()
for el in name_list:
    data = el + '\n'
    f.write(data)
f.close()
