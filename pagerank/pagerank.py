# pagerank.py
import sys
import os
import argparse
import networkx as nx

def read_graph(pathname):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  filename in data/
    OUTPUT: graph G
    """

    raise NotImplementedError

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

if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='PageRank Algorithm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='three.txt', help='filename')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graph
    G = read_graph(filepath)
    n = len(G.nodes())
    m = len(G.edges())
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))

