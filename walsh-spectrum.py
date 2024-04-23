import decompose_cap_pts
from pyfinite import ffield
from vbf_functions.ab_functions import *

if __name__ == '__main__':
    # dim = 8
    # n = int(dim / 2)
    # n = 4
    # {16} ??
    # n =6
    # {0, 8, 16, -16, -8}
    #
    for n in range(4, 11):
        dim = 2 * n
        print(f'n={n}')
        field = ffield.FField(n)
        # F = lambda p: decompose_cap_pts.gold(p, field)
        F = lambda x: kasami(x, field, find_nontrivial_k=True)
        outputs = set()
        for u in range(pow(2, n)):
            for v in range(1, pow(2, n)):
                outputs.add(walsh(F, u, v, field))
        print(outputs)
