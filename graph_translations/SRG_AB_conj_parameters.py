from vbf_functions.set_utils import *
from vbf_functions.apn_functions import *


# Assuming KG(T_F) is an SRG (strongly regular graph) if F is AB, let's compute lambda and mu
def get_adjacent_and_nonadj_pairs(ab_func):
    graph = build_graph(ab_func)
    n = ab_func.field.n
    adjacent_pair = []
    non_adjacent_pair = []
    for ab in range(2 ** (2 * n)):
        for cd in range(2 ** (2 * n)):
            if ab == cd:
                continue
            translation_by_ab = translate_set(graph, ab)
            translation_by_cd = translate_set(graph, cd)
            if len(adjacent_pair) == 0 and are_disjoint(translation_by_ab, translation_by_cd):
                adjacent_pair.extend([translation_by_ab, translation_by_cd])
            elif len(non_adjacent_pair) == 0 and not are_disjoint(translation_by_ab, translation_by_cd):
                non_adjacent_pair.extend([translation_by_ab, translation_by_cd])

            if len(adjacent_pair) != 0 and len(non_adjacent_pair) != 0:
                return adjacent_pair, non_adjacent_pair


def get_lambda_mu_of_SRG(ab_func):
    n = ab_func.field.n
    graph = build_graph(ab_func)
    adjacent_pair, non_adjacent_pair = get_adjacent_and_nonadj_pairs(ab_func)

    adj_common_neighbors = 0
    nonadj_common_neighbors = 0
    for x in range(2 ** (2 * n)):
        translation_by_x = translate_set(graph, x)
        if are_disjoint(translation_by_x, adjacent_pair[0]) and are_disjoint(translation_by_x, adjacent_pair[1]):
            adj_common_neighbors += 1
        if (are_disjoint(translation_by_x, non_adjacent_pair[0])
                and are_disjoint(translation_by_x, non_adjacent_pair[1])):
            nonadj_common_neighbors += 1

    return adj_common_neighbors, nonadj_common_neighbors


if __name__ == '__main__':
    for n in range(3, 20, 2):
        field = ffield.FField(n)
        gold_func = gold(field)
        lambda_common, mu_common = get_lambda_mu_of_SRG(gold_func)
        print(lambda_common, mu_common)
