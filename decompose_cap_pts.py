import cap
from cap import *
from pyfinite import ffield


#
# def build_pts_4(dim, f, point_structure):
#     """
#         Builds a set of points in F_{2^n} with the structure (x,y,z,w) with respect to the additive isomorphism between
#         F_{2^n} and F_{2^{n/4}} *  ... * F_{2^{n/4}}.
#         :param dim: The dimension.
#         :param fx: A function to apply to each point in F_{2^{n/4}}.
#         :param point_structure: The way to make the points. Defines the form of (x,y,z,w).
#         :return:
#         """
#     assert dim % 4 == 0
#     half_dim = int(dim / 2)
#     to_return = []
#     for p in range(int(2 ** (dim / 4))):
#         point_tuple = point_structure(p, f)
#         stitch1 = concatenate_binary_strings(point_tuple[0], point_tuple[1], dim)
#         stitch2 = concatenate_binary_strings(point_tuple[2], point_tuple[3], dim)
#         to_return.append(concatenate_binary_strings(stitch1, stitch2, dim))
#     return to_return


def concatenate_binary_strings(left, right, n):
    """
    Stitches the two binary strings of the given integers together to create a new integer.
    Given two integers p1 and p2, we return the point (p1, p2).
    :param left: p1
    :param right: p2
    :param n: The dimension of the field which both p1 and p2 lie in.
    :return: The newly constructed point which lies in dimension 2n.
    """
    return int(f"{left:0{n}b}{right:0{n}b}", 2)


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
