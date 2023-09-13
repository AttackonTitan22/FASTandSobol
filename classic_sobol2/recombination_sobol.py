import warnings
from typing import Dict, Optional, Union

import numpy as np
from scipy.stats import qmc

from SALib.sample import common_args
from SALib.util import scale_samples, read_param_file, compute_groups_matrix, _check_groups
def sample(
        problem: Dict,
        N: int,
        *,
        calc_second_order: bool = True,
        scramble: bool = True,
        skip_values: int = 0,
        base_seq=None,
        seed: Optional[Union[int, np.random.Generator]] = None,
):
    D = problem["num_vars"]
    groups = _check_groups(problem)

    # Create base sequence - could be any type of sampling
    qrng = qmc.Sobol(d=2 * D, scramble=scramble, seed=seed)

    # fast-forward logic
    if skip_values > 0 and isinstance(skip_values, int):
        M = skip_values
        if not ((M & (M - 1) == 0) and (M != 0 and M - 1 != 0)):
            msg = f"""
            Convergence properties of the Sobol' sequence is only valid if
            `skip_values` ({M}) is a power of 2.
            """
            warnings.warn(msg, stacklevel=2)

        # warning when N > skip_values
        # see https://github.com/scipy/scipy/pull/10844#issuecomment-673029539
        n_exp = int(np.log2(N))
        m_exp = int(np.log2(M))
        if n_exp > m_exp:
            msg = (
                "Convergence may not be valid as the number of "
                "requested samples is"
                f" > `skip_values` ({N} > {M})."
            )
            warnings.warn(msg, stacklevel=2)

        qrng.fast_forward(M)
    elif skip_values < 0 or not isinstance(skip_values, int):
        raise ValueError("`skip_values` must be a positive integer.")

    # 重新组合 base sequence
    base_sequence = base_seq
    # base_sequence_A=base_sequence[:,0:D]
    # base_sequence_B=base_sequence[:,D:2*D]
    # base_sequence_A=base_sequence_A[:, np.random.permutation(base_sequence_A.shape[1])]
    # base_sequence=np.c_[base_sequence_A,base_sequence_B]
    base_sequence=base_sequence[:, np.random.permutation(base_sequence.shape[1])]

    if not groups:
        Dg = problem["num_vars"]
    else:
        G, group_names = compute_groups_matrix(groups)
        Dg = len(set(group_names))

    if calc_second_order:
        saltelli_sequence = np.zeros([(2 * Dg + 2) * N, D])
    else:
        saltelli_sequence = np.zeros([(Dg + 2) * N, D])

    index = 0

    for i in range(N):
        # Copy matrix "A"
        for j in range(D):
            saltelli_sequence[index, j] = base_sequence[i, j]

        index += 1

        # Cross-sample elements of "B" into "A"
        for k in range(Dg):
            for j in range(D):
                if (not groups and j == k) or (groups and group_names[k] == groups[j]):
                    saltelli_sequence[index, j] = base_sequence[i, j + D]
                else:
                    saltelli_sequence[index, j] = base_sequence[i, j]

            index += 1

        # Cross-sample elements of "A" into "B"
        # Only needed if you're doing second-order indices (true by default)
        if calc_second_order:
            for k in range(Dg):
                for j in range(D):
                    if (not groups and j == k) or (
                            groups and group_names[k] == groups[j]
                    ):
                        saltelli_sequence[index, j] = base_sequence[i, j]
                    else:
                        saltelli_sequence[index, j] = base_sequence[i, j + D]

                index += 1

        # Copy matrix "B"
        for j in range(D):
            saltelli_sequence[index, j] = base_sequence[i, j + D]

        index += 1

    saltelli_sequence = scale_samples(saltelli_sequence, problem)
    return saltelli_sequence
