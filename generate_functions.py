from itertools import permutations
from random import shuffle
from decompose_cap_pts import *
from pyfinite import ffield
import numpy as np
import numpy.linalg as LA


def gamma(permutation, n, a, b):
    if a == 0:
        return 0
    for x in range(2 ** n):
        # F(x+a)
        f_xa = permutation[x ^ a]
        # F(x)
        f_x = permutation[x]
        if f_xa ^ f_x == b:
            # has solution
            return True
    return False


def gamma_f(f, n, a, b):
    return 0 if find_derviative_solution(f, n, a, b) is None else 1


def find_derviative_solution(f, n, a, b):
    if a == 0:
        return None
    for x in range(2 ** n):
        # F(x+a)
        f_xa = f(x ^ a)
        # F(x)
        f_x = f(x)
        if f_xa ^ f_x == b:
            return x
    return None


def check_gamma(permutation, n):
    # 2^{n-1}
    sum = 0
    for x in range(1, 2 ** n):
        sum += gamma(permutation, n, x, x)
    val = int(2 ** (n - 1))
    if n % 2 == 1:
        return sum == val, sum
    return sum == val - 1, sum


def check_gamma_powerfcn(f, n):
    # Counts along the diagonal
    sum = 0
    for x in range(1, 2 ** n):
        has_sol = gamma_f(f, n, x, x)
        sum += has_sol

    val = int(2 ** (n - 1))
    if n % 2 == 1:
        return sum == val, sum
    return sum == val - 1, sum
    # permutation = [f(x) for x in range(2 ** n)]
    # return check_gamma(permutation, n)


def is_apn_perm(permutation):
    for a in range(1, 2 ** n):
        sol_range = set()
        for x in range(0, 2 ** n):
            sol_range.add(permutation[x] ^ permutation[x ^ a])
        if len(sol_range) != 2 ** (n - 1):
            return False
    return True


def print_gamma_matrix(f, n):
    M = [[0 for _ in range(2 ** n)] for _ in range(2 ** n)]
    for a in range(2 ** n):
        for b in range(2 ** n):
            M[a][b] = gamma_f(f, n, a, b)
    print_matrix(M)
    M_np = np.array(M)
    M_minor = M_np[1:, 1:]
    print(np.dot(M_minor, np.transpose(M_minor)))
    # print('rank', LA.matrix_rank(M))
    # print('det', LA.det(M))
    evalues, evec = LA.eig(M)
    v = np.zeros((2 ** n, 1))
    v[int(2 ** n - 1)] = 1
    # print(v)
    # print(np.matmul(M, v))
    # print('evalues', evalues)
    # print('evecs?', evec)
    # print(LA.matrix_rank(np.matmul(M, np.ones((2 ** n, 2 ** n)))))
    # exit()


def balanced_tests(f, n):
    for t in range(0, 2 ** n):
        solution = find_derviative_solution(f, n, t, t)
        if solution is None:
            continue

        print(gamma_f(f, n, solution, solution))


if __name__ == '__main__':
    for n in range(3, 7, 1):
        print(f'------------------{n}------------------')
        field = ffield.FField(n)
        for d in range(3, 4):
            print(f'-------------{d}-------------')
            f = lambda x: field_exp(x, d, field)
            apn = is_apn(f, n, field)
            permutation = surjective_function(f, n, field)
            if not apn or not permutation:
                continue
            balanced_tests(f, n)
            print(print_gamma_matrix(f, n))
    '''
    for n in range(3, 20, 1):
        sums = set()
        print(f'------------------{n}-------------')
        # n odd - permutation - 2^{n-1}
        field = ffield.FField(n)
        # perms = permutations(list(range(2 ** n)))
        for d in range(3, 50):
            # f = lambda x: dobbertin(x, 2 * n, field)
            f = lambda x: field_exp(x, d, field)
            permutation_good, sum = check_gamma_powerfcn(f, n)
            is_permutation = surjective_function(f, n, field)  # surj = inj = bij
            apn = is_apn(f, n, field)
            if apn and is_permutation and not permutation_good:
                print('woah??', d, n)
                exit()
            if apn and sum not in sums:
                print_gamma_matrix(f, n)
                sums.add(sum)
        # if not permutation_good:
        # print('NOT GOOD')
        # exit()
        # print('good')
    print(sums)
    '''
'''
for n in range(3, 16, 2):
    print(f'----------{n}-----------')
    perms = permutations(list(range(2 ** n)))
    for perm in perms:
        perm_list = list(perm)
        shuffle(perm_list)
        permutation_good = check_gamma(perm_list, n)
        apn = is_apn_perm(perm_list)
        if apn:
            print(perm_list)
            if not permutation_good:
                print(perm_list)
                print('NOT GOOD')
                exit()
        # if permutation_good and not apn:
        #     print(perm_list)
        # print(permutation_good, apn)
    print('did all')
'''
