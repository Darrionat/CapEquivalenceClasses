from decompose_cap_pts import *
import numpy as np


def translate_cap(cap, p, dim):
    '''
    Translates the whole cap by (p,f(p)).
    :param cap: The cap to translate
    :param p: The representative
    :return:
    '''
    translation = stitch_pts(p, p, dim)
    return [translation ^ x for x in cap]


def scale_cap(cap, p, dim):
    translation = stitch_pts(p, p, dim)
    F = ffield.FField(dim)
    return [F.Multiply(translation, x) for x in cap]


if __name__ == '__main__':
    # Do not use AB function
    STRICTLY_APN = True
    for n in range(5, 11):
        print('n\t', n)
        dim = n * 2
        field = ffield.FField(n)
        if STRICTLY_APN:
            if n % 5 != 0:
                print('n not divisible by 5')
                continue
            f = lambda x: dobbertin(x, dim, field)
        else:
            f = lambda x: gold(x, field, dim=dim, find_nontrivial_k=True)

        cap = build_points(dim, f)
        assert is_cap(cap)
        total_points = []
        for t in range(0, 2 ** n):
            translation = translate_cap(cap, t, dim)
            total_points.extend(translation)
            if not is_cap(translation):
                # Should be impossible. Always a cap by translation
                print('Not cap\t', translation)
                exit()
        count = 0
        not_count = 0
        for p in range(2 ** dim):
            if p not in total_points:
                not_count += 1
            else:
                count += 1
        print(count, not_count)
