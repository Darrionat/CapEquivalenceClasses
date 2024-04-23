from random import shuffle

import numpy as np

from decompose_cap_pts import *

from pyfinite import ffield
from generate_functions import print_gamma_matrix


def gamma_f(fcn, n, a, b):
    if a == 0:
        return 0
    for x in range(2 ** n):
        # F(x+a)
        f_xa = fcn(x ^ a)
        # F(x)
        f_x = fcn(x)
        if f_xa ^ f_x == b:
            return 1
    return 0


def dot(a, b, n):
    a_as_array = [int(c) for c in "{0:b}".format(a).rjust(n, '0')]
    b_as_array = [int(c) for c in "{0:b}".format(b).rjust(n, '0')]
    return np.dot(a_as_array, b_as_array) % 2


def kernel_test(n):
    kernel = set()
    for b in range(2 ** n):
        sum = 0
        for x in range(2 ** n):
            sum += (-1) ** (dot(x, b, n))
        print(sum)
        if sum == 0:
            kernel.add(b)
    print(kernel)
    print(len(kernel))


def delta_sum_form_test():
    n = 3
    ones, zeros = 0, 0
    sum = 0
    field = ffield.FField(n)
    f = lambda x: gold(x, field)
    # for x in range(2 ** n):
    for u in range(2 ** n):
        for a in range(2 ** n):
            for v in range(2 ** n):
                for w in range(2 ** n):
                    # z = w ^ a
                    # if (dot(u, x, n) + dot(v, x, n)) % 2 == 0:
                    # if dot(u, x ^ a, n) == 0:
                    if dot(v, f(w) ^ f(w ^ a), n) == 0:
                        # if dot(u, x ^ a, n) ^ dot(v, x ^ f(w) ^ f(w ^ a), n) == 0:
                        # if dot(u, x ^ a, n) == 0:
                        # if dot(v, x ^ f(w) ^ f(w ^ a), n) == 0:
                        # if dot(u, x, n) ^ dot(v, x, n) == 0:
                        zeros += 1
                    else:
                        ones += 1

            # print(f'zeros={zeros}\tones{ones}')
            # print(zeros - ones)
            sum += (zeros - ones)
            zeros = 0
            ones = 0
            print(f'a={a} \t sum={sum}')
            # print(f'x={x} \t a={a} \t u={u} \t sum={sum}')
            sum = 0


if __name__ == '__main__':
    delta_sum_form_test()
    # kernel_test(4)
    # exit()
    # for n in range(1, 15, 2):
    #     print(f'----------{n}-----------')
    #     dim = 2 * n
    #     field = ffield.FField(n)
    #     f = lambda x: gold(x, field)
    #
    #     walsh_range = {}
    #     walsh_f_sum = 0
    #     for b in range(2 ** n):
    #         for x in range(2 ** n):
    #             walsh_f_sum += (-1) ** (gamma_f(f, n, x, x) + dot(x, b, n))
    #         walsh_range[b] = walsh_f_sum
    #     print(walsh_range)
    #
    #     # b_nonzero_walsh = []
    #     # b_zero_walsh = []
    #     # for b in walsh_range:
    #     #     if walsh_range[b] != 0:
    #     #         b_nonzero_walsh.append(b)
    #     #     else:
    #     #         b_zero_walsh.append(b)
    #     # print('non-zero b', b_nonzero_walsh)
    #     # print('zero b', b_zero_walsh)
    #
    #     walsh_transf_lambda = {}
    #     for b in walsh_range:
    #         # only b in the walsh support (i.e. walsh transf of f of b is non-zero)
    #         if walsh_range[b] == 0:
    #             continue
    #         walsh_lambda_sum = 0
    #         for a in range(2 ** n):
    #             walsh_lambda_sum += (-1) ** (dot(a, b, n))
    #         walsh_transf_lambda[b] = walsh_lambda_sum
    #     print(walsh_transf_lambda)
    #     print(set(walsh_transf_lambda.values()))
