# -*- coding: utf-8 -*-
# @File    : figure.py
# @Time    : 2023/9/5 21:40
# @Author  : Hubery Hao
# # 绘制坐标轴标签
import numpy as np
from matplotlib import pyplot as plt
TAE_Y=[0.19228438491834962, 0.14404845574913203, 0.08074842532219442, 0.04746458222327341, 0.024629438350495855]
TAE_E=[0.10995859865357209, 0.1267947636615491, 0.06588011801368629, 0.033193845837207955, 0.015437868881574324]
plt.xlabel("Sample Size")
plt.ylabel("Total Absolute Error")
plt.title("Case")

xpoints=[64,128,256,512,1024]
ypoints=TAE_Y

plt.ylim(0,0.6)
plt.xlim(0,1200,200)
# x = np.arange(0, 200, 1200)

plt.plot(xpoints,ypoints,linestyle="-",color="k")
# ,markeredgecolor="b",fillstyle="full"
plt.errorbar(xpoints,ypoints,yerr=TAE_E,capsize=10,capthick=1,fmt="k",ecolor="k",elinewidth=0.75)
plt.show()
