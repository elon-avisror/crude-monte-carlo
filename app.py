import os
import random
import math
import json


from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_file


app = Flask(__name__)

teminals = []


class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()

    def add_neighbor(self, v):  # create edge - add v to neighbors list
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()

    def remove_neighbor(self, v):  # remove edge -  remove v from neighbors list
        self.neighbors.remove(v)


class Graph:
    vertices = {}

    def add_vertex(self, vertex):  # add new vertex to graph
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def add_edge(self, u, v):  # add edge to graph
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add_neighbor(v)
            self.vertices[v].add_neighbor(u)
            return True
        else:
            return False

    def remove_edge(self, u, v):  # remove edge from graph
        if u in self.vertices and v in self.vertices:

            self.vertices[u].remove_neighbor(v)
            self.vertices[v].remove_neighbor(u)
            return True
        else:
            return False

    def update_graph(self, down_edges):  # create new graph without down edges
        for edge in down_edges:
            self.remove_edge(edge[0], edge[1])

    def isUp(self, T1, T2, T3):
        new_graph = self.make_dict_graph()
        if find_path(new_graph, T1, T2):
            if find_path(new_graph, T2, T3):
                return True
        return False

    def make_dict_graph(self):
        dict = {}
        for key in sorted(list(self.vertices.keys())):
            dict[str(key)] = list(self.vertices[key].neighbors)
        return dict


def init_graph():  # Build graph
    g = Graph()
    for i in range(1, 21):
        g.add_vertex(Vertex(i))

    edges = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14],
             [14, 15], [15, 6], [16, 17], [17, 18], [18, 19], [
                 19, 20], [20, 16], [16, 15], [7, 17], [18, 9], [19, 11],
             [20, 13], [1, 8], [2, 10], [3, 12], [4, 14], [5, 6]]
    for edge in edges:
        g.add_edge(edge[0], edge[1])

    return g


def Calc_down_edges(p):  # randomly down edges
    down_edges = []
    edges = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14],
             [14, 15], [15, 6], [16, 17], [17, 18], [18, 19], [
                 19, 20], [20, 16], [16, 15], [7, 17], [18, 9], [19, 11],
             [20, 13], [1, 8], [2, 10], [3, 12], [4, 14], [5, 6]]
    for i in edges:
        x = random.uniform(0, 1)

        if x > p:
            down_edges.append(i)

    return down_edges


def find_path(graph, start, end, path=[]):  # find path with backtracking
    path = path + [start]
    if start == end:
        return True

    if str(start) not in graph:
        return False
    for node in graph[str(start)]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return True
    return False


def find_random_path(graph, start, end, path):  # find path with backtracking
    path = path + [start]
    #print(path + [start])
    if start == end:
        return path

    if str(start) not in graph:
        return False
    for node in graph[str(start)]:
        #print("that is the node--->" + str(node))
        if node not in path:
            newpath = find_random_path(graph, node, end, path)
            if newpath:
                return newpath
    return False


def task_1():
    ansDict = {}
    m1 = 1000
    m2 = 10000
    r1 = 0
    r2 = 0
    Reliability_set = [0.1, 0.2, 0.3, 0.4,
                       0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, ]
    g = init_graph()
    for p in Reliability_set:  # for each probability
        for i in range(0, m1):  # 1000 iterations
            g = init_graph()
            down_edges = Calc_down_edges(p)
            g.update_graph(down_edges)
            if g.isUp(teminals[0], teminals[1], teminals[2]):
                r1 += 1

        for i in range(0, m2):  # 10000 iterations
            g = init_graph()
            down_edges = Calc_down_edges(p)
            g.update_graph(down_edges)
            if g.isUp(teminals[0], teminals[1], teminals[2]):
                r2 += 1
        r1 = r1 / m1
        r2 = r2 / m2
        ansDict[p] = [r1, r2]
        r1 = 0
        r2 = 0
    return ansDict


def task_2_A():
    time_points = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
                   0.95, 1]
    dict_timepoints_count_up = {}
    for t in time_points:
        dict_timepoints_count_up[t] = 0
    for m in range(0, 10000):
        for t in time_points:
            g = init_graph()
            down_edges = Calc_down_edges(math.e**(-t*1))
            g.update_graph(down_edges)
            if g.isUp(teminals[0], teminals[1], teminals[2]):
                dict_timepoints_count_up[t] += 1
    dictAns = {}
    for t in dict_timepoints_count_up:
        dictAns[t] = dict_timepoints_count_up[t]/10000
    return dictAns


def task_2_B():
    r2 = 0
    m2 = 10000
    e = 2.718281828
    time_points = [0, 0.2, 0.5, 0.7, 0.9]
    dict_timepoints_count_up = {}
    for t in time_points:
        dict_timepoints_count_up[t] = 0
    for m in range(0, 10000):
        for t in time_points:
            g = init_graph()
            down_edges = Calc_down_edges(math.e**(-t*1))
            g.update_graph(down_edges)
            if g.isUp(teminals[0], teminals[1], teminals[2]):
                dict_timepoints_count_up[t] += 1
    dictPoint = {}
    for t in dict_timepoints_count_up:
        dictPoint[t] = dict_timepoints_count_up[t]/10000

    counter = 0
    dict_E = {}
    for m in (1, 2, 3, 4, 5):
        dict_E[m] = 0

    for i in range(0, 10000):  # 10000 iterations
        for m in (1, 2, 3, 4, 5):
            g = init_graph()
            down_edges = Calc_down_edges(math.e ** (-0.5))
            g.update_graph(down_edges)
            if g.isUp(teminals[0], teminals[1], teminals[2]):
                dict_E[m] += 1
    dictE = {}
    relativeError=0
    for t in (1, 2, 3, 4, 5):
        dictE[t] = dict_E[t]/10000
        relativeError+=dictE[t]

    relativeError/=5
    dictAns = {}
    dictAns['E'] = dictE
    dictAns['dictPoint'] = dictPoint
    dictAns['relativeError'] = relativeError
    return dictAns


@app.route('/')
def home():
    return render_template('home.html', terminals=teminals)


@app.route('/change_teminals', methods=['POST', 'GET'])
def change_teminals():
    global teminals
    if request.method == 'POST':
        selectedArray = request.form.getlist('selectedArray[]')
        teminals = []
        for select in selectedArray:
            teminals.append(int(select))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/play_task1', methods=['POST', 'GET'])
def play_task1():
    if request.method == 'POST':
        Task = request.form.getlist('Task')
        if(Task == ['Task1']):
            ansDict = task_1()
        return json.dumps(ansDict), 200, {'ContentType': 'application/json'}


@app.route('/play_task2_a', methods=['POST', 'GET'])
def play_task2_a():
    if request.method == 'POST':
        Task = request.form.getlist('Task')
        if(Task == ['Task2_a']):
            ansDict = task_2_A()
        return json.dumps(ansDict), 200, {'ContentType': 'application/json'}


@app.route('/play_task2_b', methods=['POST', 'GET'])
def play_task2_b():
    if request.method == 'POST':
        Task = request.form.getlist('Task')
        if(Task == ['Task2_b']):
            ansDict = task_2_B()
        return json.dumps(ansDict), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
