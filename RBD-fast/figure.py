# -*- coding: utf-8 -*-
# @File    : figure.py
# @Time    : 2023/9/12 14:15
# @Author  : Hubery Hao
# # 绘制坐标轴标签plt.xlabel("Sample Size")
import csv

import numpy as np
from matplotlib import pyplot as plt


filename = '../RBD-fast/rbdfast1000.csv'
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    # 遍历csvreader对象的每一行内容并输出
    r=[row for row in csvreader ]
Si=[(float(i)) for i in r[0]]

filename = '../RBD-fast/rbdfast2000.csv'
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    # 遍历csvreader对象的每一行内容并输出
    r=[row for row in csvreader ]
Si2=[(float(i)) for i in r[0]]
filename = '../RBD-fast/sobol20000.csv'
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    # 遍历csvreader对象的每一行内容并输出
    r=[row for row in csvreader ]
Si3=[(float(i)) for i in r[0]]


plt.xlabel("Model factors")
# plt.ylabel("")
# plt.title("Case")

xpoints=[i+1 for i in range(100)]
ypoints=Si
ypoints2=Si2
ypoints3=Si3
# 设置坐标轴范围
plt.xlim(0,100,10)
plt.ylim(0,0.18,0.02)

# 设置坐标轴刻度
my_x_ticks = np.arange(0, 100, 10)
plt.xticks(my_x_ticks)

plt.axhline(y=0.0982, c='k', ls='--', lw=0.75)  # 垂直于y轴的参考线
plt.axhline(y=0.0245, c='k', ls=':', lw=0.75)  # 垂直于y轴的参考线

plt.scatter(xpoints, ypoints,s=8,c="c",marker="v")
plt.scatter(xpoints, ypoints2,s=8,c="m",marker="x")
plt.scatter(xpoints, ypoints3,s=8,c="k",marker="o")


plt.show()
