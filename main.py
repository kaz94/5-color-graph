import networkx as nx
from matplotlib import pyplot as plt
import itertools
import numpy as np
import sys, os
from tkFileBrowser import askopenfilename
from tkinter import Tk


Tk().withdraw()
file = askopenfilename(initialdir=os.path.dirname(sys.argv[0]))
if len(file) == 0:
    filename = "initial_graph.txt"
    print("Opening default graph")
else:
    filename = file

COLORS = ['salmon', 'green', 'steelblue', 'pink', 'y']
COLORS_int = [1, 2, 3, 4, 5]

G = nx.read_adjlist(filename, nodetype=int)


def five_color(graph):

    N = len(graph.nodes())
    if N <= 5:
        nodes = graph.nodes()
        for ii, node in enumerate(nodes):
            graph.node[node]['color'] = COLORS[ii]
        print("Graph successfully colored")

    else:
        nodes_contracted = False
        G_new = nx.copy.deepcopy(graph)
        nodes = G_new.nodes()
        degrees = list(G_new.degree(nodes).values())

        if 5 in degrees:
            node = nodes[degrees.index(5)]
            comb = itertools.combinations(nx.neighbors(G_new, node), 2)

            for c in comb:
                if c not in G_new.edges() and (c[1], c[0]) not in G_new.edges():
                    edge = c
                    break
            x = edge[0]
            y = edge[1]
            G_new.remove_node(node)
            G_new = nx.contracted_nodes(G_new, *edge)
            nodes_contracted = True

        else:
            tmp = np.array(list(set(degrees)))
            degree = max(tmp[tmp < 5])
            node = nodes[degrees.index(degree)]
            G_new.remove_node(node)

        GG = five_color(G_new)

        for n in GG.nodes():
            graph.node[n]['color'] = GG.node[n]['color']

        if nodes_contracted:
            graph.node[y]['color'] = graph.node[x]['color']

        av_colors = COLORS.copy()
        for n in nx.neighbors(graph, node):
            try:
                av_colors.remove(graph.node[n]['color'])
            except: ValueError

        graph.node[node]['color'] = av_colors[0]

    return graph

G_colored = five_color(G)

colors = [G.node[i]['color'] for i in G.nodes()]
position = nx.spring_layout(G_colored)
nx.draw(G_colored, pos=position, node_color=colors)
labels = nx.draw_networkx_labels(G_colored, pos=position)
#plt.show(block=False)
plt.savefig("colored_graph.png")

dict = {z_[0] : z_[1] for z_ in zip(COLORS, COLORS_int)}
data = [(n, dict[G_colored.node[n]['color']]) for n in G_colored.nodes()]
np.savetxt("colors.txt", np.array(data), fmt='%.0d', delimiter='\t', header="Node\tColor")

print("Image and file saved")

