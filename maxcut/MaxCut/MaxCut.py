from .graph import Graph
import numpy

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
        g.toString()

def R():

def S():

def SR():

def main():
    numpy.set_printoptions(threshold='nan')
    # text_to_graph("data/matching_1000.txt")
    # text_to_graph("data/pw09_100.9.txt")
    text_to_graph("data/test.txt")


if __name__ == '__main__':
    main()
