from itertools import permutations
from random import shuffle
from decompose_cap_pts import *

from pyfinite import ffield


def is_apn_perm(permutation):
    for a in range(1, 2 ** n):
        sol_range = set()
        for x in range(0, 2 ** n):
            sol_range.add(permutation[x] ^ permutation[x ^ a])
        if len(sol_range) != 2 ** (n - 1):
            return False
    return True


if __name__ == '__main__':
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
    for n in range(8, 16, 2):
        print(f'----------{n}-----------')
        perms = permutations(list(range(2 ** n)))
        for perm in perms:
            perm_list = list(perm)
            shuffle(perm_list)
            apn = is_apn_perm(perm_list)
            if apn:
                print(perm_list)
                while True:
                    pass
            # if permutation_good and not apn:
            #     print(perm_list)
            # print(permutation_good, apn)
        print('did all')
