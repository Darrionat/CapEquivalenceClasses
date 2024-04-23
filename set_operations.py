from decompose_cap_pts import *


def direct_sum(cap1, cap2):
    assert dimension(cap1) == dimension(cap2)
    d = dimension(cap1)
    to_return = set()
    for p1 in cap1:
        for p2 in cap2:
            to_return.add(concatenate_binary_strings(p1, p2, 2 * d))
    return list(to_return)


if __name__ == '__main__':
    cap1 = [0, 9, 26, 35, 44, 53, 62, 23]
    cap2 = [39, 38, 10, 20, 51, 42, 32, 60, 4]
    dir_sum = direct_sum(cap1, cap2)
    print(len(dir_sum))
    print(dir_sum)
