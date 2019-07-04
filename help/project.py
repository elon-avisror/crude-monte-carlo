import random
import math
import matplotlib.pyplot as plt
import numpy as np
from networkx import nx


terminals = [8, 12, 20]

edges = [[1, 2], [1, 5], [1, 8], [2, 3], [2, 10], [3, 4], [3, 12], [4, 5], [4, 14], [5, 6], [6, 7], [6, 15],
         [7, 8], [7, 17], [8, 9], [9, 10], [9, 18], [10, 11], [11, 12], [11, 19], [12, 13], [13, 14], [13, 20],
         [14, 15], [15, 16], [16, 17], [16, 20], [17, 18], [18, 19], [19, 20]]

def paint():

    G = nx.Graph()

    for i in range(1, 21):
        G.add_node(i, data=str(i))

    for [a, b] in edges:
        G.add_edge(a, b)

    nx.draw(G, with_labels=True)
    # display
    plt.show()

paint()


class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()

    # create edge - add v to neighbors list
    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()

    # remove edge -  remove v from neighbors list
    def remove_neighbor(self, v):
        self.neighbors.remove(v)


class Graph:
    vertices = {}

    # add new vertex to graph
    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    # add edge to graph
    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add_neighbor(v)
            self.vertices[v].add_neighbor(u)
            return True
        else:
            return False

    # remove edge from graph
    def remove_edge(self, u, v):

        if u in self.vertices and v in self.vertices:

            self.vertices[u].remove_neighbor(v)
            self.vertices[v].remove_neighbor(u)
            return True
        else:
            return False

    # create new graph without down edges
    def update_graph(self, down_edges):
        for edge in down_edges:
            self.remove_edge(edge[0], edge[1])

    def isUp(self, T1, T2, T3):
        new_graph = self.make_dict_graph()
        if find_path(new_graph, T1, T2):
            if find_path(new_graph, T2, T3):
                return True
        return False

    def print_graph(self):
        print("______________________________________")
        print("Graph by Adjacency List representation:")
        for key in sorted(list(self.vertices.keys())):
            print(str(key) + str(self.vertices[key].neighbors))

    def make_dict_graph(self):
        dict = {}
        for key in sorted(list(self.vertices.keys())):
            dict[str(key)] = list(self.vertices[key].neighbors)
        return dict

    def make_unsorted_dict_graph(self):
        dict = {}
        for key in self.vertices.keys():
            a = (list(self.vertices[key].neighbors))
            random.shuffle(a)
            dict[str(key)] = a
        return dict


# build graph
def init_graph():

    g = Graph()
    for i in range(1, 21):
        g.add_vertex(Vertex(i))

    for edge in edges:
        g.add_edge(edge[0], edge[1])

    return g


# randomly down edges
def Calc_down_edges(p):

    down_edges = []

    for i in edges:
        x = random.random()

        if x > p:
            down_edges.append(i)

    return down_edges


# find path with backtracking
def find_path(graph, start, end, path=[]):

    path = path + [start]
    if start == end:
        return True

    if str(start) not in graph:
        return False
    for node in graph[str(start)]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return True
    return False


# find path with backtracking
def find_random_path(graph, start, end, path):

    path = path + [start]
    #print(path + [start])

    if start == end:
        return path

    if str(start) not in graph:
        return False
    for node in graph[str(start)]:

        #print("that is the node --->" + str(node))
        if node not in path:
            newpath = find_random_path(graph, node, end, path)
            if newpath: return newpath
    return False


def task_1():

    m1 = 1000
    m2 = 10000
    r1 = 0
    r2 = 0

    Reliability_set = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]

    g = init_graph()
    g.print_graph()

    # for each probability
    for p in Reliability_set:

        # 1000 iterations
        for i in range(0, m1):
            g = init_graph()
            down_edges = Calc_down_edges(p)
            g.update_graph(down_edges)
            if g.isUp(terminals[0], terminals[1], terminals[2]):
                r1 += 1

        # 10000 iterations
        for i in range(0, m2):
            g = init_graph()
            down_edges = Calc_down_edges(p)
            g.update_graph(down_edges)
            if g.isUp(terminals[0], terminals[1], terminals[2]):
                r2 += 1
        r1 = r1 / m1
        r2 = r2 / m2
        print("----------------------------------------")
        print("Probability:", p)

        print("Reliability for 1000 iterations =", r1)
        print("Reliability for 10000 iterations =", r2)

        r1 = 0
        r2 = 0


def task_2_A():
    g = init_graph()
    #g.print_graph()

    time_points = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
                   0.95, 1]

    dict_timepoints_count_up = {}
    edges_life = {}

    path1 = []
    path2 = []
    path3 = []

    network_lifetime = 0

    for t in time_points:
        dict_timepoints_count_up[t] = 0
    for m in range(0, 10000):
        for i in edges:
            # create a random value between: 0 to 1
            x = random.random()

            # calculate the lifetime of the edge ????????????????????????????
            y = -math.log(x)

            # create dict with key as tuples(edges) and value as hte life time
            edges_life[tuple(i)] = y

        # find the path between: 1 to 8
        path1 = find_random_path(g.make_unsorted_dict_graph(), 8, 12, path1)

        # find the path between: 8 to 14
        path2 = find_random_path(g.make_unsorted_dict_graph(), 12, 20, path2)

        path1 += path2[1:]

        for i in range(0, len(path1) - 1):
            x = (path1[i], path1[i + 1])

            # create a list of tuples, represent the path by the edges (tuple of edges)
            path3.append(x)

        while network_lifetime == 0:

            # find the minimum lifetime of edge (from all the edges)
            edge = (min(edges_life, key=edges_life.get))
            if edge in path3:
                network_lifetime = edges_life[edge]
            else:
                edges_life.pop(edge)

        # for any time point check if its bigger then network lifetime and sum the number of iteration for this point
        for t in time_points:
            if t <= network_lifetime:
                dict_timepoints_count_up[t] += 1

        edges_life = {}
        path1 = []
        path2 = []
        path3 = []
        network_lifetime = 0
    for t in dict_timepoints_count_up:
        print("----------------------------------")
        print("Time Point: " + str(t))
        print("Result is: " + str(dict_timepoints_count_up[t]/10000))

    ans = []
    for key, value in dict_timepoints_count_up.items():
        ans.append(value/10000)

    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    plt.xticks(np.arange(min(x), max(x) + 0.1, 0.1))
    plt.plot(ans)
    plt.show()


def task_2_B():
    r2 = 0
    m2 = 10000
    e = 2.718281828
    time_points = [0, 0.2, 0.5, 0.7, 0.9]
    for t in time_points:

        # 10000 iterations
        for i in range(0, m2):
            g = init_graph()
            down_edges = Calc_down_edges(pow(e, -0.5*t))
            g.update_graph(down_edges)
            if g.isUp(terminals[0], terminals[1], terminals[2]):
                r2 += 1
        r2 = r2 / m2
        print("----------------------------------------")
        print("Time Point : ", t)
        print("Reliability for 10000 iterations =", r2)
        r2 = 0


def main():
    print("\nPart 1:")
    task_1()
    print("\nPart 2 Section A:\n")
    task_2_A()
    print("\nPart 2 Section B:")
    task_2_B()


main()