import collections
import random
from itertools import combinations
from multiprocessing import Pool
import numpy as np
import data_handler
import cap_matrix as cmat
from multiprocessing import Lock


#
def gen_equiv_classes(cap_size, arank):
    """
    Computes and saves the affine equivalence classes of a given cap size and affine rank.
    :param cap_size: The cap size
    :param arank: Affine rank
    :return: Returns an array of 2D numpy arrays (matrices) which represent equivalence classes
    """
    if cap_size < 5 or arank < 5 or arank > cap_size:
        raise Exception('Cap Size or Affine Rank Invalid')
    if cap_size == arank:
        # Trivial Case
        return []
    # If the data already exists, there is no need to make it again
    if data_handler.data_exists(cap_size, arank):
        return data_handler.load_data(cap_size, arank)
    # If k -1 = r, then the equivalence class is easily determined
    if cap_size - 1 == arank:
        to_return = []
        # Only do odd lengths
        for m in range(5, arank + 1, 2):
            # Create array of m ones
            ones = np.ones(m, dtype=int)
            # Make the rest zeros
            zeros = np.zeros(arank - m, dtype=int)
            arr = np.concatenate((ones, zeros), axis=None)
            # Converts 1D array to 2D and appends
            B = np.reshape(arr, (-1, arank))
            to_return.append(B)
        return to_return
    # Since this case is nontrivial, we need to build it from the prior caps
    return build_equiv_class_from_prior(cap_size, arank)


def build_equiv_class_from_prior(cap_size, arank):
    """
    Computes the affine equivalence class based upon the prior cases
    :param cap_size: The cap size to build
    :param arank: Affine rank
    :return: Returns the affine equivalence classes of the given cap size and arank based
    upon the past results
    """
    if not data_handler.data_exists(cap_size - 1, arank):
        raise ValueError('Prior Data does not exist')
    prev_classes = data_handler.load_data(cap_size - 1, arank)

    prev_classes_and_equals = gen_equal_classes(prev_classes)

    matrices_to_process = []
    cases = []
    for matrix in prev_classes_and_equals:
        dupe = False
        case = cmat.get_row_col_sums(matrix)
        for added_case in cases:
            if row_col_sums_equal(case, added_case):
                dupe = True
                break
        if not dupe:
            matrices_to_process.append(matrix)
            cases.append(case)

    # for matrix in prev_classes:
    #     matrices_to_process.append(matrix)
    #     for equiv_matrix in find_equiv_matrices(matrix):
    #         matrices_to_process.append(equiv_matrix)

    arank_arr = [arank] * len(matrices_to_process)
    to_process = zip(matrices_to_process, arank_arr)

    with Pool() as p:
        results = p.starmap(build_matrix, to_process)
    to_return = list(filter(lambda item: item is not None, results))
    if len(to_return) == 0:
        return None

    return to_return


def build_matrix(prev_M, arank):
    # arank = len(prev_M[0])
    # The length of affine combinations
    for aff_combo_len in range(5, arank + 1):
        # Skip even-length affine combinations
        if aff_combo_len % 2 == 0:
            continue

        # All the ways that an affine combination can be placed into the matrix
        combs = list(combinations(np.arange(arank), aff_combo_len))
        random.shuffle(combs)
        for comb in combs:
            arr = np.zeros(arank, dtype=int)
            for i in comb:
                arr[i] = 1
            new_row = np.array(arr)
            M = np.vstack([prev_M, new_row])
            if cmat.is_cap_matrix(M):
                return M


def gen_equal_classes(equivalence_classes):
    """
    Finds all equivalence classes that are equivalent to any in the given list.
    :param equivalence_classes: A set of unique equivalence classes.
    :return: All equivalence classes in the original list and those that are equivalent to any that are given.
    """
    to_return = []
    for equiv_class in equivalence_classes:
        to_return.append(equiv_class)
        # Adds multiple equivalence classes to the list
        to_return.extend(find_equiv_matrices(equiv_class))
    # Remove all strongly equivalent cases
    purge_strong_duplicate_cases(to_return)
    return to_return


def find_equiv_matrices(M):
    """
    Finds equivalent representation matrices by doing a change of basis.
    Ignores strongly equivalent cases, or in other words, the cases that have the same row and column sums).
    :param M: The representation matrix
    :return: An array of matrices cases, NOT including the original
    """
    to_return = []
    strong_equiv_cases = [cmat.get_row_col_sums(M)]

    rows = len(M)
    arank = len(M[0])
    # For each point not in the basis
    for row in range(0, rows):
        # The basis point to switch
        for to_switch in range(0, arank):
            B = cmat.change_basis(M, row, to_switch)
            if not cmat.is_cap_matrix(B):
                continue
            case = cmat.get_row_col_sums(B)
            dupe = False
            for strong_equiv_case in strong_equiv_cases:
                if row_col_sums_equal(case, strong_equiv_case):
                    dupe = True
                    break
            if dupe:
                continue
            to_return.append(B)
            strong_equiv_cases.append(case)
    return to_return


def purge_strong_duplicate_cases(equiv_classes):
    """
    Removes any cases that are strongly equivalent and only keeps unique ones
    :param equiv_classes: A list of equivalence classes
    """
    cases = []
    for M in equiv_classes:
        case = cmat.get_row_col_sums(M)
        dupe = False
        for c in cases:
            if row_col_sums_equal(case, c):
                dupe = True
                break
        if dupe:
            continue
        cases.append(case)


# Checks to see if two affine cases are equal
def row_col_sums_equal(case1, case2):
    return collections.Counter(case1[0]) == collections.Counter(case2[0]) and collections.Counter(
        case1[1]) == collections.Counter(case2[1])


# Here we aren't actually seeing if the spans are equal.
def row_spans_equiv(span1, span2):
    span_1_sums = get_span_sums(span1)
    span_2_sums = get_span_sums(span2)
    return collections.Counter(span_1_sums) == collections.Counter(span_2_sums)


def get_span_sums(span):
    to_return = []
    for v in span:
        to_return.append(np.sum(v))
    return to_return


def run_sim(cap_size_bound, arank_bound=None):
    curr_min_arank = 5
    # If no upper bound on the affine rank is set, just make it one higher than cap bound
    if arank_bound is None:
        arank_bound = cap_size_bound + 1
    for C in range(5, cap_size_bound):
        # tasks = []
        for R in range(curr_min_arank, C + 1):
            if R >= arank_bound:
                break
            if data_handler.data_exists(C, R):
                continue
            print('Working on', (C, R))
            data = gen_equiv_classes(C, R)
            if data is not None:
                data_handler.save_data(C, R, data)
            else:
                print('Max Cap:', (C - 1, R))
        curr_min_arank = data_handler.get_min_arank(C)


def print_all_cap_stats():
    for cap_size in range(5, 60):
        data_handler.print_cap_num_classes(cap_size)


def build_cap(M):
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


if __name__ == '__main__':
    run_sim(25, 15)