import random

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def build_graph(cap):
    G = nx.Graph()
    G.add_nodes_from(list(range(0, 2 ** dim)))

    for comb in combinations(list(range(0, 2 ** dim)), 2):
        sum = 0
        points = []
        for p in comb:
            sum ^= p
            points.append(p)
        if sum in cap:
            G.add_edge(points[0], points[1], weight=sum)
    return G


def get_4_cycles(G):
    cycles = nx.simple_cycles(G1, 4)
    return [cycle for cycle in cycles if len(cycle) == 4]


if __name__ == '__main__':
    # cap = [0, 1, 4, 2, 8, 16, 32, 64, 63]
    cap2 = [0, 1, 4, 2, 8, 16, 32, 64, 27]
    # cap = [0, 17, 130, 243, 196, 165, 22, 23, 168, 249, 250, 203, 140, 173, 142, 207]
    cap = [1, 4,2]
    # print(cap)
    dim = 3
    perm = list(range(2 ** dim))
    random.shuffle(perm)
    print(perm)
    G1 = build_graph(cap)
    G2 = build_graph(cap2)

    g1_cycles_of_length_4 = get_4_cycles(G1)
    print(g1_cycles_of_length_4)
    print('#g1 4-cycles', len(g1_cycles_of_length_4))

    # g2_cycles_of_length_4 = get_4_cycles(G2)
    # print(g2_cycles_of_length_4)
    # print('#g2 4-cycles', len(g2_cycles_of_length_4))

    # Create a Matplotlib figure and axes
    # fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G1)
    # print('isomorphic?', nx.is_isomorphic(G1, G2))

    # Use the axes object to draw the graph
    nx.draw(G1, with_labels=True, pos=pos)
    edge_labels = nx.get_edge_attributes(G1, "weight")
    nx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels)
    # plt.savefig('filename.png')

    plt.show()
