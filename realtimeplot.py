## for input
import serial
from datetime import datetime
from serial.tools import list_ports
## for plotting
import matplotlib as mpl
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import pandas as pd

## Finds the port where Arduino is connected
def find_arduino_port():
    ports = list(list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description: 
            return p.device
    return None

## parses input from sensors and returns as floats
def parse_line(line):
    if "Accelerometer:" in line:
        # Extract accelerometer data
        try:
            parts = line.split("Accelerometer: ")[1].split(" ")
            accel_data = list(map(float, parts[1::2])) # converts to list of floats
            accel_data.insert(0, "A") # adds ["A"] as first element to mark as accelerometer data
            return accel_data
        except Exception as e:
            print(e)
            pass
    elif "Gyroscope:" in line:
        # Extract gyroscope data
        try:
            parts = line.split("Gyroscope: ")[1].split(" ")
            gyro_data = list(map(float, parts[1::2]))
            gyro_data.insert(0, "G") # adds ["G"] as first element to mark as gyroscope data
            return gyro_data
        except Exception as e:
            print(e)
            pass
    else:
        # Attempt to parse as EMG value
        try:
            emg_value = float(line)
            return emg_value
        except Exception as e:
            print(e)
            pass

def animate(i, dataList, ser):
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            dataPoint = parse_line(line)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
            print(f"{timestamp}, {line}")
            file.write(f"{timestamp},{line}\n")  # Save timestamp and data to file
            if type(dataPoint) == list: # Adds data to appropriate lists
                if dataPoint[0] == "A":
                    dataList[4].append(dataPoint[1])
                    dataList[5].append(dataPoint[2])
                    dataList[6].append(dataPoint[3])
                else:
                    dataList[1].append(dataPoint[1])
                    dataList[2].append(dataPoint[2])
                    dataList[3].append(dataPoint[3])
            else:
                dataList[0].append(dataPoint)
    except KeyboardInterrupt:
        print(f"Data saved to {output_file}")
        ser.close()
    except:
        pass

    for i in range(len(dataList)) :
        dataList[i] = dataList[i][-50:]

    # plots data
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()
    ax7.clear()
    ax1.plot(dataList[0])
    ax2.plot(dataList[1])
    ax3.plot(dataList[2])
    ax4.plot(dataList[3])
    ax5.plot(dataList[4])
    ax6.plot(dataList[5])
    ax7.plot(dataList[6])

    # axis formatting
    ax1.set_title("EMG")
    ax1.set_ylim([0, 1000])
    # ax1.set_ylabel("μV") # Need to check/add units
    ax2.set_title("Gyroscope")
    ax5.set_title("Accelerometer")
    ax5.set_ylabel("X")
    ax5.yaxis.set_label_position("right")
    ax6.set_ylabel("Y")
    ax6.yaxis.set_label_position("right")
    ax7.set_ylabel("Z")
    ax7.yaxis.set_label_position("right")
    plt.subplots_adjust(left=0.048, bottom=0.09, right=0.95, top=0.95, wspace=0.282, hspace=0.147)

arduino_port = find_arduino_port()
if arduino_port is None:
    print("Arduino not found. Check connection or modify find_arduino_port() function.")
    exit()
    
ser = serial.Serial(arduino_port, 9600)  # Connect to detected Arduino port

output_file = "data1_from_2diy.csv"
dataList = [[],[],[],[],[],[],[]] # Data for EMG, Gyroscope X, Y, Z, Accelerometer X, Y, Z

file = open(output_file, 'w')
print("Logging data... Press Ctrl+C to stop.") # Write the header for the CSV file
file.write("Timestamp,Data\n")

fig = plt.figure()
ax1 = fig.add_subplot(1, 3, 1) # args: nrows, ncols, index EMG
ax2 = fig.add_subplot(3, 3, 2) # Gyro X
ax3 = fig.add_subplot(3, 3, 5) # Gyro Y
ax4 = fig.add_subplot(3, 3, 8) # Gyro Z
ax5 = fig.add_subplot(3, 3, 3) # Accel X
ax6 = fig.add_subplot(3, 3, 6) # Accel Y 
ax7 = fig.add_subplot(3, 3, 9) # Accel Z
print("Figure initialized")

ani = ani.FuncAnimation(fig, animate, frames=100, fargs=(dataList, ser), interval=200)
plt.show()
print(f"Data saved to {output_file}")
ser.close()