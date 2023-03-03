from itertools import combinations
import numpy as np


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
        if np.array_equal(r1, r2):
            return False
        # Sum the two arrays over Z_2
        # If the sum of the elements in the array sum to 2,
        # then these two points sum to another two points, forming a quad
        if np.sum((r1 + r2) % 2) == 2:
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
