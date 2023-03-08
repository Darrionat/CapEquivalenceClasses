import time

from sympy import Pow
from sympy.ntheory import isprime
from sympy.ntheory import factorint
from math import comb, gcd

cache = {1: 3}


def sequence(n):
    if n == 1:
        cache[1] = 3
        return 3
    # Already computed
    if n in cache:
        return cache[n]
    if n % 2 == 0:
        cache[n] = cache[n - 1] + Pow(-2, int(n / 2))
    else:
        cache[n] = cache[n - 1] + Pow(2, n)
    return cache[n]


# The sequence of exclude points of either i or j.
def exclude_sequence(n):
    if n % 2 == 0:
        return int((Pow(2, 2 * n + 4) - Pow(2, n + 2)) / 3)
    else:
        return int(2 * (Pow(2, 2 * n + 6) - Pow(2, n + 3)) / 3)


def testa():
    start = time.time()
    max = 10000
    for n in range(2, max):
        if n % 1000 == 0:
            print('Currently at n=', n)
        a_n = int(sequence(n))
        # print('a(' + str(n) + ')=' + str(a_n))
        # print(a_n)
        if isprime(a_n):
            print(n)
            # print('\tprime', isprime(a_n), 'factor')
    print('last at')
    print(cache[max - 1])
    end = time.time()
    print('Time:', end - start)


def test_a_relprime():
    """
    Test if the neighboring terms in a are rel prime
    :return:
    """
    max = 10000
    for n in range(1, max, 2):
        if n % 50000 == 0:
            print('Currently at n=', n)
        x = int(sequence(n))
        y = int(sequence(n + 1))
        if n != 1:
            z = int(sequence(n - 1))
            if gcd(x, z) != 1:
                print('Pair at', n, ',', n - 1, 'not rel prime')
                print(factorint(x))
                print(factorint(z))
                break
        if gcd(x, y) != 1:
            print('Pair at', n, ',', n + 1, 'not rel prime')
            print(factorint(x))
            print(factorint(y))
            break
        # print(x, y)


if __name__ == '__main__':
    test_a_relprime()
    # max = 100000000
    # for n in range(1, max):
    #     a2n_1 = int(sequence(2 * n - 1))
    #     a2n = int(sequence(2 * n))
    #     b2n_1 = int(exclude_sequence(2 * n - 1))
    #     b2n = int(exclude_sequence(2 * n))
    #     lhs = a2n_1 * b2n_1 + a2n * b2n
    #     rhs = comb(int(pow(2, 2 * n + 2)), 3)
    #     if lhs != rhs:
    #         print(a2n_1, a2n, b2n_1, b2n)
    #         print('Failed at n=', n)
    #         exit()
    #     if n % 1000 == 0:
    #         print(n)
