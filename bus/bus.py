import networkx as nx
import matplotlib.pyplot as plt
# Creating a graph
import sqlite3
conn = sqlite3.connect('buscap.db')
cursor = conn.cursor()
graph = nx.Graph()
g=nx.Graph()
distance=0
board_deboard=4
count=0
i=0
j=0
bus1_path=['A','B','C','D','C','B'] # bus id=1
bus2_path=['D','C','B','A','B','C'] # bus id=2

bus3_path=['P','Q','B','R','S','R','B','Q'] # bus id=3
bus4_path=['S','R','B','Q','P','Q','B','R'] # bus id=4


# Adding vertices
stops=['A','B','C','D','P','Q','R','S']

# Adding edges
graph.add_edge('A', 'B',weight=1170)
graph.add_edge('B','Q',weight=1800)
graph.add_edge('B', 'C',weight=630)
graph.add_edge('B','R',weight=1350)
graph.add_edge('C','D',weight=1530)
graph.add_edge('P', 'Q',weight=900)
graph.add_edge('R','S',weight=450)

g.add_edge('A', 'B',weight=13)
g.add_edge('B','Q',weight=20)
g.add_edge('B', 'C',weight=7)
g.add_edge('B','R',weight=15)
g.add_edge('C','D',weight=17)
g.add_edge('P', 'Q',weight=10)
g.add_edge('R','S',weight=5)


def shortestPath(src,dest):

    shortest_distance = nx.dijkstra_path_length(graph, src, dest, weight='weight')
    return shortest_distance


def busfunction(busid,present_stop,destination_stop,next_stop,buspath,t,number_of_passenger):
    #Passenger DeBoarding whose destinatination is present stop
    global count
    overhead=[]
    cursor.execute("SELECT * FROM passenger WHERE flag=? and destination_stop=? and bus_id=?",(1,present_stop,busid))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_,d,_, _, _, s,waiting_time,_,_,_,_,_ = p
        deboard(passenger_id,t)
        t=t+board_deboard
        count=count+1
        print(f"DEBOARDED {passenger_id}  {t} from {busid}")
        number_of_passenger=number_of_passenger-1

    # Passenger deboarding at junction
    cursor.execute("SELECT * FROM passenger WHERE flag=? and destination_stop!=? and bus_id=?",(1,present_stop,busid))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_, d, _, _, _, s, waiting_time,_,_,_,_,_= p
        print(present_stop)
        print(destination_stop)
        print(s)
        print(busid)
        print(findnext(s,present_stop,destination_stop))
        if(findnext(s,present_stop,destination_stop)==0):
            print(f"DEBOARDING AT JUNCTION---time{t}")
            deboard_at_junction(passenger_id,present_stop,t)
            t=t+board_deboard
            number_of_passenger = number_of_passenger - 1



    #Passenger Boarding
    cursor.execute("SELECT * FROM passenger WHERE arrival_time<=? and flag=? and arrival_stop=? and reached=?",(t,0,present_stop,0))
    p_update=cursor.fetchall()
    for p in p_update:
        passenger_id, arrival_time,_, d, _, _, _, s, waiting_time,_,_,_,_,_ = p
        if(findnext(s,present_stop,destination_stop)==1):
            board(passenger_id,t,waiting_time,arrival_time,busid)
            t=t+board_deboard
            print(f"{passenger_id}  BOARDED   {t} to {busid}")
            overhead.append(passenger_id)
            number_of_passenger = number_of_passenger +1
            if(number_of_passenger==50):
                break

    busdeparture(overhead,t)
    t=t+shortestPath(present_stop,destination_stop)
    cursor.execute("UPDATE bus set present_stop=?,destination_stop=?,time=? WHERE id=?",(destination_stop,next_stop,t,busid))
    conn.commit()
    return number_of_passenger

def busdeparture(overhead,t):
    for o in overhead:
        cursor.execute("SELECT * FROM passenger where id=?", (o,))
        p = cursor.fetchone()
        _, arrival_time, _, _, _, _, _, _, waiting_time, _, _,_,_,_ = p
        waiting_time = waiting_time + (t - arrival_time)
        cursor.execute("UPDATE passenger set bus_departure=?,waiting_time=? where id=?",(t,waiting_time,o))
        conn.commit()

def deboard(passenger_id,t):

    cursor.execute("UPDATE passenger SET flag=?, departure_time=?,reached=? WHERE id=?", (0, t,1, passenger_id))
    conn.commit()



def deboard_at_junction(passenger_id,present_stop,t):

    cursor.execute("UPDATE passenger set arrival_stop=?,flag=?,arrival_time=? WHERE id=?",(present_stop,0,t,passenger_id))
    conn.commit()

def board(passenger_id,t,waiting_time,arrival_time,busid):
    cursor.execute("UPDATE passenger set flag=?,bus_id=? WHERE id=?",(1,busid,passenger_id))
    conn.commit()


def findnext(s,present_stop,destination_stop):
    for i in range(len(s)):
        if s[i] == present_stop:
            if i + 1 < len(s) and s[i + 1]==destination_stop:
                return 1
    return 0



if __name__ == "__main__":
    i=2
    maxi = 0
    count1=0
    count2=0
    count3=0
    count4=0
    # count5 = 0
    # count6 = 0
    # count7 = 0
    # count8 = 0

    while (count < 7588):
        # print("HI")

        cursor.execute("SELECT * FROM bus ORDER BY time")
        b = cursor.fetchall()
        bus1 = b[0]
        bus2 = b[1]
        bus3 = b[2]
        bus4 = b[3]
        # bus5 = b[4]
        # bus6 = b[5]
        # bus7 = b[6]
        # bus8 = b[7]
        for bus in b:
            # print("INSIDE for loop")

            busid,present_stop,destination_stop,t,path=bus
            print(t)
            if(path=="ABCD"):
                next_stop=bus1_path[(i%6)]
                # print(f"Next stop of bus1 is {next_stop}")
                # if(b[0]==1):
                count1=busfunction(busid,present_stop,destination_stop,next_stop,bus1_path,t,count1)
                # else:
                #     count5 = busfunction(busid, present_stop, destination_stop, next_stop, bus1_path, t, count5)
            elif(path=="DCBA"):
                next_stop = bus2_path[(i % 6)]
                # print(f"bus 2 is at {present_stop} at {t}")

                count2=busfunction(busid, present_stop, destination_stop,next_stop, bus2_path,t,count2)
                # else:
                #     count6 = busfunction(busid, present_stop, destination_stop, next_stop, bus2_path, t, count6)
            elif(path=="PQBRS"):
                next_stop = bus3_path[(i % 8)]

                count3=busfunction(busid, present_stop, destination_stop,next_stop, bus3_path,t,count3)
                # else:
                #     count7 = busfunction(busid, present_stop, destination_stop, next_stop, bus3_path, t, count7)
            else:
                next_stop = bus4_path[(i % 8)]

                count4=busfunction(busid, present_stop, destination_stop,next_stop, bus4_path,t,count4)
                # else:
                #     count8 = busfunction(busid, present_stop, destination_stop, next_stop, bus4_path, t, count8)
        maxi=max(count1,count2,count3,count4,maxi)
        i=i+1
    print(maxi)
    print(distance)







