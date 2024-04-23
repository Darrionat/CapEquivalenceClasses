import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

import numpy as np
import requests


def translate_set(to_translate, t):
    """
    Given a set of points, XOR t onto each point
    :param to_translate: The set of points to translate
    :param t: The point to translate all elements in the set by
    :return: Returns a translation of the original set, i.e. t + set.
    """
    return [t ^ x for x in to_translate]


def union_of_arrays(arrays):
    result = set()
    for array in arrays:
        result.update(array)
    return result


def are_disjoint(list1, list2):
    return len(set(list1) & set(list2)) == 0


def kneser_graph(sets):
    # TODO this could be sped up by using the gamma function quick access matrix
    G = nx.Graph()
    # Add nodes to the graph
    G.add_nodes_from(sets)

    # Add edges to the graph for disjoint k-subsets
    for i, subset1 in enumerate(sets):
        for subset2 in sets[i + 1:]:
            # if subset1 != subset2:
            if not any(item in subset2 for item in subset1):
                G.add_edge(subset1, subset2)
    return G


from networkx.algorithms.distance_regular import intersection_array


def save_matrix_to_file(matrix, filename):
    with open(filename, "w") as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")


def display_kneser_graph(sets):
    G = kneser_graph(sets)
    print('Graph loaded')

    # adj_matrix = kneser_graph_adjacency_matrix(sets)
    #
    # # save_matrix_to_file(adj_matrix, "adjacency_matrix.txt")
    # # print('Saved adj matrix to file')
    #
    # matrix = []
    # for row in adj_matrix:
    #     matrix.append(row)
    #
    # binary_matrix = np.array(matrix)
    # # # Display the binary matrix as a black and white image
    # plt.imsave('gold_4_binary_image.png', binary_matrix, cmap='gray')
    #
    # fig, ax = plt.subplots(figsize=(20, 20))  # Adjust the values according to your desired size
    # plt.set_cmap('gray')  # Set the colormap
    # ax.imshow(binary_matrix, cmap='gray')
    # plt.savefig('binary_image.png')
    # plt.show()
    # G = nx.complement(G)
    # print('is-k-reg', next(iter(G.degree()))[1])
    # adj_matrix = nx.adjacency_matrix(G).todense()
    # eigenvalues = np.linalg.eigvals(adj_matrix)
    # decimals = 6  # You can adjust this as needed
    # rounded_eigenvalues = np.around(eigenvalues, decimals=decimals)
    # print(set(rounded_eigenvalues))

    """
    Temporary
    """
    # print('chromatic #', chromatic_number(G))

    # print('size of largest clique', len(list(nx.find_cliques(G))[0]))
    # print('num maximal cliques', len(list(nx.find_cliques(G))))
    # Iterate through nodes and their degrees

    # max_degree = 0
    # degrees = set()
    # for node, degree in G.degree():
    #     degrees.add(degree)
    #     # if degree > max_degree:
    #     #     max_degree = degree
    #
    # # Print the largest degree
    # print("Degrees:", degrees)
    # print("Largest Degree:", max(degrees))

    # Visualize the graph
    # pos = nx.spring_layout(G, seed=42)
    # nx.draw(G, pos, with_labels=True, node_size=500, font_size=10, font_color='black', font_weight='bold')
    # plt.title(f'Kneser Graph K({n},{k})')
    # print('DistReg', nx.is_distance_regular(G))
    # print('StrongReg', nx.is_strongly_regular(G))
    # print('numTriangles', sum(nx.triangles(G).values()) / 3)
    # print('edges', G.number_of_edges())
    # print('regular?', nx.is_regular(G))
    # if nx.is_connected(G):
    #     print('diam', nx.diameter(G))
    # print('If SRG', get_SRG_lambda_mu_value(G))
    print(get_graph6_string(G))
    # print('#connected compoennets', nx.number_connected_components(G))
    #
    # print('NumNodes', G.number_of_nodes())
    # pos = nx.spring_layout(G)
    # coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    # node_colors = [coloring[node] for node in G.nodes()]
    # nx.draw(G, pos, node_color=node_colors, with_labels=False, node_size=500, cmap=plt.get_cmap("viridis"))
    # plt.show()


def get_SRG_lambda_mu_value(G):
    """
    Finds the lambda and mu values for a strongly regular graph.
    :param G:  A strongly regular graph.
    :return:  Returns the lambda and mu values that define the SRG.
    """
    common_neighbors_adjacent, common_neighbors_non_adjacent = -1, -1
    for node1 in nx.nodes(G):
        for node2 in nx.nodes(G):
            if node1 == node2:
                continue
            if G.has_edge(node1, node2) and common_neighbors_adjacent == -1:
                common_neighbors_adjacent = len(list(nx.common_neighbors(G, node1, node2)))
            if not G.has_edge(node1, node2) and common_neighbors_non_adjacent == -1:
                common_neighbors_non_adjacent = len(list(nx.common_neighbors(G, node1, node2)))
            if common_neighbors_adjacent != -1 and common_neighbors_non_adjacent != -1:
                return common_neighbors_adjacent, common_neighbors_non_adjacent


def kneser_graph_adjacency_matrix(sets):
    G = kneser_graph(sets)
    adj_matrix = nx.adjacency_matrix(G)
    return adj_matrix.toarray()


def chromatic_number(G):
    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    return max(coloring.values()) + 1


def get_graph6_string(G):
    graph6_string = nx.to_graph6_bytes(G)
    return graph6_string.decode('utf-8')


def share_common_element(arrays):
    if not arrays:
        return False
    common_elements = set(arrays[0])
    for arr in arrays:
        common_elements.intersection_update(arr)
        if len(common_elements) == 0:  # If there are no common elements, return False
            return False
    return True  # All arrays have been checked, and they must share an element
