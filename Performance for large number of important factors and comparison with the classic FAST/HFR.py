# -*- coding: utf-8 -*-
# @File    : HFR.py
# @Time    : 2023/9/12 15:33
# @Author  : Hubery Hao
import csv

import numpy as np
from SALib.analyze import rbd_fast
from SALib.test_functions import Sobol_G
from matplotlib import pyplot as plt

import HRF_sample
problem = {
    'num_vars': 20,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8','x9','x10',
              'x11', 'x12', 'x13','x14', 'x15', 'x16','x17', 'x18','x19','x20'],
    'bounds': [[0,1]]*20
}
# 设置两组 x1-x4,x5-x8
X = HRF_sample.sample(problem, 5000,w=[11,21,27,35,39])
# X = fast_sampler.sample(problem, 1000)
factors=np.zeros(20)
factors[10:]=0
factors[:10]=99

Y = Sobol_G.evaluate(X,factors)
Si = rbd_fast.analyze(problem, X, Y, print_to_console=True,M=6)
# ST = fast.analyze(problem, Y, print_to_console=True)
print(Si['S1'])

# 将本次数据存入文件中
csv_file = open('../Performance for large number of important factors and comparison with the classic FAST/HFR5000.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(Si['S1'])

# for i in range(len(data['name'])):
#     writer.writerow([data['name'][i], data['age'][i]])
csv_file.close()
# 设置坐标轴范围
plt.xlim(0,20,2)
plt.ylim(0,0.03,0.005)

# 设置坐标轴刻度
my_x_ticks = np.arange(0, 20,2)
my_y_ticks = np.arange(0,0.03,0.005)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

xpoints=[i+1 for i in range(20)]
ypoints=Si['S1']


plt.axhline(y=0.0199, c='k', ls='-', lw=0.75)  # 垂直于y轴的参考线

plt.scatter(xpoints, ypoints,s=5,c="black",marker="d")
plt.show()
