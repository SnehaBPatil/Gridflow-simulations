from itertools import permutations
import random
import networkx as nx
import sqlite3
import numpy as np
elements = ['A', 'B', 'C', 'D', 'P', 'Q', 'R', 'S']
conn = sqlite3.connect('buscap.db')
cursor = conn.cursor()
#
# c2 = sqlite3.connect('graphbus.db')
# cursor2 = c2.cursor()
#
# c3 = sqlite3.connect('newedgegraph.db')
# cursor3 = c3.cursor()
# #
# c4 = sqlite3.connect('buscap.db')
# cursor4 = c4.cursor()
# pairs = permutations(elements, 2)
#
# conn=sqlite3.connect('newedgegraph.db')
# cursor=conn.cursor()

graph = nx.Graph()
g=nx.Graph()

graph.add_edge('A', 'B',weight=1170)
graph.add_edge('B','Q',weight=1800)
graph.add_edge('B', 'C',weight=630)
graph.add_edge('B','R',weight=1350)
graph.add_edge('C','D',weight=1530)
graph.add_edge('P', 'Q',weight=900)
graph.add_edge('R','S',weight=450)


node_positions = {
    'A': (-12.55, 3.36),
    'B': (0, 0),
    'C': (0, -7),
    'D': (14.72, -15.5),
    'P': (8.66, 5),
    'Q': (0, 20),
    'R': (-14.48, -3.88),
    'S': (-14.48, -7.88)
}

def generate_random_arrival_time():
    return random.randint(0, 64800)


def shortestPath(src,dest):
    shortest_path = nx.dijkstra_path(graph, src, dest, weight='weight')
    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_path




for i in range(0,7):
    pairs = permutations(elements, 2)
    for pair in pairs:
        pair=list(pair)
        arrival_stop=pair[0]
        destination_stop=pair[1]
        arrival_time = generate_random_arrival_time()
        path=shortestPath(arrival_stop,destination_stop)
        path=''.join(path)
        cursor.execute("INSERT INTO passenger (arrival_time,arrival_stop,destination_stop,bus_departure,departure_time,flag,path,waiting_time,bus_id,reached,t) "
            "VALUES (?, ?, ?, ?,?, ?, ?, ?,?,?,?)",
            (arrival_time, arrival_stop, destination_stop, 0, 0, 0, path, 0, 0, 0,arrival_time))
        conn.commit()
    i=i+1
print("Passenger added successfully")
