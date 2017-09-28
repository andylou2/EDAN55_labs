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
    line = f.readline().rstrip().lstrip()

    while not (line == ''):
        if line[0] == 'c':
            # comment
            pass
        elif line[0] == 'p':
            # problem descriptor
            _, _, n, m = str.split(line, " ")
            n, m = map(int, [n, m])

            # add nodes as int indexed from [1,..., n]
            G.add_nodes_from(np.arange(1, n + 1))
        else:
            # edge
            src, dest = map(int, str.split(line," "))
            assert(src <= n and dest <= n)
            G.add_edge(src, dest)

        line = f.readline().rstrip().lstrip()

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
    line = f.readline().rstrip().lstrip()

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
            tokens = str.split(line, " ")
            bag_idx = int(tokens[1])
            T.add_node(bag_idx,contents=[int(token) for token in tokens[2:]])
            
        else:
            # edge
            src, dest = map(int, str.split(line," "))
            T.add_edge(src, dest)

        line = f.readline().rstrip().lstrip()

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
        tree_data[i]['vertices'] = t.nodes(data=True)[i-1][1]['contents'] #parse_contents_(i, t)
        tree_data[i]['dp'] = np.full(2**len(tree_data[i]['vertices']), -1).tolist()
    return tree, tree_data


# def parse_contents_(i, t):
#     s = t.nodes(data=True)[i - 1][1]['contents']
#     if s == '':
#         return []
#     return list(map(lambda x: int(x), str.split(s, " ")))

def MIS(G, T_dict, tw, T, debug=False):
    """
    DESC:   Calculate MIS using K&T algorithm
    INPUT:  original graph G networkx object
            tree T_dict in dictionary format
            treewidth tw
            tree T networkx object
            debug flag for print statements debugging
            assumption: tree T rooted at 1
    OUTPUT: alpha MIS value
    """

    alpha = 0
    # dp table stored in tree T under 'dp' key

    #################################################
    #  create order to process from leaves to root  #
    #################################################

    # stack structure - leaves at top of the stack
    processing_stack = []
    # queue structure
    tmp_queue = []

    root = 1

    #################################################
    #          calculate MIS from leaves up         #
    #################################################

    if debug:
        print("processing order {}".format(processing_stack))

    # post-order for processing leaves before parent
    processing_stack = list(nx.dfs_postorder_nodes(T, root))
    # processing_stack = [processing_stack[0]]
    for curr_bag in processing_stack:
        if T_dict[curr_bag]['children'] == []:
            # is leaf
            for u_binary in isets(T_dict[curr_bag]["vertices"], G):
                # memoize local MIS
                T_dict[curr_bag]["dp"][u_binary] = bin(u_binary).count('1')

            if debug:
                print("leaf {} dp:\t{}".format(curr_bag, T_dict[curr_bag]["dp"]))

        else:
            # internal node
            v_t = T_dict[curr_bag]["vertices"]

            if debug:
                print("internal bag {}".format(curr_bag))
                print("bag contents {}".format(v_t))

            # loop over independent set U of current bag
            for u_binary in isets(v_t, G):
                w = bin(u_binary).count('1')
                u = parse_bits(v_t, u_binary)           # TODO: maybe need to sort v_t

                if debug:
                    print("\tw: {}\tu:{}".format(w, u))

                MIS_over_sum_child = 0

                # calculate summation portion over children
                for child in T_dict[curr_bag]["children"]:
                    if debug:
                        print("\t\tchild bag {}".format(child))
                    v_t_i = T_dict[child]["vertices"]

                    sub_MIS = []

                    # loop over independent set U_i
                    for u_i_binary, c_iset in enumerate(T_dict[child]['dp']):
                        # condition 2: check U_i is independent
                        if c_iset != -1:
                            u_i = parse_bits(v_t_i, u_i_binary)     # TODO: maybe need to sort v_t_i

                            u_i_intersect_v_t = list(filter(lambda x: x in v_t, u_i))
                            v_t_i_intersect_u =list(filter(lambda x: x in v_t_i, u))
                            if debug:
                                print("\t\t\tu_i intersects v_t: {}".format(u_i_intersect_v_t))
                                print("\t\t\tv_t_i intersects u: {}".format(v_t_i_intersect_u))
                            # condition 1: # check that U_i ^ V_t = U ^ V_t_i
                            if u_i_intersect_v_t == v_t_i_intersect_u:
                                sub_MIS.append((c_iset - len(list(filter(lambda x: x in u, u_i)))))
                    # end loop over independentset U_i

                    if len(sub_MIS) == 0:
                        MIS_over_sum_child += 0
                    else:
                        MIS_over_sum_child += max(sub_MIS)
                    if debug:
                        print("\t\tsub_MIS:{}".format(sub_MIS))
                        print("\t\t\tMIS_over_sum_child:{}".format(MIS_over_sum_child))
                #end summation

                T_dict[curr_bag]["dp"][u_binary] = w + MIS_over_sum_child

            if debug:
                print("internal {} dp:\t{}".format(curr_bag, T_dict[curr_bag]["dp"]))
    #################################################
    #        return Max Independent Set (MIS)       #
    #################################################

    # get T_r(U), where U is independent subset of bag Vr

    print(T_dict[root]["dp"])
    alpha = max(T_dict[root]["dp"])

    return alpha


def isets(bag, G):
    s = len(bag)
    ind_sets = np.arange(0, 2**s)
    return list(filter(lambda x: is_independent(bag, x, G), ind_sets))

def is_independent(bag, set, G, flag=False):
    if(set & (set - 1)) == 0:
        return True

    indicies_to_check = []
    i = 1
    while set > 0:
        if set % 2 == 1:
            indicies_to_check.append(i)
        i += 1
        set = set >> 1

    # print("indicies_to_check:{}".format(indicies_to_check))
    for j in range(len(indicies_to_check)):
        for k in range(len(indicies_to_check)):
            # if flag:
            #     print("checking edge: ({}, {})".format(bag[indicies_to_check[j] - 1], bag[indicies_to_check[k] - 1]))
            if (not j == k) and G.has_edge(bag[indicies_to_check[j]-1], bag[indicies_to_check[k]-1]):
                # print("edge: ({}, {}) exists".format(bag[indicies_to_check[j] - 1], bag[indicies_to_check[k] - 1]))
                return False

    return True

def parse_bits(vertex_set, iset):
    indicies_to_check = []
    i = 0
    while iset > 0:
        if iset % 2 == 1:
            indicies_to_check.append(i)
        i += 1
        iset = iset >> 1

    vertices = []
    for j in range(len(indicies_to_check)):
        vertices.append(vertex_set[indicies_to_check[j]])
    return vertices



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

    # if (args.debug):
    #     pp.pprint(T_dict)

    # args.debug = False
    alpha = MIS(G, T_dict, tw, T, args.debug)

    # if (args.debug):
        # pp.pprint(T_dict)

    print("MIS alpha:{}".format(alpha))
