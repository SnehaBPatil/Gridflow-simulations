import networkx as nx
import matplotlib.pyplot as plt
# Creating a graph
import sqlite3

conn = sqlite3.connect('collide.db')
cursor = conn.cursor()
graph = nx.Graph()
board_deboard = 4
g = nx.Graph()
distance = 0
# Adding vertices
stops = ['A', 'B', 'C', 'D', 'P', 'Q', 'R', 'S']
minimum_distance = 4
# Adding edges
graph.add_edge('A', 'B', weight=1170)
graph.add_edge('B', 'Q', weight=1800)
graph.add_edge('B', 'C', weight=630)
graph.add_edge('B', 'R', weight=1350)
graph.add_edge('C', 'D', weight=1530)
graph.add_edge('P', 'Q', weight=900)
graph.add_edge('R', 'S', weight=450)


g.add_edge('A', 'B', weight=13)
g.add_edge('B', 'Q', weight=20)
g.add_edge('B', 'C', weight=7)
g.add_edge('B', 'R', weight=15)
g.add_edge('C', 'D', weight=17)
g.add_edge('P', 'Q', weight=10)
g.add_edge('R', 'S', weight=5)



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


# nx.draw(graph, pos=node_positions, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold')
# labels = nx.get_edge_attributes(graph, 'weight')
# nx.draw_networkx_edge_labels(graph, pos=node_positions, edge_labels=labels)

# Finding the shortest path using Dijkstra's algorithm
def shortestPath(src, dest):
    shortest_path = nx.dijkstra_path(graph, src, dest, weight='weight')
    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_distance


def short(src, dest):
    shortest_path = nx.dijkstra_path(g, src, dest, weight='weight')
    shortest_distance = nx.dijkstra_path_length(g, src, dest, weight='weight')
    return shortest_distance


def pick(passenger_id, arrival_time, src, dest,path):
    min_time = 40000000
    final_pod = None
    final_time = 0
    pod_departure = 0
    for stop in stops:
        pod = check_at_stop(stop)
        if (pod != None):
            id, _, _, stop_time = pod
            weight = shortestPath(stop, src)
            if (stop != src):
                if (stop_time > arrival_time):
                    if (stop_time + weight < min_time):
                        final_pod = pod
                        min_time = stop_time + weight

                else:
                    if (arrival_time + weight < min_time):
                        final_pod = pod
                        min_time = arrival_time + weight

            else:
                if (stop_time < min_time):
                    final_pod = pod
                    min_time = stop_time
                    # print(stop)

    id, stop, _, time = final_pod
    # print(f'final pod is---{final_pod}')
    # print(f'Selected {min_time} for {src} to {dest} from stop {stop}')

    weight = shortestPath(stop, src)
    global distance

    travel_time = shortestPath(src, dest)
    if (stop != src):
        distance = distance + short(stop, src)
        if (arrival_time > time):
            pod_departure = arrival_time + weight
            final_time = pod_departure + travel_time+board_deboard*2

        else:
            pod_departure = time + weight
            final_time = pod_departure + travel_time+board_deboard*2
    else:
        if (arrival_time > time):
            pod_departure = arrival_time
            final_time = pod_departure + travel_time+board_deboard*2
        else:
            # print(f'pod_departure for {src} to {dest}')
            pod_departure = time
            final_time = pod_departure + travel_time+board_deboard*2

    l=[]
    l.append(passenger_id)
    for i in path:

        # cursor.execute(
        #     "SELECT * FROM passenger WHERE INSTR(path, ?) > 0 ",(i,))
        query = """
            SELECT * 
            FROM passenger 
            WHERE pid NOT IN ({}) 
            AND INSTR(path, ?) > 0
        """.format(', '.join(['?'] * len(l)))


        cursor.execute(query, l + [i])

        # Fetch the results

        coming_to_stop = cursor.fetchall()
        # print(len(coming_to_stop))
        for c in coming_to_stop:

            cid, a, dest, _, dep, _, pdep, _, _ = c
            # print(f"pod departure of presenet {pod_departure}")
            # print(f"pdep of presenet {pdep}")

            if (dep!=0 and ((abs((pod_departure+shortestPath(src,i))-(pdep + shortestPath(a, i))) <4))):
                print(i)
                print(abs((pod_departure + shortestPath(src, i)) - (pdep + shortestPath(a, i))))
                if(i==src):
                    pod_departure = pod_departure + minimum_distance
                final_time = final_time + minimum_distance


                print(f'for passenger id{passenger_id}---{c}')
                l.append(cid)
    # print("next")

    cursor.execute(
        "UPDATE pod SET time = ?,current_stop=?,destination_stop=?  WHERE id = ?",
        (final_time, dest, dest, id))
    conn.commit()
    cursor.execute("UPDATE passenger set departure_time = ?,flag=?,pod_departure=?  WHERE pid = ?",
                   (final_time, 1, pod_departure, passenger_id))
    # print("Executed")
    conn.commit()


def check_at_stop(stop):
    cursor.execute(
        "SELECT * FROM pod WHERE current_stop = ? AND destination_stop = ? "
        "AND time IN (SELECT MIN(time) FROM pod WHERE current_stop = ? AND destination_stop = ?)",
        (stop, stop, stop, stop))

    pod_available = cursor.fetchone()

    return pod_available


count = 1
flag = 0
while (count != 0):

    cursor.execute("SELECT * FROM passenger  WHERE flag=? and departure_time=? ORDER BY arrival_time", (0, 0))
    passenger_to_update_at_a = cursor.fetchall()
    count = len(passenger_to_update_at_a)

    for p in passenger_to_update_at_a:
        passenger_id, cstop, dest, t, _, _, _, _, path = p
        pick(passenger_id, t, cstop, dest,path)

# print(f"extra distance is {distance} km")
