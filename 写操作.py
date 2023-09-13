# -*- coding: utf-8 -*-
# @File    : 写操作.py
# @Time    : 2023/9/6 16:24
# @Author  : Hubery Hao
import csv
data = {'name': ['xiaoming', 'xiaohong', 'xiaoli'], 'age': [24, 25, 26]}

csv_file = open('example.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(['name', 'age'])
for i in range(len(data['name'])):
    writer.writerow([data['name'][i], data['age'][i]])
csv_file.close()