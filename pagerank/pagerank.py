# pagerank.py
import sys
import os
import argparse
import random
import networkx as nx
import re
import operator
import numpy as np
import numpy.matlib

def read_graph(pathname):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  filename in data/
    OUTPUT: directed multigraph DG
    """
    f = open(pathname, 'r')
    n = int(f.readline())                   # number of vertices
    DG = nx.MultiDiGraph()

    for i in range(n):
        DG.add_node(i)

    v = []
    line = f.readline()
    while not (line == ''):
        nodes = re.split("\s", line)        # splits by all tabs and single spaces
        for i in range(len(nodes)):
            if nodes[i].isdigit():
                v.append(int(nodes[i]))     # only taking integer nodes
        for i in range(0, len(v) - 1, 2):   # adds the edge based on every 2 elements
            DG.add_edge(v[i], v[i+1])

        line = f.readline()
        v = []

    f.close()

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

    outcome[curr] = 1
    for itr in range(nSteps):
        # node has no outgoing edge, jump randomly
        if ((random.random() < alpha) and
            DG.out_degree(curr) != 0):
            nxt = random.choice(DG.out_edges(curr))[1]

        else:
            nxt = random.choice(DG.nodes())

        try:
            outcome[nxt] += 1
        except KeyError:
            outcome[nxt] = 1
        curr = nxt

    #calculate relative frequencies
    for node in outcome:
        outcome[node] = outcome[node] / (nSteps + 0.0)

    sorted_outcome = sorted(outcome.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_outcome


def pagerank_matrix(DG, alpha, r):
    """
    DESC:   Calculate pagerank outcome percentages by
            matrix multiplication
    INPUT:  Directed Multigraph DG
            damping factor alpha
            int r for number times to multiply matrix
    OUTPUT:  array p of outcome percentages
    :param DG:
    :param alpha:
    :param r:
    :return:
    """
    v = len(DG.nodes())
    P = np.matlib.zeros((v, v))
    p = np.matlib.zeros((1, v))
    p[0,0] = 1
    for i in range(0, v):
        e = DG.out_degree(i)
        if (e == 0):
            P[i:] = 1.0/v
        else:
            for j in range(0, v):
                P[i,j] = (1-alpha)/v
                ej = DG.number_of_edges(i,j)
                if (ej > 0):
                    P[i,j] += (alpha*ej)/e

    for i in range(0, r):
        p = p*P

    outcome = {}
    for i in range(v):
        outcome[i] = p.item(i)

    sorted_outcome = sorted(outcome.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_outcome



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
    parser.add_argument('-m', '--matrix', action='store_true',
                        help='matrix - to run the matrix calculation')

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
    if (args.matrix is not None):
        print("Calculating pagerank...")
        outcome = pagerank_matrix(DG, args.alpha, args.steps)
    else:
        print("Simulating pagerank...")
        outcome = pagerank(DG, args.alpha, args.steps)
    print("\tdamping factor:\t{}".format(args.alpha))
    print("\tnSteps:\t{}".format(args.steps))
    print("\toutcome:\t{}".format(outcome))
