# independentset.py
import sys
import os
import argparse
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

def R0(G):
    """
    DESC:   analyzes a vertices-weighted graph G and returns the Max
            Independent Set (MIS) using algorithm R0
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
        alpha = 1 + R0(G)
        # restore graph
        G.add_node(u)
        G.add_edges_from(edges_to_u)
        return alpha

    exclude_u = R0(G)

    edges_to_neighbors = G.edges(neighbors) # saved for restoration
    G.remove_nodes_from(neighbors)

    include_u = 1 + R0(G)

    # restore graph
    G.add_nodes_from([u] + neighbors)
    G.add_edges_from(edges_to_u + edges_to_neighbors)


    return max(include_u, exclude_u)

def R1(G):
    """
    DESC:   analyzes a vertices-weighted graph G and returns the Max
            Independent Set (MIS) using algorithm R1
    INPUT:  graph G
    OUTPUT: MIS value alpha
    """

    global counter
    counter += 1

    # base case: V(G) = 0
    if G.nodes() == []:
        return 0

    # dict of degrees (value) indexed by vertex (key)
    degs = G.degree()

    if 1 in degs.values():
        u = degs.keys()[degs.values().index(1)] # get vertex with deg = 1
    else:
        u = max(degs, key=degs.get)         # get vertex with max degree

    neighbors = G.neighbors(u) 

    edges_to_u = G.edges(u)                 # saved for restoration
    G.remove_node(u)

    # R1 mod: add vertex u and exclude neighbors
    if len(neighbors) == 1:
        edges_to_neighbors = G.edges(neighbors) # saved for restoration
        G.remove_nodes_from(neighbors)
        alpha = 1 + R1(G)
        # restore graph
        G.add_nodes_from([u] + neighbors)
        G.add_edges_from(edges_to_u + edges_to_neighbors)
        return alpha

    # loner nodes added at no penalty
    if len(neighbors) == 0:
        alpha = 1 + R1(G)
        # restore graph
        G.add_node(u)
        G.add_edges_from(edges_to_u)
        return alpha

    exclude_u = R1(G)

    edges_to_neighbors = G.edges(neighbors) # saved for restoration
    G.remove_nodes_from(neighbors)

    include_u = 1 + R1(G)

    # restore graph
    G.add_nodes_from([u] + neighbors)
    G.add_edges_from(edges_to_u + edges_to_neighbors)


    return max(include_u, exclude_u)

def R2(G):
    """
    DESC:   analyzes a vertices-weighted graph G and returns the Max
            Independent Set (MIS) using algorithm R2
    INPUT:  graph G
    OUTPUT: MIS value alpha
    """

    #print G.nodes()
    #print G.edges()
    global counter
    counter += 1

    # base case: V(G) = 0
    if G.nodes() == []:
        return 0

    # dict of degrees (value) indexed by vertex (key)
    degs = G.degree()

    if 2 in degs.values():
        u = degs.keys()[degs.values().index(2)] # get vertex with deg = 2
        # print('\tpicked\t:\t{}'.format(u))
    elif 1 in degs.values():
        u = degs.keys()[degs.values().index(1)] # get vertex with deg = 1
    else:
        u = max(degs, key=degs.get)             # get vertex with max degree

    neighbors = G.neighbors(u) 
    edges_to_u = G.edges(u)                     # saved for restoration
    G.remove_node(u)


    # R2 mod: vertex u has two neighbors x,y and xy is an edge
    if len(neighbors) == 2:
        # neighbors of x & y without u (for R2)
        neighbors_of_x_y = G.neighbors(neighbors[0]) + G.neighbors(neighbors[1])

        edges_to_neighbors = G.edges(neighbors) # saved for restoration excld. u

        # if xy is an edge, add u and remove x & y
        if ((neighbors[0],neighbors[1]) in G.edges()
                or (neighbors[1],neighbors[0]) in G.edges()):
            G.remove_nodes_from(neighbors)
            alpha = 1 + R2(G)
            # restore graph
            G.add_nodes_from([u] + neighbors)
            G.add_edges_from(edges_to_u + edges_to_neighbors)
            return alpha
        # else add new vertex z, connect to x & y neighbors (less u)
        # and remove v,x,y
        else:
            G.remove_nodes_from(neighbors)
            # the new vertex z taking on u's key
            z = u
            G.add_node(z)   
            # connect z to all of x & y neighbors, excluding u
            G.add_edges_from(zip([z for i in range(len(neighbors_of_x_y))],
                                 neighbors_of_x_y)) 

            alpha = 1 + R2(G)

            # restore graph
            G.remove_node(z)
            G.add_nodes_from([u] + neighbors)
            G.add_edges_from(edges_to_u + edges_to_neighbors)
            return alpha

    # R1 mod: add vertex u and exclude neighbors
    if len(neighbors) == 1:
        edges_to_neighbors = G.edges(neighbors) # saved for restoration
        G.remove_nodes_from(neighbors)
        alpha = 1 + R2(G)
        # restore graph
        G.add_nodes_from([u] + neighbors)
        G.add_edges_from(edges_to_u + edges_to_neighbors)
        return alpha

    # loner nodes added at no penalty
    if len(neighbors) == 0:
        alpha = 1 + R2(G)
        # restore graph
        G.add_node(u)
        G.add_edges_from(edges_to_u)
        return alpha

    exclude_u = R2(G)

    edges_to_neighbors = G.edges(neighbors) # saved for restoration
    G.remove_nodes_from(neighbors)

    include_u = 1 + R2(G)

    # restore graph
    G.add_nodes_from([u] + neighbors)
    G.add_edges_from(edges_to_u + edges_to_neighbors)


    return max(include_u, exclude_u)
if __name__ == "__main__":

    # parse cmdline args
    parser = argparse.ArgumentParser(description='Max Independent Set Algoritm')
    parser.add_argument('--filename', '-f', nargs='?',
                        default='g30.in', help='filename g*.in')
    parser.add_argument('-a', '--algorithm', nargs='+',
                        default=['R0'], help='algorithm R0, R1, R2(not impl)')

    args = parser.parse_args()

    filepath = os.path.join(os.getcwd(),'data',args.filename)
    
    # read graph
    G = read_graph(filepath)
    n = len(G.nodes())
    m = len(G.edges())
    print("num nodes:\t{}".format(n))
    print("num edges:\t{}".format(m))


    algorithms = {
            'R0': R0,
            'R1': R1,
            'R2': R2
            }
    # run algorithms to find size of largest independent set
    for alg in args.algorithm:
        counter = 0
        alpha = algorithms[alg](G)
        
        print("{} results".format(alg))
        print("\tfilename\t\t:\t{}".format(args.filename))
        print("\talpha\t\t\t:\t{}".format(alpha))
        print("\tnum recursive calls\t:\t{}".format(counter))
