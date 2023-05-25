import cap
from cap import *
from pyfinite import ffield


def build_points(dim, f):
    """
    Builds a set of points in F_{2^n} with the structure (x, f(x)) with respect to the additive isomorphism between
    F_{2^n} and F_{2^{n/2}} * F_{2^{n/2}}.
    :param dim: The dimension.
    :param fx: A function to apply to each point in F_{2^{n/2}}.
    :return:
    """
    assert dim % 2 == 0
    to_return = []
    for p in range(int(2 ** (dim / 2))):
        to_return.append(stitch_pts(p, f(p), dim))
    return to_return


def build_pts_4(dim, f, point_structure):
    """
        Builds a set of points in F_{2^n} with the structure (x,y,z,w) with respect to the additive isomorphism between
        F_{2^n} and F_{2^{n/4}} *  ... * F_{2^{n/4}}.
        :param dim: The dimension.
        :param fx: A function to apply to each point in F_{2^{n/4}}.
        :param point_structure: The way to make the points. Defines the form of (x,y,z,w).
        :return:
        """
    assert dim % 4 == 0
    half_dim = int(dim / 2)
    to_return = []
    for p in range(int(2 ** (dim / 4))):
        point_tuple = point_structure(p, f)
        stitch1 = stitch_pts(point_tuple[0], point_tuple[1], half_dim)
        stitch2 = stitch_pts(point_tuple[2], point_tuple[3], half_dim)
        to_return.append(stitch_pts(stitch1, stitch2, dim))
    return to_return


def stitch_pts(left, right, dim):
    """
    Stitches the two binary strings of the given points together.
    Given two point p1 and p2, we return the point (p1, p2).
    :param left: p1
    :param right: p2
    :param dim: The dimension of the point to return.
    :return:
    """
    assert dim % 2 == 0
    half_dim = int(dim / 2)
    # Left
    bin_left = "{0:b}".format(left)
    bin_right = "{0:b}".format(right)
    padded_left = bin_left.rjust(half_dim, '0')
    padded_right = bin_right.rjust(half_dim, '0')
    left_bin_str = padded_left[0:half_dim]
    right_bin_str = padded_right[0:half_dim]
    # Right
    return int(left_bin_str + right_bin_str, 2)


def field_exp(x, exp, F):
    # 'Fast' exponentiation (Wikipedia)
    # https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    n = exp
    if n == 0:
        return 1
    a = x
    y = 1
    while n > 1:
        if n % 2 == 0:
            a = F.Multiply(a, a)
            n = n / 2
        else:
            y = F.Multiply(a, y)
            a = F.Multiply(a, a)
            n = (n - 1) / 2
    return F.Multiply(a, y)
    # Old, slow and naive algorithm
    # product = x
    # for i in range(exp - 1):
    #     # print(x, exp, product)
    #     product = F.Multiply(x, product)
    # return product


def print_matrix(M):
    for i in M:
        for j in i:
            print(j, end="\t")
        print()


def pow_funcs_sum_to_zero():
    """
    Print what power functions sum to zero.
    """
    to_return = []
    for dim in range(6, 27, 2):
        print('Dim', dim)
        F = ffield.FField(int(dim / 2))

        exp_arr = []
        for exp in range(20):
            sum = 0
            for p in range(int(2 ** int(dim / 2))):
                sum ^= field_exp(p, exp, F)
            exp_arr.append(sum == 0)
        to_return.append(exp_arr)
    print_matrix(to_return)


def inverse(p):
    if p != 0:
        return F.Inverse(p)
    return 0


def gold(p, F, k=1, dim=-1, find_nontrivial_k=False):
    assert math.gcd(dim, k) == 1
    if find_nontrivial_k:
        for l in range(2, dim // 2 + 1):
            if math.gcd(dim, l) == 1:
                k = l
                break
    # print(k)
    return field_exp(p, int(2 ** k) + 1, F)


def kasami(p, F, k=1, dim=-1, find_nontrivial_k=False):
    assert math.gcd(dim, k) == 1
    if find_nontrivial_k:
        for l in range(2, dim + 1):
            if math.gcd(dim, l) == 1:
                k = l
    pow = 2 ** (2 * k) + (-2) ** k + 1
    return field_exp(p, pow, F)


def dobbertin(p, dim, F):
    assert dim % 5 == 0
    t = dim / 5
    pow = int(2 ** (4 * t) + 2 ** (3 * t) + 2 ** (2 * t) + 2 ** t - 1)
    return field_exp(p, pow, F)


def inverse(p, dim, F):
    assert dim % 2 == 1
    t = (dim - 1) / 2
    pow = int(2 ** (2 * t) - 1)
    return field_exp(p, pow, F)


def surjective_function(f, field_dim, field):
    all_points = list(range(2 ** field_dim))
    for p in range(2 ** field_dim):
        if f(p) in all_points:
            all_points.remove(f(p))
    return len(all_points) == 0


if __name__ == '__main__':
    # pow = 3
    dim = 10
    F = ffield.FField(int(dim / 2))
    f = lambda p: kasami(p, F, dim=dim, find_nontrivial_k=True)
    # f = lambda p: kasami(p, F, dim=int(dim / 2), findNonTrivialk=True)
    # f = lambda p: dobbertin(p, int(dim / 2), F)
    # for dim in range(6, 25, 2):
    #     F = ffield.FField(int(dim / 2))
    #     f = lambda p: gold(p, F, dim=int(dim / 2), find_nontrivial_k=True)
    #     pts = build_points(dim, f)
    pts = build_points(dim, f)
    if is_cap(pts):
        print('dim', dim, 'pow', 'nontrivial', 'cap:', pts)
        print(cap.exclude_dist(pts))
        # if is_k_cover(pts):
        #     print('Is a k-cover')
        # else:
        #     print('Not k-cover')
    else:
        print(pts)

# func_matrix = []
# for pow in range(1, 33):
#     print('Doing powers of', pow)
#     dims = []
#     for dim in range(4, 27, 2):
#         F = ffield.FField(int(dim / 2))
#         f = lambda p: field_exp(p, pow, F)
#         pts = build_points(dim, f)
#         # the is_cap method is what takes the longest since it's of order n choose 2
#         if is_cap(pts):
#             dims.append(dim)
#             # print('dim', dim, 'pow', pow, 'cap:', pts)
#     func_matrix.append(dims)
# print_matrix(func_matrix)
