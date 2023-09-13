# -*- coding: utf-8 -*-
# @File    : Getpictures_sobol.py
# @Time    : 2023/9/6 16:48
# @Author  : Hubery Hao
import csv

from matplotlib import pyplot as plt

filename = '../sobol_TAE/groupD_TAE.csv'
with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)

    # 遍历csvreader对象的每一行内容并输出
    TAE=[row for row in csvreader ]
TAE_Y=[(float(i)) for i in TAE[0]]
TAE_E=[(float(i)) for i in TAE[1]]

# # 绘制坐标轴标签plt.xlabel("Sample Size")
plt.xlabel("Sample Size")
plt.ylabel("Total Absolute Error")
plt.title("Case")
# x = np.arange(0, 200, 1200)

xpoints=[64,128,256,512,1024]
ypoints=TAE_Y

plt.xlim(0,1200,200)
plt.ylim(0,0.6)

plt.plot(xpoints,ypoints,linestyle="-",color="k")
plt.errorbar(xpoints,ypoints,yerr=TAE_E,capsize=10,capthick=1,fmt="k",ecolor="k",elinewidth=0.75)
plt.show()
