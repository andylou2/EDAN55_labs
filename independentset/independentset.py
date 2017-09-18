# independentset.py
import sys
import os
import argparse
import networkx as nx

def read_graph(pathname):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  string "gXX.in" in data/
    OUTPUT: graph G
    """

    print("reading file: {}".format(pathname))
    f = open(pathname, 'r')
    n = int(f.readline())                   # number of vertices
    G = nx.Graph()

    for src in range(n):
        G.add_node(src)                     # add a vertices
        edges = str.split(f.readline()," ")[:-1]
        for (dest, e) in enumerate(edges):  # add all edges
            if e == '1':
                G.add_edge(src, dest)

    return G

def MIS(G):
    """
    DESC:   analyzes a vertices-weighted graph G and returns the Max
            Independent Set (MIS)
    INPUT:  graph G
    OUTPUT: MIS value alpha
    """

    # base case: V(G) = 0
    if G.nodes() == []:
        return 0

    # dict of degrees indexed by vertex
    degs = G.degree()

    u = max(degs, key=degs.get)   # get lowest valued vertex with max degree

    # loner nodes added at no penalty
    if G.degree(u) == 0:
        G0 = G.copy()
        G0.remove_node(u)
        return 1 + MIS(G0)

    neighbors = G.neighbors(u) 

    # include vertex u, thus excluding its neighbors
    G1 = G.copy()
    G1.remove_nodes_from(neighbors)
    G1.remove_node(u)
    
    # exclude vertex u
    G2 = G.copy()
    G2.remove_node(u)

    return max(1 + MIS(G1), MIS(G2))

if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='Max Independent Set Algoritm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='g30.in', help='filename g*.in')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graph
    G = read_graph(filepath)
    n = len(G.nodes())
    m = len(G.edges())
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))

    # run algorithm R0 to find size of largest independent set
    alpha = MIS(G)
    
    print("MIS results")
    print("\tfilename:\t{}".format(args.filename))
    print("\talpha:\t\t{}".format(alpha))

