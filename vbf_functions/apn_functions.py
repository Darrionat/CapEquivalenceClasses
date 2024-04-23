from vbf_functions.vbfs import *


def gold(field, k=1, find_nontrivial_k=False, use_caching=True):
    n = field.n
    assert math.gcd(n, k) == 1
    if find_nontrivial_k:
        # k can always be taken less than n/2 due to conjugacy [c.f. Carlet, Picek]
        for l in range(2, n // 2 + 1):
            if math.gcd(n, l) == 1:
                k = l
                break
    d = int(2 ** k) + 1
    return PowerVBF(d, field, use_caching, apn=True, ab=(n % 2 == 1))


def kasami(field, k=1, find_nontrivial_k=False, use_caching=True):
    n = field.n
    k_exp = k
    if find_nontrivial_k:
        # k can always be taken less than n/2 due to conjugacy
        # See "On the exponents of APN power functions and Sidon sets,
        # sum-free sets, and Dickson polynomials" by Carlet, Picek).
        for l in range(2, n // 2 + 1):
            if math.gcd(n, l) == 1:
                k_exp = l
    exp = int(2 ** (2 * k_exp)) - int(2 ** k_exp) + 1
    return PowerVBF(exp, field, use_caching, apn=True, ab=(n % 2 == 1))


def welch(field, use_caching=True):
    n = field.n
    assert n % 2 == 1
    m = (n - 1) / 2
    exp = int(2 ** m) + 3
    return PowerVBF(exp, field, use_caching, apn=True, ab=True)


def niho(field, use_caching=True):
    n = field.n
    assert n % 2 == 1
    t = (n - 1) // 2
    if t % 2 == 0:
        d = int(2 ** t + 2 ** (t / 2) - 1)
    else:
        d = int(2 ** t + 2 ** ((3 * t + 1) / 2) - 1)
    return PowerVBF(d, field, use_caching, apn=True, ab=True)


def inverse(field):
    n = field.n
    assert field.n % 2 == 1
    m = (n - 1) / 2
    return PowerVBF(int(2 ** (2 * m)) - 1, field, use_caching=True, apn=True, ab=False)


def dobbertin(field, use_caching=True):
    n = field.n
    assert n % 5 == 0
    t = n / 5
    d = int(2 ** (4 * t) + 2 ** (3 * t) + 2 ** (2 * t) + 2 ** t - 1)
    return PowerVBF(d, field, use_caching, apn=True, ab=False)


def quadratic_CCZ_inquiv_to_power(field, a=1, use_caching=True):
    """
    This function is inquivalent to any Gold function for n >= 7, and for n=7, it's inequivalent to any power mapping.
    :param field:
    :param a:
    :param use_caching:
    :return:
    """
    assert a != 0
    a_inv = field.Inverse(a)
    a3 = field_exp(a, 3, field)
    trace_of_a3x9 = lambda x: (
        trace(field.Multiply(a3, field_exp(x, 9, field)), field))
    fcn = lambda x: (field_exp(x, 3, field) ^
                     field.Multiply(a_inv, trace_of_a3x9(x)))
    return VBF(field, fcn, use_caching, ab=(field.n % 2 == 1))


def quadratic_CCZ_inquiv_to_power2(field, a=1, use_caching=True):
    assert a != 0
    assert n % 3 == 0
    a_inv = field.Inverse(a)
    a3 = field_exp(a, 3, field)
    a6 = field_exp(a, 6, field)
    trace3_of_a3x9_plus_a6x18 = lambda x: (
        trace(field.Multiply(a3, field_exp(x, 9, field)) ^ field.Multiply(a6, field_exp(x, 18, field)),
              field, m=3))
    fcn = lambda x: field_exp(x, 3, field) ^ field.Multiply(a_inv, trace3_of_a3x9_plus_a6x18(x))
    return VBF(field, fcn, use_caching, ab=(field.n % 2 == 1))


def dillion_APN_permutation_dim6(field, use_caching=True):
    assert field.n == 6
    c_powers = [25, 30, 32, 37, 23, 39, 44, 4, 18, 46, 51, 52, 18, 56, 53, 30, 1, 58, 60, 37, 51, 1, 2, 4, 44, 32, 18,
                1, 9, 17, 51, 17, 18, 0, 16, 13]
    x_powers = [57, 56, 50, 49, 48, 43, 42, 41, 40, 36, 35, 34, 33, 32, 29, 28, 25, 24, 22, 21, 20, 18, 17, 15, 14, 13,
                12, 11, 10, 8, 7, 6, 5, 4, 3, 1]

    c = find_primitive_element(field)
    return VBF(field, lambda x: compute_polynomial(x, c, x_powers, c_powers, field), use_caching, apn=True, ab=False)


# def inverse(field):
#     assert field.n % 2 == 1
#     return VBF(field,
#                lambda x: 0 if x == 0 else field.Inverse(x),
#                use_caching=True, apn=True)


def run_test_for_all_apn_power_functions(n, to_run):
    """
    Runs a test on all applicable APN power functions.
    :param n: The dimension
    :param to_run: A function which takes arguments (function (p field), n)
    :return:
    """
    field = ffield.FField(n)

    # identity = VBF(field, lambda x: x)
    # print(f'-----Identity Function n={n}-----')
    # to_run(identity, n)
    gold_func = gold(field)
    print(f'-----Gold Function n={n} d={gold_func.get_exponent()}-----')
    to_run(gold_func, n)

    # gold_func_2 = gold(field, find_nontrivial_k=True)
    # if gold_func_2.get_exponent() != gold_func.get_exponent():
    #     print(f'-----Gold Function2 n={n} d={gold_func_2.get_exponent()}-----')
    #     to_run(gold_func_2, n)

    kasami_func = kasami(field, find_nontrivial_k=True)
    if n % 2 == 1 and not kasami_func.cyclomatic_equivalent(gold_func):
        print(f'-----Kasami Function n={n} d={kasami_func.get_exponent()}-----')
        to_run(kasami_func, n)  # apn for n >= 1. ab if odd

    if n % 2 == 1:
        welch_func = welch(field)
        print(f'-----Welch Function n={n} d={welch_func.get_exponent()}-----')
        to_run(welch_func, n)

        niho_func = niho(field)
        print(f'-----Niho Function n={n} d={niho_func.get_exponent()}-----')
        to_run(niho_func, n)

        inverse_func = inverse(field)
        print(f'-----Inverse Function n={n}------')
        to_run(inverse_func, n)

    if n % 5 == 0:
        dobbertin_func = dobbertin(field)
        print(f'-----Dobbertin Function n={n} d={dobbertin_func.get_exponent()}-----')
        to_run(dobbertin_func, n)

    quad_fcn1 = quadratic_CCZ_inquiv_to_power(field)
    print(f'-----Quadratic Function n={n} x^3 + a^(-1)tr_n(a^3 x^9)')
    to_run(quad_fcn1, n)

    if n % 3 == 0:
        quad_fcn2 = quadratic_CCZ_inquiv_to_power2(field)
        print(f'-----Quadratic Function n={n} x^3 + a^(-1) tr_n^3(a^3 x^9 + a^6x^(18))-----')
        to_run(quad_fcn2, n)

    if n == 6:
        dillion_perm = dillion_APN_permutation_dim6(field)
        print(f'-----Dillions APN Permutation n=6-----')
        to_run(dillion_perm, 6)


def exclude_dist_gap_test(F, n):
    graph = build_graph(F)
    dist = cap.exclude_dist(graph)
    min_k = min(dist)
    max_k = max(dist)
    print(graph)
    print(dist)
    print(f'min={min_k} \t max={max_k}')
    print(f'difference={max_k - min_k}')
    print(walsh_spectrum(F))


def get_local_dist(graph, x, dim):
    n = dim // 2
    counts = exclude_points_multiplicities(graph)
    local_dist = {}
    local_counts = {}
    for y in range(2 ** n):
        point = concatenate_binary_strings(x, y, n)
        if point in graph:
            continue
        local_counts[point] = counts[point]
    for v in local_counts.values():
        # For each point, get its exclude multiplicity, and add to exclude distribution
        local_dist[v] = local_dist.get(v, 0) + 1
    local_dist[0] = 2 ** n - sum(local_dist.values()) - 1  # -1 for the point in the graph
    return local_dist


def exclude_symmetric(F, n):
    if F.is_ab():
        return True, True
    graph = build_graph(F)
    print(graph)
    dim = 2 * n
    zero_local_dist = get_local_dist(graph, 0, dim)
    one_local_dist = get_local_dist(graph, 1, dim)
    # base values before looping
    exclude_sym_for_all = zero_local_dist == one_local_dist
    exclude_sym_for_nonzero = True
    for x in range(2, 2 ** n):
        local_dist = get_local_dist(graph, x, dim)
        if local_dist != one_local_dist:
            return False, False
        if local_dist != zero_local_dist:
            exclude_sym_for_all = False
    return exclude_sym_for_all, exclude_sym_for_nonzero


if __name__ == '__main__':
    field = ffield.FField(5)

    print(build_graph(dobbertin(field)))
    print(inverse(field).is_permutation())
    exit()
    gold = gold(field)
    print(gold.get_exponent())
    welch = welch(field)
    print(welch.get_exponent())
    print('cyclotomic equiv', gold.cyclomatic_equivalent(welch))
    exit()
    # print('Computing Walsh spectrum of Dobbertin n = 10')
    # arr = [16, 25, 27, 30, 29]
    arr_dobbertin = [72, 67, 77, 91, 84]
    goal_dobbertin = [97, 101, 112, 124, 127]
    arr = []
    goal = []
    # excludes of original (top left) (72, 67, 77, 91, 84)
    # 16->201 (b/c 16 ^ 17(cap pt) ^ 200(cappt) = 201)
    # excludes of new 218, 188, 175 goal
    print('Goal:')
    dim = 10
    for x in goal:
        print(x, int(binary_split(x, dim)[0], 2), int(binary_split(x, dim)[1], 2))
    print()
    field = ffield.FField(5)
    print(build_graph(dobbertin(field)))
    dobbertin_func = dobbertin(field)
    cap_point1, cap_point2 = 73, 119
    x, fx = binary_split(cap_point1, dim)
    x = int(x, 2)
    fx = int(fx, 2)
    y, fy = binary_split(cap_point2, dim)
    y = int(y, 2)
    fy = int(fy, 2)
    for ab in arr:
        a, b = binary_split(ab, dim)
        a = int(a, 2)  # assert a == x
        b = int(b, 2)

        c = y
        d = inverse_element(field, x ^ y)
        print(concatenate_binary_strings(c, d, dim // 2), c, d)
    exit()

    for n in range(5, 6, 1):
        print(f'------------------n={n}------------------')
        # func = quadratic_CCZ_inquiv_to_power(field)
        # graph = build_graph(func)
        test = lambda F, n: print(exclude_symmetric(F, n))
        run_test_for_all_apn_power_functions(n, test)
        continue
        exit()
        # print(f'd={func.get_exponent()}')
        # C1 = [x for x in graph if x < (2 ** (2 * n - 1))]
        # print(C1)
        C2 = [x for x in graph if x >= (2 ** (2 * n - 1))]
        print('C1 Maximal', cap.maximal(C1))
        print('C2 maximal in hyperplane', cap.exclude_dist(C2)[0] == (2 ** (2 * n - 1)))
