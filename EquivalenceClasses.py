import collections
import os.path
import random
from itertools import combinations
from multiprocessing import Pool
import numpy as np
import time


def data_exists(cap_size, arank):
    return os.path.exists(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True))


def load_data(cap_size, arank):
    return np.load(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True), allow_pickle=True)


def save_data(cap_size, arank):
    print('Working on', cap_size, arank)
    # Data already exists or this is a max cap
    if data_exists(cap_size, arank) or data_exists(cap_size, arank + 1):
        return
    data = get_equiv_classes(cap_size, arank)
    if data is None:
        return
    folder = get_folder_path(cap_size)
    try:
        os.mkdir(folder)
    except OSError:
        pass
    np.save(folder + os.sep + get_file_path(cap_size, arank), data)


def get_file_path(cap_size, arank, add_file_ext=False):
    name = str(cap_size) + '_' + str(arank) + '_classes'
    return name + '.npy' if add_file_ext else name


def get_folder_path(cap_size):
    return str(cap_size) + '_caps'


# Returns an array of 2D numpy arrays (matrices) which represent equivalence classes
def get_equiv_classes(cap_size, arank):
    # print('Working on', cap_size, arank)
    # if (cap_size, arank) in equiv_classes:
    #     return equiv_classes[cap_size, arank]
    if cap_size < 5 or arank < 5 or arank > cap_size:
        raise Exception('Cap Size or Affine Rank Invalid')
    if cap_size == arank:
        return []
    if cap_size - 1 == arank:
        to_return = []
        for m in range(5, arank + 1):
            # Skip even-length affine combinations
            if m % 2 == 0:
                continue
            ones = np.ones(m)
            zeros = np.zeros(arank - m)
            arr = np.concatenate((ones, zeros), axis=None)
            # reshapes the matrix into 2D
            B = np.reshape(arr, (-1, arank))
            # print(B)
            # M = np.matrix(arr)
            to_return.append(B)
        return to_return
    if data_exists(cap_size, arank):
        return load_data(cap_size, arank)
    return build_equiv_class_from_prior(cap_size, arank)


def build_equiv_class_from_prior(cap_size, arank):
    # Save both the row/col sums and the more complicated verified cases
    # row_col_sums_verified_cases = []
    # row_span_verified_cases = []
    # failed_cases = []
    # Build off of prior equiv classes

    prev_classes = get_equiv_classes(cap_size - 1, arank)

    start = time.time()

    with Pool() as p:
        prev_classes_and_equiv = np.array(p.map(find_equiv_matrices, prev_classes))

    matrices_to_process = []
    cases = []
    for c in prev_classes_and_equiv:
        for matrix in c:
            dupe = False
            case = get_row_col_sums(matrix)
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

    end = time.time()
    init_queue_time = end - start

    arank_arr = [arank] * len(matrices_to_process)
    to_process = zip(matrices_to_process, arank_arr)

    start = time.time()
    with Pool() as p:
        results = p.starmap(build_matrix, to_process)
    to_return = list(filter(lambda item: item is not None, results))
    if len(to_return) == 0:
        return None

    end = time.time()
    process_time = end - start
    print('init_time=', init_queue_time, 'process_time=', process_time, 'n=', len(matrices_to_process))
    return to_return
    #
    # for prev_M in get_equiv_classes(cap_size - 1, arank):


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
            arr = np.zeros(arank)
            for i in comb:
                arr[i] = 1
            new_row = np.array(arr)
            M = np.vstack([prev_M, new_row])
            if verify_matrix(M):
                return M


def find_equiv_matrices(M):
    """
    Finds equivalent representation matrices by doing a change of basis.
    Ignores strongly equivalent cases, or in other words, the cases that have the same row and column sums).
    :param M: The representation matrix
    :return: An array of matrices cases, including the original
    """
    to_return = [M]
    strong_equiv_cases = [get_row_col_sums(M)]

    rows = len(M)
    arank = len(M[0])
    # For each point not in the basis
    for row in range(0, rows):
        # The basis point to switch
        for to_switch in range(0, arank):
            B = change_basis(M, row, to_switch)
            if not verify_matrix(B):
                continue
            case = get_row_col_sums(B)
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


# Checks to see if row/col sums are equal first
def get_row_col_sums(M):
    row_sums = np.sum(M, axis=1)
    col_sums = np.sum(M, axis=0)
    return row_sums, col_sums


# Checks to see if two affine cases are equal
def row_col_sums_equal(case1, case2):
    return collections.Counter(case1[0]) == collections.Counter(case2[0]) and collections.Counter(
        case1[1]) == collections.Counter(case2[1])


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


def verify_matrix(M):
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


# Gets the lowest possible affine rank for a given cap size
def get_min_arank(cap_size):
    for arank in range(5, cap_size + 1):
        if data_exists(cap_size, arank):
            return arank


# cap_size_bound = 34
# max_R = 13;
# Object to store all equivalence classes in
# equiv_classes = {}


def calculate_equiv_classes(cap_size_bound, arank_bound=None):
    curr_min_arank = 5
    # If no upper bound on the affine rank is set, just make it one higher than cap bound
    if arank_bound is None:
        arank_bound = cap_size_bound + 1
    for C in range(5, cap_size_bound):
        # tasks = []
        for R in range(curr_min_arank, C + 1):
            if R >= arank_bound:
                break
            # tasks.append((C, R))
            # R = min(R, 11)
            # classes = get_equiv_classes(C, R)
            # if classes is not None:
            # equiv_classes[C, R] = classes
            save_data(C, R)
        # save_data(C, R)
        # print(tasks)
        # with Pool() as p:
        #     p.starmap(save_data, tasks)
        curr_min_arank = get_min_arank(C)
        # Progress Updates
        # cap_rank_stats = []
        # for R in range(curr_min_arank, C + 1):
        #     if R >= arank_bound:
        #         break
        #     # if (C, R) not in equiv_classes:
        #     #     continue
        #     # caseAmt = len(equiv_classes[(C, R)]) if R != C else 1
        #     cap_rank_stats.append((R, caseAmt))
        # # print('Size=', C, 'Stats=', cap_rank_stats)


def get_equiv_class_count(cap_size, arank):
    if not data_exists(cap_size, arank):
        return -1
    data = get_equiv_classes(cap_size, arank)
    return len(data) if cap_size != arank else 1


def print_cap_num_classes(cap_size):
    arr = []
    minrank = get_min_arank(cap_size)
    if minrank is None:
        minrank = 5
    for arank in range(minrank, cap_size + 1):
        count = get_equiv_class_count(cap_size, arank)
        if count != -1:
            arr.append(count)
    print(str(cap_size) + '-Cap Equiv Class Count', arr)


def print_all_cap_stats():
    for cap_size in range(5, 60):
        print_cap_num_classes(cap_size)


# calculate_equiv_classes(100, 14)
# calculate_equiv_classes(1000)
# print_all_cap_stats()


# This works, as it should
# M = [[1, 1, 1, 1, 1, 1, 1, 0, 0],
#      [0, 0, 1, 1, 1, 1, 1, 1, 1],
#      [1, 0, 1, 1, 0, 0, 0, 1, 1]]
# B = [[1, 1, 1, 1, 1, 1, 1, 0, 0],
#      [1, 1, 1, 0, 0, 0, 0, 1, 1],
#      [0, 1, 1, 0, 1, 1, 1, 1, 1]]
# span = (get_row_span(M))
# span_2 = get_row_span(B)
# print(span)
# print(row_spans_equiv(span, span_2))

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


# print_all_cap_stats()

# # Change of basis test
# M = [np.array([1, 1, 1, 1, 1, 1, 1, 0, 0]),
#      np.array([0, 0, 1, 1, 1, 1, 1, 1, 1]),
#      np.array([1, 0, 1, 1, 0, 0, 0, 1, 1])]
# # print(change_basis(M, 0, 2))
# # print(M)
# equiv_matrices = find_equiv_matrices(M)
# print('change of basis:', equiv_matrices)
# print(len(equiv_matrices))
# for equiv_matrix in equiv_matrices:
#     print(get_row_col_sums(equiv_matrix))
# print(find_equiv_matrices(M))


if __name__ == '__main__':
    # I saw a 52 in dim 12, could not find 53
    # saw 68 in dim 13
    # saw 88 in dim 14, found an 89
    # print(len(get_equiv_classes(32, 12)))
    # rows = 5
    # for row_sample_size in range(rows, 0, -1):
    #     for comb in combinations(range(rows), row_sample_size):
    #         print(comb)
    #
    # for M in get_equiv_classes(14, 9):
    #     print(M)
    #     print(build_cap(M))

    calculate_equiv_classes(26, 14)  # recommended test

