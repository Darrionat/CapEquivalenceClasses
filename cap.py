from itertools import combinations
import cap_matrix as cmat
import numpy as np
import math
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
        pair_sum = 0
        for x in comb:
            pair_sum ^= x
        if pair_sum in pairs:
            return False
        pairs.add(pair_sum)
    return True


def is_k_cover(cap):
    assert is_cap(cap)
    return len(exclude_dist(cap)) == 1


"""
Cache the binary string arrow 
"""
binStringCache = {}


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


def excludes_count(cap):
    excludes = {}
    for comb in combinations(cap, 3):
        sum = 0
        for p in comb:
            sum ^= p
        if sum not in excludes:
            excludes[sum] = 1
        else:
            excludes[sum] += 1
    return excludes


def exclude_dist(cap):
    counts = excludes_count(cap)
    dist = {}
    for key in counts:
        v = counts[key]
        if v not in dist:
            dist[v] = 1
        else:
            dist[v] += 1
    return dist


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


if __name__ == '__main__':
    for d in range(4, 64, 2):
        print('Dimension:', d)
        cap = build_tait_won_sidon(d)
        print('Cap:', cap)
        print('Size:', len(cap))
        dist = exclude_dist(cap)
        for k in dist:
            print('\t' + str(k) + '\t' + str(dist[k]))
