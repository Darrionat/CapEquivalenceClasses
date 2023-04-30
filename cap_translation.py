import sys

from decompose_cap_pts import *
import numpy as np
import pickle


def translate_cap(cap, p1, p2, dim):
    translation = stitch_pts(p1, p2, dim)
    return [translation ^ x for x in cap]


def special_translate_cap(cap, p, dim):
    """
    Translates the whole cap by (p,f(p)).
    :param cap: The cap to translate
    :param p: The representative
    :return:
    """
    return translate_cap(cap, p, p, dim)


def scale_cap(cap, p, dim):
    translation = stitch_pts(p, p, dim)
    F = ffield.FField(dim)
    return [F.Multiply(translation, x) for x in cap]


def special_translators_sim(n, apn_not_ab):
    # print('n\t', n)
    dim = n * 2
    field = ffield.FField(n)
    if apn_not_ab:
        if n % 2 == 1:
            f = lambda x: inverse(x, n, field)
        elif n % 5 == 0:
            f = lambda x: dobbertin(x, n, field)
        else:
            exit(1)
    else:
        f = lambda x: gold(x, field, dim=n, find_nontrivial_k=True)

    cap = build_points(dim, f)
    # total_points = set()
    # two_fixed = 0
    # with open('total_points', 'w') as f:
    for t in range(0, 2 ** n):
        # x in cap
        # (t,t) + x for all x
        translation = special_translate_cap(cap, t, dim)
        for p in translation:
            print(p)
            # f.write(f'{p}\n')
        # total_points.update(translation)
        # fixed_points = len(set(translation) & set(cap))
        # if fixed_points == 2:
        #     two_fixed += 1


# count = len(total_points)
# not_count = 2 ** dim - count
# print('Translation Cover #\t', count, 'Translation Not-Cover #\t', not_count)
# print('2-Fix\t', two_fixed)


if __name__ == '__main__':
    '''
    USAGE: python3 cap_translation.py [0 or 1 for strict_apn] [n] | sort -nu > total_points_sorted && wc -l total_points_sorted
    '''
    n = int(sys.argv[-1])
    strict_apn = int(sys.argv[-2])
    special_translators_sim(n, strict_apn)
