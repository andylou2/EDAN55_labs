import sys
import os
import argparse
import random
import networkx as nx
import numpy as np
import json
import pprint

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

def root_tree(t):
    """
    :param t:   tree
    :return:    dictionary of dictionary holding the children, bag contents,
                table of each node in the tree
    """
    tree_data = {}
    tree = nx.dfs_tree(T, 1)
    for i in range(1, len(t.nodes()) + 1):
        tree_data[i] = {}
        
        # returns array of the ith nodes children
        tree_data[i]['children'] = tree.neighbors(i)
        # parses the node contents from int to string
        tree_data[i]['vertices'] = parse_contents_(i, t)                      
        tree_data[i]['dp'] = np.full(2**len(tree_data[i]['vertices']) +
                                1, -1).tolist()
    return tree, tree_data


def parse_contents_(i, t):
    s = t.nodes(data=True)[i - 1][1]['contents']
    return list(map(lambda x: int(x), str.split(s, " ")))

def MIS(G, T, tw):
    """
    DESC:   Calculate MIS using K&T algorithm
    INPUT:  original graph G networkx object
            tree T in dictionary format
            treewidth tw 
            assumption: tree T rooted at 1
    OUTPUT: alpha MIS value
    """

    alpha = 0
    n_T = len(T.keys())             # number of bags
    n_W = 2**(tw+1)                 # max subsets of each bag
    # dp table stored in tree T under 'dp' key

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
        curr_bag = processing_line.pop()
        if T[curr_bag]['children'] == []:
            # is leaf
            for iset in isets(T[curr_bag]["vertices"], G):
                # memoize local MIS
                dp[curr_bag][iset] = bin(iset).count('1')

        else:
            # internal node
            for iset in isets(T[curr_bag]["vertices"], G):
                for child in T[curr_bag]["children"]:
                    dp[curr_bag][iset] = (bin(iset).count('1') +
                                         max(T[child]["dp"]))

    #################################################
    #        return Max Independent Set (MIS)       #
    #################################################

    # get T_r(U), where U is independent subset of bag Vr
    alpha = max(T[root]["dp"])

    return alpha

def isets(bag, G):
    raise NotImplementedError

if __name__ == "__main__":

    # pretty printer
    pp = pprint.PrettyPrinter(indent=4)
    # parse cmdline args
    parser = argparse.ArgumentParser(description='Treewidth Algorithm')
    parser.add_argument('-f', '--filename', nargs='?',
                        default='eppstein', help='filename')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug mode: print the tree')

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

    _, T_dict = root_tree(T)

    if (args.debug): 
        pp.pprint(T_dict)

    alpha = MIS(G, T_dict, tw)

    print("MIS alpha:{}".format(alpha))
