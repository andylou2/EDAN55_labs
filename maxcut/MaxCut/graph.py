import numpy as np


class Graph:

    def __init__(self, nodes, edges):
        """
        creates 2d array, components, such that the y axis represents the source node and the
        x axis represents the destination node
        read 2d array, components, as a adjacency matrix
        :param vertices:
        :param edges:
        :return:
        """
        self.nodes = nodes
        self.edges = edges
        self.components = np.zeros((nodes, nodes))


    def add_edge(self, source, dest, weight):
        #even if the graph is not simple (multiple edges from same node) we can still "combine"
        # the edge by adding the weights together and treating it as one edge
        self.components[source-1][dest-1] += weight
        self.components[dest-1][source-1] += weight

    def toString(self):
        print(self.components)

    # todo implement node and edge removal