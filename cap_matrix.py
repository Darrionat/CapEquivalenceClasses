from itertools import combinations
import numpy as np
import collections


# Todo: Row span could be a way of determining equivalence
def get_row_span(M):
    rows = len(M)
    arank = len(M[0])
    # We don't need to include the zero vector as that is trivial
    span = []
    for k in range(1, rows + 1):  # Choose from 1 to rows (inclusive)
        k_combs = combinations(np.arange(rows), k)
        for row_comb in k_combs:
            row_sum = np.zeros(arank)
            for row_index in row_comb:
                row_sum += M[row_index]
            row_sum %= 2
            span.append(row_sum)
    return span


# Checks to see if two affine cases are equal
def row_col_sums_equal(case1, case2):
    return collections.Counter(case1[0]) == collections.Counter(case2[0]) and collections.Counter(
        case1[1]) == collections.Counter(case2[1])


def equiv_cap_matrices(A, B):
    span1 = get_row_span(A)
    span2 = get_row_span(B)
    case1 = get_row_col_sums(span1)
    case2 = get_row_col_sums(span2)
    return row_col_sums_equal(case1, case2)


def get_row_col_sums(M):
    """
    Compute the sums of the rows and columns of the matrix
    :param M: A cap matrix
    :return: A tuple of arrays that represent the row and column sums
    """
    row_sums = np.sum(M, axis=1)
    col_sums = np.sum(M, axis=0)
    return row_sums, col_sums


def is_cap_matrix(M):
    for row_sum in get_row_col_sums(M)[0]:
        if row_sum % 2 == 0:
            return False
    row_amt = len(M)
    # Get all possible combinations of two integers between [0,rowAmt)
    # np.arange(row_amt) == [0, ..., row_amt -1]
    two_combs = combinations(np.arange(row_amt), 2)
    for comb in two_combs:
        # The two rows to compare
        r1, r2 = M[comb[0]], M[comb[1]]
        sum = np.sum((r1 + r2) % 2)
        # If sum == 0, then rows are equal
        # If the sum of the elements in the array sum to 2,
        # then these two points sum to another two points, forming a quad
        if sum == 0 or sum == 2:
            return False

    three_combs = combinations(np.arange(row_amt), 3)
    for comb in three_combs:
        # The three rows to compare
        r1, r2, r3 = M[comb[0]], M[comb[1]], M[comb[2]]
        # Sum the two arrays over Z_2
        # If the sum of the elements in the array sum to 1,
        # then these three points sum to another point, forming a quad
        if np.sum((r1 + r2 + r3) % 2) == 1:
            return False
    four_combs = combinations(np.arange(row_amt), 4)
    for comb in four_combs:
        r1, r2, r3, r4 = M[comb[0]], M[comb[1]], M[comb[2]], M[comb[3]]
        # Return false if the sum of r1 through r4 is the zero vector
        if not np.any((r1 + r2 + r3 + r4) % 2):
            return False
    # All tests have been passed, return true
    return True


def change_basis(M, row, to_switch):
    """
    Performs a basis change on a representation matrix
    :param A: The representation matrix
    :param row: The row (representing a non-basis point) to operate on
    :param to_switch: The basis point to switch
    :return: A new representation matrix that went through a basis change
    """
    to_add = np.array(M[row])
    to_add[to_switch] = 0
    to_return = []
    for i in range(0, len(M)):
        if i == row or M[i][to_switch] == 0:
            to_return.append(M[i])
            continue
        to_return.append(np.mod(np.add(M[i], to_add), 2))
    return to_return


def build_cap(M):
    """
    Returns a list containing cap points that can be added to the cap finder
    :param M: The cap matrix
    :return:  A cap with the given cap matrix
    """
    r = len(M)
    k = r + len(M[0])  # r + k-r = k
    cap = [0]
    # Init the basis
    for i in range(1, k - r):
        cap.append(pow(2, i - 1))
    for row in M:
        pt = 0
        for i in range(0, len(row)):
            if row[i] == 1:
                pt ^= int(pow(2, i - 1))
        cap.append(pt)
    return cap
