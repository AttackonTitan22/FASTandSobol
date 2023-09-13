# -*- coding: utf-8 -*-
# @File    : rbdfast.py
# @Time    : 2023/9/11 17:28
# @Author  : Hubery Hao
# Define the model inputs
import numpy as np
from SALib.analyze import rbd_fast, fast
from SALib.sample import latin, fast_sampler
from SALib.test_functions import Sobol_G
import rbdfast_sample
problem = {
    'num_vars': 8,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8'],
    'bounds': [[0,1]]*8
}
# X = latin.sample(problem, 1000)
X = rbdfast_sample.sample(problem, 1000)
# X = fast_sampler.sample(problem, 1000)

Y = Sobol_G.evaluate(X,np.array([0, 1, 4.5, 9, 99, 99, 99, 99]))
Si = rbd_fast.analyze(problem, X, Y, print_to_console=True,M=6)
# ST = fast.analyze(problem, Y, print_to_console=True)
