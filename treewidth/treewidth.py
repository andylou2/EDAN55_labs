# treewidth.py
import sys
import os
import argparse
import random
import networkx as nx
import numpy as np

def read_graphs(pathname):
    """
    DESC:   reads graph G and its associated treewidth decomposition T
            using the lab's input format
    INPUT:  filename data/*.{gr|td}
    OUTPUT: graph G, tree decomposition T, treewidth tw
    """

    G = read_G_ (pathname + '.gr')
    T,tw = read_T_ (pathname + '.td')

    return G, T, tw

def read_G_ (pathname):
    """
    DESC:   helper to read graph G
    INPUT:  filename data/*.gr
    OUTPUT: graph G
    """
    f = open(pathname, 'r')
    G = nx.Graph()

    # build graph G
    line = f.readline()

    while not (line == ''):
        if line[0] == 'c':
            # comment
            pass
        elif line[0] == 'p':
            # problem descriptor
            _, _, n, m = str.split(line, " ")
            n, m = map(int, [n, m])
        else:
            # edge
            src, dest = map(int, str.split(line," "))
            G.add_edge(src, dest)

        line = f.readline().rstrip()

    # error checking
    assert n == len(G.nodes()), 'error in read_G_(): incorrect num nodes'
    assert m == len(G.edges()), 'error in read_G_(): incorrect num edges'

    f.close()

    return G

def read_T_ (pathname):
    """
    DESC:   helper to read tree T
    INPUT:  filename data/*.td
    OUTPUT: tree T, treewidth tw
    """
    f = open(pathname, 'r')
    T = nx.Graph()

    # build tree T
    line = f.readline()

    while not (line == ''):
        if line[0] == 'c':
            # comment
            pass
        elif line[0] == 's':
            # solution descriptor
            _, _, n_bags, size, n = str.split(line, " ")
            n_bags, size, n = map(int, [n_bags, size, n])

        elif line[0] == 'b':
            # contents of each bag
            bag_idx = int(line[2])
            T.add_node(bag_idx,contents=line[4:])
            
        else:
            # edge
            src, dest = map(int, str.split(line," "))
            T.add_edge(src, dest)

        line = f.readline().rstrip()

    # error checking
    assert n_bags == len(T.nodes()), 'error in read_T_(): incorrect num bags'

    f.close()

    return T, size-1

def root_tree(G):
    raise NotImplementedError

def MIS(T, tw):
    """
    DESC:   Calculate MIS using K&T algorithm
    INPUT:  tree T in dictionary format
            treewidth tw 
            assumption: tree T rooted at 1
    OUTPUT: alpha MIS value
    """

    alpha = 0
    n_T = len(T.keys())             # number of bags
    n_W = 2**(tw+1)                 # 
    dp = np.full((n_T,n_W), np.inf)

    #################################################
    #  create order to process from leaves to root  #
    #################################################

    # stack structure - leaves at top of the stack
    processing_line = []
    # queue structure
    tmp_line = []

    root = 1
    processing_line.append(root)
    tmp_line.insert(0, root)

    while tmp_line != []:
        curr = tmp_line.pop()
        for child in T[curr]['children']:
            processing_line.append(child) # add bags index (int)
            tmp_line.insert(0, child)

    #################################################
    #          calculate MIS from leaves up         #
    #################################################

    while processing_line != []:
        curr = processing_line.pop()
        if T[curr]['children'] == []:
            # is leaf
            #for subset in list(it.powerset(T["vertices"])):
            #    dp[curr][subset] = len(subset)
            pass 


    return alpha

if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='Treewidth Algorithm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='eppstein', help='filename')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graphs *.{gr|td}

    G, T, tw = read_graphs(filepath)
    g_n = len(G.nodes())
    g_m = len(G.edges())
    t_n = len(T.nodes())
    t_m = len(T.edges())
    print("filename:{}".format(args.filename))
    print("G")
    print("\tnum nodes:\t{}".format(g_n))
    print("\tnum edges:\t{}".format(g_m))
    print("T")
    print("\ttreewidth:\t{}".format(tw))
    print("\tnum nodes:\t{}".format(t_n))
    print("\tnum edges:\t{}".format(t_m))

    # T_dict = root_tree(T)

    T_dict = {
            1: {
                'children': [2,3,4],
                'vertices': [1]
                },
            2: {
                'children': [5],
                'vertices': [2]
                },
            3: {
                'children': [7,8],
                'vertices': [2]
                },
            4: {
                'children': [],
                'vertices': [2]
                },
            5: {
                'children': [6],
                'vertices': [2]
                },
            6: {
                'children': [],
                'vertices': [3]
                },
            7: {
                'children': [],
                'vertices': [3]
                },
            8: {
                'children': [],
                'vertices': [3]
                }
            }
    alpha = MIS(T_dict, tw)

    print("MIS alpha:{}".format(alpha))

