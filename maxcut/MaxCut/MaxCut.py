from .graph import Graph
import numpy as np
import random

def text_to_graph(file):
        """
        populates a new graph instance based on a given text file
        :param file:
        :return:
        """
        f = open(file, 'r')
        firstLine = f.readline()
        data = firstLine.split() #splits string based on spaces

        g = Graph(int(data[0]), int(data[1]))

        for line in f:
            data = line.split()
            g.add_edge(int(data[0]), int(data[1]), int(data[2]))

        f.close()
        # g.toString()
        return g


def R(g):
    '''
    DESC:   Implements algorithm R
            Randomly partitions graph g and calculates MaxCut
    INPUT:  Graph g
    OUTPUT: Value of maxcut w
    '''
    A = []
    B = []
    # print("g nodes:".format)
    A, B = randomPartition(A, B, g)
    w = cutSize(A, B, g)
    return w

def S(g):
    '''
    DESC:   Implements algorithm S
            greedily swap a node between paritions until MaxCut cannot
            be improved
    INPUT:  Graph g
    OUTPUT: Value of maxcut w
    '''
    # start with all nodes in A
    A = [i for i in range(g.nodes)]
    B = []

    # keep track of current cutsize

    # pick a random node and "recolor" it the cut size increases
    # while True:
    #
    #     val = random.randint(1, g.nodes)

    difference = S_helper(A, B, g)
    i = 0
    while True:
        #if there was no change after checking every node again, we break out of loop
        # print("delta:{}".format(difference))
        i += 1
        if difference <= 0:
            break
        difference = S_helper(A, B, g)
    print(i)
    return cutSize(A, B, g)

def SR(g):
    '''
    DESC:   Implementation of SR algorithm
            1) Randomly paritions graph g
            2) greedily calculate MaxCut
    INPUT:  Graph g
    OUTPUT: Value of maxcut w
    '''
    A = []
    B = []
    randomPartition(A, B, g)

    difference = S_helper(A, B, g)
    i = 0
    while True:
        #if there was no change after checking every node again, we break out of loop
        i += 1
        # print("delta:{}".format(difference))
        if difference <= 0:
            break
        difference = S_helper(A, B, g)
    print(i)
    return cutSize(A, B, g)



def S_helper(A, B, g):
    cum_d = 0
    for val in range(g.nodes):
        d = cutSizeDelta(val, A, B, g)
        if d > 0:
            cum_d += d
            if val in A:
                A.remove(val) # recolor
                B.append(val)
            else:
                A.append(val)
                B.remove(val)

    return cum_d


def randomPartition(A, B, g):
    for i in range(g.nodes):
        r = random.randint(0,1)
        if r == 0:
            A.append(i)
        else:
            B.append(i)
    return A, B

def cutSizeDelta(val, A, B, g):
    delta = 0
    if val in A:
        # calculating the change in cut size if val were moved from partition A to B
        for dest in A:
            delta += g.components[val][dest]
        for dest in B:
            delta -= g.components[val][dest]
    else:
        # calculating the change in cut size if val were moved from partition B to A
        for dest in B:
            delta += g.components[val][dest]
        for dest in A:
            delta -= g.components[val][dest]
    return delta


def cutSize(A, B, g):
    weight = 0
    for n in A:
        for dest in B:
            weight += g.components[n][dest]
    return weight


def main():
    np.set_printoptions(threshold='nan')

    # parse input graph
    # g = text_to_graph("data/matching_1000.txt")
    g = text_to_graph("data/pw09_100.9.txt")
    # text_to_graph("data/test.txt")

    algo = "SR"
    num_trials = 100

    # Accumuates values for each trial
    vals = []
    # tracks maxcut over several trials
    max_val = 0

    data = open("data_" + algo + ".txt", "w+")

    print("--- start --- ")
    print("Running Algorithm {}".format(algo))
    print("num_trials = {}".format(num_trials))
    
    # Simulate experiment over several trials
    for i in range(num_trials):
        if algo == "SR":
            val = SR(g)
        elif algo == "S":
            val = S(g)
        else:
            val = R(g)

        data.write(str(int(val)) + "\n")
        print(val)
        vals += [val]
        if val > max_val:
            max_val = val

    data.close()
    print("\t maximum:{}".format(max_val))
    print("\t average:{}".format(np.mean(np.array(vals))))
    print("---  end  ---")


if __name__ == '__main__':
    main()
