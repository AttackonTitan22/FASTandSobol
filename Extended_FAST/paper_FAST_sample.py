# -*- coding: utf-8 -*-
# @File    : paper_FAST_sample.py
# @Time    : 2023/9/7 15:02
# @Author  : Hubery Hao
import math

import numpy as np

from SALib. util import scale_samples, read_param_file


def sample(problem, N, M=4, seed=None):
    if seed:
        np.random.seed(seed)

    if N <= 4 * M**2:
        raise ValueError("""
        Sample size N > 4M^2 is required. M=4 by default.""")

    D = problem['num_vars']

    omega = np.zeros([D])
    omega[0] = math.floor((N - 1) / (2 * M))
    m = math.floor(omega[0] / (2 * M))

    if m >= (D - 1):
        omega[1:] = np.floor(np.linspace(1, m, D - 1))
    else:
        omega[1:] = np.arange(D - 1) % m + 1

    # Discretization of the frequency space, s
    s = (2 * math.pi / N) * np.arange(N)

    # Transformation to get points in the X space
    X = np.zeros([N * D, D])
    omega2 = np.zeros([D])

    for i in range(D):
        omega2[i] = omega[0]
        idx = list(range(i)) + list(range(i + 1, D))
        omega2[idx] = omega[1:]
        l = range(i * N, (i + 1) * N)

        # random phase shift on [0, 2pi) following Saltelli et al.
        # Technometrics 1999
        phi = 2 * math.pi * np.random.rand()

        for j in range(D):
            g = 0.5 + (1 / math.pi) * np.arcsin(np.sin(omega2[j] * s + phi))
            X[l, j] = g

    X = scale_samples(X, problem)

    return X,s


