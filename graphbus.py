import networkx as nx
import matplotlib.pyplot as plt
# Creating a graph
import sqlite3
conn = sqlite3.connect('graphbus.db')
cursor = conn.cursor()
graph = nx.Graph()
board_deboard=4
count=0

speed=40000
bus1_path=['A','B','C','D','C','B'] # bus id=1
bus2_path=['D','C','B','A','B','C'] # bus id=2

bus3_path=['P','Q','B','R','S','R','B','Q'] # bus id=3
bus4_path=['S','R','B','Q','P','Q','B','R'] # bus id=4


# Adding vertices
stops=['A','B','C','D','P','Q','R','S']

# Adding edges
graph.add_edge('A', 'B',weight=13000)
graph.add_edge('B','Q',weight=20000)
graph.add_edge('B', 'C',weight=7000)
graph.add_edge('B','R',weight=15000)
graph.add_edge('C','D',weight=17000)
graph.add_edge('P', 'Q',weight=10000)
graph.add_edge('R','S',weight=5000)

def shortestPath(src,dest):  #returns shortest path

    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_distance

def busfunction(busid,present_stop,destination_stop,next_stop,buspath,final_time):
    #Passenger DeBoarding whose destinatination is present stop
    global count
    overhead=[]
    cursor.execute("SELECT * FROM passenger WHERE flag=? and destination_stop=? and bus_id=?",(1,present_stop,busid))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_,d,_, _, _, s,waiting_time,_,_ = p
        deboard(passenger_id,final_time)
        final_time=final_time+board_deboard
        count=count+1
        print(f"DEBOARDED {passenger_id}  {final_time} from {busid}")

    # Passenger deboarding at junction
    cursor.execute("SELECT * FROM passenger WHERE flag=? and destination_stop!=? and bus_id=?",(1,present_stop,busid))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_, d, _, _, _, s, waiting_time,_,_ = p
        print(present_stop)
        print(destination_stop)
        print(s)
        print(busid)
        print(findnext(s,present_stop,destination_stop))
        if(findnext(s,present_stop,destination_stop)==0):
            print(f"DEBOARDING AT JUNCTION---time{final_time}")
            deboard_at_junction(passenger_id,present_stop,final_time)
            final_time=final_time+board_deboard


    #Passenger Boarding
    cursor.execute("SELECT * FROM passenger WHERE arrival_time<=? and flag=? and arrival_stop=? and reached=?",(final_time,0,present_stop,0))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_, d, _, _, _, s, waiting_time,_,_ = p
        if(findnext(s,present_stop,destination_stop)==1):
            board(passenger_id,final_time,waiting_time,arrival_time,busid)
            final_time=final_time+board_deboard
            print(f"{passenger_id}  BOARDED   {final_time} to {busid}")
            overhead.append(passenger_id)  #passenger who gets into bus his id is added to overhead list.this used later to update bus departure time
    busdeparture(overhead,final_time)
    final_time=final_time+shortestPath(present_stop,destination_stop)/speed
    cursor.execute("UPDATE bus set present_stop=?,destination_stop=?,time=? WHERE id=?",(destination_stop,next_stop,final_time,busid))
    conn.commit()

def busdeparture(overhead,final_time):  #TO update bus departure for all the passenger in that bus
    for o in overhead:
        cursor.execute("SELECT * FROM passenger where id=?", (o,))
        p = cursor.fetchone()
        _, arrival_time, _, _, _, _, _, _, waiting_time, _, _ = p
        waiting_time = waiting_time + (final_time - arrival_time)
        cursor.execute("UPDATE passenger set bus_departure=?,waiting_time=? where id=?",(final_time,waiting_time,o))
        conn.commit()

def deboard(passenger_id,final_time): #updating database .The passenger has reached his destination and completed his journey

    cursor.execute("UPDATE passenger SET flag=?, departure_time=?,reached=? WHERE id=?", (0, final_time,1, passenger_id))
    conn.commit()



def deboard_at_junction(passenger_id,present_stop,final_time): #updating that passenger deboards the bus and hasnt completed his journey
                                                      #he waits for next stop.he deboards at the junction

    cursor.execute("UPDATE passenger set arrival_stop=?,flag=?,arrival_time=? WHERE id=?",(present_stop,0,final_time,passenger_id))
    conn.commit()

def board(passenger_id,final_time,waiting_time,arrival_time,busid):  #updates in database that passsenger boarded the bus and enter the busid which he boards
    cursor.execute("UPDATE passenger set flag=?,bus_id=? WHERE id=?",(1,busid,passenger_id))
    conn.commit()


def findnext(s,present_stop,destination_stop): #this function checks whether the passenger's next stop is equal to bus next stop
    for i in range(len(s)):
        if s[i] == present_stop:
            if i + 1 < len(s) and s[i + 1]==destination_stop:
                return 1
    return 0


if __name__ == "__main__":
    i=2
    while (count < 896): #here count represents the number of passengers who completed the journey
        cursor.execute("SELECT * FROM bus ORDER BY time")
        b = cursor.fetchall()
        bus1 = b[0]
        bus2 = b[1]
        bus3 = b[2]
        bus4 = b[3]
        for bus in b:
            
            busid,present_stop,destination_stop,final_time,path=bus

            if(path=="ABCD"):
                next_stop=bus1_path[(i%6)]
                # print(f"Next stop of bus1 is {next_stop}")
                busfunction(busid,present_stop,destination_stop,next_stop,bus1_path,final_time)
            elif(path=="DCBA"):
                next_stop = bus2_path[(i % 6)]
                print(f"bus 2 is at {present_stop} at {final_time}")
                busfunction(busid, present_stop, destination_stop,next_stop, bus2_path,final_time)
            elif(path=="PQBRS"):
                next_stop = bus3_path[(i % 8)]
                busfunction(busid, present_stop, destination_stop,next_stop, bus3_path,final_time)
            else:
                next_stop = bus4_path[(i % 8)]
                busfunction(busid, present_stop, destination_stop,next_stop, bus4_path,final_time)
        i=i+1











