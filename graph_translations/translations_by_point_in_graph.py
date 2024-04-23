from vbf_functions.set_utils import *
from vbf_functions.apn_functions import *


def get_graph_translations_by_point_in_graph(F):
    # Returns the set of translations of the form (x, F(x)) + G_F
    graph = build_graph(F)
    print(graph)
    return [translate_set(graph, t) for t in graph]


def union_size(lists):
    result_set = set()
    for lst in lists:
        result_set.update(lst)
    return len(result_set)


def size_of_union_of_point_in_graph_translations(F, n):
    translations = get_graph_translations_by_point_in_graph(F)
    print(gamma_weight(F, n))
    print(union_size(translations))


if __name__ == '__main__':
    for n in range(1, 15, 1):
        test = lambda F, n: size_of_union_of_point_in_graph_translations(F, n)
        run_test_for_all_apn_power_functions(n, test)
