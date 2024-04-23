from decompose_cap_pts import *


def derivative_image(f, a, n):
    deriv_range = set()
    for x in range(0, 2 ** n):
        deriv_range.add(f(x) ^ f(x ^ a))
    return list(deriv_range)


def symmetric_design_test(apn_func, n):
    [x, y] = random.sample(list(range(1, 2 ** n)), 2)
    count_a = 0
    for a in range(1, 2 ** n):
        f_deriv_image = derivative_image(apn_func, a, n)
        if x in f_deriv_image and y in f_deriv_image:
            count_a += 1
    print(count_a)


if __name__ == '__main__':
    for n in range(5, 20, 1):
        print(f'---------n={n}---------')
        field = ffield.FField(n)
        apn_func = lambda x: dobbertin(x, n, field)
        assert is_apn(apn_func, n, field)
        print(f'Permutation={surjective_function(apn_func, n, field)}')
        symmetric_design_test(apn_func, n)
        print(f'Expected: 2^(n-2)={2 ** (n - 2)}')
        print(f'permuation={surjective_function(apn_func, n, field)}')
