# -*- coding: utf-8 -*-
# @File    : dsf.py
# @Time    : 2023/9/11 15:15
# @Author  : Hubery Hao
import numpy as np

a=[1,2]

b=np.zeros(8)
b[:5]=a[0]
b[5:]=a[1]
print(b)