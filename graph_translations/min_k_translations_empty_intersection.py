from pyfinite import ffield

from vbf_functions.crooked_functions import gold
from vbf_functions.vbfs import build_graph
from vbf_functions.set_utils import *
from itertools import combinations
from decompose_cap_pts import concatenate_binary_strings


def find_minimal_k_empty_translation_intersection(F, field):
    """
    Finds the minimal k such that the intersection of any k translations of the graph of F must be empty.
    """
    n = field.n
    graph = build_graph(F, n)  # G_F

    ordered_pairs = [(a, b)  # set of all (a,b) in F_2^{2n}
                     for a in range(0, 2 ** n)
                     for b in range(0, 2 ** n)]

    for k in range(2, 2 ** (2 * n)):
        print(f'k={k}')
        non_empty_intersection_found = False
        # set of size k of ordered pairs (a,b) which will be translating G_F
        for translator_comb in combinations(ordered_pairs, k):
            translations = []  # all the translated graphs that we will be sampling
            for translator in translator_comb:
                # translator = (a,b)
                t = concatenate_binary_strings(translator[0], translator[1], n)
                translated_graph = translate_set(graph, t)
                translations.append(translated_graph)

            if share_common_element(translations):
                non_empty_intersection_found = True
                break
        if non_empty_intersection_found:
            continue
        return k
    raise Exception("Something went wrong. Contact developer")


if __name__ == '__main__':
    for n in range(2, 10):
        print(f'n={n}')
        field = ffield.FField(n)
        # F = lambda x: gold(x, field)
        F = lambda x: x
        print('min k=', find_minimal_k_empty_translation_intersection(F, field))
