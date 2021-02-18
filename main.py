#from PySimpleAutomata import DFA, automata_IO

import networkx as nx
import matplotlib.pyplot as plt

"""

VN={S, A, B}, VT={a, b, c, d},
P={
1. S -> bS
2. S -> dA
3. A -> aA
4. A -> dB
5. B -> cB
6. A -> b
7. B -> a
}


S1 -> bS | dA
S -> bS | dA
A -> aA | dB | b
B -> cB | a

VN = {S, A, B, C}, VT={a, b, c, d},
P={
1. S -> dA
2. A -> aB
3. B -> bC
4. C -> cB
5. A -> bA
6. B -> aB
7. B -> d }


S, A, B, C

"""


def check_string(VN, VT, P, input_str):
    for c in input_str:
        if c not in VT:
            print('Bad string.')
            break

    start_is_good = False
    last_terminal = None
    for start_symbols in P['S']:
        if input_str[0] in start_symbols:
            start_is_good = True
            last_terminal = start_symbols[-1]
    if not start_is_good:
        return False

    input_str = input_str[1:]
    middle_is_ok = False
    for c in input_str:
        #print(c)
        for middle_symbols in P[last_terminal]:
            if c in middle_symbols:
                last_terminal = middle_symbols[-1]
                middle_is_ok = True
        if not middle_is_ok:
            return False, "Middle is not ok"
        if c == last_terminal:
            return True, "Everything is fine"
        middle_is_ok = False
    return False, "String has bad finish character"


if __name__ == "__main__":

    VN = ['S', 'A', 'B', 'C']
    VT = ['a', 'b', 'c', 'd']
    P = {
        'S': ['dA'],
        'A': ['aB', 'bA'],
        'B': ['bC', 'aB', 'd'],
        'C': ['cB']
    }

    input_str = input("Input your string here: ")
    if input_str:
        is_string_ok, message = check_string(VN, VT, P, input_str)
        print("Is string ok: {}, Message: {}".format(is_string_ok, message))

    G = nx.Graph()
    G.add_edge("S", "A")
    G.add_edge("A", "B")
    G.add_edge("A", "A")
    G.add_edge("B", "B")
    G.add_edge("B", "C")
    G.add_edge("B", "*")
    G.add_edge("C", "B")
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()})

    edge_labels = {
        ("S", "A"): "d",
        ("A", "B"): "a",
        ("A", "A"): "b",
        ("B", "B"): "a",
        ("B", "C"): "b",
        ("B", "*"): "d",
        ("C", "B"): "c",
    }

    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.show()


    #https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx