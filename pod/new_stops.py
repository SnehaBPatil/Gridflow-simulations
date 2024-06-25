import numpy as np
import math
import matplotlib.pyplot as plt

def generate_poisson_disc_points(x_min, x_max, y_min, y_max, min_distance, num_points):
    # Constants
    k = 30  # Maximum number of attempts for each point

    # Cell size for grid
    cell_size = min_distance / math.sqrt(2)

    # Number of grid cells in x and y directions
    cols = math.ceil((x_max - x_min) / cell_size)
    rows = math.ceil((y_max - y_min) / cell_size)

    # Initialize grid
    grid = [[None] * cols for _ in range(rows)]

    # Initialize active and sample lists
    active_list = []
    sample_points = []

    def get_random_point_around(point, min_dist, max_dist):
        r = np.random.uniform(min_dist, max_dist)
        theta = np.random.uniform(0, 2 * math.pi)
        x = point[0] + r * math.cos(theta)
        y = point[1] + r * math.sin(theta)
        return x, y

    def get_grid_index(point):
        col = math.floor((point[0] - x_min) / cell_size)
        row = math.floor((point[1] - y_min) / cell_size)
        return col, row

    def is_valid_point(point):
        col, row = get_grid_index(point)
        for c in range(max(0, col - 2), min(cols, col + 3)):
            for r in range(max(0, row - 2), min(rows, row + 3)):
                neighbor = grid[r][c]
                if neighbor is not None and calculate_distance(point, neighbor) < min_distance:
                    return False
        return True

    def calculate_distance(coord1, coord2):
        return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

    # Choose initial point randomly
    initial_point = (np.random.uniform(x_min, x_max), np.random.uniform(y_min, y_max))
    active_list.append(initial_point)
    sample_points.append(initial_point)
    col_init, row_init = get_grid_index(initial_point)
    grid[row_init][col_init] = initial_point

    while active_list:
        # Randomly select an active point
        index = np.random.randint(len(active_list))
        active_point = active_list[index]

        # Generate new points around active point
        found_valid_point = False
        for _ in range(k):
            new_point = get_random_point_around(active_point, min_distance, 2 * min_distance)
            if (x_min <= new_point[0] <= x_max) and (y_min <= new_point[1] <= y_max) and \
                    is_valid_point(new_point):
                active_list.append(new_point)
                sample_points.append(new_point)
                col_new, row_new = get_grid_index(new_point)
                grid[row_new][col_new] = new_point
                found_valid_point = True
                break

        if not found_valid_point:
            active_list.pop(index)

    return sample_points

# Define the range of x and y values
x_min, x_max = -15, 15
y_min, y_max = -16, 20

# Minimum distance for Poisson disc sampling
min_distance = 2.0  # Adjust as needed

# Generate Poisson disc points
num_points = 500
poisson_points = generate_poisson_disc_points(x_min, x_max, y_min, y_max, min_distance, num_points)

# Plot the points
x_values, y_values = zip(*poisson_points)

points = [(x, y) for x, y in zip(x_values, y_values)]


import numpy as np
import math
import matplotlib.pyplot as plt
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


# Generate random points


def find_nearest_stop(coord):
    min_distance = float('inf')
    nearest_stop = None

    for stop, stop_coord in node_positions.items():
        distance = calculate_distance(coord, stop_coord)
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop

    return nearest_stop,min_distance



i=0

for i in range(1,11):
    net_distance = 0
    data = {}
    j=0
    for point in points:
        g.add_node(point)
        total_distance=0
        # Update node_positions with the coordinates of the new node
        node_positions['New'] = point
        # print("Nodes in graph after adding new node:", g.nodes())
        # print("Node positions after adding new node:", node_positions)
        for c in points:
            nearest_stop,min_distance=find_nearest_stop(c)
            total_distance=total_distance+min_distance

        data[j]={'x':point[0],
                 'y':point[1],
                 'distance':total_distance

        }
        g.remove_node(point)
        del node_positions['New']
        j=j+1

    sorted_coordinates = sorted(data.values(), key=lambda k: k['distance'])
    x = sorted_coordinates[0]['x']
    y = sorted_coordinates[0]['y']
    p=(x,y)
    g.add_node(p)
    node_positions[f'{i}'] = p
    i=i+1
    for c in points:
        nearest_stop, min_distance = find_nearest_stop(c)
        net_distance = net_distance + min_distance
    print(net_distance/1000)

print(node_positions)

