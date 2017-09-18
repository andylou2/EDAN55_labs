# independentset.py
import sys
import os

def read_graph(filename):
    """
    DESC:   reads a graph using the lab's input format
    INPUT:  string "gXX.in" in data/
    OUTPUT: graph G
    """
    raise NotImplementedError

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
    
    # read graph
    G = read_graph(filename)

    # run algorithm R0 to find size of largest independent set
    alpha = MIS(G)
    
    print("MIS results")
    print("\tfilename:\t{}".format(filename))
    print("\talpha:\t{}".format(alpha))

