import networkx as nx
import matplotlib.pyplot as plt

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

# Finding the shortest path using Dijkstra's algorithm
def shortestPath(src, dest):
    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_distance

def short(src, dest):

    shortest_distance = nx.dijkstra_path_length(g, src, dest, weight='weight')
    return shortest_distance

def emptypod(stop,src,final_pod,present_start_time):
    path=nx.dijkstra_path(graph, stop, src, weight='weight') #path from stop to source stop of passenger
    id,_,_,_=final_pod
    l1=[] #will contain empty pods  ids which will collide in journey
    l2=[] #will contain pods with passenger ids which will collide in journey
    l1.append(id)
    for i in range(0,len(path)-1):
        id_list = ",".join(map(str, l1))
        query = f"SELECT * FROM emptypod WHERE (src = ?) AND pod_id NOT IN ({id_list})"
        #It selects row which has source as their present stop from table emptypod
        cursor.execute(query,(path[i]))
        comming_to_stop=cursor.fetchall()
        for c in comming_to_stop:
            _,_,_,start_time,stop_time,podid=c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4)):
                print(f'{c} pod {podid}---- in stop {path[i]}')
                present_start_time = present_start_time + minimum_distance
                l1.append(podid)



        id_list = ",".join(map(str, l2))
        query = f"SELECT * FROM journey WHERE (src = ?) AND pid NOT IN ({id_list})"
        #It selects row which has source as their present stop from table journey.
        cursor.execute(query,(path[i]))
        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, cid = c
            #stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4)):
                print(f'{c} passenger {cid}---- in stop {path[i]}')
                present_start_time = present_start_time + minimum_distance
                l2.append(cid)

        #Next stop
        present_stop_time=present_start_time+shortestPath(path[i], path[i+1])
        i=i+1
        # It selects row which has source as their present stop from table emptypod
        id_list = ",".join(map(str, l1))
        query = f"SELECT * FROM emptypod WHERE (src = ?) AND pod_id NOT IN ({id_list})"
        cursor.execute(query,(path[i]))

        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, podid = c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4 )):
                print(f'{c} pod {podid}---- in stop {path[i]}')
                present_stop_time = present_stop_time + minimum_distance
                l1.append(podid)


        # It selects row which has source as their present stop from table journey.
        id_list = ",".join(map(str, l2))
        query = f"SELECT * FROM journey WHERE (src = ? ) AND pid NOT IN ({id_list})"
        cursor.execute(query,(path[i]))
        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, cid = c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4)):
                print(f'{c} passenger {cid}---- in stop {path[i]}')
                print(f'present start time {present_start_time} and present stop time {present_stop_time}')
                present_stop_time = present_stop_time + minimum_distance
                l2.append(cid)

        cursor.execute("INSERT INTO emptypod (src, dest, start_time, stop_time, pod_id) VALUES (?, ?, ?, ?, ?)",
                       (path[i-1], path[i], present_start_time, present_stop_time, id)) #update one part of journey in empytypod table.
        conn.commit()
        present_start_time = present_stop_time

    return present_start_time

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

            present_start_time = emptypod(stop, src, final_pod,arrival_time)
            # pod_departure = arrival_time + weight  #+weight
            pod_departure=present_start_time
            # final_time = pod_departure + travel_time

        else:
            # pod_departure =  time+weight
            present_start_time = emptypod(stop, src, final_pod,time)
            pod_departure=present_start_time
            # final_time = pod_departure + travel_time
    else:
        if (arrival_time > time):
            pod_departure = arrival_time
            # final_time = pod_departure + travel_time
        else:
            # print(f'pod_departure for {src} to {dest}')
            pod_departure = time
            # final_time = pod_departure + travel_time


    l1=[] # will contains empty pod ids which will collide in journey
    l1.append(id)
    l2=[] #will contain pods with passenger ids which will collide in journey

    present_start_time=pod_departure
    present_stop_time=0
    l2.append(passenger_id)
    for i in range(0,len(path)-1):

        id_list = ",".join(map(str, l1))
        # It selects row which has source as their present stop from table emptypod
        query = f"SELECT * FROM emptypod WHERE (src = ? ) AND pod_id NOT IN ({id_list})"
        cursor.execute(query,(path[i]))
        print(f"Present start time {present_start_time} and {present_stop_time} for passengerid {passenger_id}")
        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, podid = c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            print(f'{c} pod {podid}---- in stop {path[i]}')
            if ((abs(start_time-present_start_time)<4 )):
                if(path[i]==src):
                    pod_departure=pod_departure+minimum_distance
                present_start_time = present_start_time + minimum_distance
                l1.append(podid)

        id_list = ",".join(map(str, l2))
        query = f"SELECT * FROM journey WHERE (src = ? ) AND pid NOT IN ({id_list})"
        cursor.execute(query,(path[i]))
        # It selects row which has source as their present stop from table journey
        coming_to_stop = cursor.fetchall()

        for c in coming_to_stop:
            _,_,_,start_time,stop_time,cid=c
            if ((abs(start_time-present_start_time)<4 )):
                # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
                print(f'{c} passenger----{passenger_id} in stop {path[i]}')
                if(path[i]==src):
                    pod_departure = pod_departure + minimum_distance
                present_start_time = present_start_time + minimum_distance
                print(f'for passenger id{passenger_id}---{c}')
                l2.append(cid)
        present_stop_time=present_start_time+shortestPath(path[i],path[i+1])
        i=i+1   #checking next stop

        id_list = ",".join(map(str, l1))
        query = f"SELECT * FROM emptypod WHERE (src = ?) AND pod_id NOT IN ({id_list})"
        # It selects row which has source as their present stop from table emptypod
        cursor.execute(query,(path[i]))
        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, podid = c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4 )):
                print(f'{c}----pod  {podid} in stop {path[i]}')
                present_stop_time = present_stop_time + minimum_distance
                l1.append(podid)



        id_list = ",".join(map(str, l2))
        query = f"SELECT * FROM journey WHERE (src = ? ) AND pid NOT IN ({id_list})"
        # It selects row which has source as their present stop from table journey
        cursor.execute(query,(path[i]))
        comming_to_stop = cursor.fetchall()
        for c in comming_to_stop:
            _, _, _, start_time, stop_time, podid = c
            # stop time and start time are time at which the pod comes to stop and leaves the stop these are from table
            if ((abs(start_time-present_start_time)<4)):
                print(f'{c}  passenger----{passenger_id} in stop {path[i]}')
                present_stop_time = present_stop_time + minimum_distance
                l2.append(podid)

        cursor.execute("INSERT INTO journey (src, dest, start_time, stop_time, pid) VALUES (?, ?, ?, ?, ?)",
                       (path[i - 1], path[i], present_start_time, present_stop_time, passenger_id))
        conn.commit()  # update part of journey of passenger in journey table.

        present_start_time=present_stop_time
    final_time=present_stop_time

    cursor.execute(
        "UPDATE pod SET time = ?,current_stop=?,destination_stop=?  WHERE id = ?",
        (final_time, dest, dest, id))
    conn.commit()
    cursor.execute("UPDATE passenger set departure_time = ?,flag=?,pod_departure=?  WHERE pid = ?",
                   (final_time, 1, pod_departure, passenger_id))  #update whole journey in passenger table.
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
