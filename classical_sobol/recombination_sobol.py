# -*- coding: utf-8 -*-
# @File    : recombination_sobol.py
# @Time    : 2023/9/5 17:10
# @Author  : Hubery Hao
# -*- coding: utf-8 -*-
# @File    : constant_sobol.py
# @Time    : 2023/9/5 16:00
# @Author  : Hubery Hao
from typing import Dict, Optional
import math
import warnings

import numpy as np

from SALib.sample import common_args
from SALib.sample import sobol_sequence
from SALib.util import (scale_samples, read_param_file,
                    compute_groups_matrix, _check_groups)


def sample(problem: Dict, N: int, calc_second_order: bool = True,base_seq=None,
           skip_values: int = None):

    # bit-shift test to check if `N` == 2**n
    if not ((N & (N-1) == 0) and (N != 0 and N-1 != 0)):
        msg = f"""
        Convergence properties of the Sobol' sequence is only valid if
        `N` ({N}) is equal to `2^n`.
        """
        warnings.warn(msg)

    if skip_values is None:
        # If not specified, set skip_values to next largest power of 2
        skip_values = int(2**math.ceil(math.log(N)/math.log(2)))

        # 16 is arbitrarily selected here to avoid initial points
        # for very low sample sizes
        skip_values = max(skip_values, 16)

    elif skip_values > 0:
        M = skip_values
        if not ((M & (M-1) == 0) and (M != 0 and M-1 != 0)):
            msg = f"""
            Convergence properties of the Sobol' sequence is only valid if
            `skip_values` ({M}) is a power of 2.
            """
            warnings.warn(msg)

        # warning when N > skip_values
        # (see: https://github.com/scipy/scipy/pull/10844#issuecomment-673029539)
        n_exp = int(math.log(N, 2))
        m_exp = int(math.log(M, 2))
        if n_exp > m_exp:
            msg = (
                "Convergence may not be valid as the number of requested samples is"
                f" > `skip_values` ({N} > {M})."
            )
            warnings.warn(msg)
    elif skip_values == 0:
        warnings.warn("Duplicate samples will be taken as no points are skipped.")
    else:
        assert isinstance(skip_values, int) and skip_values >= 0, \
            "`skip_values` must be a positive integer."

    D = problem['num_vars']
    groups = _check_groups(problem)

    if not groups:
        Dg = problem['num_vars']
    else:
        G, group_names = compute_groups_matrix(groups)
        Dg = len(set(group_names))

    # 重新组合 base sequence
    base_sequence = base_seq
    # base_sequence_A=base_sequence[:,0:D]
    # base_sequence_B=base_sequence[:,D:2*D]
    # base_sequence_A=base_sequence_A[:, np.random.permutation(base_sequence_A.shape[1])]
    # base_sequence=np.c_[base_sequence_A,base_sequence_B]
    base_sequence=base_sequence[:, np.random.permutation(base_sequence.shape[1])]

    if calc_second_order:
        saltelli_sequence = np.zeros([(2 * Dg + 2) * N, D])
    else:
        saltelli_sequence = np.zeros([(Dg + 2) * N, D])
    index = 0

    for i in range(skip_values, N + skip_values):

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
                    if (not groups and j == k) or (groups and group_names[k] == groups[j]):
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


# def cli_parse(parser):
#     """Add method specific options to CLI parser.
#
#     Parameters
#     ----------
#     parser : argparse object
#
#     Returns
#     ----------
#     Updated argparse object
#     """
#     parser.add_argument('--max-order', type=int, required=False, default=2,
#                         choices=[1, 2],
#                         help='Maximum order of sensitivity indices \
#                            to calculate')
#     parser.add_argument('--skip-values', type=int, required=False, default=None,
#                         help='Number of sample points to skip (default: next largest power of 2 from `samples`)')
#
#     # hacky way to remove an argument (seed option is not relevant for Saltelli)
#     remove_opts = [x for x in parser._actions if x.dest == 'seed']
#     [parser._handle_conflict_resolve(None, [('--seed', x), ('-s', x)]) for x in remove_opts]
#
#     return parser
#
#
# def cli_action(args):
#     """Run sampling method
#
#     Parameters
#     ----------
#     args : argparse namespace
#     """
#     problem = read_param_file(args.paramfile)
#     param_values = sample(problem, args.samples,
#                           calc_second_order=(args.max_order == 2),
#                           skip_values=args.skip_values)
#     np.savetxt(args.output, param_values, delimiter=args.delimiter,
#                fmt='%.' + str(args.precision) + 'e')
#
#
# if __name__ == "__main__":
#     common_args.run_cli(cli_parse, cli_action)
