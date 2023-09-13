# -*- coding: utf-8 -*-
# @File    : sobol20000.py
# @Time    : 2023/9/12 14:49
# @Author  : Hubery Hao
import csv

import numpy as np
from SALib.analyze import rbd_fast, fast
from SALib.sample import latin, fast_sampler, saltelli
from SALib.test_functions import Sobol_G
from matplotlib import pyplot as plt

import rbdfast_sample
problem = {
    'num_vars': 100,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8','x9','x10',
              'x11', 'x12', 'x13','x14', 'x15', 'x16','x17', 'x18','x19','x20',
              'x21', 'x22', 'x23','x24', 'x25', 'x26','x27', 'x28','x29','x30',
              'x31', 'x32', 'x33','x34', 'x35', 'x36','x37', 'x38','x39','x40',
              'x41', 'x42', 'x43','x44', 'x45', 'x46','x47', 'x48','x49','x50',
              'x51', 'x52', 'x53','x54', 'x55', 'x56','x57', 'x58','x59','x60',
              'x61', 'x62', 'x63','x64', 'x65', 'x66','x67', 'x68','x69','x70',
              'x71', 'x72', 'x73','x74', 'x75', 'x76','x77', 'x78','x79','x80',
              'x81', 'x82', 'x83','x84', 'x85', 'x86','x87', 'x88','x89','x90',
              'x91', 'x92', 'x93','x94', 'x95', 'x96','x97', 'x98','x99','x100'],
    'bounds': [[0,1]]*100
}
# X = latin.sample(problem, 1000)
X = saltelli.sample(problem, 10200,calc_second_order=False)
# X = fast_sampler.sample(problem, 1000)
factor=np.zeros(100)
factor[:]=99
factor[10]=0
factor[20]=0
factor[30]=0
factor[40]=0
factor[15]=1
factor[25]=1
factor[35]=1
factor[45]=1
factor[46:48]=9
Y = Sobol_G.evaluate(X,factor)
from SALib.analyze import sobol as sb

Si = sb.analyze(problem, Y, print_to_console=True,calc_second_order=False)
# ST = fast.analyze(problem, Y, print_to_console=True)
print(Si['S1'])
# 将本次数据存入文件中
csv_file = open('../RBD-fast/sobol20000.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(Si['S1'])

# for i in range(len(data['name'])):
#     writer.writerow([data['name'][i], data['age'][i]])
csv_file.close()

plt.xlabel("Model factors")
# plt.ylabel("")
# plt.title("Case")

xpoints=[i+1 for i in range(100)]
ypoints=Si['S1']
# 设置坐标轴范围
plt.xlim(0,100,10)
plt.ylim(0,0.18,0.02)

# 设置坐标轴刻度
my_x_ticks = np.arange(0, 100, 10)
plt.xticks(my_x_ticks)

plt.axhline(y=0.0982, c='k', ls='--', lw=0.75)  # 垂直于y轴的参考线
plt.axhline(y=0.0245, c='k', ls=':', lw=0.75)  # 垂直于y轴的参考线

plt.scatter(xpoints, ypoints,s=5,c="black",marker="o")
plt.show()
