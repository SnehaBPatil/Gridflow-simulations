import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample data for boxplots
#  EXPERIMENT 1
df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/392b.csv')
bus = df['waiting_time']
data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/392.csv')
pod = data['waiting_time']

df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/896b.csv')
bus1 = df['waiting_time']
data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/896.csv')
pod1 = data['waiting_time']

df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/2968b.csv')
bus2 = df['waiting_time']
data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/2968.csv')
pod2 = data['waiting_time']

df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/4032b.csv')
bus3 = df['waiting_time']
data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/4032.csv')
pod3 = data['waiting_time']

df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/5040b.csv')
bus4 = df['waiting_time']
data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/5040.csv')
pod4 = data['waiting_time']

# df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/buswithlimit/7952.csv')
# bus5 = df['waiting_time']
# data = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/pod/8ka.csv')
# pod5 = data['waiting_time']


pod_data = [pod, pod1, pod2, pod3,pod4]
bus_data = [bus, bus1, bus2, bus3,bus4]


plt.rcParams.update({'font.size': 18})  # Set default font size for all text
plt.rcParams.update({'xtick.labelsize': 18})  # Set font size for x-axis tick labels
plt.rcParams.update({'ytick.labelsize': 18})

df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/392.csv')
buss = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/896.csv')
buss1 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/2968.csv')
buss2 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/4032.csv')
buss3 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/5040.csv')
buss4 = df['waiting_time']

#
# df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/from_stop/bus50/8000.csv')
# buss5 = df['waiting_time']
#
#


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/extension of exp3/392.csv')
p1 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/extension of exp3/896.csv')
p2 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/extension of exp3/2968.csv')
p3 = df['waiting_time']


df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/extension of exp3/4032.csv')
p4 = df['waiting_time']

# df = pd.read_csv('C:/Users/Sneha B Patil/OneDrive/Desktop/extension of exp3/5040.csv')
# p5 = df['waiting_time']


p=[p1,p2,p3,p4]
bus_data1 = [buss, buss1, buss2, buss3,buss4]

def calculate(x, y, color, label):
    mean_y = np.mean(y)
    std_dev = np.std(y, ddof=1)  # Using ddof=1 for sample standard deviation

    # Calculate standard error
    n_samples = len(y)
    std_error = std_dev / np.sqrt(n_samples)

    # Define error bars (2 times the standard error)
    error_bars = 2 * std_error

    # Plotting with custom colors and error bars
    plt.errorbar(x, mean_y, yerr=error_bars, fmt='o', color=color)

def connect_points(x1, x2, y1, y2, color):
    plt.plot([x1, x2], [y1, y2], color=color)

plt.figure(figsize=(10, 6))  # Set figure size


for i in range(len(pod_data)):
    # Calculate x positions for bus and pod error bars
    x_bus = i * 2  # Even index for bus
    x_pod = i * 2   # Odd index for pod

    # Calculate means and standard deviations, plot with colors and error bars

    calculate(x_bus, bus_data[i], color='red', label='Bus ' + str(i+1))
    calculate(x_pod, pod_data[i], color='blue', label='Pod ' + str(i+1))



    # Connect successive points
    if i > 0 :
        connect_points(x_bus_prev, x_bus, mean_bus_prev, np.mean(bus_data[i]), color='red')
        connect_points(x_pod_prev, x_pod, mean_pod_prev, np.mean(pod_data[i]), color='blue')


    # Store previous values for connecting lines
    x_bus_prev, x_pod_prev = x_bus, x_pod
    mean_bus_prev, mean_pod_prev = np.mean(bus_data[i]), np.mean(pod_data[i])

for i in range(len(bus_data1)):
    # Calculate x positions for bus and pod error bars
    x_bus = i * 2  # Even index for bus
      # Odd index for pod

    # Calculate means and standard deviations, plot with colors and error bars

    calculate(x_bus, bus_data1[i], color='green', label='Bus with limit of 50 passengers' + str(i + 1))


    # Connect successive points
    if i > 0:
        connect_points(x_bus_prev, x_bus, mean_bus_prev, np.mean(bus_data1[i]), color='green')



    # Store previous values for connecting lines
    x_bus_prev = x_bus
    mean_bus_prev = np.mean(bus_data1[i])


for i in range(len(p)):
    # Calculate x positions for bus and pod error bars
    x_bus = i * 2  # Even index for bus
      # Odd index for pod

    # Calculate means and standard deviations, plot with colors and error bars

    calculate(x_bus, p[i], color='orange', label='Pod with exp3 distribution' + str(i + 1))


    # Connect successive points
    if i > 0:
        connect_points(x_bus_prev, x_bus, mean_bus_prev, np.mean(p[i]), color='orange')



    # Store previous values for connecting lines
    x_bus_prev = x_bus
    mean_bus_prev = np.mean(p[i])

# Set x-ticks and labels
plt.xticks(range(0, len(pod_data) * 2, 2), ['392', '896','2968', '4032','5040'])

# Set labels and title
plt.axhline(y=1800, color='black', linestyle='--', linewidth=2)
# plt.axhline(y=25, color='black', linestyle='dotted', linewidth=2)

plt.xlabel('No of passengers')
plt.ylabel('Passenger waiting time (s)')

# plt.title('70% Passenger from Junc 4 seconds between the pods,4 bus')
plt.errorbar(0,0, fmt='o', color='red',label='Bus limit 80')
plt.errorbar(0,0, fmt='o', color='green',label='Bus limit 50 ')
plt.errorbar(0,0, fmt='o', color='blue',label='Pod')
plt.errorbar(0,0, fmt='o', color='orange',label='Pod with exp 3 distribution')
# plt.errorbar(0,0, fmt='o', color='white')

plt.legend(loc='upper left')
# Show grid
plt.grid(True)

# Show plot
plt.show()
