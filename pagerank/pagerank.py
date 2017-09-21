# pagerank.py
import sys
import os
import argparse
import networkx as nx

def read_graph(pathname):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  filename in data/
    OUTPUT: directed multigraph DG
    """

    print("reading file: {}".format(pathname))
    f = open(pathname, 'r')
    n = int(f.readline())                   # number of vertices
    DG = nx.MultiDiGraph()

    for src in range(n):
        DG.add_node(src)                     # add a vertices
        edges = [(str.split(e," ")) for
                 e in str.split(f.readline().rstrip(),"   ")]
        for e in edges:
            src = int(e[0])
            dst = int(e[1])
            DG.add_edge(src, dst)

    return DG

if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='PageRank Algorithm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='three.txt', help='filename')
    parser.add_argument('-a', '--alpha', nargs='?',
                        default=0.85, help='alpha - damping factor')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graph
    print("damping factor:\t{}".format(args.alpha))
    DG = read_graph(filepath)
    n = len(DG.nodes())
    m = len(DG.edges())
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))

