# -*- coding: utf-8 -*-
# @File    : Hybird rbd_fast.py
# @Time    : 2023/9/11 21:36
# @Author  : Hubery Hao
import numpy as np
from SALib.analyze import rbd_fast
from SALib.test_functions import Sobol_G
import HRF_sample
problem = {
    'num_vars': 8,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8'],
    'bounds': [[0,1]]*8
}
# 设置两组 x1-x4,x5-x8
X = HRF_sample.sample(problem, 1000,w=[11,35])
# X = fast_sampler.sample(problem, 1000)

Y = Sobol_G.evaluate(X,np.array([0, 1, 4.5, 9, 99, 99, 99, 99]))
Si = rbd_fast.analyze(problem, X, Y, print_to_console=True,M=6)
# ST = fast.analyze(problem, Y, print_to_console=True)
X = HRF_sample.sample(problem, 10000,w=[11,35])
# X = fast_sampler.sample(problem, 1000)

Y = Sobol_G.evaluate(X,np.array([0, 1, 4.5, 9, 99, 99, 99, 99]))
Si = rbd_fast.analyze(problem, X, Y, print_to_console=True,M=6)
