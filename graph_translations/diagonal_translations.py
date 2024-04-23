from vbf_functions.set_utils import *
from vbf_functions.apn_functions import *


def diagonal_translations(F, n):
    graph = build_graph(F)
    return [translate_set(graph, concatenate_binary_strings(t, t, n)) for t in range(0, 2 ** n)]


def size_of_diagonal_translation_union(F, n):
    diag_translations = diagonal_translations(F, n)
    print(len(union_of_arrays(diag_translations)))


if __name__ == '__main__':
    for n in range(1, 16):
        pass
        test = lambda F, n: size_of_diagonal_translation_union(F, n)
        run_test_for_all_apn_power_functions(n, test)
