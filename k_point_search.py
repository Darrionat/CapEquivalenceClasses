from cap import exclude_dist, exclude_points_multiplicities
from itertools import combinations
import random
import os


def random_complete_cap(dim):
    cap = [0]
    # standard basis
    for i in range(0, dim):
        cap.append(int(2 ** i))
    available_pts = list(range(0, 2 ** dim))
    # init excludes check
    for comb in combinations(cap, 3):
        sum = 0
        for p in comb:
            sum ^= p
        available_pts.remove(sum)  # always since we're using the standard basis

    while len(available_pts) > 0:
        to_add = random.choice(available_pts)
        for comb in combinations(cap, 2):
            sum = to_add
            for p in comb:
                sum ^= p
            if sum in available_pts:
                available_pts.remove(sum)
        cap.append(to_add)
    return list(set(cap))


def close():
    duration = 3  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    exit()


import time

if __name__ == '__main__':
    dim = 10
    k = 11
    while True:
        # 5 pt in 8 dim
        # 7 pt in 9 dim
        # 11 pt in 10 dim
        # 13 pt in 11 dim?
        random_cap = random_complete_cap(dim)
        codes_constr = {4: 6,
                        5: 7,
                        6: 9,
                        7: 12,
                        8: 18,
                        9: 24,
                        10: 34,
                        11: 48,
                        12: 66,
                        13: 82,
                        14: 129,
                        15: 152}
        if len(random_cap) > codes_constr[dim] - 1:
            print('very lage cap')
            print(random_cap)
        if k in exclude_points_multiplicities(random_cap).values():
            print(random_cap)
            close()
