import math
import sqlite3
import random
import numpy as np
import matplotlib.pyplot as plt
# Connect to SQLite database
conn = sqlite3.connect('visualize.db')
cursor = conn.cursor()

travel_time=4500
x1, y1 = 0, 0  # Starting point
x2, y2 = 5,8.95
x3,y3= 10,0




def waiting(t):
    cursor.execute("SELECT * FROM passenger WHERE arrival_time<=? and pod_departure>?", (t, t))
    p_update = cursor.fetchall()
    print(len(p_update))
    xa = []
    ya = []
    xb=[]
    yb=[]
    xc=[]
    yc=[]
    print("Waiting for pod")
    # Waiting for pod
    for p in p_update:
        _, arrival_station, _, time, _, _, pod_time = p
        pod_time = (t-time)/travel_time*10
        if (arrival_station == 'A'):
            xa.append(5)
            ya.append(8.95)
        if (arrival_station == 'B'):
            xb.append(0)
            yb.append(0)
        if (arrival_station == 'C'):
            xc.append(10)
            yc.append(0)




        # if (from_stop == 'A'):
        #     start_x = 5
        #     start_y = 8.95
        #     if (arrival_station == 'B'):
        #         angle_radians = np.radians(-120)
        #     else:
        #         angle_radians = np.radians(-60)
        #     delta_x = start_x + pod_time * np.cos(angle_radians)
        #     delta_y = start_y + pod_time * np.sin(angle_radians)
        #     plt.scatter(delta_x, delta_y, color='white',marker='o',edgecolor='blue',linewidth=2,s=150)
        # elif (from_stop == 'B'):
        #     start_x = 0
        #     start_y = 0
        #     if (arrival_station == 'A'):
        #         angle_radians = np.radians(60)
        #     else:
        #         angle_radians = np.radians(0)
        #     delta_x = start_x + pod_time * np.cos(angle_radians)
        #     delta_y = start_y + pod_time * np.sin(angle_radians)
        #     plt.scatter(delta_x, delta_y, color='white', marker='o', edgecolor='blue', linewidth=2, s=150)
        # elif(from_stop=='C'):
        #     start_x = 10
        #     start_y = 0
        #     if (arrival_station == 'A'):
        #         angle_radians = np.radians(120)
        #     else:
        #         angle_radians = np.radians(180)
        #     delta_x = start_x + pod_time * np.cos(angle_radians)
        #     delta_y = start_y + pod_time * np.sin(angle_radians)
        #     plt.scatter(delta_x, delta_y, color='white', marker='o', edgecolor='blue', linewidth=2, s=150)
        #

    jitter_amount = 0.2
    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xa]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in ya]
    # Plotting
    plt.scatter(x_jittered, y_jittered, color='red',marker='^',s=150)
    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xb]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yb]
    # Plotting
    plt.scatter(x_jittered, y_jittered, color='red', marker='o', s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xc]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yc]
    # Plotting
    plt.scatter(x_jittered, y_jittered, color='red', marker='s', s=150)




def injourney(t):
    x = []
    y = []
    #Middle of the journey
    cursor.execute("SELECT * FROM passenger WHERE arrival_time<=? and departure_time>? and pod_departure<?",(t,t,t))
    p_update = cursor.fetchall()
    for p in p_update:
        _,arrival_stop,destination_stop,_,_,_,dep=p
        dep=(t-dep)/travel_time*10

        if(arrival_stop=='A'):
            start_x = 5
            start_y = 10
            if(destination_stop=='B'):
                angle_radians=np.radians(-120)
            else:
                angle_radians=np.radians(-60)
                start_x = 5
                start_y = 10


            delta_x = start_x + dep * np.cos(angle_radians)
            delta_y = start_y + dep * np.sin(angle_radians)
            plt.scatter(delta_x, delta_y, color='blue', marker='^', s=150)
        elif(arrival_stop=='B'):

            if(destination_stop=='A'):
                angle_radians=np.radians(60)
                start_x = 0
                start_y = 0
            else:
                angle_radians=np.radians(0)
                start_x = 0
                start_y = 0

            delta_x = start_x + dep * np.cos(angle_radians)
            delta_y = start_y + dep * np.sin(angle_radians)
            plt.scatter(delta_x, delta_y, color='blue', marker='o', s=150)
        else:

            if(destination_stop=='A'):
                angle_radians=np.radians(120)
                start_x = 10
                start_y = 0

            else:
                angle_radians=np.radians(180)
                start_x = 11
                start_y = -0.6

            delta_x = start_x + dep * np.cos(angle_radians)
            delta_y = start_y + dep * np.sin(angle_radians)
            plt.scatter(delta_x, delta_y, color='blue', marker='s', s=150)


    plt.scatter(x, y,color='blue',s=150)


def getspod(t):
    xa = []
    ya = []
    xb=[]
    yb=[]
    xc=[]
    yc=[]
    cursor.execute("SELECT * FROM passenger WHERE arrival_time=? and pod_departure=? ", (t, t))
    p_update = cursor.fetchall()
    for p in p_update:
        _, arrival_station, _, _, _, _, _ = p
        if (arrival_station == 'A'):
            xa.append(5)
            ya.append(8.95)
        if (arrival_station == 'B'):
            xb.append(0)
            yb.append(0)
        if (arrival_station == 'C'):
            xc.append(10)
            yc.append(0)
    #print("AS soon as he comes if he gets pod")

    jitter_amount = 0.05  # Adjust this value to control the amount of jitter
    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xa]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in ya]
    plt.scatter(x_jittered, y_jittered, color='blue',marker='^',s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xb]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yb]
    plt.scatter(x_jittered, y_jittered, color='blue', marker='o',s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xc]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yc]
    plt.scatter(x_jittered, y_jittered, color='blue',marker='s',s=150)


def notarrived(t):

    xa = []
    ya = []
    xb = []
    yb = []
    xc = []
    yc = []

    cursor.execute("SELECT * FROM passenger WHERE arrival_time>? and pod_departure>?",(t,t))
    p_update=cursor.fetchall()
    for p in p_update:
        _,arrival_station,_,_,_,_,_=p
        if(arrival_station=='A'):
            xa.append(5)
            ya.append(11)
        elif(arrival_station=='B'):
            xb.append(0)
            yb.append(-5)
        elif(arrival_station=='C'):
            xc.append(10)
            yc.append(-5)
    #print("Not arrived")

    jitter_amount = 0.5  # Adjust this value to control the amount of jitter

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xa]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in ya]
    plt.scatter(x_jittered, y_jittered, color='black',marker='^',s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xb]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yb]
    plt.scatter(x_jittered, y_jittered, color='black', marker='o',s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xc]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yc]
    plt.scatter(x_jittered, y_jittered, color='black',marker='s',s=150)

def reach(t):
    xa=[]
    ya=[]
    xb=[]
    yb=[]
    xc=[]
    yc=[]
    cursor.execute("SELECT * FROM passenger WHERE departure_time<=?", (t,))
    p_update = cursor.fetchall()
    for p in p_update:
        _, arrival_station, destination, _, _, _, _ = p
        if(arrival_station=='A'):
            if(destination=='B'):
                xa.append(-2)
                ya.append(-1)
            else:
                xa.append(12)
                ya.append(-1)
        elif(arrival_station=='B'):
            if(destination=='A'):
                xb.append(5)
                yb.append(13)
            else:
                xb.append(12)
                yb.append(-1)


        elif(arrival_station=='C'):
            if(destination=='A'):
                xc.append(5)
                yc.append(13)

            else:
                xc.append(-2)
                yc.append(-1)

    jitter_amount = 0.5  # Adjust this value to control the amount of jitter
    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xa]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in ya]
    plt.scatter(x_jittered, y_jittered, color='green', marker='^', s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xb]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yb]
    plt.scatter(x_jittered, y_jittered, color='green', marker='o', s=150)

    x_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in xc]
    y_jittered = [val + np.random.uniform(-jitter_amount, jitter_amount) for val in yc]
    plt.scatter(x_jittered, y_jittered, color='green', marker='s', s=150)



t=0
while(t<=69420):
    plt.figure(figsize=(16, 16))
    print(f"Time t is {t}")
    waiting(t)

    injourney(t)

    getspod(t)

    notarrived(t)

    reach(t)
    plt.plot([x1, x2], [y1, y2], 'k-')  # 'k-' means black color and solid line
    plt.plot([x2, x3], [y2, y3], 'k-')
    plt.plot([x3, x1], [y3, y1], 'k-')
    plt.plot([-1, 5], [-0.6, 10],'k-')
    plt.plot([11, 5], [-0.6, 10],'k-')
    plt.plot([-1, 11], [-0.6, -0.6],'k-')

    plt.xlim(-5,15)
    plt.ylim(-10 ,20)

    plt.axis('off')
    plt.savefig(f'C:/Users/Sneha B Patil/OneDrive/Desktop/vis/{t}.png')
      # Pause the plot for 1 second
    #plt.show()
    plt.close()

    t=t+60
