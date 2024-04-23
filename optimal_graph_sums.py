from itertools import permutations
from random import shuffle

from decompose_cap_pts import *

from pyfinite import ffield


def is_optimal(cap, dim):
    triplesums = set()
    for comb in combinations(cap, 3):
        sum = 0
        for p in comb:
            sum ^= p
        triplesums.add(sum)
    return len(triplesums) + len(cap) == (2 ** dim)


def is_apn_perm(permutation):
    """
    Checks to see if a permutation is APN
    """
    for a in range(1, 2 ** n):
        sol_range = set()
        for x in range(0, 2 ** n):
            sol_range.add(permutation[x] ^ permutation[x ^ a])
        if len(sol_range) != 2 ** (n - 1):
            return False
    return True


def build_points_from_perm(perm_list, dim):
    """
      Builds a set of points in F_{2^n} with the structure (x, f(x)) with respect to the additive isomorphism between
      F_{2^n} and F_{2^{n/2}} * F_{2^{n/2}}.
      :param perm_list: A list which represents a permutation, with indices corresponding.
      :param dim: The dimension.
      :return:
      """
    assert dim % 2 == 0
    to_return = []
    for p in range(int(2 ** (dim / 2))):
        to_return.append(concatenate_binary_strings(p, perm_list[p], dim))
    return to_return


if __name__ == '__main__':
    # Thm by Carlet:
    # G_F is an optimal Sidon Set iff G_F + G_F + G_F is covers (\F_2^n)^2
    # Can we generalize this?
    # By Rose, Redman, Walker x -> x^3 is optimal, so let's try the Gold function.
    '''
    for n in range(2, 20, 2):
        dim = 2 * n
        print(f'------------------{n}-------------')
        field = ffield.FField(n)
        for d in range(0, 50):
            f = lambda x: field_exp(x, d, field)
            cap = build_points(dim, f)
            if not is_cap(cap):
                continue
            # apn = is_apn(f, n, field)
            # if not apn:
            #     continue
            if not is_optimal(cap, dim):
                print(d)
                print(cap)
                exit()
        '''

    for n in range(7, 16, 1):
        # All work for 3
        dim = 2 * n
        print(f'----------{n}-----------')
        perms = permutations(list(range(2 ** n)))
        for perm in perms:
            perm_list = list(perm)
            shuffle(perm_list)
            # permutation_good = check_gamma(perm_list, n)
            apn = is_apn_perm(perm_list)
            if apn:
                cap = build_points_from_perm(perm_list, dim)
                optimal = is_optimal(cap, dim)
                if not optimal:
                    print(perm_list)
                    exit()
                else:
                    print(f'{perm_list} optimal')
        print('did all')
