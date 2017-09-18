# independentset.py
import sys
import os
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

def alpha(G):
    """
    DESC:   analyzes a vertices-weighted graph G and returns the Max
            Independent Set (MIS)
    INPUT:  graph G
    OUTPUT: MIS value alpha
    """
    raise NotImplementedError

if __name__ == "__main__":

    filename = "g30.in"
    filepath = os.path.join(os.getcwd(),'data',filename)
    
    # read graph
    G = read_graph(filepath)
    n = len(G.nodes())
    m = len(G.edges())
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))

    # run algorithm R0 to find size of largest independent set
    alpha = MIS(G)
    
    print("MIS results")
    print("\tfilename:\t{}".format(filename))
    print("\talpha:\t{}".format(alpha))

