import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import asyncio

class MarkingTree:
    def __init__(self, trial):
        self.trial = trial
        h = 2
        N = 2**(h+1) - 1
        # num = np.arrange(1, N)
        self.gr = nx.balanced_tree(2, h)

        #relabeling nodes to be indexed from 1
        mapping = dict(zip(self.gr.nodes(), range(1,N+1)))
        self.gr = nx.relabel_nodes(self.gr, mapping)


        # self.nodes = [x+1 for x in self.gr.nodes()]
        self.nodes = self.gr.nodes()
        self.colored = []
        self.justColored = []
        self.needsChecking = asyncio.Queue(maxsize=0)

        self.rnd = 0

        while (len(self.colored) != N):
            self.show(self.rnd)
            self.rnd += 1
            print("current round: {}".format(self.rnd))
            choice = random.randint(1, N)
            print("Chose node: {}".format(choice))
            # color if not already colored
            if choice not in self.colored:
                self.colored += [choice]
                # checking for cascading effect
                self.cascade(choice) #nodes colored recently
                # print("Things that have been colored: {}".format(newlyColored))
                self.justColored += [choice]
                while not self.needsChecking.empty():
                    self.cascade(self.needsChecking.get())


    def cascade(self, currNode):
        print("checking node {}".format(currNode))
        neighbors = self.gr.neighbors(currNode)
        print("neighbors: {}".format(neighbors))
        if currNode != 1: #root
            parent = math.floor(currNode/2)
        if currNode % 2 == 0: #even
            sibling = currNode + 1
            if len(neighbors) != 1: #not leaf
                    leftChild = currNode * 2
                    rightChild = currNode * 2 + 1
        else:
            if len(neighbors) != 1: #not leaf
                    leftChild = currNode * 2
                    rightChild = currNode * 2 + 1
            sibling = currNode - 1

        if len(neighbors) == 1: #leaf
            if sibling in self.colored and parent not in self.colored:
                self.colored += [parent]
                # print("colored parent {}".format(parent))
                self.justColored += [parent]
                self.needsChecking.put(parent)
            elif parent in self.colored and sibling not in self.colored:
                self.colored += [sibling]
                # print("colored sibling {}".format(sibling))
                self.justColored += [sibling]
                self.needsChecking.put(sibling)

        elif len(neighbors) == 2: #root
            if leftChild in self.colored and rightChild not in self.colored:
                self.colored += [rightChild]
                # print("colored rightChild {}".format(rightChild))
                self.justColored += [rightChild]
                self.needsChecking.put(rightChild)
            elif rightChild in self.colored and leftChild not in self.colored:
                self.colored += [leftChild]
                # print("colored leftChild {}".format(leftChild))
                self.needsChecking.put(leftChild)
                self.justColored += [leftChild]

        elif len(neighbors) == 3: #internal
            if sibling in self.colored and parent not in self.colored:
                self.colored += [parent]
                # print("colored parent {}".format(parent))
                self.needsChecking.put(parent)
                self.justColored += [parent]
            elif parent in self.colored and sibling not in self.colored:
                self.colored += [sibling]
                # print("colored sibling {}".format(sibling))
                self.needsChecking.put(sibling)
                self.justColored += [sibling]
            if leftChild in self.colored and rightChild not in self.colored:
                self.colored += [rightChild]
                # print("colored rightChild {}".format(rightChild))
                self.needsChecking.put(rightChild)
                self.justColored += [rightChild]
            elif rightChild in self.colored and leftChild not in self.colored:
                self.colored += [leftChild]
                # print("colored leftChild {}".format(leftChild))
                self.needsChecking.put(leftChild)
                self.justColored += [leftChild]


    def show(self, i):
        pos=nx.drawing.nx_agraph.graphviz_layout(self.gr,prog='dot',args='')
        plt.figure(figsize=(8,8))

        color_values = [ 'g' if node in self.colored else 'r' for node in self.gr.nodes()]
        nx.draw(self.gr,pos,alpha=0.5,node_color=color_values, with_labels=True)

        plt.axis('equal')
        # plt.title("Colored Nodes: {}".format(self.justColored), loc='center')
        plt.title("test", loc='center')
        plt.savefig("./graphs/trial{}_round{}.png".format(self.trial, i))
        plt.show()

def main():

    N = 3
    H = math.log(N-1, 2)
    T = 1

    results = []

    for i in range(T):
        m = MarkingTree(i)
        # m.show()
        results += [m.rnd]
        print('trial {} rounds:{}'.format(i, m.rnd))

    sd = np.std(results)
    mean = np.mean(results)

    print('{} +- {}'.format(mean, sd))


if __name__ == '__main__':
    main()