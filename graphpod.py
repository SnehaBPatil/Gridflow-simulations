import networkx as nx
import matplotlib.pyplot as plt
# Creating a graph
import sqlite3
conn = sqlite3.connect('graph.db')
cursor = conn.cursor()
graph = nx.Graph()
board_deboard=4
minimum_distance=4
speed=40000 # speed of pod in m/s
# Adding vertices
# ARRIVAL pod_available_time IS pod_available_time AT WHICH PASSENGER ARRIVES TO THE STATION.
# FINAL pod_available_time IS THE pod_available_time AT WHICH PASSENGER REACHES THE DESTINATION
# BOARD_DEBOARD VARIABLE IS FOR PASSENGER BOARDING AND DEBOARDING THAT IS 4+4 SECONDS
# FUNCTION shortestPath() IS TO CALCULATE THE SHORTEST PATH BETWEEN SOURCE TO DESTINATION USING DIJKSTRA'S ALGORITHM
# FUNCTION pick() IS RUNS FOR EACH PASSENGER AND DECIDES WHICH POD THE PASSENGER TAKES,IN THIS FUNCTION WE TAKE THE 
# MIN(AVAILABILITY OF PODS AT EACH STATION+pod_available_time TAKEN TO REACH THE ARRIVAL STATION).THE MINIMUM IS SELECTED
# TRAVEL_TIME IS pod_available_time TAKEN TO REACH THE DESTINATION
stops=['A','B','C','D','P','Q','R','S']

# Adding edges which are routes distances are the weights of undirected graph
graph.add_edge('A', 'B',weight=13000)
graph.add_edge('B','Q',weight=20000)
graph.add_edge('B', 'C',weight=7000)
graph.add_edge('B','R',weight=15000)
graph.add_edge('C','D',weight=17000)
graph.add_edge('P', 'Q',weight=10000)
graph.add_edge('R','S',weight=5000)


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
def shortestPath(src,dest):
    shortest_path = nx.dijkstra_path(graph, src, dest, weight='weight')
    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_distance,shortest_path

def pick(passenger_id,arrival_time,src,dest,path):
    min_time=40000000
    final_pod=None
    final_time=0
    pod_departure=0
    for stop in stops:

        pod=check_at_stop(stop)
        if(pod!=None):
            id, _, _, pod_available_time = pod
            distance, _ = shortestPath(stop, src)
            weight=distance/speed
            if(stop!=src):

                if(pod_available_time+weight<min_time):
                    print(pod_available_time)
                    final_pod = pod
                    min_time = pod_available_time + weight


            else:
                if(pod_available_time<min_time):
                    final_pod=pod
                    min_time=pod_available_time
                    print(stop)



    id,stop,_,pod_available_time = final_pod  #pod_available_time is the pod_available_time at which pod is available 
    print(f'final pod is---{final_pod}')


    weight, _ = shortestPath(stop, src)
    weight=weight/speed
    travel_time,_= shortestPath(src,dest)/speed
    if(stop!=src):
        if(arrival_time>pod_available_time):                  
            pod_departure=arrival_time+weight   # IF arrival_time is 60s and pod_available_time is 40s then the pod is available before the passenger arrives

        else:
            pod_departure=pod_available_time+weight

    else:                                   # IF arrival_time is 40s and pod_available_time is 60s then the pod is available after the passenger arrives
        if(arrival_time>pod_available_time):      
            pod_departure=arrival_time  

        else:
            print(f'pod_departure for {src} to {dest}')
            pod_departure=pod_available_time
    final_time=pod_departure+travel_time+board_deboard+board_deboard
    cursor.execute(
        "SELECT * FROM passenger WHERE INSTR(path, ?) > 0 ",(src,))


    l=[]
    l.append(passenger_id)
    for i in path:
    #Here this query will list out all the passengers in transit and whose  have current stop in their path.
 
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
            
            #Here estimate of the other pods which will be in vicinity is checked
            if (dep!=0 and ((abs((pod_departure+shortestPath(src,i))-(pdep + shortestPath(a, i))) <4))):
                print(i)
                print(abs((pod_departure + shortestPath(src, i)) - (pdep + shortestPath(a, i))))
                if(i==src):
                    pod_departure = pod_departure + minimum_distance
                final_time = final_time + minimum_distance


                
                l.append(cid)


    cursor.execute(
        "UPDATE pod SET pod_available_time = ?,current_stop=?,destination_stop=?  WHERE id = ?",
        (final_time, dest, dest, id))   #updating in database pod
    conn.commit()
    cursor.execute("UPDATE passenger set departure_time = ?,flag=?,pod_departure=?  WHERE pid = ?",
                   (final_time, 1, pod_departure, passenger_id))    #updating in database passenger
    conn.commit()

def check_at_stop(stop):
    cursor.execute(
        "SELECT * FROM pod WHERE current_stop = ? AND destination_stop = ? "
        "AND pod_available_time IN (SELECT MIN(pod_available_time) FROM pod WHERE current_stop = ? AND destination_stop = ?)",
        (stop, stop,stop,stop))     #fetching data from pod table to find the earliest pod availability at given stop i.e stop

    pod_available = cursor.fetchone()  #selecting the first pod

    return pod_available 

count = 1
flag=0
while(count!=0):

    cursor.execute("SELECT * FROM passenger  WHERE flag=? and departure_time=? ORDER BY arrival_time", (0, 0)) # sorting passengers and serving based on arrival pod_available_time
    passenger_to_update_at_a = cursor.fetchall()
    count=len(passenger_to_update_at_a)

    for p in passenger_to_update_at_a:
        passenger_id, cstop, dest,t,_,_,_,_,path = p
        pick(passenger_id,t,cstop,dest)

