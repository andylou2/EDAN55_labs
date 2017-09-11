import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
import random
import numpy as np
import math
import asyncio
from multiprocessing import Queue
from multiprocessing import SimpleQueue

class MarkingTree:
    def __init__(self, trial, h):
        self.trial = trial
        self.N = 2**(h+1) - 1
        # num = np.arrange(1, N)
        self.gr = nx.balanced_tree(2, h)

        #relabeling nodes to be indexed from 1
        mapping = dict(zip(self.gr.nodes(), range(1,self.N+1)))
        self.gr = nx.relabel_nodes(self.gr, mapping)

        # possibleChoices = np.arange(1,self.N + 1)
        # new_possibleChoices = self.knuth_shuffle(possibleChoices)

        self.nodes = self.gr.nodes()
        self.colored = []
        self.justColored = []
        self.needsChecking = SimpleQueue()

        self.rnd = 0
        i = 0

        while (len(self.colored) != self.N):
            # print("length: {}".format(len(self.colored)))
            # if(len(self.colored) >= N-5):
            # self.show(self.rnd)
            i+=1
            # print("current round: {}".format(self.rnd))

            choice = random.randint(1, self.N)
            # print("round: {}".format(self.rnd))
            # print("possible_choices: {}".format(new_possibleChoices))
            # choice = new_possibleChoices[i - 1]
            self.rnd += 1

            # print("Chose node: {}".format(choice))
            # color if not already colored
            if choice not in self.colored:
                # print("Chose node: {}".format(choice))
                self.colored += [choice]
                # checking for cascading effect
                self.cascade(choice) #nodes colored recently
                # print("Things that have been colored: {}".format(newlyColored))
                self.justColored += [choice]
                # if not self.needsChecking.empty():
                #     print("queue is not empty!")
                while not self.needsChecking.empty():
                    # print("queue length: {}".format(self.needsChecking))
                    self.cascade(self.needsChecking.get())


    def cascade(self, currNode):
        # print("calling cascade on node: {}".format(currNode))
        # neighbors = self.gr.neighbors(currNode)
        # print("neighbors: {}".format(neighbors))
        # if len(neighbors) != 1: #not leaf


        # if currNode <= math.floor(self.N/2):
        #     leftChild = currNode * 2
        #     rightChild = currNode * 2 + 1
        # if currNode != 1: #not root
        #     parent = math.floor(currNode/2)
        # if currNode % 2 == 0: #even
        #     sibling = currNode + 1
        # else:
        #     sibling = currNode - 1

        if currNode > math.floor(self.N/2): #leaf
            parent = math.floor(currNode/2)
            if currNode % 2 == 0: #even
                sibling = currNode + 1
            else:
                sibling = currNode - 1

            if sibling in self.colored and parent not in self.colored:
                self.colored += [parent]
                # print("colored parent {}".format(parent))
                self.justColored += [parent]
                self.needsChecking.put(parent)
            if parent in self.colored and sibling not in self.colored:
                self.colored += [sibling]
                # print("colored sibling {}".format(sibling))
                self.justColored += [sibling]
                self.needsChecking.put(sibling)

        elif currNode == 1: #root
            leftChild = currNode * 2
            rightChild = currNode * 2 + 1

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

        elif currNode != 1 and currNode <= math.floor(self.N/2): #internal
            leftChild = currNode * 2
            rightChild = currNode * 2 + 1
            parent = math.floor(currNode/2)
            if currNode % 2 == 0: #even
                sibling = currNode + 1
            else:
                sibling = currNode - 1

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
        # print("queue length: {} after cascade".format(self.needsChecking))
        # self.show(1)

    def show(self, i):
        pos=nx.drawing.nx_agraph.graphviz_layout(self.gr,prog='dot',args='')
        plt.figure(figsize=(8,8))

        color_values = ['g' if node in self.colored else 'r' for node in self.gr.nodes()]
        nx.draw(self.gr,pos,alpha=0.5,node_color=color_values, with_labels=True)

        plt.axis('equal')
        # plt.title("Colored Nodes: {}".format(self.justColored), loc='center')
        plt.title("test", loc='center')
        plt.savefig("./graphs/trial{}_round{}.png".format(self.trial, i))
        plt.show()

    def knuth_shuffle(self, arr):
        new_arr = np.array(arr, copy=True)
        for i in range(len(arr) - 1, 0, -1):
            j = random.randint(0, i)
            temp = new_arr[i]
            new_arr[i] = new_arr[j]
            new_arr[j] = temp
        return new_arr
def main():

    # N = 1048575
    N = 1023
    H = int(math.log(N+1, 2))
    T = 10

    results = []
    for j in range(18, 19):
        for i in range(T):
            m = MarkingTree(i, j)
            # m.show()
            results += [m.rnd]
            # print("rounds: {}".format(m.rnd))
            # print('height: {}, trial: {}, rounds:{}'.format(j, i, m.rnd))

        # print(results)
        sd = np.std(results)
        mean = np.mean(results)
        results = []

        print('height: {}, mean: {} +- {}'.format(j, mean, sd))


if __name__ == '__main__':
    main()