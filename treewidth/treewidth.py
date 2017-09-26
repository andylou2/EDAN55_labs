# treewidth.py
import sys
import os
import argparse
import random
import networkx as nx
import numpy as np
import json

def read_graphs(pathname):
    """
    DESC:   reads graph G and its associated treewidth decomposition T
            using the lab's input format
    INPUT:  filename data/*.{gr|td}
    OUTPUT: graph G, treewidth T
    """

    G = read_G_ (pathname + '.gr')
    T = read_T_ (pathname + '.td')

    return G,T

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
    OUTPUT: tree T
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

    return T


def root_tree(t):
    """
    :param t: tree
    :return: dictionary of dictionary holding the children, bag contents, and table of each node in the tree
    """
    tree_data = {}
    tree = nx.dfs_tree(T, 1)
    for i in range(1, len(t.nodes()) + 1):
        tree_data[i] = {}
        print(tree.neighbors(i))
        tree_data[i]['children'] = tree.neighbors(i)                         # returns array of the ith nodes children
        tree_data[i]['vertices'] = parse_contents(i, t)                      # parses the node contents from int to string
        tree_data[i]['table'] = np.zeros(2**len(tree_data[i]['vertices']) + 1).tolist()
    return tree, tree_data


def parse_contents(i, t):
    s = t.nodes(data=True)[i - 1][1]['contents']
    return list(map(lambda x: int(x), str.split(s, " ")))


if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='Treewidth Algorithm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='eppstein', help='filename')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graphs *.{gr|td}

    G,T = read_graphs(filepath)
    g_n = len(G.nodes())
    g_m = len(G.edges())
    t_n = len(T.nodes())
    t_m = len(T.edges())
    print("filename:{}".format(args.filename))
    print("G")
    print("\tnum nodes:\t{}".format(g_n))
    print("\tnum edges:\t{}".format(g_m))
    print("T")
    print("\tnum nodes:\t{}".format(t_n))
    print("\tnum edges:\t{}".format(t_m))

    # t, x = root_tree(T)
    # f = open("test.txt", 'w+')

    # json.dump(x, f, sort_keys=True, indent=4, separators=(',', ': '))
    # f.close()


