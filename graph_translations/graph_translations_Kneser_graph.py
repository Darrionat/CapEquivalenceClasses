from vbf_functions.set_utils import *
from vbf_functions.apn_functions import *


def get_all_graph_translations(F):
    n = F.field.n
    graph = build_graph(F)
    # return [tuple(translate_set(graph, t)) for t in range(0, 2 ** (2 * n))]
    return list(set([tuple(sorted(translate_set(graph, t))) for t in range(0, 2 ** (2 * n))]))


def get_diagonal_graph_translations(F):
    n = F.field.n
    graph = build_graph(F)
    return [tuple(translate_set(graph, concatenate_binary_strings(t, t, n)))
            for t in range(0, 2 ** n)]


def display_all_graph_translations_kneser_graph(F, n):
    all_translations = get_all_graph_translations(F)
    display_kneser_graph(all_translations)


def display_diagonal_graph_translations_kneser_graph(F, n):
    diagonal_translations = get_diagonal_graph_translations(F)
    display_kneser_graph(diagonal_translations)


def count_edges_between_cliques(F, n):
    n = F.field.n
    a1, a2 = 0, 1
    graph = build_graph(F)
    translations_a1_t = [tuple(translate_set(graph, concatenate_binary_strings(a1, t, n))) for t in range(2 ** n)]
    translations_a2_t = [tuple(translate_set(graph, concatenate_binary_strings(a2, t, n))) for t in range(2 ** n)]
    union_list = translations_a1_t + translations_a2_t
    display_kneser_graph(union_list)


if __name__ == '__main__':
    n = 1
    test = lambda F, n: display_all_graph_translations_kneser_graph(F, n)
    run_test_for_all_apn_power_functions(n, test)
    exit()
    # gold and gold2 don't have same chromatic # at n = 6
    diagonal = False
    print('Diagonals Only', diagonal)
    for n in range(5, 6, 2):
        # ab iff dist regular??
        # gold n = 2, d=3, not dist regular. but this is n = 2,
        #   so it's a bit low and could be a low-dim CE

        # this means ab does not ALWAYS imply dist reg
        # does dist reg imply ab?
        if diagonal:
            # test = lambda F, n: count_edges_between_cliques(F, n)
            test = lambda F, n: display_diagonal_graph_translations_kneser_graph(F, n)
        else:
            # test = lambda F, n: count_edges_between_cliques(F, n)
            test = lambda F, n: display_all_graph_translations_kneser_graph(F, n)
        run_test_for_all_apn_power_functions(n, test)
