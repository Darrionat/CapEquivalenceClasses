from numpy import sort

from cap_translation import translate_cap
from decompose_cap_pts import *

if __name__ == '__main__':
    # Count
    for n in range(10, 11):
        dim = 2 * n
        field = ffield.FField(n)
        f = lambda x: gold(x, field, n=n, find_nontrivial_k=False)
        # f = lambda x: kasami(x, field, n=n, find_nontrivial_k=True)
        # f = lambda x: dobbertin(x, n, field)
        # f = lambda x: quadratic_apn_5(x, n, field)
        if not is_apn(f, n, field):
            print(f'{n}:', 'Not APN, skipping')
            continue
        cap = build_points(dim, f)
        none_fixed = 0
        two_fixed = 0
        for t in range(0, 2 ** n):
            translation = translate_cap(cap, t, t, dim)
            fixed_points = len(set(translation) & set(cap))
            if fixed_points == 0:
                none_fixed += 1
            elif fixed_points == 2:
                two_fixed += 1
        print(f'{n}:', none_fixed, two_fixed)
