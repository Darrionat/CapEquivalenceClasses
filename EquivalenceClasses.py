import collections
import os.path
import random
from itertools import combinations

import numpy as np


def data_exists(cap_size, arank):
    return os.path.exists(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True))


def load_data(cap_size, arank):
    return np.load(get_folder_path(cap_size) + os.sep + get_file_path(cap_size, arank, True), allow_pickle=True)


def save_data(cap_size, arank):
    if data_exists(cap_size, arank):
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
    to_return = []
    verified_cases = []
    # failed_cases = []
    # Build off of prior equiv classes
    for prev_M in get_equiv_classes(cap_size - 1, arank):
        # The length of affine combinations
        for aff_combo_len in range(5, arank + 1):
            # Skip even-length affine combinations
            if aff_combo_len % 2 == 0:
                continue
            failed = True

            # All the ways that an affine combination can be placed into the matrix
            combs = list(combinations(np.arange(arank), aff_combo_len))
            random.shuffle(combs)
            for comb in combs:
                arr = np.zeros(arank)
                for i in comb:
                    arr[i] = 1
                new_row = np.array(arr)
                # print('Row to Append', new_row)
                # print('PrevM', prev_M)
                M = np.vstack([prev_M, new_row])
                # print('NewM', M)
                # for failed_case in failed_cases:
                #     if collections.Counter(failed_case) == collections.Counter(case):
                #         # Although this case does fail, we do not want to add it to the list once again,
                #         # so set failed to false, avoid excess memory usage.
                #         # failed = False
                #         break
                # Check for duplicates before verifying
                # This is to avoid revalidating the same case multiple times
                if not verify_matrix(M):
                    continue
                failed = False
                dupe = False
                case = get_affine_case(M)
                for verified_case in verified_cases:
                    if affine_cases_equal(case, verified_case):
                        dupe = True
                        break
                if dupe:
                    # print('Duplicate')
                    break
                verified_cases.append(case)
                to_return.append(M)
                break

            if failed:
                # failed_cases.append(case)
                # todo can we break here? no further can be fit if this can't be fit, right?
                break
    if len(to_return) == 0:
        return None
    return to_return


# Returns the affine case of a given matrix
def get_affine_case(M):
    # for row in M:
    #     row_sums.append(np.sum(row))
    row_sums = np.sum(M, axis=1)
    col_sums = np.sum(M, axis=0)
    return row_sums, col_sums


# Checks to see if two affine cases are equal
def affine_cases_equal(case1, case2):
    return collections.Counter(case1[0]) == collections.Counter(case2[0]) and collections.Counter(
        case1[1]) == collections.Counter(case2[1])


def verify_matrix(M):
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
        for R in range(curr_min_arank, C + 1):
            if R >= arank_bound:
                break
            # R = min(R, 11)
            # classes = get_equiv_classes(C, R)
            # if classes is not None:
            # equiv_classes[C, R] = classes
            print('Working on', C, R)
            save_data(C, R)
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
    for cap_size in range(5, 42):
        print_cap_num_classes(cap_size)


# calculate_equiv_classes(100, 14)
# calculate_equiv_classes(1000)
#calculate_equiv_classes(100, 13)
print_all_cap_stats()