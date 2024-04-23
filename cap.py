from functools import reduce
from itertools import combinations

import cap_matrix
import cap_matrix as cmat
import numpy as np
import math

import decompose_cap_pts
import linalg
import random
from tait_won_sidon import build_tait_won_sidon


def required_dimension(x):
    """
    Required dimension for a point.
    :param x: A point.
    :return: The dimension required for x to exist.
    """
    return 1 if x == 0 else math.ceil(math.log2(x + 1))


def dimension(points):
    x = max(points)
    return required_dimension(x)


def is_cap(points):
    """
    Checks to see if any exclude points are contained in the set of points.
    :param points: The points to check
    :return: True/false if the points are a cap.
    """
    pairs = set()
    for comb in combinations(points, 2):
        sum_xor = comb[0] ^ comb[1]
        if sum_xor in pairs:
            return False
        pairs.add(sum_xor)
    return True


def is_k_cover(cap):
    # assert is_cap(cap)
    return len(exclude_dist(cap)) == 1


"""
Cache the binary string arrow 
"""
binStringCache = {}


def calc_arank(points):
    binStringCache = {}
    """
    Computes the affine rank of the given points.
    :param cap:  Some points.
    :return:  The affine rank of the given points.
    """
    if len(points) <= 5:
        return len(points)
    dim = dimension(points)
    M = []
    fixed_pt = -1
    for p in points:
        if fixed_pt == -1:
            fixed_pt = p
            continue
        translate = p ^ fixed_pt
        # todo there could be cacheing for this
        if translate in binStringCache:
            arr = binStringCache[translate]
        else:
            # Convert to binary
            binary = "{0:b}".format(translate)
            # Add proper padding
            paddedBin = binary.rjust(dim, '0')
            arr = [int(d) for d in str(paddedBin)]
            binStringCache[translate] = arr
        # Converts into an array of char
        M.append(arr)
    transpose = np.transpose(M)
    return linalg.rankOfMatrix(transpose, dim, len(M)) + 1


def find_ind_subset_with_arank(points, arank):
    """
    Tries to find a subset with the given arank.
    :param points:  The points
    :param arank:  The arank required for the subset.
    :return: A subset with the given arank or None.
    """
    set_rank = calc_arank(points)
    if arank > set_rank:
        raise ValueError('Cannot have rank higher than cap rank')
    if len(points) == set_rank:
        return points
    # We know that points has more points than the arank
    subset = points.copy()

    while len(subset) != calc_arank(subset):  # We probably don't need a while-loop, but for safety measures
        for p in subset:
            new_subset = subset.copy()
            new_subset.remove(p)
            if calc_arank(new_subset) >= arank:
                subset = new_subset
    return subset


def find_basis(points):
    """
    Finds a basis that spans the given points.
    :param points: The points to span.
    :return: A maximally independent set in the dimension that the points lie in.
    """
    return find_ind_subset_with_arank(points, calc_arank(points))


def find_cap_matrix(cap):
    """
    Finds a cap matrix of the given cap
    :param cap: The given cap
    :return:
    """
    if not is_cap(cap):
        raise ValueError('Given points are not a cap')
    cap_size = len(cap)
    arank = calc_arank(cap)
    if cap_size == arank:
        raise ValueError('No cap matrix. Affinely independent Cap')

    basis = find_basis(cap)  # Note that len(basis) is equal to arank

    dependents = []
    # Keys are the points that are spanned
    # Values are indices of basis points that spanned to the key
    span = {}
    lowest_sum_len = 5
    for p in cap:
        if p in basis:
            continue
        dependents.append(p)
        if p in span:
            continue
        # Do the odd sums
        for sum_len in range(lowest_sum_len, arank + 1, 2):
            for comb in combinations(np.arange(arank), sum_len):
                # indices of the basis elements
                indices = []
                sum = 0
                for i in comb:
                    indices.append(i)
                    sum ^= basis[i]
                # this condition isn't needed, but it'll give us the smallest sums for each in the end
                if sum not in span:
                    span[sum] = indices
                if sum == p:
                    break
            if p in span:
                break
            # At the end, update new lowest_sum length to prevent over calculation
            lowest_sum_len = sum_len
    # Build matrix
    M = []
    for p in dependents:
        row = np.zeros(arank, dtype=int)
        # Set 1 for each basis element
        row[span[p]] = 1
        M.append(row)
    return M


def change_basis(cap):
    M = find_cap_matrix(cap)
    arank = calc_arank(cap)
    subset_rank = -1
    new_basis = None
    # Randomly find a basis with the same arank in that dimension
    while subset_rank != arank:
        new_basis = random.sample(list(np.arange(2 ** dimension(cap))), arank)
        subset_rank = calc_arank(new_basis)
    # Build the new cap based on the old matrix
    to_return = []
    to_return.extend(new_basis)
    for row in M:
        sum = 0
        col = 0
        for b in row:
            if b == 1:
                sum ^= new_basis[col]
            col += 1
        to_return.append(sum)
    return to_return


def normalize_cap(cap):
    """
    Returns an affinely equivalent cap with the standard basis.
    :param cap: A cap.
    :return: A cap with basis points that are powers of 2.
    """
    M = find_cap_matrix(cap)
    return cmat.build_cap(M)


def exclude_points_multiplicities(cap):
    """
    Returns a dictionary where keys are the exclude points and the value is their exclude multiplicity.
    If a point has an exclude multiplicity of k, then we call it a k-point.
    Throws an exception if the given array of points is not a cap.
    :param cap: The cap
    :return: The exclude points and their multiplicities
    """
    excludes = {}
    for comb in combinations(cap, 3):
        sum_xor = reduce(lambda x, y: x ^ y, comb)
        excludes[sum_xor] = excludes.get(sum_xor, 0) + 1
    if set(cap) & set(excludes.keys()):
        raise Exception("Points given are not a cap")
    return excludes


def exclude_dist(cap):
    """
    Returns a dictionary where keys are the k-points that appear in a cap, and the values being their frequency.
    If there are no k-points of a cap, then the value k will not be a key of the returned dictionary.
    :param cap: The cap
    :return: The exclude distribution of the cap
    """
    counts = exclude_points_multiplicities(cap)
    dist = {}
    for v in counts.values():
        dist[v] = dist.get(v, 0) + 1
    n = dimension(cap)
    dist[0] = 2 ** n - (sum(dist.values())) - len(cap)
    return dist


def maximal(cap):
    """
    Here maximal is defined as having no zero-points.
    """
    return exclude_dist(cap)[0] == 0


def tait_won_case():
    for d in range(4, 64, 2):
        cap = build_tait_won_sidon(d)
        sum = 0
        for p in cap:
            sum ^= p
        print(sum)


def tait_won_change_basis(dim):
    cap = build_tait_won_sidon(dim)
    print(change_basis(cap))


def print_exclude_dist(cap):
    print('Affine Rank:', calc_arank(cap))
    print('Cap:', cap)
    print('Size:', len(cap))
    dist = exclude_dist(cap)
    for k in dist:
        print('\t' + str(k) + '\t' + str(dist[k]))


def print_matrix(M):
    for i in M:
        for j in i:
            print(j, end="\t")
        print()


# Sorts the columns and rows into descending order w.r.t. row/column sums
def sort_matrix_rows_cols(M):
    row_sums, col_sums = cap_matrix.get_row_col_sums(M)
    # Sort the columns based on the non-zero counts in descending order
    # Create a list of column indices sorted by non-zero counts in descending order
    sorted_column_indices = sorted(range(len(col_sums)), key=lambda x: col_sums[x],
                                   reverse=True)

    # Create a sorted matrix based on the sorted column indices
    col_sorted_matrix = [[M[row][col] for col in sorted_column_indices] for row in range(len(M))]

    # do the same for rows
    sorted_row_indices = sorted(range(len(row_sums)), key=lambda x: row_sums[x], reverse=True)

    # Create a sorted matrix based on the sorted row indices
    return [col_sorted_matrix[row_idx] for row_idx in sorted_row_indices]


def complete_caps_primeKpoint_matrices():
    # dim2_1point = [0, 1, 2] too small for matrix
    # dim3_1point = [0, 1, 4, 2] too small for matrix
    dim4_2point = [0, 1, 4, 2, 8, 15]
    dim5_2point = [0, 1, 4, 2, 8, 15, 16]
    dim6_3point = [0, 1, 4, 2, 8, 15, 16, 32, 54]
    dim7_3point = [0, 1, 4, 2, 8, 15, 16, 64, 32, 85, 54, 109]
    dim8_5point = [0, 1, 4, 2, 8, 15, 16, 64, 32, 128, 165, 85, 54, 201, 250]
    dim9_7point = [0, 1, 2, 4, 8, 16, 32, 63, 64, 89, 94, 128, 173, 207, 256, 269, 316, 327, 423, 442, 457]
    dim10_11point = [0, 1, 2, 4, 8, 16, 32, 64, 128, 166, 248, 256, 308, 367, 369, 482, 507, 512, 540, 619, 630, 707,
                     753, 823, 841, 846, 868, 923, 933, 938, 982, 984, 1021]

    complete_caps_primeKpoint = [dim4_2point, dim5_2point, dim6_3point, dim7_3point, dim8_5point, dim9_7point,
                                 dim10_11point]
    for cap in complete_caps_primeKpoint:
        normal_cap = normalize_cap(cap)
        print(f'dim={dimension(cap)}\ncap={cap}')
        matrix = find_cap_matrix(cap)
        sorted_matrix = sort_matrix_rows_cols(matrix)
        print_matrix(sorted_matrix)
        print(f'newcap={cmat.build_cap(sorted_matrix)}')
        print()


def binary_split(n, k):
    # Convert n to a binary string of length k
    binary_str = format(n, f'0{k}b')

    # Calculate the midpoint index for splitting
    midpoint = k // 2

    # Split the binary string into two parts
    first_half = binary_str[:midpoint]
    second_half = binary_str[midpoint:]

    return first_half, second_half

#
# if __name__ == '__main__':
#     dim4_2point = [0, 1, 4, 2, 8, 15]
#     dim5_2point = [0, 1, 4, 2, 8, 15, 16]
#     dim6_3point = [0, 1, 4, 2, 8, 15, 16, 32, 54]
#     dim7_3point = [0, 1, 4, 2, 8, 15, 16, 64, 32, 85, 54, 109]
#     dim8_5point = [0, 1, 4, 2, 8, 15, 16, 64, 32, 128, 165, 85, 54, 201, 250]
#     dim9_7point = [0, 1, 2, 4, 8, 16, 32, 63, 64, 89, 94, 128, 173, 207, 256, 269, 316, 327, 423, 442, 457]
#     dim10_11point = [0, 1, 2, 4, 8, 16, 32, 64, 128, 166, 248, 256, 308, 367, 369, 482, 507, 512, 540, 619, 630, 707,
#                      753, 823, 841, 846, 868, 923, 933, 938, 982, 984, 1021]
#
#     # complete_caps_primeKpoint = [dim4_2point, dim5_2point, dim6_3point, dim7_3point, dim8_5point, dim9_7point,
#     #                              dim10_11point]
#
#     normal_cap = normalize_cap(dim8_5point)
#     dim = dimension(normal_cap)
#     print(normal_cap)
#     for point in normal_cap:
#         bin_split = binary_split(point, dim)
#         print(f'{bin_split[0]}')
#
#     # for d in range(4, 64, 2):
#     #     print('Dimension:', d)
#     #     cap = build_tait_won_sidon(d)
#     #     print('Cap:', cap)
#     #     print('Size:', len(cap))
#     #     dist = exclude_dist(cap)
#     #     for k in dist:
#     #         print('\t' + str(k) + '\t' + str(dist[k]))
