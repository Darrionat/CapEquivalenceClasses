import math


def is_prime(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True


def largest_prime_less_than_or_equal_to(n):
    if n < 2:
        return None
    if n == 2:
        return 2
    if n % 2 == 0:
        n -= 1  # Ensure we start with an odd number
    to_return = n
    while to_return >= 2:
        if is_prime(to_return):
            return to_return
        to_return -= 2
    return to_return


def sidon_set_upperbound(dim):
    return math.floor(math.sqrt(2) * (2 ** (dim / 2)))


def k_max_upperbound(dim):
    # s_max = maximum sidon set size
    # The idea is that: k_max <= s_max / 3
    return sidon_set_upperbound(dim) // 3


if __name__ == '__main__':
    for d in range(2, 100):
        print(d)
        upper_bound = k_max_upperbound(d)
        # print(f'dim={d}')
        print(largest_prime_less_than_or_equal_to(upper_bound))
        # print(f'largest_prime_<=_to={largest_prime_less_than_or_equal_to(upper_bound)}\n')
