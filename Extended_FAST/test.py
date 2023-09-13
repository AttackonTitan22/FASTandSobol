# -*- coding: utf-8 -*-
# @File    : figure.py
# @Time    : 2023/9/7 16:01
# @Author  : Hubery Hao
import csv

from SALib.sample import fast_sampler
from SALib.test_functions import Sobol_G
import numpy as np
from matplotlib import pyplot as plt
from numpy import mean

from Extended_FAST import paper_FAST_sample, constant_FAST_sample

# 切换group时，更改seq["group x"]以及求TAE的偏差式


# Define the model inputs
problem = {
    'num_vars': 8,
    'names': ['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8'],
    'bounds': [[0,1]]*8
}

seq={"group A":[0,0,0,0,0,0,0,0],"group B":[99,99,99,99,99,99,99,99],"group C":[0,1,4.5,9,99,99,99,99],
     "group D":[99,0,9,0,99,4.5,1,99]}


# Generate samples
param_values=fast_sampler.sample(problem, 257)

# Run model
Y = Sobol_G.evaluate(param_values, np.array(seq["group A"]))

from SALib.analyze import fast

# Perform analysis
Si = fast.analyze(problem, Y, print_to_console=False)



