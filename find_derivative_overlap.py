from itertools import permutations
from random import shuffle

from decompose_cap_pts import *

from pyfinite import ffield
from generate_functions import *


def print_gamma_matrix_combos(f, n):
    M = [[0 for _ in range(2 ** n)] for _ in range(2 ** n)]
    for a in range(2 ** n):
        for b in range(2 ** n):
            M[a][b] = gamma_f(f, n, a, b)
    for comb in combinations(range(2 ** n), 2):
        j, a, b = 0, 0, 0
        for p in comb:
            if j == 0:
                a = p
                j += 1
            else:
                b = p
        if a == 0 or b == 0:
            continue
        a_row = M[a]
        b_row = M[b]
        for i in range(len(a_row)):
            if a_row[i] == 0 == b_row[0]:
                print(f'D_{a}F and D_{b}F do not map to {i}')
                print(f'a=\t{a}\tb=\t{b}\tf(a)={f(a)}\tf(b)={f(b)}\tf(a+b)={f(a ^ b)}')
                print(f'D_aF(b)={f(b) ^ f(a ^ b)}')
                print()
                # a, b, i)


if __name__ == '__main__':
    for n in range(1, 20, 1):
        dim = 2 * n
        print(f'------------------{n}-------------')
        field = ffield.FField(n)
        for d in range(0, 50):
            print(f'-----{d}-------')
            f = lambda x: field_exp(x, d, field)
            apn = is_apn(f, n, field)
            if not apn or not surjective_function(f, n, field):
                continue
            permutation_good, sum = check_gamma_powerfcn(f, n)
            if not permutation_good:
                print('error?', n, d, sum)
                exit(1)
            print_gamma_matrix(f, n)
            for x in range(2 ** n):

                for a in range(1, 2 ** n):
                    if a > 2:
                        break
                    # cycle = set()
                    d_afx = f(x ^ a) ^ f(x)
                    print(f'a = {a}\tx = {x}\tD_{a}F(x) = {d_afx}')
                    # while d_afx not in cycle:
                    #     cycle.add(d_afx)
                    #     d_afx = f(d_afx ^ a) ^ f(d_afx)
                    # print(f'a = {a}\tx = {x}\tcycle = {cycle}')

            # print_gamma_matrix_combos(f, n)
            exit(1)
