# pagerank.py
import sys
import os
import argparse
import random
import networkx as nx

def read_graph(pathname):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  filename in data/
    OUTPUT: directed multigraph DG
    """
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

def pagerank(DG, alpha, nSteps):
    """
    DESC:   simulate a surfer over a graph
    INPUT:  Multiple Digraph DG
            damping factor alpha
            int nSteps for number of steps surfer takes
    OUTPUT: dict outcome of visited vertices
    """

    outcome = {} 
    start = 0       # starting node
    curr = start    # current node it is on

    for itr in range(nSteps):
        # node has no outgoing edge, jump randomly
        if ((random.random() < alpha) and
            DG.out_degree(curr) != 0):

            nxt = random.choice(DG.neighbors(curr))
            try:
                outcome[nxt] += 1
            except KeyError:
                outcome[nxt] = 1
            curr = nxt
        else:
            nxt = random.choice(DG.nodes())
            try:
                outcome[nxt] += 1
            except KeyError:
                outcome[nxt] = 1
            curr = nxt

    #calculate relative frequencies
    for node in outcome:
        outcome[node] = outcome[node] / nSteps

    return outcome 

if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='PageRank Algorithm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='three.txt', help='filename')
    parser.add_argument('-a', '--alpha', nargs='?', type=float,
                        default=0.85, help='alpha - damping factor')
    parser.add_argument('-s', '--steps', nargs='?', type=int,
                        default=100,
                        help='steps - # steps to run simulation')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graph
    DG = read_graph(filepath)
    n = len(DG.nodes())
    m = len(DG.edges())
    print("filename:\t{}".format(args.filename))
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))


    # simulate pagerank
    print("Simulating pagerank...")
    outcome = pagerank(DG, args.alpha, args.steps)
    print("\tdamping factor:\t{}".format(args.alpha))
    print("\tnSteps:\t{}".format(args.steps))
    print("\toutcome:\t{}".format(outcome))
