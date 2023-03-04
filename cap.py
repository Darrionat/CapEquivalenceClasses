from itertools import combinations
import cap_matrix as cmat
import numpy as np
import math
import linalg


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
    for comb in combinations(points, 3):
        exclude = 0
        for x in comb:
            exclude ^= x
        if exclude in points:
            return False
    return True


def calc_arank(points):
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
        # Convert to binary
        binary = "{0:b}".format(translate)
        # Add proper padding
        paddedBin = binary.rjust(dim, '0')
        # Converts into an array of char
        arr = [int(d) for d in str(paddedBin)]
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


def normalize_cap(cap):
    """
    Returns an affinely equivalent cap with the standard basis.
    :param cap: A cap.
    :return: A cap with basis points that are powers of 2.
    """
    M = find_cap_matrix(cap)
    return cmat.build_cap(M)


if __name__ == '__main__':
    dim10_5cover = [0, 33, 258, 483, 324, 997, 742, 135, 840, 809, 106, 203, 300, 973, 174, 655, 464, 593, 722, 403,
                    788, 533, 694,
                    887, 88, 921, 378, 635, 444, 253, 574, 959]
    # basis = find_ind_subset_with_arank(dim12_56cap, 13)
    print(normalize_cap(dim10_5cover))
