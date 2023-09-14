# -*- coding: utf-8 -*-
# @File    : HRF_sample.py
# @Time    : 2023/9/11 21:42
# @Author  : Hubery Hao
import math

import numpy as np

from SALib. util import scale_samples, read_param_file


def sample(problem, N, M=4, seed=None,w=None):
    if seed:
        np.random.seed(seed)

    if N <= 4 * M**2:
        raise ValueError("""
        Sample size N > 4M^2 is required. M=4 by default.""")

    D = problem['num_vars']

    # Transformation to get points in the X space
    X = np.zeros([N * D, D])
    omega2=np.zeros(D)
    omega2[:4]=w[0]
    omega2[4:8]=w[1]
    omega2[8:12]=w[2]
    omega2[12:16]=w[3]
    omega2[16:]=w[4]



    for i in range(D):
        l = range(i * N, (i + 1) * N)

        # Discretization of the frequency space, s
        s = (2 * math.pi / N) * np.arange(N)

        # random phase shift on [0, 2pi) following Saltelli et al.
        # Technometrics 1999
        phi = 2 * math.pi * np.random.rand()

        for j in range(D):
            g = 0.5 + (1 / math.pi) * np.arcsin(np.sin(omega2[j] * s + phi))
            np.random.shuffle(g)
            X[l, j] = g

    X = scale_samples(X, problem)

    return X


