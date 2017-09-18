# independentset.py
import sys
import os
import argparse
import networkx as nx

counter = 0

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

    global counter
    counter += 1
    # base case: V(G) = 0
    if G.nodes() == []:
        return 0

    # dict of degrees indexed by vertex
    degs = G.degree()

    u = max(degs, key=degs.get)             # get vertex with max degree
    neighbors = G.neighbors(u) 

    edges_to_u = G.edges(u)                 # saved for restoration
    G.remove_node(u)

    # loner nodes added at no penalty
    if len(neighbors) == 0:
        alpha = 1 + MIS(G)
        # restore graph
        G.add_node(u)
        G.add_edges_from(edges_to_u)
        return alpha

    exclude_u = MIS(G)

    edges_to_neighbors = G.edges(neighbors) # saved for restoration
    G.remove_nodes_from(neighbors)

    include_u = 1 + MIS(G)

    # restore graph
    G.add_nodes_from([u] + neighbors)
    G.add_edges_from(edges_to_u + edges_to_neighbors)


    return max(include_u, exclude_u)

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
    print("\tfilename\t\t:\t{}".format(args.filename))
    print("\talpha\t\t\t:\t{}".format(alpha))
    print("\tnum recursive calls\t:\t{}".format(counter))

