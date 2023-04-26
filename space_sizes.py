import math
import cap


# dims = [d for d in range(4, 33) if d % 2 == 0]
# space_size = list(map(lambda d: pow(2, d), dims))
# cap_sizes = list(map(lambda d: pow(2, d / 2), dims))
#

def base_convert(i, b):
    result = []
    while i > 0:
        result.insert(0, i % b)
        i = i // b
    return result


def print_cap_base4(cap):
    cap.sort()
    for p in cap:
        print(base_convert(p, 4))


if __name__ == '__main__':
    # Are there any interesting patterns in base 4? No
    print_cap_base4(cap.normalize_cap([0, 17, 130, 243, 196, 165, 22, 23, 168, 249, 250, 203, 140, 173, 142, 207]))
    print()
    print_cap_base4(cap.normalize_cap(
        [0, 33, 258, 483, 324, 997, 742, 135, 840, 809, 106, 203, 300, 973, 174, 655, 464, 593, 722, 403, 788, 533, 694,
         887, 88, 921, 378, 635, 444, 253, 574, 959]))
