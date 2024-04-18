import numpy as np
import math

# Define the stops and their coordinates
from itertools import permutations
import random
import networkx as nx
g = nx.Graph()
g.add_edge('A', 'B',weight=13)
g.add_edge('B','Q',weight=20)
g.add_edge('B', 'C',weight=7)
g.add_edge('B','R',weight=15)
g.add_edge('C','D',weight=17)
g.add_edge('P', 'Q',weight=10)
g.add_edge('R','S',weight=5)
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

def calculate_distance(coord1, coord2):
    # Calculate Euclidean distance between two points
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
# Define the range of x and y values
x_min, x_max = -15, 15
y_min, y_max = -16, 20

# Generate random points
num_points = 1000
x_values = np.random.uniform(x_min, x_max, num_points)
y_values = np.random.uniform(y_min, y_max, num_points)

# Create a list to store the points
points = [(x, y) for x, y in zip(x_values, y_values)]
# print(points[:10])


def find_nearest_stop(coord):
    min_distance = float('inf')
    nearest_stop = None

    for stop, stop_coord in node_positions.items():
        distance = calculate_distance(coord, stop_coord)
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop

    return nearest_stop,min_distance


data={}
i=0
for point in points:
    # new_node = (0, 2)
    g.add_node(point)
    total_distance=0
    # Update node_positions with the coordinates of the new node
    node_positions['New'] = point
    # print("Nodes in graph after adding new node:", g.nodes())
    # print("Node positions after adding new node:", node_positions)
    for c in points:
        nearest_stop,min_distance=find_nearest_stop(c)
        total_distance=total_distance+min_distance
        # print(total_distance)
    total_distance=total_distance/1000
    data[i]={'x':point[0],
             'y':point[1],
             'distance':total_distance

    }
    g.remove_node(point)
    del node_positions['New']
    i=i+1

#
# for edge,d in data.items():
  #   print(f"Edge {edge}: x = {d['x']}, y = {d['y']}, distance = {d['distance']:.2f}")

sorted_coordinates = sorted(data.values(), key=lambda k: k['distance'])

for s in sorted_coordinates:
    print(s)
